# -*- coding: utf-8 -*-
"""Back-port compiler for Python 3.8 assignment expressions."""

import argparse
import glob
import io
import os
import re
import sys

import parso
import tbtrim
from bpc_utils import BOOLEAN_STATES, CPU_CNT, LOCALE_ENCODING, UUID4Generator, archive_files, detect_files, mp

__all__ = ['walrus', 'convert']

# version string
__version__ = '0.1.4'

# macros
grammar_regex = re.compile(r"grammar(\d)(\d)\.txt")
WALRUS_VERSION = sorted(filter(lambda version: version >= '3.8',  # when Python starts to have walrus operator
                               map(lambda path: '%s.%s' % grammar_regex.match(os.path.split(path)[1]).groups(),
                                   glob.glob(os.path.join(parso.__path__[0], 'python', 'grammar??.txt')))))
del grammar_regex

# will be set in every call to `convert()`
uuid_gen = None


class ConvertError(SyntaxError):
    """Parso syntax error."""


class ContextError(RuntimeError):
    """Missing conversion context."""


class EnvironError(EnvironmentError):
    """Invalid environment."""


###############################################################################
# Traceback trim (tbtrim)

# root path
ROOT = os.path.dirname(os.path.realpath(__file__))


def predicate(filename):  # pragma: no cover
    if os.path.basename(filename) == 'walrus':
        return True
    return ROOT in os.path.realpath(filename)


tbtrim.set_trim_rule(predicate, strict=True, target=(ConvertError, ContextError))

###############################################################################
# Main convertion implementation

# walrus wrapper template
NAME_TEMPLATE = '''\
if False:
%(tabsize)s%(name_list)s = NotImplemented
'''.splitlines()  # `str.splitlines` will remove trailing newline
CALL_TEMPLATE = '__walrus_wrapper_%(name)s_%(uuid)s(%(expr)s)'
FUNC_TEMPLATE = '''\
def __walrus_wrapper_%(name)s_%(uuid)s(expr):
%(tabsize)s"""Wrapper function for assignment expression."""
%(tabsize)s%(keyword)s %(name)s
%(tabsize)s%(name)s = expr
%(tabsize)sreturn %(name)s
'''.splitlines()  # `str.splitlines` will remove trailing newline

# special template for lambda
LAMBDA_CALL_TEMPLATE = '__walrus_wrapper_lambda_%(uuid)s'
LAMBDA_FUNC_TEMPLATE = '''\
def __walrus_wrapper_lambda_%(uuid)s(%(param)s):
%(tabsize)s"""Wrapper function for lambda definitions."""
%(tabsize)s%(suite)s
'''.splitlines()  # `str.splitlines` will remove trailing newline

# special templates for ClassVar
## locals dict
LCL_DICT_TEMPLATE = '_walrus_wrapper_%(cls)s_dict = dict()'
LCL_NAME_TEMPLATE = '_walrus_wrapper_%(cls)s_dict[%(name)r]'
LCL_CALL_TEMPLATE = '__WalrusWrapper%(cls)s.get_%(name)s_%(uuid)s()'
LCL_VARS_TEMPLATE = '''\
[setattr(%(cls)s, k, v) for k, v in _walrus_wrapper_%(cls)s_dict.items()]
del _walrus_wrapper_%(cls)s_dict
'''.splitlines()  # `str.splitlines` will remove trailing newline
## class clause
CLS_CALL_TEMPLATE = '__WalrusWrapper%(cls)s.set_%(name)s_%(uuid)s(%(expr)s)'
CLS_NAME_TEMPLATE = '''\
class __WalrusWrapper%(cls)s:
%(tabsize)s"""Wrapper class for assignment expression."""
'''.splitlines()  # `str.splitlines` will remove trailing newline
CLS_FUNC_TEMPLATE = '''\
%(tabsize)s@staticmethod
%(tabsize)sdef set_%(name)s_%(uuid)s(expr):
%(tabsize)s%(tabsize)s"""Wrapper function for assignment expression."""
%(tabsize)s%(tabsize)s_walrus_wrapper_%(cls)s_dict[%(name)r] = expr
%(tabsize)s%(tabsize)sreturn _walrus_wrapper_%(cls)s_dict[%(name)r]

%(tabsize)s@staticmethod
%(tabsize)sdef get_%(name)s_%(uuid)s():
%(tabsize)s%(tabsize)s"""Wrapper function for assignment expression."""
%(tabsize)s%(tabsize)sif %(name)r in _walrus_wrapper_%(cls)s_dict:
%(tabsize)s%(tabsize)s%(tabsize)sreturn _walrus_wrapper_%(cls)s_dict[%(name)r]
%(tabsize)s%(tabsize)sraise NameError('name %%r is not defined' %% %(name)r)
'''.splitlines()  # `str.splitlines` will remove trailing newline


