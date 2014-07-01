"""
The :mod:`pynusmv.model` module provides a way to define NuSMV modules in
Python: the :class:`Module` class represents a generic NuSMV module, and must be
subclassed to define specific NuSMV modules.

"""

__all__ = ["Identifier", "ComplexIdentifier", "Boolean", "Word", "Range",
           "Conversion", "WordFunction", "Count", "Next", "Init", "Case",
           "Subscript", "BitSelection", "ArrayAccess", "Set", "Not", "Concat",
           "Minus", "Mult", "Div", "Mod", "Add", "Sub", "ShiftL", "ShiftR",
           "Union", "In", "Eq", "Neq", "Lt", "Gt", "Le", "Ge", "And", "Or",
           "Xor", "Xnor", "Ite", "Iff", "Implies", "TBoolean", "TWord", "TEnum",
           "TRange", "TArray", "TModule", "Variables", "InputVariables",
           "FrozenVariables", "Defines", "Assigns", "Constants", "Trans",
           "SInit", "Invar", "Fairness", "Justice", "Compassion",
           "Var", "IVar", "FVar", "Def",
           "Module"]

import inspect
import sys
import collections

from .utils import update


class Element(object):
    """A parsed element."""
    source = None

# ------------------------------------------------------------------------------
# ----- EXPRESSIONS
# ------------------------------------------------------------------------------

class Expression(Element):
    """An expression"""
    precedence = 0
    
    def __lt__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Lt(self, other)
        
    def __le__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Le(self, other)
        
    def __eq__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Eq(self, other)
       
    def __ne__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Neq(self, other)
        
    def __gt__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Gt(self, other)
        
    def __ge__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Ge(self, other)
    
    def __add__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Add(self, other)
    
    def __sub__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Sub(self, other)
    
    def __mul__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Mult(self, other)
    
    def __truediv__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Div(self, other)
    
    def __mod__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Mod(self, other)
    
    def __lshift__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return ShiftL(self, other)
    
    def __rshift__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return ShiftR(self, other)
    
    def __and__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return And(self, other)
    
    def __rand__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return And(self, other)
    
    def __xor__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Xor(self, other)
    
    def __or__(self, other):
        from .parser import parseAllString, next_expression
        if isinstance(other, str):
            other = parseAllString(next_expression, other)
        return Or(self, other)
    
    def __neg__(self):
        return Minus(self)
    
    def __invert__(self):
        return Not(self)
    
    # TODO BitSelection and Subscript need modifications
    #def __getitem__(self, key):
    #    if isinstance(key, slice):
    #        start, stop = slice.start, slice.stop
    #        if isinstance(start, str):
    #            start = parseAllString(next_expression, start)
    #        if isinstance(stop, str):
    #            stop = parseAllString(next_expression, stop)
    #        return BitSelection(self, start, stop)
    #    elif isinstance(key, str):
    #        key = parseAllString(next_expression, key)
    #        return Subscript(self, key)
    #    else:
    #        return Subscript(self, key)
    
    def __contains__(self, item):
        from .parser import parseAllString, next_expression
        if isinstance(item, str):
            item = parseAllString(next_expression, item)
        return In(self, other)
    

class Identifier(Expression):
    """An identifier."""
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.name)
    
    def __hash__(self):
        return 17 + 23 * hash("Identifier") + 23**2 * hash(self.name)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.name == other.name
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Identifier") + 23**2 * hash(self.name)

class ComplexIdentifier(Expression):
    """A complex identifier."""
    
    def __init__(self, body):
        self.body = body
    
    def __str__(self):
        if self.source:
            return self.source
        return "".join(str(element) for element in self.body)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.body == other.body
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("ComplexIdentifier") + 23**2 * hash(self.body)

class Constant(Expression):
    """A generic constant."""

class Boolean(Constant):
    """A boolean constant."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.value)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value == other.value
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Boolean") + 23**2 * hash(self.value)

class Word(Constant):
    """A word constant."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.value)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value == other.value
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Word") + 23**2 * hash(self.value)

