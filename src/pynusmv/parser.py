"""
The :mod:`pynusmv.parser` module provides functions to parse strings
and return corresponding ASTs.

"""


__all__ = ['parse_simple_expression', 'parse_next_expression',
           'parse_identifier',
           "identifier", "simple_expression", "constant", "next_expression",
           "type_identifier",
           "var_section", "ivar_section", "frozenvar_section", "define_section",
           "constants_section",
           "assign_constraint", "trans_constraint", "init_constraint",
           "invar_constraint", "fairness_constraint",
           "module", "model",
           "parseAllString"]


from .exception import NuSMVParsingError, Error

from .utils import update
from .model import *
     
from .nusmv.parser import parser as nsparser
from .nusmv.node import node as nsnode

from pyparsing import (Word as PWord, Keyword, Forward, Optional, Literal,
                       OneOrMore, NotAny, FollowedBy, Suppress, ZeroOrMore,
                       Combine, Group,
                       oneOf, infixNotation, delimitedList, restOfLine,
                       alphas, alphanums, nums, opAssoc,
                       ParserElement,
                       getTokensEndLoc)
from collections import OrderedDict
from functools import reduce


def parse_simple_expression(expression):
    """
    Parse a simple expression.
    
    :param string expression: the expression to parse
    :raise: a :exc:`NuSMVParsingError
            <pynusmv.exception.NuSMVParsingError>`
            if a parsing error occurs
    
    .. warning:: Returned value is a SWIG wrapper for the NuSMV node_ptr.
       It is the responsibility of the caller to manage it.
    
    """
    node, err = nsparser.ReadSimpExprFromString(expression)
    if err:
        errlist = []
        errors = nsparser.Parser_get_syntax_errors_list()
        while errors is not None:
            error = nsnode.car(errors)
            err = nsparser.Parser_get_syntax_error(error)
            errlist.append(Error(*err[1:]))
            errors = nsnode.cdr(errors)
        raise NuSMVParsingError(tuple(errlist))
    else:
        return nsnode.car(node) # Get rid of the top SIMPWFF node
        
        
def parse_next_expression(expression):
    """
    Parse a "next" expression.
    
    :param string expression: the expression to parse
    :raise: a :exc:`NuSMVParsingError
            <pynusmv.exception.NuSMVParsingError>`
            if a parsing error occurs
    
    .. warning:: Returned value is a SWIG wrapper for the NuSMV node_ptr.
       It is the responsibility of the caller to manage it.
    
    """
    node, err = nsparser.ReadNextExprFromString(expression)
    if err:
        errlist = []
        errors = nsparser.Parser_get_syntax_errors_list()
        while errors is not None:
            error = nsnode.car(errors)
            err = nsparser.Parser_get_syntax_error(error)
            errlist.append(Error(*err[1:]))
            errors = nsnode.cdr(errors)
        raise NuSMVParsingError(tuple(errlist))
    else:
        return nsnode.car(node) # Get rid of the top NEXTWFF node
        
        
def parse_identifier(expression):
    """
    Parse an identifier
    
    :param string expression: the identifier to parse
    :raise: a :exc:`NuSMVParsingError
            <pynusmv.exception.NuSMVParsingError>`
            if a parsing error occurs
    
    .. warning:: Returned value is a SWIG wrapper for the NuSMV node_ptr.
       It is the responsibility of the caller to manage it.
    
    """
    node, err = nsparser.ReadIdentifierExprFromString(expression)
    if err:
        errlist = []
        errors = nsparser.Parser_get_syntax_errors_list()
        while errors is not None:
            error = nsnode.car(errors)
            err = nsparser.Parser_get_syntax_error(error)
            errlist.append(Error(*err[1:]))
            errors = nsnode.cdr(errors)
        raise NuSMVParsingError(tuple(errlist))
    else:
        return nsnode.car(node) # Get rid of the top COMPID node