def parse(string, source):
    """Parse source string.

    Args:
     - `string` -- `str`, context to be converted
     - `source` -- `str`, source of the context

    Envs:
     - `WALRUS_VERSION` -- convert against Python version (same as `--python` option in CLI)

    Returns:
     - `parso.python.tree.Module` -- parso AST

    Raises:
     - `ConvertError` -- when source code contains syntax errors

    """
    grammar = parso.load_grammar(version=os.getenv('WALRUS_VERSION', WALRUS_VERSION[-1]))
    module = grammar.parse(string, error_recovery=True)
    errors = grammar.iter_errors(module)

    if errors:
        error_messages = '\n'.join('[L%dC%d] %s' % (*error.start_pos, error.message) for error in errors)
        raise ConvertError('source file %r contains following syntax errors:\n' % source + error_messages)

    return module


class Context:
    """Conversion context."""

    @property
    def string(self):
        return self._buffer

    @property
    def lambdef(self):
        return self._lamb

    @property
    def variables(self):
        return self._vars

    @property
    def functions(self):
        return self._func

    @property
    def global_stmt(self):
        if self._root.type == 'funcdef':
            return list()
        return self._context

    def __init__(self, node,
                 column=0, tabsize=None,
                 linesep=None, keyword=None,
                 context=None, raw=False):
        """Conversion context.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST
         - `column` -- `int`, current indentation level
         - `tabsize` -- `Optional[int]`, indentation tab size
         - `linesep` -- `Optional[str]`, line seperator
         - `keyword` -- `Optional[str]`, keyword for wrapper function
         - `context` -- `Optional[List[str]]`, global context
         - `raw` -- `bool`, raw processing flag

        Envs:
         - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)
         - `WALRUS_TABSIZE` -- indentation tab size (same as `--tabsize` option in CLI)
         - `WALRUS_LINTING` -- lint converted codes (same as `--linting` option in CLI)

        """
        if tabsize is None:
            tabsize = self.guess_tabsize(node)
        if linesep is None:
            linesep = self.guess_linesep(node)
        if keyword is None:
            keyword = self.guess_keyword(node)
        if context is None:
            context = list()
        self._linting = BOOLEAN_STATES.get(os.getenv('WALRUS_LINTING', '0').casefold(), False)

        self._root = node  # root node
        self._column = column  # current indentation
        self._tabsize = tabsize  # indentation size
        self._linesep = linesep  # line seperator
        self._keyword = keyword  # global / nonlocal keyword
        self._context = list(context)  # names in global statements

        self._prefix_or_suffix = True  # flag if buffer is now prefix
        self._node_before_walrus = None  # node preceding node with walrus

        self._prefix = ''  # codes before insersion point
        self._suffix = ''  # codes after insersion point
        self._buffer = ''  # final result

        self._vars = list()  # variable initialisation
        self._lamb = list()  # converted lambda definitions ({param, suite, uuid})
        self._func = list()  # wrapper functions ({name, uuid, keyword})

        self._walk(node)  # traverse children
        if raw:
            self._buffer = self._prefix + self._suffix
        else:
            self._concat()  # generate final result

    def __iadd__(self, code):
        if self._prefix_or_suffix:
            self._prefix += code
        else:
            self._suffix += code
        return self

    def __str__(self):
        return self._buffer.strip()

    def _walk(self, node):
        """Start traversing the AST module.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        """
        # process node
        if hasattr(node, 'children'):
            last_node = None
            for child in node.children:
                if self.has_walrus(child):
                    self._prefix_or_suffix = False
                    self._node_before_walrus = last_node
                self._process(child)
                last_node = child
            return

        # process leaf
        self += node.get_code()

    def _process(self, node):
        """Walk parso AST.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        """
        # 'funcdef', 'classdef', 'if_stmt', 'while_stmt', 'for_stmt', 'with_stmt', 'try_stmt'
        func_name = '_process_%s' % node.type
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            func(node)
            return

        if hasattr(node, 'children'):
            for child in node.children:
                func_name = '_process_%s' % child.type
                func = getattr(self, func_name, self._process)
                func(child)
            return

        # leaf node
        self += node.get_code()

    def _process_suite_node(self, node, func=False, raw=False, cls_ctx=None):
        """Process indented suite (`suite` or ...).

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, suite node
         - `func` -- `bool`, if the suite is of function definition
         - `raw` -- `bool`, raw processing flag
         - `cls_ctx` -- `Optional[str]`, class name when suite if of class contextion

        """
        if not self.has_walrus(node):
            self += node.get_code()
            return

        indent = self._column + self._tabsize
        self += self._linesep + '\t'.expandtabs(indent)

        if func:
            keyword = 'nonlocal'
        else:
            keyword = self._keyword

        # process suite
        if cls_ctx is None:
            ctx = Context(node=node, context=self._context,
                          column=indent, tabsize=self._tabsize,
                          linesep=self._linesep, keyword=keyword, raw=raw)
        else:
            ctx = ClassContext(cls_ctx=cls_ctx,
                               node=node, context=self._context,
                               column=indent, tabsize=self._tabsize,
                               linesep=self._linesep, keyword=keyword, raw=raw)
        self += ctx.string.lstrip()

        # keep records
        if raw:
            self._lamb.extend(ctx.lambdef)
            self._vars.extend(ctx.variables)
            self._func.extend(ctx.functions)
        self._context.extend(ctx.global_stmt)

    def _process_namedexpr_test(self, node):
        """Process assignment expression (`namedexpr_test`).

        Args:
         - `node` -- `parso.python.tree.PythonNode`, assignment expression node

        """
        # split assignment expression
        node_name, _, node_expr = node.children
        name = node_name.value
        nuid = uuid_gen.gen()

        # calculate expression string
        ctx = Context(node=node_expr, context=self._context,
                      column=self._column, tabsize=self._tabsize,
                      linesep=self._linesep, keyword=self._keyword, raw=True)
        expr = ctx.string.strip()
        self._vars.extend(ctx.variables)
        self._func.extend(ctx.functions)

        # replacing codes
        code = CALL_TEMPLATE % dict(name=name, uuid=nuid, expr=expr)
        prefix, suffix = self.extract_whitespaces(node)
        self += prefix + code + suffix

        self._context.extend(ctx.global_stmt)
        if name in self._context:
            keyword = 'global'
        else:
            keyword = self._keyword

        # keep records
        self._vars.append(name)
        self._func.append(dict(name=name, uuid=nuid, keyword=keyword))

    def _process_global_stmt(self, node):
        """Process function definition (``global_stmt``).

        Args:
         - `node` -- `parso.python.tree.GlobalStmt`, global statement node

        """
        children = iter(node.children)

        # <Keyword: global>
        next(children)
        # <Name: ...>
        name = next(children)
        self._context.append(name.value)

        while True:
            try:
                # <Operator: ,>
                next(children)
            except StopIteration:
                break

            # <Name: ...>
            name = next(children)
            self._context.append(name.value)

        # process code
        self += node.get_code()

    def _process_classdef(self, node):
        """Process class definition (``classdef``).

        Args:
         - `node` -- `parso.python.tree.Class`, class node

        """
        flag = self.has_walrus(node)
        code = node.get_code()

        # <Name: ...>
        name = node.name
        if flag:
            if self._linting:
                buffer = self._prefix if self._prefix_or_suffix else self._suffix

                self += self._linesep * self.missing_whitespaces(prefix=buffer, suffix=code,
                                                                 blank=1, linesep=self._linesep)

            self += '\t'.expandtabs(self._column) \
                 + LCL_DICT_TEMPLATE % dict(cls=name.value) \
                 + self._linesep

            if self._linting:
                blank = 2 if self._column == 0 else 1
                buffer = self._prefix if self._prefix_or_suffix else self._suffix

                self += self._linesep * self.missing_whitespaces(prefix=buffer, suffix=code,
                                                                 blank=1, linesep=self._linesep)

        # <Keyword: class>
        # <Name: ...>
        # [<Operator: (>, PythonNode(arglist, [...]]), <Operator: )>]
        # <Operator: :>
        for child in node.children[:-1]:
            self._process(child)

        # PythonNode(suite, [...]) / PythonNode(simple_stmt, [...])
        suite = node.children[-1]
        self._process_suite_node(suite, cls_ctx=name.value)

        if flag:
            indent = '\t'.expandtabs(self._column)
            tabsize = '\t'.expandtabs(self._tabsize)

            if self._linting:
                blank = 2 if self._column == 0 else 1
                buffer = self._prefix if self._prefix_or_suffix else self._suffix
                self += self._linesep * self.missing_whitespaces(prefix=buffer, suffix='',
                                                                 blank=blank, linesep=self._linesep)

            self += indent \
                 + ('%s%s' % (self._linesep, indent)).join(LCL_VARS_TEMPLATE) % dict(tabsize=tabsize, cls=name.value) \
                 + self._linesep

            if self._linting:
                buffer = self._prefix if self._prefix_or_suffix else self._suffix

                code = ''
                leaf = node.get_next_leaf()
                while leaf is not None:
                    code += leaf.get_code()
                    leaf = leaf.get_next_leaf()
                self += self._linesep * self.missing_whitespaces(prefix=buffer, suffix=code,
                                                                 blank=1, linesep=self._linesep)

    def _process_funcdef(self, node):
        """Process function definition (``funcdef``).

        Args:
         - `node` -- `parso.python.tree.Function`, function node

        """
        # 'def' NAME '(' PARAM ')' [ '->' NAME ] ':' SUITE
        for child in node.children[:-1]:
            self._process(child)
        self._process_suite_node(node.children[-1], func=True)

    def _process_lambdef(self, node):
        """Process lambda definition (``lambdef``).

        Args:
         - `node` -- `parso.python.tree.Lambda`, lambda node

        """
        if not self.has_walrus(node):
            self += node.get_code()
            return

        children = iter(node.children)

        # <Keyword: lambda>
        next(children)

        # vararglist
        para_list = list()
        for child in children:
            if child.type == 'operator' and child.value == ':':
                break
            para_list.append(child)
        param = ''.join(map(lambda n: n.get_code(), para_list))

        # test_nocond | test
        indent = self._column + self._tabsize
        ctx = LambdaContext(node=next(children), context=self._context,
                            column=indent, tabsize=self._tabsize,
                            linesep=self._linesep, keyword='nonlocal')
        suite = ctx.string.strip()

        # keep record
        nuid = uuid_gen.gen()
        self._lamb.append(dict(param=param, suite=suite, uuid=nuid))

        # replacing lambda
        self += LAMBDA_CALL_TEMPLATE % dict(uuid=nuid)

    def _process_if_stmt(self, node):
        """Process if statement (``if_stmt``).

        Args:
         - `node` -- `parso.python.tree.IfStmt`, if node

        """
        children = iter(node.children)

        # <Keyword: if>
        self._process(next(children))
        # namedexpr_test
        self._process(next(children))
        # <Operator: :>
        self._process(next(children))
        # suite
        self._process_suite_node(next(children))

        while True:
            try:
                # <Keyword: elif | else>
                key = next(children)
            except StopIteration:
                break
            self._process(key)

            if key.value == 'elif':
                # namedexpr_test
                self._process(next(children))
                # <Operator: :>
                self._process(next(children))
                # suite
                self._process_suite_node(next(children))
                continue
            if key.value == 'else':
                # <Operator: :>
                self._process(next(children))
                # suite
                self._process_suite_node(next(children))
                continue

    def _process_while(self, node):
        """Process while statement (``while_stmt``).

        Args:
         - `node` -- `parso.python.tree.WhileStmt`, if node

        """
        children = iter(node.children)

        # <Keyword: while>
        self._process(next(children))
        # namedexpr_test
        self._process(next(children))
        # <Operator: :>
        self._process(next(children))
        # suite
        self._process_suite_node(next(children))

        try:
            key = next(children)
        except StopIteration:
            return

        # <Keyword: else>
        self._process(key)
        # <Operator: :>
        self._process(next(children))
        # suite
        self._process_suite_node(next(children))

    def _process_for_stmt(self, node):
        """Process for statement (``for_stmt``).

        Args:
         - `node` -- `parso.python.tree.ForStmt`, for node

        """
        children = iter(node.children)

        # <Keyword: for>
        self._process(next(children))
        # exprlist
        self._process(next(children))
        # <Keyword: in>
        self._process(next(children))
        # testlist
        self._process(next(children))
        # <Operator: :>
        self._process(next(children))
        # suite
        self._process_suite_node(next(children))

        try:
            key = next(children)
        except StopIteration:
            return

        # <Keyword: else>
        self._process(key)
        # <Operator: :>
        self._process(next(children))
        # suite
        self._process_suite_node(next(children))

    def _process_with_stmt(self, node):
        """Process with statement (``with_stmt``).

        Args:
         - `node` -- `parso.python.tree.WithStmt`, with node

        """
        children = iter(node.children)

        # <Keyword: with>
        self._process(next(children))

        while True:
            # with_item | <Operator: ,>
            item = next(children)
            self._process(item)

            # <Operator: :>
            if item.type == 'operator' and item.value == ':':
                break

        # suite
        self._process_suite_node(next(children))

    def _process_try_stmt(self, node):
        """Process try statement (``try_stmt``).

        Args:
         - `node` -- `parso.python.tree.TryStmt`, try node

        """
        children = iter(node.children)

        while True:
            try:
                key = next(children)
            except StopIteration:
                break

            # <Keyword: try | else | finally> | PythonNode(except_clause, [...]
            self._process(key)
            # <Operator: :>
            self._process(next(children))
            # suite
            self._process_suite_node(next(children))

    def _process_argument(self, node):
        """Process function argument (`argument`).

        Args:
         - `node` -- `parso.python.tree.PythonNode`, argument node

        """
        children = iter(node.children)

        # test
        test = next(children)
        try:
            # <Operator: :=>
            op = next(children)
        except StopIteration:
            self._process(test)
            return

        if self.is_walrus(op):
            self._process_namedexpr_test(node)
            return

        # not walrus
        self._process(test)
        self._process(op)
        for child in children:
            self._process(child)

    def _concat(self):
        """Concatenate final string."""
        flag = self.has_walrus(self._root)

        # strip suffix comments
        prefix, suffix = self._strip()

        # first, the prefix codes
        self._buffer += self._prefix + prefix
        if flag and self._linting and self._buffer:
            if (self._node_before_walrus is not None \
                    and self._node_before_walrus.type in ('funcdef', 'classdef') \
                    and self._column == 0):
                blank = 2
            else:
                blank = 1
            self._buffer += self._linesep * self.missing_whitespaces(prefix=self._buffer, suffix='',
                                                                     blank=blank, linesep=self._linesep)

        # then, the variables and functions
        indent = '\t'.expandtabs(self._column)
        tabsize = '\t'.expandtabs(self._tabsize)
        if self._linting:
            linesep = self._linesep * (1 if self._column > 0 else 2)
        else:
            linesep = ''
        if self._vars:
            name_list = ' = '.join(sorted(set(self._vars)))
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(NAME_TEMPLATE) % dict(tabsize=tabsize, name_list=name_list) + self._linesep
        for func in sorted(self._func, key=lambda func: func['name']):
            if self._buffer:
                self._buffer += linesep
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(FUNC_TEMPLATE) % dict(tabsize=tabsize, **func) + self._linesep
        for lamb in self._lamb:
            if self._buffer:
                self._buffer += linesep
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(LAMBDA_FUNC_TEMPLATE) % dict(tabsize=tabsize, **lamb) + self._linesep

        # finally, the suffix codes
        if flag and self._linting:
            blank = 2 if self._column == 0 else 1
            self._buffer += self._linesep * self.missing_whitespaces(prefix=self._buffer, suffix=suffix,
                                                                     blank=blank, linesep=self._linesep)
        self._buffer += suffix

    def _strip(self):
        """Strip comments from suffix buffer.

        Returns:
         - `str` -- prefix comments
         - `str` -- suffix strings

        """
        prefix = ''
        suffix = ''

        lines = io.StringIO(self._suffix, newline=self._linesep)
        for line in lines:
            if line.strip().startswith('#'):
                prefix += line
                continue
            suffix += line
            break

        for line in lines:
            suffix += line
        return prefix, suffix

    @classmethod
    def has_walrus(cls, node):
        """Check if node has assignment expression. (`namedexpr_test`)

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Returns:
         - `bool` -- if node has assignment expression

        """
        if cls.is_walrus(node):
            return True
        if hasattr(node, 'children'):
            for child in node.children:
                if cls.has_walrus(child):
                    return True
        return False

    @classmethod
    def guess_keyword(cls, node):
        """Guess keyword based on node position.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Returns:
         - `str` -- keyword

        """
        if isinstance(node, parso.python.tree.Module):
            return 'global'

        parent = node.parent
        if isinstance(parent, parso.python.tree.Module):
            return 'global'
        if parent.type in ['funcdef', 'classdef']:
            return 'nonlocal'
        return cls.guess_keyword(parent)

    @classmethod
    def guess_tabsize(cls, node):
        """Check indentation tab size.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Env:
         - `WALRUS_TABSIZE` -- indentation tab size (same as `--tabsize` option in CLI)

        Returns:
         - `int` -- indentation tab size

        """
        for child in node.children:
            if child.type != 'suite':
                if hasattr(child, 'children'):
                    return cls.guess_tabsize(child)
                continue
            return child.children[1].get_first_leaf().column
        return int(os.getenv('WALRUS_TABSIZE', __walrus_tabsize__))

    @staticmethod
    def guess_linesep(node):
        """Guess line separator based on source code.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Envs:
         - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)

        Returns:
         - `str` -- line separator

        """
        root = node.get_root_node()
        code = root.get_code()

        pool = {
            '\r': 0,
            '\r\n': 0,
            '\n': 0,
        }
        for line in code.splitlines(True):
            if line.endswith('\r'):
                pool['\r'] += 1
            elif line.endswith('\r\n'):
                pool['\r\n'] += 1
            else:
                pool['\n'] += 1

        sort = sorted(pool, key=lambda k: pool[k])
        if pool[sort[0]] > pool[sort[1]]:
            return sort[0]

        env = os.getenv('WALRUS_LINESEP', os.linesep)
        env_name = env.upper()
        if env_name == 'CR':
            return '\r'
        if env_name == 'CRLF':
            return '\r\n'
        if env_name == 'LF':
            return '\n'
        if env in ['\r', '\r\n', '\n']:
            return env
        raise EnvironError('invalid line separator %r' % env)

    @staticmethod
    def is_walrus(node):
        """Check if node is assignment expression.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Returns:
         - `bool` -- if node is assignment expression

        """
        if node.type == 'namedexpr_test':
            return True
        if node.type == 'operator' and node.value == ':=':
            return True
        return False

    @staticmethod
    def missing_whitespaces(prefix, suffix, blank, linesep):
        """Count missing preceding or succeeding blank lines.

        Args:
         - `prefix` -- `str`, preceding source code
         - `suffix` -- `str`, succeeding source code
         - `blank` -- `int`, number of expecting blank lines
         - `linesep` -- `str`, line seperator

        Returns:
         - `int` -- number of preceding blank lines

        """
        count = 0
        if prefix:
            for line in reversed(prefix.split(linesep)):
                if line.strip():
                    break
                count += 1
            if count > 0:  # keep trailing newline in `prefix`
                count -= 1
        if suffix:
            for line in suffix.split(linesep):
                if line.strip():
                    break
                count += 1

        if count < 0:
            count = 0
        missing = blank - count
        if missing > 0:
            return missing
        return 0

    @staticmethod
    def extract_whitespaces(node):
        """Extract preceding and succeeding whitespaces.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST

        Returns:
         - `str` -- preceding whitespaces
         - `str` -- succeeding whitespaces

        """
        code = node.get_code()

        # preceding whitespaces
        prefix = ''
        for char in code:
            if char not in ' \t\n\r\f\v':
                break
            prefix += char

        # succeeding whitespaces
        suffix = ''
        for char in reversed(code):
            if char not in ' \t\n\r\f\v':
                break
            suffix += char

        return prefix, suffix


