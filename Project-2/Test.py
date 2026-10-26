# The spaces in the following expected outputs are just for readability.
# They will be ignored during comparison.

# Test Case 1: Declaration and Assignment
test_input_1 = """
var x : Integer;
var y : Boolean := False;
var variable :Boolean;
Put(variable);
var Booleannn : Boolean := True;
"""
expected_output_1 = """
Block([
Decl(Identifier(x),Type(Integer),None),
Decl(Identifier(y),Type(Boolean),Boolean(False)),
Decl(Identifier(variable),Type(Boolean),None),
Put(Identifier(variable)),
Decl(Identifier(Booleannn),Type(Boolean),Boolean(True))
])
"""

# Test Case 2: Declaration and Assignment
test_input_2 = """
var x : Integer := True;
"""
expected_output_2 = """
Invalid
"""

# Test Case 3: Declaration and Assignment
test_input_3 = """
var x : Integer;
var x : Boolean;
"""
expected_output_3 = """
Invalid
"""

# Test Case 4: scoping
test_input_4 = """
var x : Integer := 10;
while x > 0 loop
    var y : Boolean := True;
    Put(x);
    Put(y);
end loop;
"""
expected_output_4 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(10)),
    WhileLoop(Comparison(Identifier(x),>,Integer(0)),
        Block([
            Decl(Identifier(y),Type(Boolean),Boolean(True)),
            Put(Identifier(x)),
            Put(Identifier(y))
        ])
    )
])
"""

# Test Case 5: scoping
test_input_5 = """
var x : Integer;
if x > 1 then
    Put(x);
else
    x := x - 1;
end if;
"""
expected_output_5 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    If(Comparison(Identifier(x),>,Integer(1)),
        Block([Put(Identifier(x))]),
        Block([
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)]))
        ])
    )
])
"""

# Test Case 6: scoping
test_input_6 = """
var x : Boolean := False;
while x loop
    var x : Integer := 10;
    x := x - 1;
    Put(x);
end loop;
x := True;
"""
expected_output_6 = """
Block([
    Decl(Identifier(x),Type(Boolean),Boolean(False)),
    WhileLoop(Identifier(x),
        Block([
            Decl(Identifier(x),Type(Integer),Integer(10)),
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)])),
            Put(Identifier(x))
        ])
    ),
    Assign(Identifier(x),Boolean(True))
])
"""

# Test Case 7: scoping
test_input_7 = """
while False loop
    var x : Integer;
end loop;
x := 5;
"""
expected_output_7 = """
Invalid
"""

# Test Case 8: scoping
test_input_8 = """
if True then
    var i : Integer;
    i := 1;
else
    var i : Boolean;
    i := True;
end if;
"""
expected_output_8 = """
Block([
    If(Boolean(True),
        Block([
            Decl(Identifier(i),Type(Integer),None),
            Assign(Identifier(i),Integer(1))
        ]),
        Block([
            Decl(Identifier(i),Type(Boolean),None),
            Assign(Identifier(i),Boolean(True))
        ])
    )
])
"""