class Range(Constant):
    """A range of integers."""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.start) + ".." + str(self.stop)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.start == other.start and self.stop == other.stop
        else:
            return False
    
    def __hash__(self):
        return ( 17 + 23 * hash("Range")
               + 23**2 * hash(self.start) + 23**3 * hash(self.stop) )

class Function(Expression):
    """A generic function."""

class Conversion(Function):
    """Converting an expression into a specific type."""
    
    def __init__(self, target_type, value):
        self.target_type = target_type
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.target_type) + "(" + str(self.value) + ")"
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.target_type == other.target_type and
                    self.value.equals(other.value))
        else:
            return False
    
    def __hash__(self):
        return ( 17 + 23 * hash("Conversion")
               + 23** 2 * hash(self.target_type)
               + 23**3 * hash(self.value) )

class WordFunction(Function):
    """A function applied on a word."""
    
    def __init__(self, function, value, size):
        self.function = function
        self.value = value
        self.size = size
    
    def __str__(self):
        if self.source:
            return self.source
        return ( str(self.function) + "(" + str(self.value)
               + ", " + str(self.size) +")" )
    
    def equals(self, other):
        if type(self) is type(other):
            return ( self.function == other.function and
                     self.value.equals(other.value) and
                     self.size.equals(other.size) )
        else:
            return False
    
    def __hash__(self):
        return ( 17 + 23 * hash("WordFunction")
               + 23**2 * hash(self.function)
               + 23**3 * hash(self.value) 
               + 23**4 * hash(self.size) )

class Count(Function):
    """A counting function."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return "count(" + str(self.value) + ")"
    
    def equals(self, other):
        if type(self) is type(other):
            if len(self.value) != len(other.value):
                return False
            for sval, oval in zip(self.value, other.value):
                if not sval.equals(oval):
                    return False
            return True
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Count") + 23**2 * hash(self.value)

class Next(Expression):
    """A next expression."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return "next(" + str(self.value) + ")"
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value.equals(other.value)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Next") + 23**2 * hash(self.value)

class Init(Expression):
    """An init expression."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return "init(" + str(self.value) + ")"
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value.equals(other.value)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Init") + 23**2 * hash(self.value)

class Case(Expression):
    """A case expression."""
    
    def __init__(self, values):
        self.values = values
    
    def __str__(self):
        if self.source:
            return self.source
        return ("case " + "\n".join(str(cond) + ": " + str(body) + ";"
                                    for cond, body in self.values.items())
                        + " esac")
    
    def equals(self, other):
        if type(self) is type(other):
            return self.values == other.values
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Case") + 23**2 * hash(self.values)

class Subscript(Expression):
    """Array subscript."""
    
    def __init__(self, index):
        self.index = index
    
    def __str__(self):
        if self.source:
            return self.source
        return "[" + str(self.index) + "]"
    
    def equals(self, other):
        if type(self) is type(other):
            return self.index.equals(other.index)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Subscript") + 23**2 * hash(self.index)

class BitSelection(Expression):
    """Word bit selection."""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def __str__(self):
        if self.source:
            return self.source
        return "[" + str(self.start) + ":" + str(self.stop) + "]"
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.start.equals(other.start) and
                    self.stop.equals(other.stop))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("BitSelection") + 23**2 * hash(self.start)
                + 23**3 * hash(self.stop))

class ArrayAccess(Expression):
    """Accessing a member of an array."""
    
    def __init__(self, array, accesses):
        self.array = array
        self.accesses = accesses
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.array) + "".join(str(access)
                                         for access in self.accesses)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.array.equals(other.array) and
                    self.accesses == other.accesses)
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("ArrayAccess") + 23**2 * hash(self.array)
               + 23**3 * hash(self.accesses))

class Set(Expression):
    """A set."""
    
    def __init__(self, elements):
        self.elements = elements
    
    def __str__(self):
        if self.source:
            return self.source
        return "{" + ", ".join(str(element) for element in self.elements) + "}"
    
    def equals(self, other):
        if type(self) is type(other):
            return frozenset(self.elements) == frozenset(other.elements)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Set") + 23**2 * hash(frozenset(self.elements))

class Operator(Expression):
    """An operator."""
    
    def _enclose(self, expression):
        """
        Return the string representation of expression,
        enclosed in parentheses if needed.
        """
        if (isinstance(expression, Operator)
            and expression.precedence > self.precedence):
                return "(" + str(expression) + ")"
        return str(expression)

class Not(Operator):
    """A negated expression."""
    
    precedence = 1
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            self.source
        return "! " + self._enclose(self.value)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value.equals(other.value)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Not") + 23**2 * hash(self.value)

class Concat(Operator):
    """A concatenation of expressions."""
    
    precedence = 2
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + "::" + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Concat") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Minus(Operator):
    """Minus expression."""
    
    precedence = 3
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        if self.source:
            return self.source
        return "- " + self._enclose(self.value)
    
    def equals(self, other):
        if type(self) is type(other):
            return self.value.equals(other.value)
        else:
            return False
    
    def __hash__(self):
        return 17 + 23 * hash("Minus") + 23**2 * hash(self.value)

class Mult(Operator):
    """A multiplication of expressions."""
    
    precedence = 4
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " * " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Mult") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Div(Operator):
    """A division of expressions."""
    
    precedence = 4
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " / " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Div") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Mod(Operator):
    """A modulo of expressions."""
    
    precedence = 4
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " mod " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Mod") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Add(Operator):
    """An addition of expressions."""
    
    precedence = 5
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " + " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Add") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Sub(Operator):
    """A subtraction of expressions."""
    
    precedence = 5
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " - " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Sub") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class ShiftL(Operator):
    """A left shift of expressions."""
    
    precedence = 6
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " << " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("ShiftL") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class ShiftR(Operator):
    """A right shift of expressions."""
    
    precedence = 6
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " >> " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("ShiftR") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Union(Operator):
    """A union of expressions."""
    
    precedence = 7
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " union " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Union") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class In(Operator):
    """The "in" expression."""
    
    precedence = 8
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " in " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("In") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Eq(Operator):
    """The "=" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " = " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Eq") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))
    
    def __bool__(self):
        if ( isinstance(self.left, Expression) and
             isinstance(self.right, Expression)):
            return self.left.equals(self.right)
        else:
            return self.left == self.right