class LambdaContext(Context):
    """Lambda (suite) conversion context."""

    def _concat(self):
        """Concatenate final string."""
        flag = self.has_walrus(self._root)

        # first, the variables and functions
        indent = '\t'.expandtabs(self._column)
        tabsize = '\t'.expandtabs(self._tabsize)
        if self._linting:
            linesep = self._linesep * (1 if self._column > 0 else 2)
        else:
            linesep = ''
        if self._vars:
            name_list = ' = '.join(sorted(set(self._vars)))
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(NAME_TEMPLATE) % dict(tabsize=tabsize, name_list=name_list) + self._linesep
        for func in sorted(self._func, key=lambda func: func['name']):
            if self._buffer:
                self._buffer += linesep
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(FUNC_TEMPLATE) % dict(tabsize=tabsize, **func) + self._linesep
        for lamb in self._lamb:
            if self._buffer:
                self._buffer += linesep
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(LAMBDA_FUNC_TEMPLATE) % dict(tabsize=tabsize, **lamb) + self._linesep
        if flag and self._linting:
            blank = 2 if self._column == 0 else 1
            self._buffer += self._linesep * self.missing_whitespaces(prefix=self._buffer, suffix=self._prefix,
                                                                     blank=blank, linesep=self._linesep)

        # then, the `return` statement
        self._buffer += indent + 'return'

        # finally, the source codes
        self._buffer += self._prefix + self._suffix