# Test Case 9: type compatibility
test_input_9 = """
var x : Integer := 1;
var y : Integer := 2;
var z : Integer;
x := y + z;
var a : Boolean := True;
var b : Boolean := False;
Put(a and (b or False));
"""
expected_output_9 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(1)),
    Decl(Identifier(y),Type(Integer),Integer(2)),
    Decl(Identifier(z),Type(Integer),None),
    Assign(Identifier(x),Term([Identifier(y),+,Identifier(z)])),
    Decl(Identifier(a),Type(Boolean),Boolean(True)),
    Decl(Identifier(b),Type(Boolean),Boolean(False)),
    Put(And([Identifier(a),Or([Identifier(b),Boolean(False)])]))
])
"""

# Test Case 10: type compatibility
test_input_10 = """
var b1 : Boolean;
var b2 : Boolean;
var b3 : Boolean;
var i1 : Integer;
var i2 : Integer;
var i3 : Integer;
b1 := (b2 or b3) and i1 /= i2 or i2 mod i3 = 0;
"""
expected_output_10 = """
Block([
    Decl(Identifier(b1),Type(Boolean),None),
    Decl(Identifier(b2),Type(Boolean),None),
    Decl(Identifier(b3),Type(Boolean),None),
    Decl(Identifier(i1),Type(Integer),None),
    Decl(Identifier(i2),Type(Integer),None),
    Decl(Identifier(i3),Type(Integer),None),
    Assign(Identifier(b1),
        Or([
            And([
                Or([Identifier(b2),Identifier(b3)]),
                Comparison(Identifier(i1),/=,Identifier(i2))
            ]),
            Comparison(
                Factor([Identifier(i2),mod,Identifier(i3)]),
                =,
                Integer(0)
            )
        ])
    )
])
"""

# Test Case 11: type compatibility
test_input_11 = """
var x : Integer;
var y : Boolean;
x := 1 + y;
"""
expected_output_11 = """
Invalid
"""

# Test Case 12: type compatibility
test_input_12 = """
var x : Integer;
var y : Boolean;
y := x /= 0;
"""
expected_output_12 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    Decl(Identifier(y),Type(Boolean),None),
    Assign(Identifier(y),Comparison(Identifier(x),/=,Integer(0)))
])
"""

# Test Case 13: combined
test_input_13 = """
var x : Integer;
if x mod 2 = 0 then
    Put(1 + x);
else
    var x : Boolean := True;
    Put(x or False);
end if;
"""
expected_output_13 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    If(Comparison(Factor([Identifier(x),mod,Integer(2)]),=,Integer(0)),
        Block([
            Put(Term([Integer(1),+,Identifier(x)]))
        ]),
        Block([
            Decl(Identifier(x),Type(Boolean),Boolean(True)),
            Put(Or([Identifier(x),Boolean(False)]))
        ])
    )
])
"""

# Test Case 14: combined
test_input_14 = """
var x : Boolean;
while x loop
    if x then
        x := False;
    else
        var x : Integer;
        x := True;
    end if;
end loop;
"""
expected_output_14 = """
Invalid
"""

# Test Case 15: combined
test_input_15 = """
var x : Integer;
var y : Boolean;
var z : Boolean;
if (x + 1) > 0 and (y or z) then
    x := x - 1;
    if z then
        var y : Integer;
    end if;
    y := False;
end if;
"""
expected_output_15 = """
Block([
    Decl(Identifier(x),Type(Integer),None),
    Decl(Identifier(y),Type(Boolean),None),
    Decl(Identifier(z),Type(Boolean),None),
    If(And([
            Comparison(Term([Identifier(x),+,Integer(1)]),>,Integer(0)),
            Or([Identifier(y),Identifier(z)])
            ]),
        Block([
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)])),
            If(Identifier(z),
                Block([Decl(Identifier(y),Type(Integer),None)]),
                None),
            Assign(Identifier(y),Boolean(False))
        ]),
        None
    )
])
"""

# Test Case 16: self-reference in initializer
test_input_16 = """
var x : Integer := x;
"""
expected_output_16 = """
Invalid
"""

# Test Case 17: shadowing in nested scope
test_input_17 = """
var x : Integer := 5;
if True then
    var x : Boolean := False;
    Put(x);
end if;
Put(x);
"""
expected_output_17 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(5)),
    If(Boolean(True),
        Block([
            Decl(Identifier(x),Type(Boolean),Boolean(False)),
            Put(Identifier(x))
        ]),
        None
    ),
    Put(Identifier(x))
])
"""

# Test Case 18: initializer uses outer variable
test_input_18 = """
var x : Integer := 10;
if True then
    var x : Integer := x;
end if;
"""
expected_output_18 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(10)),
    If(Boolean(True),
        Block([
            Decl(Identifier(x),Type(Integer),Identifier(x))
        ]),
        None
    )
])
"""

# Test Case 19: invalid if condition
test_input_19 = """
var x : Integer := 1;
if x then
    Put(x);
end if;
"""
expected_output_19 = """
Invalid
"""

# Test Case 20: invalid while condition
test_input_20 = """
var x : Integer := 5;
while x + 1 loop
    x := x - 1;