class Neq(Operator):
    """The "!=" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " != " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((not self.left.equals(other.left) or
                     not self.right.equals(other.right)) and
                    (not self.left.equals(other.right) or
                     not self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Add") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))
    
    def __bool__(self):
        if ( isinstance(self.left, Expression) and
             isinstance(self.right, Expression)):
            return not self.left.equals(self.right)
        else:
            return self.left != self.right

class Lt(Operator):
    """The "<" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " < " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Lt") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Gt(Operator):
    """The ">" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " > " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Gt") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Le(Operator):
    """The "<=" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " <= " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Le") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class Ge(Operator):
    """The ">=" expression."""
    
    precedence = 9
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " >= " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Ge") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))

class And(Operator):
    """The & expression."""
    
    precedence = 10
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " & " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("And") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Or(Operator):
    """The | expression."""
    
    precedence = 11
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " | " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Or") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Xor(Operator):
    """The xor expression."""
    
    precedence = 11
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " xor " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Xor") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Xnor(Operator):
    """The xnor expression."""
    
    precedence = 11
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " xnor " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Xnor") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Ite(Operator):
    """The ? : expression."""
    
    precedence = 12
    
    def __init__(self, condition, left, right):
        self.condition = condition
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return ( self._enclose(self.condition) + " ? "
               + self._enclose(self.left) + " : "
               + self._enclose(self.right))
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.condition.equals(other.condition) and
                    self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Ite") + 23**2 * hash(self.condition)
                + 23**3 * hash(self.left) + 23**4 * hash(self.right))

class Iff(Operator):
    """The <-> expression."""
    
    precedence = 13
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " <-> " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return ((self.left.equals(other.left) and
                     self.right.equals(other.right)) or
                    (self.left.equals(other.right) and
                     self.right.equals(other.left)))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Iff") + 23**2 * hash(self.left)
                + 23**2 * hash(self.right))

