# The spaces in the following expected outputs are just for readability.
# They will be ignored during comparison.

# Test Case 1: Basic Statements of Assignment and Put
test_input_1 = """
x := 123;
y_:=False;
forever :=y;
Put(forever);Put(01);

"""
expected_output_1 = """
Block([
    Assign(Identifier(x),Integer(123)),
    Assign(Identifier(y_),Boolean(False)),
    Assign(Identifier(forever),Identifier(y)),
    Put(Identifier(forever)),
    Put(Integer(01))
])
"""

# Test Case 2: If Statement
test_input_2 = """
if x then
    y := 10;
end if;
"""
expected_output_2 = """
Block([
    If(Identifier(x),
        Block([Assign(Identifier(y),Integer(10))]),
        None
    )
])
"""

# Test Case 3: If-Else Statement
test_input_3 = """
if y then
    z := 10;
else
    z := 20;
    x := y;
end if;
"""
expected_output_3 = """
Block([
    If(Identifier(y),
        Block([Assign(Identifier(z),Integer(10))]),
        Block([Assign(Identifier(z),Integer(20)),Assign(Identifier(x),Identifier(y))])
    )
])
"""

# Test Case 4: While Loop
test_input_4 = """
while False loop
    Put(0);
end loop;
"""
expected_output_4 = """
Block([
    WhileLoop(Boolean(False),
        Block([Put(Integer(0))])
    )
])
"""

# Test Case 5: While Loop
test_input_5 = """
while x loop
    Put(x);
    x := x - 1;
    while x + y loop
        Put(y);
        y := y - 1;
    end loop;
end loop;
"""
expected_output_5 = """
Block([
    WhileLoop(Identifier(x),
        Block([
            Put(Identifier(x)),
            Assign(Identifier(x),Term([Identifier(x),-,Integer(1)])),
            WhileLoop(Term([Identifier(x),+,Identifier(y)]),
                Block([
                    Put(Identifier(y)),
                    Assign(Identifier(y),Term([Identifier(y),-,Integer(1)]))
                ])
            )
        ])
    )
])
"""

# Test Case 6: While Loop
test_input_6 = """
while False loop
end loop;
"""
expected_output_6 = """
Block([
    WhileLoop(Boolean(False),
        Block([])
    )
])
"""

# Test Case 7: For Loop
test_input_7 = """
for i in 1 .. 5 loop
    Put(i);
end loop;
"""
expected_output_7 = """
Block([
    ForLoop(Identifier(i),Integer(1),Integer(5),
        Block([
            Put(Identifier(i))
        ])
    )
])
"""

# Test Case 8: For Loop
test_input_8 = """
for i in 1 .. 5 loop
    Put(i);
    for j in i + 1 .. 10 - i loop
    end loop;
end loop;
"""
expected_output_8 = """
Block([
    ForLoop(Identifier(i),Integer(1),Integer(5),
        Block([
            Put(Identifier(i)),
            ForLoop(Identifier(j),Term([Identifier(i),+,Integer(1)]),Term([Integer(10),-,Identifier(i)]),
            Block([])
            )
        ])
    )
])
"""

# Test Case 9: Empty Program
test_input_9 = """
"""
expected_output_9 = """
Block([])
"""

# Test Case 10: Logical Expressions
test_input_10 = """
a := True;
b := False;
c := a or False;
d := False or False or a;
e := b and True;
f := a and b or c;
g := a and (b or c); 
"""
expected_output_10 = """
Block([
    Assign(Identifier(a),Boolean(True)),
    Assign(Identifier(b),Boolean(False)),
    Assign(Identifier(c),Or([Identifier(a),Boolean(False)])),
    Assign(Identifier(d),Or([Boolean(False),Boolean(False),Identifier(a)])),
    Assign(Identifier(e),And([Identifier(b),Boolean(True)])),
    Assign(Identifier(f),Or([And([Identifier(a),Identifier(b)]),Identifier(c)])),
    Assign(Identifier(g),And([Identifier(a),Or([Identifier(b),Identifier(c)])]))
])
"""

