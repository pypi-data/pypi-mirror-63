"""
Utility methods for element-wise operations on basic Python sequence types.
"""
import builtins, math
from typing import TypeVar, Union, List, Tuple, Sequence

_Num = Union[int, float, complex]

def sum(augend: Sequence[_Num], *addends : Sequence[_Num]) -> Sequence[_Num]:
	"""
	Returns a structure that is the same type/shape of the augend, but with the
	*addends added element-wise sequentially to it. Returns just the augend
	if no other parameters are given.

	Example:
	
	sum([1, 2], (3, 1j, 6), (0, 1)) -> [4, (3+1j)]

	Args:

	augend: (sequence of numbers): The structure to be added to, and whose type
	to format the output as

	addends: (sequences of numbers): The sequences of numbers to sequentially
	add to the augend while the augend's iteration has not been exhausted
	"""

	#Sequentially adds the members of addends to augend
	zipped = zip(augend, *addends)
	summed = [builtins.sum(x) for x in zipped]
	#Casts the summed sequence to the augend's type
	return type(augend)(summed)

def product(multiplier: Sequence[_Num], 
            *multiplicands : Sequence[_Num]) -> Sequence[_Num]:
	"""
	Returns a structure that is the same type/shape of the multiplier, but with
	the multiplicands multiplied element-wise sequentially by it. Returns just the 
	multiplier if no other parameters are given.

	Example:
	
	product([1, 2], (3, 1j, 6), (0, 1)) -> [0, 2j]

	Args:

	multiplier: (sequence of numbers): The structure by which to sequentially
	multiply the multiplicands, and whose type to format the output as

	multiplicands: (sequences of numbers): The sequences of numbers to 
	sequentially multiply by the multiplier by while the multiplier's iteration
	has not been exhausted
	"""

	#Sequentially multiplies by the multiplier (or the previous multiplication
	#	result) the multiplicands
	zipped = zip(multiplier, *multiplicands)
	multiplied = [math.prod(x) for x in zipped]
	#Casts the product sequence to the multiplier's type
	return type(multiplier)(multiplied)