end loop;
"""
expected_output_20 = """
Invalid
"""

# Test Case 21: boolean assigned arithmetic
test_input_21 = """
var b : Boolean;
b := 1 + 2;
"""
expected_output_21 = """
Invalid
"""

# Test Case 22: integer assigned boolean expression
test_input_22 = """
var x : Integer;
var y : Boolean := True;
x := y and False;
"""
expected_output_22 = """
Invalid
"""

# Test Case 23: invalid boolean comparison
test_input_23 = """
var x : Boolean := True;
var y : Boolean := False;
if x = y then
    Put(x);
end if;
"""
expected_output_23 = """
Invalid
"""

# Test Case 24: arithmetic with boolean identifier
test_input_24 = """
var x : Integer := 1;
var y : Boolean := False;
x := x + y;
"""
expected_output_24 = """
Invalid
"""

# Test Case 25: logic with integer identifier
test_input_25 = """
var x : Integer := 1;
var y : Boolean := True;
y := y and x;
"""
expected_output_25 = """
Invalid
"""

# Test Case 26: if-scope variable used outside
test_input_26 = """
if True then
    var x : Integer := 1;
end if;
Put(x);
"""
expected_output_26 = """
Invalid
"""

# Test Case 27: while-scope variable used outside
test_input_27 = """
while False loop
    var x : Integer := 2;
end loop;
x := 3;
"""
expected_output_27 = """
Invalid
"""

# Test Case 28: redeclaration in same inner scope
test_input_28 = """
if True then
    var x : Integer;
    var x : Boolean;
end if;
"""
expected_output_28 = """
Invalid
"""

# Test Case 29: valid mixed arithmetic + boolean
test_input_29 = """
var x : Integer := 4;
var y : Integer := 2;
var b : Boolean;
b := (x mod y = 0) and (x > y);
"""
expected_output_29 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(4)),
    Decl(Identifier(y),Type(Integer),Integer(2)),
    Decl(Identifier(b),Type(Boolean),None),
    Assign(Identifier(b),
        And([
            Comparison(Factor([Identifier(x),mod,Identifier(y)]),=,Integer(0)),
            Comparison(Identifier(x),>,Identifier(y))
        ])
    )
])
"""

# Test Case 30: valid for-loop
test_input_30 = """
var i : Integer;
for i in 1 .. 3 loop
    Put(i);
end loop;
"""
expected_output_30 = """
Block([
    Decl(Identifier(i),Type(Integer),None),
    ForLoop(Identifier(i), Integer(1), Integer(3),
        Block([
            Put(Identifier(i))
        ])
    )
])
"""

# Test Case 31: invalid for-loop iterator type
test_input_31 = """
var i : Boolean;
for i in 1 .. 3 loop
    Put(i);
end loop;
"""
expected_output_31 = """
Invalid
"""

# Test Case 32: invalid for-loop start bound
test_input_32 = """
var i : Integer;
var b : Boolean := True;
for i in b .. 3 loop
    Put(i);
end loop;
"""
expected_output_32 = """
Invalid
"""

# Test Case 33: invalid for-loop end bound
test_input_33 = """
var i : Integer;
var b : Boolean := False;
for i in 1 .. b loop
    Put(i);
end loop;
"""
expected_output_33 = """
Invalid
"""

# Test Case 34: undeclared iterator
test_input_34 = """
for i in 1 .. 3 loop
    Put(i);
end loop;
"""
expected_output_34 = """
Invalid
"""

# Test Case 35: valid boolean expression initializer
test_input_35 = """
var x : Integer := 1;
var y : Integer := 2;
var b : Boolean := (x < y) or (x = y);
"""
expected_output_35 = """
Block([
    Decl(Identifier(x),Type(Integer),Integer(1)),
    Decl(Identifier(y),Type(Integer),Integer(2)),
    Decl(Identifier(b),Type(Boolean),
        Or([
            Comparison(Identifier(x),<,Identifier(y)),
            Comparison(Identifier(x),=,Identifier(y))
        ])
    )
])
"""