class Implies(Operator):
    """The -> expression."""
    
    precedence = 14
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        if self.source:
            return self.source
        return self._enclose(self.left) + " -> " + self._enclose(self.right)
    
    def equals(self, other):
        if type(self) is type(other):
            return (self.left.equals(other.left) and
                    self.right.equals(other.right))
        else:
            return False
    
    def __hash__(self):
        return (17 + 23 * hash("Implies") + 23**2 * hash(self.left)
                + 23**3 * hash(self.right))


# ------------------------------------------------------------------------------
# ----- TYPES
# ------------------------------------------------------------------------------

class Type(Element):
    """A generic type specifier."""

class SimpleType(Type):
    """A simple type: boolean, word, enum, range, array."""

class TBoolean(SimpleType):
    """A boolean type."""
    
    def __str__(self):
        if self.source:
            return self.source
        return "boolean"

class TWord(SimpleType):
    """A word type."""
    
    def __init__(self, size, sign=None):
        self.size = size
        self.sign = sign
    
    def __str__(self):
        if self.source:
            return self.source
        return ( (self.sign + " " if self.sign else "") + "word"
               + "[" + str(self.size) + "]" )

class TEnum(SimpleType):
    """An enumeration type."""
    
    def __init__(self, values):
        self.values = values
    
    def __str__(self):
        if self.source:
            return self.source
        return "{" + ", ".join(str(value) for value in self.values) + "}"

class TRange(SimpleType):
    """A range type."""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def __str__(self):
        if self.source:
            return self.source
        return str(self.start) + ".." + str(self.stop)

class TArray(SimpleType):
    """An array type."""
    
    def __init__(self, start, stop, elementtype):
        self.start = start
        self.stop = stop
        self.elementtype = elementtype
    
    def __str__(self):
        if self.source:
            return self.source
        return ( "array " + str(self.start) + ".." + str(self.stop)
               + " of " + str(self.elementtype) )

class TModule(Type):
    """A module instantiation."""
    
    def __init__(self, modulename, args, process=False):
        self.process = process
        self.modulename = modulename
        self.args = args
    
    def __str__(self):
        if self.source:
            return self.source
        return ( ("process " if self.process else "") + str(self.modulename)
               + "(" + ", ".join(str(arg) for arg in self.args) + ")" )


# ------------------------------------------------------------------------------
# ----- SECTIONS
# ------------------------------------------------------------------------------

class Section(Element):
    """A section of a module."""
    
    def __init__(self, name, body):
        self.name = name
        self.body = body
    
    def __str__(self):
        if self.source:
            return self.source
        return self.name + "\n" + str(self.body)

class MappingSection(Section):
    """Section based on a mapping of identifier and others."""
    
    def __init__(self, name, mapping, separator=": ", indentation=" " * 4):
        """
        :param name: the name of the section.
        :param mapping: the mapping of identifiers to their corresponding
                        expression.
        :param separator: the separator of identifiers and expressions
                          for printing the section.
        :param indentation: the indentation for the printed expressions.
        """
        super().__init__(name, mapping)
        self.separator = separator
        self.indentation = indentation
    
    def update_body(self, otherbody):
        self.body.update(otherbody)
    
    def __str__(self):
        if self.source:
            return self.source
        return (self.name + "\n" +
                "\n".join(self.indentation + str(identifier)
                          + self.separator + str(expr) + ";"
                          for identifier, expr in self.body.items()))

class Variables(MappingSection):
    """Declaring variables."""
    
    def __init__(self, variables):
        super().__init__("VAR", variables)

class InputVariables(MappingSection):
    """Declaring input variables."""
    
    def __init__(self, ivariables):
        super().__init__("IVAR", ivariables)

class FrozenVariables(MappingSection):
    """Declaring frozen variables."""
    
    def __init__(self, fvariables):
        super().__init__("FROZENVAR", fvariables)

class Defines(MappingSection):
    """Declaring defines."""
    
    def __init__(self, defines):
        super().__init__("DEFINE", defines, separator=" := ")

class Assigns(MappingSection):
    """Declaring assigns."""
    
    def __init__(self, assigns):
        super().__init__("ASSIGN", assigns, separator=" := ")