class ClassContext(Context):
    """Class (suite) conversion context."""

    @property
    def cls_var(self):
        return self._cls_var

    def __init__(self, node,
                 cls_ctx, cls_var=None,
                 column=0, tabsize=None,
                 linesep=None, keyword=None,
                 context=None, raw=False):
        """Conversion context.

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, parso AST
         - `cls_ctx` -- `str`, class context name
         - `cls_var` -- `Dict[str, str]`, mapping for assignment variable and its UUID
         - `column` -- `int`, current indentation level
         - `tabsize` -- `Optional[int]`, indentation tab size
         - `linesep` -- `Optional[str]`, line seperator
         - `keyword` -- `Optional[str]`, keyword for wrapper function
         - `context` -- `Optional[List[str]]`, global context
         - `raw` -- `bool`, raw context processing flag

        Envs:
         - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)
         - `WALRUS_TABSIZE` -- indentation tab size (same as `--tabsize` option in CLI)
         - `WALRUS_LINTING` -- lint converted codes (same as `--linting` option in CLI)

        """
        if cls_var is None:
            cls_var = dict()

        self._cls_raw = raw
        self._cls_var = cls_var
        self._cls_ctx = cls_ctx

        super().__init__(node=node, context=context,
                         column=column, tabsize=tabsize,
                         linesep=linesep, keyword=keyword, raw=raw)

    def _process_suite_node(self, node, func=False, raw=False, cls_ctx=None):
        """Process indented suite (`suite` or ...).

        Args:
         - `node` -- `Union[parso.python.tree.PythonNode, parso.python.tree.PythonLeaf]`, suite node
         - `func` -- `bool`, if the suite is of function definition
         - `raw` -- `bool`, raw context processing flag
         - `cls_ctx` -- `Optional[str]`, class name when suite if of class contextion

        """
        if not self.has_walrus(node):
            self += node.get_code()
            return

        indent = self._column + self._tabsize
        self += self._linesep + '\t'.expandtabs(indent)

        if cls_ctx is None:
            cls_ctx = self._cls_ctx
        cls_var = self._cls_var

        if func:
            keyword = 'nonlocal'

            # process suite
            ctx = Context(node=node, context=self._context,
                          column=indent, tabsize=self._tabsize,
                          linesep=self._linesep, keyword=keyword)
        else:
            keyword = self._keyword

            # process suite
            ctx = ClassContext(cls_ctx=cls_ctx, cls_var=cls_var,
                               node=node, context=self._context,
                               column=indent, tabsize=self._tabsize,
                               linesep=self._linesep, keyword=keyword)
        self += ctx.string.lstrip()

        # keep record
        if raw:
            self._lamb.extend(ctx.lambdef)
            self._vars.extend(ctx.variables)
            self._func.extend(ctx.functions)
            self._cls_var.update(ctx.cls_var)
        self._context.extend(ctx.global_stmt)

    def _process_namedexpr_test(self, node):
        """Process assignment expression (`namedexpr_test`).

        Args:
         - `node` -- `parso.python.tree.PythonNode`, assignment expression node

        """
        # split assignment expression
        node_name, _, node_expr = node.children
        name = node_name.value
        nuid = uuid_gen.gen()

        # calculate expression string
        ctx = ClassContext(cls_ctx=self._cls_ctx, cls_var=self._cls_var,
                           node=node_expr, context=self._context,
                           column=self._column, tabsize=self._tabsize,
                           linesep=self._linesep, keyword=self._keyword, raw=True)
        expr = ctx.string.strip()
        self._lamb.extend(ctx.lambdef)
        self._vars.extend(ctx.variables)
        self._func.extend(ctx.functions)
        self._cls_var.update(ctx.cls_var)

        # replacing codes
        code = CLS_CALL_TEMPLATE % dict(cls=self._cls_ctx, name=name, uuid=nuid, expr=expr)
        prefix, suffix = self.extract_whitespaces(node)
        self += prefix + code + suffix

        self._context.extend(ctx.global_stmt)
        if name in self._context:
            keyword = 'global'
        else:
            keyword = self._keyword

        # keep records
        self._vars.append(name)
        self._func.append(dict(name=name, uuid=nuid, keyword=keyword))
        self._cls_var[name] = nuid

    def _process_defined_name(self, node):
        """Process defined name (`name`).

        Args:
         - `node` -- `parso.python.tree.Name`, defined name node

        """
        name = node.value
        nuid = uuid_gen.gen()

        prefix, _ = self.extract_whitespaces(node)
        self += prefix + LCL_NAME_TEMPLATE % dict(cls=self._cls_ctx, name=name)

        self._vars.append(name)
        self._func.append(dict(name=name, uuid=nuid, keyword=self._keyword))
        self._cls_var[name] = nuid

    def _process_expr_stmt(self, node):
        """Process variable name (`expr_stmt`).

        Args:
         - `node` -- `parso.python.tree.ExprStmt`, expression statement

        """
        # right hand side expression
        rhs = node.get_rhs()

        for child in node.children:
            if child == rhs:
                self._process(child)
                continue
            if child.type == 'name':
                self._process_defined_name(child)
                continue
            self += child.get_code()

    def _process_name(self, node):
        """Process variable name (`name`).

        Args:
         - `node` -- `parso.python.tree.Name`, variable name

        """
        name = node.value

        if name in self._cls_var:
            prefix, _ = self.extract_whitespaces(node)
            self += prefix + LCL_CALL_TEMPLATE % dict(cls=self._cls_ctx, name=name, uuid=self._cls_var[name])
            return

        # normal processing
        self += node.get_code()

    def _concat(self):
        """Concatenate final string."""
        flag = self.has_walrus(self._root)

        # strip suffix comments
        prefix, suffix = self._strip()

        # first, the prefix codes
        self._buffer += self._prefix + prefix

        # then, the class and functions
        indent = '\t'.expandtabs(self._column)
        tabsize = '\t'.expandtabs(self._tabsize)
        linesep = self._linesep
        if flag:
            if self._linting:
                if (self._node_before_walrus is not None
                        and self._node_before_walrus.type in ('funcdef', 'classdef')
                        and self._column == 0):
                    blank = 2
                else:
                    blank = 1
                self._buffer += self._linesep * self.missing_whitespaces(prefix=self._buffer, suffix='',
                                                                         blank=blank, linesep=self._linesep)
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(CLS_NAME_TEMPLATE) % dict(tabsize=tabsize, cls=self._cls_ctx) + linesep
        for func in sorted(self._func, key=lambda func: func['name']):
            if self._buffer:
                self._buffer += linesep
            self._buffer += indent + (
                '%s%s' % (self._linesep, indent)
            ).join(CLS_FUNC_TEMPLATE) % dict(tabsize=tabsize, cls=self._cls_ctx, **func) + linesep

        # finally, the suffix codes
        if flag and self._linting:
            blank = 2 if self._column == 0 else 1
            self._buffer += self._linesep * self.missing_whitespaces(prefix=self._buffer, suffix=suffix,
                                                                     blank=blank, linesep=self._linesep)
        self._buffer += suffix