def _reduce_list_to_expr(l):
    """
    Reduces l to its token representation.
    l a list of tokens separated by operators, with at least one token.
    """
    
    _otc = {"*": Mult, "/": Div, "mod": Mod, "+": Add, "-": Sub,
            "<<": ShiftL, ">>": ShiftR,
            "=": Eq, "!=": Neq, "<": Lt, ">": Gt, "<=": Le, ">=": Ge,
            "|": Or, "xor": Xor, "xnor": Xnor}
    
    res = l[0]
    for op, t in zip(l[1::2], l[2::2]):
        res = _otc[op](res, t)
    return res
    

# Identifiers
identifier = PWord(alphas + "_", alphanums + "_$#-")
identifier.setParseAction(lambda s, l, t: Identifier(t[0]))

simple_expression = Forward()

# Variable and DEFINE identifiers
_cip = Forward()
_cip <<= Optional( "." + Literal("self") + _cip
                 | "." + identifier + _cip
                 | "[" + simple_expression + "]" + _cip
                 )
_complex_identifier = ( (FollowedBy("self") + Literal("self") + _cip)
                      | (identifier + _cip)
                      )
_complex_identifier.setParseAction(lambda s, l, t: ComplexIdentifier(t))

_define_identifier = _complex_identifier
_variable_identifier = _complex_identifier


# Integer numbers
_integer_number = Combine(Optional("-") + PWord(nums))
_integer_number.setParseAction(lambda s, l, t: int(t[0]))

# Constants
_boolean_constant = oneOf("TRUE FALSE")
_boolean_constant.setParseAction(lambda s, l, t: Boolean(t[0]))

_integer_constant = _integer_number
_symbolic_constant = identifier
_range_constant = _integer_number + Suppress("..") + _integer_number
_range_constant.setParseAction(lambda s, l, t: Range(t[0], t[1]))

_word_sign_specifier = oneOf("u s")
_word_base = oneOf("b B o O d D h H")
_word_width = PWord(nums)
_word_value = PWord("0123456789abcdefABCDEF", "0123456789abcdefABCDEF_")
_word_constant = Combine( Literal("0") + Optional(_word_sign_specifier) 
                          + _word_base + Optional(_word_width) + "_"
                          + _word_value)
_word_constant.setParseAction(lambda s, l, t: Word(t[0]))

constant = ( _word_constant
           # Range constant is removed to follow the parser implemented by NuSMV
           #| _range_constant 
           | _integer_constant | _boolean_constant | _symbolic_constant)

# Basic expressions
_basic_expr = Forward()
_conversion = ( Literal("word1") + Suppress("(") + _basic_expr + Suppress(")")
              | Literal("bool") + Suppress("(") + _basic_expr + Suppress(")")
              | Literal("toint") + Suppress("(") + _basic_expr + Suppress(")")
              | Literal("signed") + Suppress("(") + _basic_expr + Suppress(")")
              | Literal("unsigned") + Suppress("(") + _basic_expr
                + Suppress(")")
              )
_conversion.setParseAction(lambda s, l, t: Conversion(t[0], t[1]))

_word_function = ( Literal("extend") + Suppress("(") + _basic_expr + ","
                                     + _basic_expr + Suppress(")")
                 | Literal("resize") + Suppress("(") + _basic_expr + ","
                                     + _basic_expr + Suppress(")")
                 )
_word_function.setParseAction(lambda s, l, t: WordFunction(t[0], t[1], t[2]))

_count = ( Literal("count") + Suppress("(") + delimitedList(_basic_expr)
                            + Suppress(")"))
_count.setParseAction(lambda s, l, t: Count(t[1]))

_next = Literal("next") + Suppress("(") + _basic_expr + Suppress(")")
_next.setParseAction(lambda s, l, t: Next(t[1]))

def _case_action(string, location, tokens):
    print(tokens)
    d = OrderedDict()
    for key, value in zip(tokens[::2], tokens[1::2]):
        d[key] = value
    return d
_case_case = _basic_expr + Suppress(":") + _basic_expr + Suppress(";")
_case_body = OneOrMore(_case_case)
_case_body.setParseAction(lambda s, l, t: OrderedDict(zip(t[::2], t[1::2])))
_case = Suppress("case") + _case_body + Suppress("esac")
_case.setParseAction(lambda s, l, t: Case(t[0]))