class ListingSection(Section):
    """A section made of a list of elements."""
    
    def __init__(self, name, listing, separator="\n", indentation=" " * 4):
        """
        :param name: the name of the section.
        :param listing: a list of expressions.
        :param separator: the separator of expressions for printing the section.
        :param indentation: the indentation for the printed expressions.
        """
        super().__init__(name, listing)
        self.separator = separator
        self.indentation = indentation
    
    def update_body(self, otherbody):
        self.body += otherbody
    
    def __str__(self):
        if self.source:
            return self.source
        return (self.name + "\n" +
                self.separator.join(self.indentation + str(element)
                                    for element in self.body))

class Constants(ListingSection):
    """Declaring constants."""
    
    def __init__(self, constants):
        super().__init__("CONSTANTS", constants, separator=", ")

class Trans(ListingSection):
    """A TRANS section."""
    
    def __init__(self, body):
        super().__init__("TRANS", body, separator="\nTRANS\n")

class SInit(ListingSection):
    """An INIT section."""
    
    def __init__(self, body):
        super().__init__("INIT", body, separator="\nINIT\n")

class Invar(ListingSection):
    """An INVAR section."""
    
    def __init__(self, body):
        super().__init__("INVAR", body, separator="\nINVAR\n")

class Fairness(ListingSection):
    """A FAIRNESS section."""
    
    def __init__(self, body):
        super().__init__("FAIRNESS", body, separator="\nFAIRNESS\n")

class Justice(ListingSection):
    """A Justice section."""
    
    def __init__(self, body):
        super().__init__("JUSTICE", body, separator="\nJUSTICE\n")

class Compassion(ListingSection):
    """A COMPASSION section."""
    
    def __init__(self, body):
        super().__init__("COMPASSION", body, separator="\nCOMPASSION\n")


# ------------------------------------------------------------------------------
# ----- DECLARATIONS
# ------------------------------------------------------------------------------

class Declaration(Identifier):
    """
    A Declaration behaves like an identifier, except that it knows which type
    it belongs to. Furthermore, it does not know its name for sure, and
    cannot be printed without giving it a name.
    
    """
    
    def __init__(self, type_, section, name=None):
        self._name = name
        self.type = type_
        self.section = section
    
    @property
    def name(self):
        if not self._name:
            raise AttributeError("Unknown declaration name.")
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

class Var(Declaration):
    def __init__(self, type_, name=None):
        super().__init__(type_, "VAR", name=name)

class IVar(Declaration):
    def __init__(self, type_, name=None):
        super().__init__(type_, "IVAR", name=name)

class FVar(Declaration):
    def __init__(self, type_, name=None):
        super().__init__(type_, "FROZENVAR", name=name)

class Def(Declaration):
    def __init__(self, type_, name=None):
        super().__init__(type_, "DEFINE", name=name)