def convert(string, source='<unknown>'):
    """The main conversion process.

    Args:
     - `string` -- `str`, context to be converted
     - `source` -- `str`, source of the context

    Envs:
     - `WALRUS_VERSION` -- convert against Python version (same as `--python` option in CLI)
     - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)
     - `WALRUS_LINTING` -- lint converted codes (same as `--linting` option in CLI)

    Returns:
     - `str` -- converted string

    """
    # Initialise new UUID4Generator for identifier UUIDs
    global uuid_gen
    uuid_gen = UUID4Generator(dash=False)

    # parse source string
    module = parse(string, source)

    # convert source string
    string = Context(module).string

    # return converted string
    return string


def walrus(filename):
    """Wrapper works for conversion.

    Args:
     - `filename` -- `str`, file to be converted

    Envs:
     - `WALRUS_QUIET` -- run in quiet mode (same as `--quiet` option in CLI)
     - `WALRUS_ENCODING` -- encoding to open source files (same as `--encoding` option in CLI)
     - `WALRUS_VERSION` -- convert against Python version (same as `--python` option in CLI)
     - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)
     - `WALRUS_LINTING` -- lint converted codes (same as `--linting` option in CLI)

    """
    WALRUS_QUIET = BOOLEAN_STATES.get(os.getenv('WALRUS_QUIET', '0').casefold(), False)
    if not WALRUS_QUIET:  # pragma: no cover
        print('Now converting %r...' % filename)

    # fetch encoding
    encoding = os.getenv('WALRUS_ENCODING', LOCALE_ENCODING)

    # file content
    with open(filename, 'r', encoding=encoding, newline='') as file:
        text = file.read()

    # do the dirty things
    text = convert(text, filename)

    # dump back to the file
    with open(filename, 'w', encoding=encoding, newline='') as file:
        file.write(text)