_base = ( _complex_identifier ^
        ( _conversion
        | _word_function
        | _count
        | _next
        | Suppress("(") + _basic_expr + Suppress(")")
        | _case
        | constant
        )
        )
        
_ap = Forward()
_array_subscript = Suppress("[") + _basic_expr + Suppress("]")
_array_subscript.setParseAction(lambda s, l, t: Subscript(t[0]))

_word_bit_selection = (Suppress("[") + _basic_expr + Suppress(":")
                                     + _basic_expr + Suppress("]"))
_word_bit_selection.setParseAction(lambda s, l, t: BitSelection(t[0], t[1]))

_ap <<= Optional( _array_subscript + _ap | _word_bit_selection + _ap)
_array = _base + _ap
_array.setParseAction(lambda s, l, t:
                      t[0] if len(t) <= 1 else ArrayAccess(t[0], t[1:]))

_not = ZeroOrMore("!") + _array
_not.setParseAction(lambda s, l, t: reduce(lambda e, n: Not(e), t[:-1], t[-1]))

_concat = _not + ZeroOrMore(Suppress("::") + _not)
_concat.setParseAction(lambda s, l, t: reduce(lambda e, n: Concat(e, n),
                                              t[0:1] + t[2::2]))

_minus = ZeroOrMore("-") + _concat
_minus.setParseAction(lambda s, l, t: reduce(lambda e, n: Minus(e),
                                             t[:-1], t[-1]))

_mult = _minus + ZeroOrMore(oneOf("* / mod") + _minus)
_mult.setParseAction(lambda s, l, t: _reduce_list_to_expr(t))

_add = _mult + ZeroOrMore(oneOf("+ -") + _mult)
_add.setParseAction(lambda s, l, t: _reduce_list_to_expr(t))

_shift = _add + ZeroOrMore(oneOf("<< >>") + _add)
_shift.setParseAction(lambda s, l, t: _reduce_list_to_expr(t))

_set_set = Suppress("{") + delimitedList(_basic_expr) + Suppress("}")
_set_set.setParseAction(lambda s, l, t: Set(t))
_set = ( _range_constant | _shift | _set_set )

_union = _set + ZeroOrMore("union" + _set)
_union.setParseAction(lambda s, l, t: reduce(lambda e, n: Union(e, n),
                                             t[0:1] + t[2::2]))

_in = _union + ZeroOrMore("in" + _union)
_in.setParseAction(lambda s, l, t: reduce(lambda e, n: In(e, n),
                                          t[0:1] + t[2::2]))

_comparison = _in + ZeroOrMore(oneOf("= != < > <= >=") + _in)
_comparison.setParseAction(lambda s, l, t: _reduce_list_to_expr(t))

_and = _comparison + ZeroOrMore("&" + _comparison)
_and.setParseAction(lambda s, l, t: reduce(lambda e, n: And(e, n),
                                           t[0:1] + t[2::2]))

_or = _and + ZeroOrMore(oneOf("| xor xnor") + _and)
_or.setParseAction(lambda s, l, t: _reduce_list_to_expr(t))

_ite = Forward()
_ite <<= _or + Optional("?" + _ite + ":" + _ite)
_ite.setParseAction(lambda s, l, t:
                                 t[0] if len(t) <= 1 else Ite(t[0], t[2], t[4]))

_iff = _ite + ZeroOrMore("<->" + _ite)
_iff.setParseAction(lambda s, l, t: reduce(lambda e, n: Iff(e, n),
                                           t[0:1] + t[2::2]))

_implies = Forward()
_implies <<= _iff + ZeroOrMore("->" + _implies)
_implies.setParseAction(lambda s, l, t: reduce(lambda e, n: Implies(n, e),
                                               t[0:1] + t[2::2]))

_basic_expr <<= _implies

simple_expression <<= _basic_expr
next_expression = _basic_expr

# Type specifier
_simple_type_specifier = Forward()