class ModuleMetaClass(type):
    """
    The meta class for modules, allowing modules to be printed.
    
    The string representation of the module is its NuSMV code. This 
    representation includes:
    * the `NAME` member of the class, used as the name of the module;
      if absent, the name of the class is used.
    * the `ARGS` member, used as the list of arguments of the module;
      if ARGS is not defined, the module is declared without arguments.
    * members named after NuSMV module sections:
      VAR, IVAR, FROZENVAR, DEFINE, CONSTANTS, ASSIGN, TRANS, INIT, INVAR,
      FAIRNESS, JUSTICE, COMPASSION.
    
    Module sections must satisfy the following pattern:
    * pair-based sections such as VAR, IVAR, FROZENVAR, DEFINE and ASSIGN
      must be mapping objects where keys are identifiers and values are types
      (for VAR, IVAR and FROZENVAR) or expressions (for DEFINE and ASSIGN).
    * list-based sections such as CONSTANTS must be enumerations
      composed of elements of the section.
    * expression-based sections such as TRANS, INIT, INVAR, FAIRNESS, JUSTICE
      and COMPASSION must be enumerations composed of expressions.
    
    """
    
    # The list of module sections that are considered
    # each key is the section name
    # each value is a tuple giving:
    # * the type of expected value (mapping, enumeration, bodies)
    # * a format string for mappings, based on key and value,
    #   or the separator for enumerations,
    #   or nothing for bodies,
    #   used for printing the section body
    _sections = {"VAR": ("mapping", "{key}: {value};"),
                 "IVAR": ("mapping", "{key}: {value};"),
                 "FROZENVAR": ("mapping", "{key}: {value};"),
                 "DEFINE": ("mapping", "{key} := {value};"),
                 "ASSIGN": ("mapping", "{key} := {value};"),
                 "CONSTANTS": ("enumeration", ", "),
                 "TRANS": ("bodies",),
                 "INIT": ("bodies",),
                 "INVAR": ("bodies",),
                 "FAIRNESS": ("bodies",),
                 "JUSTICE": ("bodies",),
                 "COMPASSION": ("bodies",)}
    
    @classmethod
    def __prepare__(metacls, name, bases, **keywords):
        return collections.OrderedDict()
    
    def __new__(cls, name, bases, namespace, **keywords):
        newnamespace = collections.OrderedDict()
        # Update namespace with sections and declared identifiers
        for member in namespace:
            if member in cls._sections:
                internal = cls._section_internal(member, namespace[member])
                if member in newnamespace:
                    update(newnamespace[member], internal)
                else:
                    newnamespace[member] = internal
            elif isinstance(namespace[member], Declaration):
                decl = namespace[member]
                decl.name = member
                if decl.section not in newnamespace:
                    newnamespace[decl.section] = collections.OrderedDict()
                newnamespace[decl.section][decl] = decl.type
            else:
                newnamespace[member] = namespace[member]
        
        result = type.__new__(cls, name, bases, dict(newnamespace))
        result.members = tuple(newnamespace)
        result.source = None
        return result
    
    @classmethod
    def _section_internal(cls, section, body):
        """
        Return the internal representation of `body` of `section`.
        
        This representation depends on the type of `section`.
        
        `section` is a mapping
        ----------------------
        
        The internal representation is a mapping where keys are identifiers
        and values are expressions or type identifiers.
        
        * If `body` is a single string, `body` is treated as the whole body of
          the section, and parsed accordingly.
        * If `body` is a mapping, it is copied and treated as the required
          mapping. This means that each key or value is parsed as the part it
          represent, if it is a string, or kept as it is otherwise.
        * If `body` is enumerable, each element is treated separated: either it 
          is a string, and parsed as a key-value pair, otherwise it is a couple
          of values, and the first one is treated as a key (and parsed if
          necessary), and the second one as a value (and parsed if necessary).
        
        `section` is an enumeration
        ---------------------------
        
        The internal representation is an enumeration containing the different
        elements of the section.
        
        * If `body` is a single string, it is parsed as the whole body of the
          section.
        * If `body` is an enumerable, each element is parsed as a single element
          if it is a string, or kept as it is otherwise.
        
        `section` is a list of bodies
        -----------------------------
        
        The internal representation is an enumeration of expressions.
        
        * If `body` is a single string, it is parsed as one expression, and
          kept as the single expression of the section.
        * If `body` is an enumeration, each element is parsed as an expression
          if it is a string, or kept as it is otherwise.
        
        """
        
        
        from .parser import (parseAllString,
                             _var_section_body, identifier, type_identifier,
                             _ivar_section_body, _simple_type_specifier,
                             _frozenvar_section_body, _define_section_body,
                             _assign_constraint_body, _assign_identifier,
                             simple_expression, _constants_section_body,
                             _trans_constraint_body, _init_constraint_body,
                             _invar_constraint_body, _fairness_constraint_body,
                             _justice_constraint_body,
                             _compassion_constraint_body)
        
        # The list of module sections that are considered
        # each key is the section name
        # each value is a tuple giving:
        # * the type of expected value (mapping, enumeration, bodies)
        # * a list parsers: three for mappings (whole section, key and value),
        #   one for enumerations (whole section) and one for bodies (whole
        #   section)
        _sections_parsers = {
                     "VAR": ("mapping",
                             _var_section_body,
                             identifier,
                             type_identifier),
                     "IVAR": ("mapping",
                              _ivar_section_body,
                              identifier,
                              _simple_type_specifier),
                     "FROZENVAR": ("mapping",
                                   _frozenvar_section_body,
                                   identifier,
                                   _simple_type_specifier),
                     "DEFINE": ("mapping",
                                _define_section_body,
                                identifier,
                                _simple_type_specifier),
                     "ASSIGN": ("mapping",
                                _assign_constraint_body,
                                _assign_identifier,
                                simple_expression),
                     "CONSTANTS": ("enumeration",
                                   _constants_section_body),
                     "TRANS": ("bodies", _trans_constraint_body),
                     "INIT": ("bodies", _init_constraint_body),
                     "INVAR": ("bodies", _invar_constraint_body),
                     "FAIRNESS": ("bodies", _fairness_constraint_body),
                     "JUSTICE": ("bodies", _justice_constraint_body),
                     "COMPASSION": ("bodies", _compassion_constraint_body)}
        
        
        if section not in cls._sections:
            raise Exception("Unknown section: {}.".format(section))
        
        if cls._sections[section][0] == "mapping":
            section_parser, key_parser, value_parser = (_sections_parsers
                                                        [section][-3:])
            if isinstance(body, collections.abc.Mapping):
                res = collections.OrderedDict()
                for key, value in body.items():
                    if isinstance(key, str):
                        key = parseAllString(key_parser, key)
                    if isinstance(value, str):
                        value = parseAllString(value_parser, value)
                    res[key] = value
                
                return res
            
            else:
                if isinstance(body, str):
                    body = [body]
                
                res = collections.OrderedDict()
                for line in body:
                    if isinstance(line, str):
                        line = parseAllString(section_parser, line)
                        update(res, line)
                        
                    else:
                        # line is an enumeration
                        key, value = line[0:2]
                        if isinstance(key, str):
                            key = parseAllString(key_parser, key)
                        if isinstance(value, str):
                            value = parseAllString(value_parser, value)
                        res[key] = value
                
                return res
        
        elif (cls._sections[section][0] == "enumeration" or
              cls._sections[section][0] == "bodies"):
            
            if isinstance(body, str):
                body = [body]
            
            elif isinstance(body, Expression):
                body = [body]
            
            # body is a list of expressions
            parser = _sections_parsers[section][-1]
            
            exprs = []
            for expr in body:
                if isinstance(expr, str):
                    expr = parseAllString(parser, expr)
                
                update(exprs, [expr])
            
            return exprs
        
        else:
            raise Exception("Unknown section type: "
                            "{} for section {}.".format(
                                _sections[section][0],
                                section))
    
    def _trim(cls, string, indentation=""):
        """
        Reformat `string` (:class:`str`) with the following rules:
        
        * tabulations are converted into spaces;
        * leading and trailing empty lines are removed;
        * every line is indented with its relative indentation to the least
          indented non-empty line;
        * the whole string is indented with `indentation`.
        
        """
        if not string:
            return ''
        # Convert tabs to spaces (following the normal Python rules)
        # and split into a list of lines:
        lines = string.expandtabs().splitlines()
        # Determine minimum indentation (first line doesn't count):
        indent = sys.maxsize
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = min(indent, len(line) - len(stripped))
        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent < sys.maxsize:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())
        # Strip off trailing and leading blank lines:
        while trimmed and not trimmed[-1]:
            trimmed.pop()
        while trimmed and not trimmed[0]:
            trimmed.pop(0)
        # Return a single string:
        return '\n'.join(indentation + line for line in trimmed)
    
    def _section_str(cls, section, body, indentation=""):
        """
        Return the string representation of `section`, depending on `section`
        value, and including `body`, indented with `indentation`.
        `section` must be a key of `cls._sections`.
        
        """
        
        if section not in cls._sections:
            raise Exception("Unknown section: {}.".format(section))
        
        if cls._sections[section][0] == "mapping":
            # body is a mapping
            # use format given in _sections
            strformat = cls._sections[section][1]
            value = (indentation + section + "\n"
                    + "\n".join(((indentation * 2) + strformat)
                                 .format(key=str(name), value=str(expr))
                                for name, expr in body.items()))
            return value
        
        elif cls._sections[section][0] == "enumeration":
            # body is an enumeration
            # use separator given in _sections
            separator = cls._sections[section][1]
            return (indentation + section + "\n"
                    + separator.join(str(value) for value in body))
        
        elif cls._sections[section][0] == "bodies":
            # body is an enumeration of bodies
            # return a set of sections with these bodies
            return "\n".join(indentation + section + "\n"
                             + cls._trim(str(value), indentation * 2)
                             for value in body)
        
        else:
            raise Exception("Unknown section type: "
                            "{} for section {}.".format(
                                _sections[section][0],
                                section))
    
    def __str__(cls):
        if cls.source:
            return cls.source
        
        indentation = " " * 4
        try:
            name = cls.NAME
        except AttributeError:
            name = cls.__name__
        try:
            args = "(" + ", ".join(str(arg) for arg in cls.ARGS) + ")"
        except AttributeError:
            args = ""
        
        representation = ["MODULE " + str(name) + args]
        for section in [member for member in cls.members
                               if member in cls._sections]:
            representation.append(cls._section_str(section,
                                                   cls.__dict__[section],
                                                   indentation))
        return "\n".join(representation)


