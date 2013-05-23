MIW
===
Here the code I use for my PhD project Mathematical Inferential Wikipedia is stored.

===
Package "bunny_exploration" holds the code for the attribute explorations of
algebras of type (2, 1, 0) - Binary, Unary, Nulary operations, that's why they are
called BUNnies. The formal context consists of bunnies as objects and identities
as attributes.
Example of bunny:
f2:	  __0___1		f1:				f0:
	0|	0	1			0|	1			0
	1|	1	1			1|	0
	
Example of identity:
-x = a*[-x], where x - variable, a = f0 - nulary operation or constant,
-x = f1(x) - unary operation, x*y = f2(x,y) - binary operation, squared brackets
define the order.

The language for building identities is described in more details in the corresponding
module term_parser.py which holds the parser.

===
Package "error_check" holds the code for finding errors in formal objects. The
closely debugger is inside this package. More info inside.

===
"reducing" package holds function capable of clarifiyng and reducing formal contexts.