###############################################################################
# CLI & entry point

# default values
__cwd__ = os.getcwd()
__archive__ = os.path.join(__cwd__, 'archive')
__walrus_version__ = os.getenv('WALRUS_VERSION', WALRUS_VERSION[-1])
__walrus_encoding__ = os.getenv('WALRUS_ENCODING', LOCALE_ENCODING)
__walrus_linesep__ = os.getenv('WALRUS_LINESEP', os.linesep)
__walrus_tabsize__ = os.getenv('WALRUS_TABSIZE', '4')


def get_parser():
    """Generate CLI parser.

    Returns:
     - `argparse.ArgumentParser` -- CLI parser for walrus

    """
    parser = argparse.ArgumentParser(prog='walrus',
                                     usage='walrus [options] <python source files and folders...>',
                                     description='Back-port compiler for Python 3.8 assignment expressions.')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-q', '--quiet', action='store_true', help='run in quiet mode')

    archive_group = parser.add_argument_group(title='archive options',
                                              description="duplicate original files in case there's any issue")
    archive_group.add_argument('-na', '--no-archive', action='store_false', dest='archive',
                               help='do not archive original files')
    archive_group.add_argument('-p', '--archive-path', action='store', default=__archive__, metavar='PATH',
                               help='path to archive original files (%(default)s)')

    convert_group = parser.add_argument_group(title='convert options',
                                              description='compatibility configuration for non-unicode files')
    convert_group.add_argument('-c', '--encoding', action='store', default=__walrus_encoding__, metavar='CODING',
                               help='encoding to open source files (%(default)s)')
    convert_group.add_argument('-v', '--python', action='store', metavar='VERSION',
                               default=__walrus_version__, choices=WALRUS_VERSION,
                               help='convert against Python version (%(default)s)')
    convert_group.add_argument('-s', '--linesep', action='store', default=__walrus_linesep__, metavar='SEP',
                               help='line separator to process source files (%(default)r)')
    convert_group.add_argument('-nl', '--no-linting', action='store_false', dest='linting',
                               help='do not lint converted codes')
    convert_group.add_argument('-t', '--tabsize', action='store', default=__walrus_tabsize__, metavar='INDENT',
                               help='indentation tab size (%(default)s)', type=int)

    parser.add_argument('file', nargs='+', metavar='SOURCE', default=__cwd__,
                        help='python source files and folders to be converted (%(default)s)')

    return parser