class Module(object, metaclass=ModuleMetaClass):
    """
    A generic module.
    
    To create a new module, the user must subclass the :class:`Module` class and
    add class attributes with names corresponding to sections of NuSMV module
    definitions: `VAR`, `IVAR`, `FROZENVAR`, `DEFINE`, `CONSTANTS`, `ASSIGN`,
    `TRANS`, `INIT`, `INVAR`, `FAIRNESS`, `JUSTICE`, `COMPASSION`.
    
    In addition to these attributes, the `ARGS` and `NAME` attributes can be 
    defined. If `NAME` is defined, it overrides module name for the NuSMV module
    name. If `ARGS` is defined, it must be a sequence object where each
    element's string representation is an argument of the module.
    
    Treatment of the section depends of the type of the section and the value
    of the corresponding attribute.
    
    CONSTANTS section
        If the value of the section is a string (:class:`str`), it is used as
        the body of the constants declaration. Otherwise, the value must be a
        sequence and it is used as the defined constants.
    
    VAR, IVAR, FROZENVAR, DEFINE, ASSIGN sections
        If the value of the section is a string (:class:`str`), it is used as
        the body of the declaration. If it is a dictionary (:class:`dict`), keys
        are used as names of variables (or input variables, define, etc.) and
        values as bodies of the declaration. Otherwise, the value must be a
        sequence, and each element is treated  separately, and joined with line
        returns to build the body of the section:
        
        * if the element is a string (:class:`str`), it is kept as it is;
        * otherwise, the element must be a sequence, and the first element is
          used as the name of the variable (or input variable, define, etc.) and
          the second one as the body of the declaration.

    TRANS, INIT, INVAR, FAIRNESS, JUSTICE, COMPASSION sections
        If the value of the section is a string (:class:`str`), it is used as
        the body of the section. Otherwise, it must be a sequence and the
        string representation of the elements of the sequence are declared
        as different sections.
    
    
    For example, the class ::
    
        class TwoCounter(Module):
            NAME = "twoCounter"
            ARGS = ["run"]
            VAR = {"c1": "0..2",
                   "c2": "0..2"}
            INIT = ["c1 = 0",
                    "c2 = 0"]
            TRANS = \"\"\"
                    next(c1) = run ? c1+1 mod 2 : c1 &
                    next(c2) = run ? c2+1 mod 2 : c2
                    \"\"\"
    
    defines the module ::
    
        MODULE twoCounter(run)
            VAR
                c1 : 0..2;
                c2 : 0..2;
            INIT
                c1 = 0
            INIT
                c2 = 0
            TRANS
                next(c1) = run ? c1+1 mod 2 : c1 &
                next(c2) = run ? c2+1 mod 2 : c2
    
    
    After creation, module sections satisfy the following patterns:
    * pair-based sections such as VAR, IVAR, FROZENVAR, DEFINE and ASSIGN
      are mapping objects (dictionaries) where keys are identifiers and values
      are types (for VAR, IVAR and FROZENVAR) or expressions (for DEFINE and
      ASSIGN).
    * list-based sections such as CONSTANTS are enumerations  composed of
      elements of the section.
    * expression-based sections such as TRANS, INIT, INVAR, FAIRNESS, JUSTICE
      and COMPASSION are enumerations composed of expressions.
    
    """
    
    pass