_boolean_type = Literal("boolean")
_boolean_type.setParseAction(lambda s, l, t: TBoolean())

_word_type = ( Optional(Literal("unsigned") | Literal("signed"))
               + Literal("word") + Suppress("[") + _basic_expr + Suppress("]") )
_word_type.setParseAction(lambda s, l, t: TWord(t[1]) if t[0] == "word"
                                          else TWord(t[2], sign=t[0]))

_enum_type = ( Suppress("{")
              + delimitedList(_integer_number | _symbolic_constant)
              + Suppress("}") )
_enum_type.setParseAction(lambda s, l, t: TEnum(t))

_range_type = _shift + Suppress("..") + _shift
_range_type.setParseAction(lambda s, l, t: TRange(t[0], t[1]))

_array_type = ( Suppress("array") + _shift + Suppress("..") + _shift
                + Suppress("of") + _simple_type_specifier )
_array_type.setParseAction(lambda s, l, t: TArray(t[0], t[1], t[2]))

_simple_type_specifier <<= ( _boolean_type
                           | _word_type
                           | _enum_type
                           | _array_type
                           | _range_type
                           )

_module_type_specifier = ( Optional("process") + identifier
                         + Optional(Suppress("(")
                                    + Optional(delimitedList(simple_expression))
                                    + Suppress(")"))
                         )
_module_type_specifier.setParseAction(lambda s, l, t:
                                      TModule(t[1],
                                              t[2:] if len(t) >= 3 else [],
                                              process=True)
                                      if t[0] == "process"
                                      else TModule(t[0],
                                                  t[1:] if len(t) >= 2 else []))

type_identifier = _simple_type_specifier | _module_type_specifier

# Variables
_var_declaration = identifier + Suppress(":") + type_identifier + Suppress(";")
_var_section_body = OneOrMore(_var_declaration)
_var_section_body.setParseAction(lambda s, l, t:
                                 OrderedDict(zip(t[::2], t[1::2])))
var_section = Suppress("VAR") + _var_section_body
var_section.setParseAction(lambda s, l, t: Variables(t[0]))

_ivar_declaration = ( identifier + Suppress(":") + _simple_type_specifier
                    + Suppress(";") )
_ivar_section_body = OneOrMore(_ivar_declaration)
_ivar_section_body.setParseAction(lambda s, l, t:
                                  OrderedDict(zip(t[::2], t[1::2])))
ivar_section = Suppress("IVAR") + _ivar_section_body
ivar_section.setParseAction(lambda s, l, t: InputVariables(t[0]))

_frozenvar_declaration = ( identifier + Suppress(":") + _simple_type_specifier
                         + Suppress(";") )
_frozenvar_section_body = OneOrMore(_frozenvar_declaration)
_frozenvar_section_body.setParseAction(lambda s, l, t:
                                       OrderedDict(zip(t[::2], t[1::2])))
frozenvar_section = Suppress("FROZENVAR") + _frozenvar_section_body
frozenvar_section.setParseAction(lambda s, l, t: FrozenVariables(t[0]))

# DEFINE and CONSTANTS
_define_declaration = ( identifier + Suppress(":=") + simple_expression
                      + Suppress(";") )
_define_section_body = OneOrMore(_define_declaration)
_define_section_body.setParseAction(lambda s, l, t:
                                    OrderedDict(zip(t[::2], t[1::2])))
define_section = Suppress("DEFINE") + _define_section_body
define_section.setParseAction(lambda s, l, t: Defines(t[0]))

_constants_section_body = delimitedList(identifier) + Suppress(";")
_constants_section_body.setParseAction(lambda s, l, t: list(t))
constants_section = Suppress("CONSTANTS") + _constants_section_body
constants_section.setParseAction(lambda s, l, t: Constants(list(t)))

# ASSIGN, TRANS, INIT, INVAR, FAIRNESS
_assign_identifier = ( Literal("init") + Suppress("(") + _complex_identifier
                       + Suppress(")")
                     | Literal("next") + Suppress("(") + _complex_identifier
                       + Suppress(")")
                     | _complex_identifier )
