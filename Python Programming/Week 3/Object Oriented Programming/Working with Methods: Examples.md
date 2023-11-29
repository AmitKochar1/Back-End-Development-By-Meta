Working with Methods: Examples
You have learned how to use objects, classes and the methods inside them.  You have covered these both in cases where there is only one class, as well as when there are multiple classes. You also explored how multiple inheritance works in Python and the role Method Resolution Order(MRO) plays in determining the call for the method. 

The following examples demonstrate how the function call is resolved in cases of multiple inheritance in different scenarios. Note that all the functions have the same names in all of the examples.

Example 1:

# Example 1
class A:
   def a(self):
       return "Function inside A"

class B:
    def a(self):
        return "Function inside B"

class C(B,A):
    pass

# Driver code
c = C()
print(c.a())

output:
Function inside B

Class C inherits from classes B and A. When I don't find any function a() inside class C, I should search for classes B and A and its important that I do it in that order.

I will now add one more level to this and note the output.

Example 2:

class A:
    def b(self):
        return "Function inside A"

class B:
    def b(self):
        return "Function inside B"

class C(A, B):
    def b(self):
        return "Function inside C"
    pass

class D(C):
    pass

d = D()
print(d.b())

Output:

Function inside C

Class D inherits from class C, which in turn inherits from classes A and B. Class D accesses the immediate superclass of class D, which is class C and resolves the value of the variable once it's found in that superclass.

Now let’s say I comment out the declaration inside class C.

    # def b(self):
    #     return "Function inside C" 

And replace it with the pass keyword to keep the code functional.

Since there was no value present inside class C either, the function call above would go to A. That is because class C will point to class A as having higher precedence while inheriting.

Now let's take another example of a similar scenario.

Example 3:

class A:
    def c(self):
        return "Function inside A"

class B:
    def c(self):
        return "Function inside B"

class C(A, B):
    def c(self):
        return "Function inside C"

class D(A, C):
    pass

d = D()
print(d.a)

The output is:
Traceback (most recent call last):
  File "/Users/intropython/PycharmProjects/practicePython/inherit.py", line 10, in <module>
    class D(A, C):
TypeError: Cannot create a consistent method resolution
order (MRO) for bases A, C

Note that this throws an error. In the code above, class D inherits from both class A and class C.

Class C is its immediate superclass, but since this is multiple inheritance, the rules are more complicated and it also has to check the classes passed to it for precedence.

In this particular case, class D is unable to resolve the order that should be followed, while resolving the value for the variable in cases where the variable is not present in the class of the given object.

It results in a TypeError because it's unable to create method resolution order (MRO). MRO is Python’s way of resolving the order of precedence of classes while dealing with inheritance.

Let's examine one final example.

Example 4:

class A:
    def d(self):
        return "Function inside A"

class B:
    def d(self):
        return "Function inside B"


class C:
    def d(self):
        return "Function inside C"


class D(A, B):
    def d(self):
        return "Function inside D"


class E(B, C):
    def d(self):
        return "Function inside E"


class F(E,D,C):
    pass

f = F()
print(f.d())
print(F.mro())

Output:

Function inside E
[<class '__main__.F'>, <class '__main__.E'>, <class '__main__.D'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class 'object'>]

The code here is simple. class F directly inherits from its immediate superclass and the first class that is passed to it. The second line then demonstrates the return from the mro() function. 

The examples in this reading demonstrate how code in which multiple inheritance is used, can get complicated and very messy, very fast. Multiple inheritance, with all the advantages and flexibility that it provides, should only be used once you have a strong command of Python as a language to avoid creating 'spaghetti code' that's difficult to understand and update.