def main(argv=None):
    """Entry point for walrus.

    Args:
     - `argv` -- `List[str]`, CLI arguments (default: None)

    Envs:
     - `WALRUS_QUIET` -- run in quiet mode (same as `--quiet` option in CLI)
     - `WALRUS_ENCODING` -- encoding to open source files (same as `--encoding` option in CLI)
     - `WALRUS_VERSION` -- convert against Python version (same as `--python` option in CLI)
     - `WALRUS_LINESEP` -- line separator to process source files (same as `--linesep` option in CLI)
     - `WALRUS_LINTING` -- lint converted codes (same as `--linting` option in CLI)
     - `WALRUS_TABSIZE` -- indentation tab size (same as `--tabsize` option in CLI)

    """
    parser = get_parser()
    args = parser.parse_args(argv)

    # set up variables
    ARCHIVE = args.archive_path
    os.environ['WALRUS_VERSION'] = args.python
    os.environ['WALRUS_ENCODING'] = args.encoding
    os.environ['WALRUS_TABSIZE'] = str(args.tabsize)
    WALRUS_QUIET = os.getenv('WALRUS_QUIET')
    os.environ['WALRUS_QUIET'] = '1' if args.quiet else ('0' if WALRUS_QUIET is None else WALRUS_QUIET)
    WALRUS_LINTING = os.getenv('WALRUS_LINTING')
    os.environ['WALRUS_LINTING'] = '1' if args.linting else ('0' if WALRUS_LINTING is None else WALRUS_LINTING)

    linesep = args.linesep.upper()
    if linesep == 'CR':
        os.environ['WALRUS_LINESEP'] = '\r'
    elif linesep == 'CRLF':
        os.environ['WALRUS_LINESEP'] = '\r\n'
    elif linesep == 'LF':
        os.environ['WALRUS_LINESEP'] = '\n'
    elif args.linesep in ['\r', '\r\n', '\n']:
        os.environ['WALRUS_LINESEP'] = args.linesep
    else:
        raise EnvironError('invalid line separator %r' % args.linesep)

    # fetch file list
    filelist = sorted(detect_files(args.file))

    # if no file supplied
    if not filelist:  # pragma: no cover
        parser.error('no valid source file found')

    # make archive
    if args.archive:
        archive_files(filelist, ARCHIVE)

    # process files
    if mp is None or CPU_CNT <= 1:
        [walrus(filename) for filename in filelist]  # pylint: disable=expression-not-assigned # pragma: no cover
    else:
        with mp.Pool(processes=CPU_CNT) as pool:
            pool.map(walrus, filelist)


if __name__ == '__main__':
    sys.exit(main())
