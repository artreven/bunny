MIW
===
Here the code I use for my PhD project Mathematical Inferential Wikipedia is stored.

bunny_exploration
-------------------
===
Holds the code for the attribute explorations of
algebras of type (2, 1, 0) - Binary, Unary, Nulary operations, that's why they are
called BUNnies. The formal context consists of bunnies as objects and identities
as attributes.
Example of bunny:
<table>
  <td>
  <table>
    <tr>
      <td>f2</td> <th>0</th> <th>1</th>
    </tr>
    <tr>
      <th>0</th> <td>0</td> <td>1</td>
    </tr>
    <tr>
      <th>1</th> <td>0</td> <td>1</td>
    </tr>
  </table>
  </td>
  
  <td>
  <table>
    <tr>
      <td>f1</td>
    </tr>
    <tr>
      <th>0</th> <td>1</td>
    </tr>
    <tr>
      <th>1</th> <td>0</td>
    </tr>
  </table>
  </td>
  
  <td>
  <table>
    <tr>
      <td>f1</td>
    </tr>
    <tr>
      <tв></tв> <td>0</td>
    </tr>
  </table>
  </td>
</table>

Example of identity:
-x = a*[-x], where x - variable, a = f0 - nulary operation or constant,
-x = f1(x) - unary operation, x*y = f2(x,y) - binary operation, squared brackets
define the order.

The language for building identities is described in more details in the corresponding
module term_parser.py which holds the parser.

error_check
-------------
===
Holds the code for finding errors in formal objects. The
closely debugger is inside this package. More info inside.


reducing
----------
===
Holds function capable of clarifiyng and reducing formal contexts.

===
The polar fox is sweet, but dangerous for bunnies.