_assign_identifier.setParseAction(lambda s, l, t:
                                  Init(t[1]) if t[0] == "init"
                                  else Next(t[1]) if t[0] == "next"
                                  else t[0])
_assign = ( _assign_identifier + Suppress(":=") + simple_expression
          + Suppress(";") )
_assign_constraint_body = OneOrMore(_assign)
_assign_constraint_body.setParseAction(lambda s, l, t:
                                       OrderedDict(zip(t[::2], t[1::2])))
assign_constraint = Suppress("ASSIGN") + _assign_constraint_body
assign_constraint.setParseAction(lambda s, l, t: Assigns(t[0]))

_trans_constraint_body = next_expression + Optional(Suppress(";"))
_trans_constraint_body.setParseAction(lambda s, l, t: list(t))
trans_constraint = Suppress("TRANS") + _trans_constraint_body
trans_constraint.setParseAction(lambda s, l, t: Trans(list(t)))

_init_constraint_body = simple_expression + Optional(Suppress(";"))
_init_constraint_body.setParseAction(lambda s, l, t: list(t))
init_constraint = Suppress("INIT") + _init_constraint_body
init_constraint.setParseAction(lambda s, l, t: SInit(list(t)))

_invar_constraint_body = simple_expression + Optional(Suppress(";"))
_invar_constraint_body.setParseAction(lambda s, l, t: list(t))
invar_constraint = Suppress("INVAR") + _invar_constraint_body
invar_constraint.setParseAction(lambda s, l, t: Invar(list(t)))

_fairness_constraint_body = simple_expression + Optional(Suppress(";"))
_fairness_constraint_body.setParseAction(lambda s, l, t: list(t))
fairness_constraint = Suppress("FAIRNESS") + _fairness_constraint_body
fairness_constraint.setParseAction(lambda s, l, t: Fairness(list(t)))

_justice_constraint_body = simple_expression + Optional(Suppress(";"))
_justice_constraint_body.setParseAction(lambda s, l, t: list(t))
justice_constraint = Suppress("JUSTICE") + _justice_constraint_body
justice_constraint.setParseAction(lambda s, l, t: Justice(list(t)))

_compassion_constraint_body = ( Suppress("(")
                              + simple_expression + Suppress(",")
                              + simple_expression + Suppress(")")
                              + Optional(Suppress(";"))
                              )
_compassion_constraint_body.setParseAction(lambda s, l, t: [t[0], t[1]])
compassion_constraint = Suppress("COMPASSION") + _compassion_constraint_body
compassion_constraint.setParseAction(lambda s, l, t: Compassion(list(t)))


# Module declaration
_module_element = ( var_section
                  | ivar_section
                  | frozenvar_section
                  | define_section
                  | constants_section
                  | assign_constraint
                  | trans_constraint
                  | init_constraint
                  | invar_constraint
                  | fairness_constraint
                  | justice_constraint
                  | compassion_constraint)
_module_args = (Suppress("(") + Optional(Group(delimitedList(identifier))) +
                Suppress(")"))
module = ( Suppress("MODULE") + identifier + Optional(_module_args)
         + ZeroOrMore(_module_element)
         )

def _create_module(string, location, tokens):
    
    from .model import ModuleMetaClass, Module as ModuleClass
    
    name = tokens[0]
    args = tokens[1]
    namespace = OrderedDict()
    namespace["NAME"] = name
    namespace["ARGS"] = args
    for section in tokens[2:]:
        if section.name not in namespace:
            namespace[section.name] = section.body
        else:
            update(namespace[section.name], section.body)
    return ModuleMetaClass(str(name), (ModuleClass,), namespace)

module.setParseAction(_create_module)

# Model declaration
comment = ("--" + restOfLine).suppress()
model = OneOrMore(module)
model.ignore(comment)

def parseAllString(parser, string):
    """
    Parse the complete given string with parser and set source of the result
    to string. parser is assumed to return a one-element list when parsing
    the string.
    """
    res = parser.parseString(string, parseAll=True)
    if hasattr(res[0], "source"):
        res[0].source = string
    return res[0]