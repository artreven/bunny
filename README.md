Bunny
===
Here you can find the code I used for the exploration of implicative theory of algebraic identities.
The implicative theory is the set of all implications that hold in a given data domain.
Here the data domain is the algebraic indentities.

![alt tag](https://raw.githubusercontent.com/artreven/bunny/master/bunny_hello.png)

Project holds the code for the attribute explorations of
algebras of type (2, 1, 0) - Binary, Unary, Nulary operations, that's why they are
called BUNnies. The data consists of three parts:

1. Bunnies;
2. Identities (of size 5 initially);
3. Relation between bunnies and identities: a bunny is in relation with an identity if the identity holds in the bunny. 

Example of a bunny:
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

* -x = a*(-x), where x - variable, a = f0: nulary operation or constant, -x = f1(x): unary operation, x*y = f2(x,y): binary operation, brackets define the order.

The language for building identities is described in more details in the corresponding
module term_parser.py, which holds the parser.


===
The polar fox is sweet, but dangerous for bunnies.