# Test Case 11: Comparison Expressions
test_input_11 = """
a := 1 = 2;
b := 3 <= 4 and 5;
c := 6 /= 7;
"""
expected_output_11 = """
Block([
    Assign(Identifier(a),Comparison(Integer(1),=,Integer(2))),
    Assign(Identifier(b),And([Comparison(Integer(3),<=,Integer(4)),Integer(5)])),
    Assign(Identifier(c),Comparison(Integer(6),/=,Integer(7)))
])
"""

# Test Case 12: Arithmetic Expressions
test_input_12 = """
x := 10 - 5 * 2 mod 4;
y := (x + 1) * (z - 1);
"""
expected_output_12 = """
Block([
    Assign(Identifier(x),
        Term(
            [Integer(10),
            -,
            Factor([Integer(5),*,Integer(2),mod,Integer(4)])]
        )
    ),
    Assign(Identifier(y),
        Factor(
            [Term([Identifier(x),+,Integer(1)]),
            *,
            Term([Identifier(z),-,Integer(1)])]
        )
    )
])
"""

# A: OR / AND chaining
test_input_A = """
a := x or y or z;
b := x and y and z;
"""
expected_output_A = """
Block([
    Assign(Identifier(a),Or([Identifier(x),Identifier(y),Identifier(z)])),
    Assign(Identifier(b),And([Identifier(x),Identifier(y),Identifier(z)]))
])
"""

# B: precedence (AND before OR)
test_input_B = """
x := a or b and c;
"""
expected_output_B = """
Block([
    Assign(Identifier(x),
        Or([Identifier(a),And([Identifier(b),Identifier(c)])])
    )
])
"""

# C: comparisons inside AND
test_input_C = """
x := a < b and c > d;
"""
expected_output_C = """
Block([
    Assign(Identifier(x),
        And([
            Comparison(Identifier(a),<,Identifier(b)),
            Comparison(Identifier(c),>,Identifier(d))
        ])
    )
])
"""

# D: mixed arithmetic precedence
test_input_D = """
x := a + b * c - d / e mod f;
"""
expected_output_D = """
Block([
    Assign(Identifier(x),
        Term([
            Identifier(a),
            +,
            Factor([Identifier(b),*,Identifier(c)]),
            -,
            Factor([Identifier(d),/,Identifier(e),mod,Identifier(f)])
        ])
    )
])
"""

# E: nested parentheses
test_input_E = """
x := ((a + b) * (c + d));
"""
expected_output_E = """
Block([
    Assign(Identifier(x),
        Factor([
            Term([Identifier(a),+,Identifier(b)]),
            *,
            Term([Identifier(c),+,Identifier(d)])
        ])
    )
])
"""

# F: if with complex condition
test_input_F = """
if x then
    y := 1;
else
    y := 2;
end if;
"""
expected_output_F = """
Block([
    If(
        Identifier(x),
        Block([Assign(Identifier(y),Integer(1))]),
        Block([Assign(Identifier(y),Integer(2))])
    )
])
"""

# G: empty block
test_input_G = """
while False loop
end loop;
"""
expected_output_G = """
Block([
    WhileLoop(Boolean(False),Block([]))
])
"""

# H: for loop with expressions
test_input_H = """
for i in x+1 .. y-1 loop
    Put(i);
end loop;
"""
expected_output_H = """
Block([
    ForLoop(
        Identifier(i),
        Term([Identifier(x),+,Integer(1)]),
        Term([Identifier(y),-,Integer(1)]),
        Block([Put(Identifier(i))])
    )
])
"""

# I: boolean parentheses
test_input_I = """
x := (a or b) and (c or d);
"""
expected_output_I = """
Block([
    Assign(Identifier(x),
        And([
            Or([Identifier(a),Identifier(b)]),
            Or([Identifier(c),Identifier(d)])
        ])
    )
])
"""

# J: single element collapse
test_input_J = """
x := (5);
"""
expected_output_J = """
Block([
    Assign(Identifier(x),Integer(5))
])
"""



