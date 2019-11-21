exponentiation

setup
+>>>

input a^b
,>,

multiply by a 'b' times
[
    subtract one from b
    -

    copy over a to multiply spot
    <[-<+<+>>] <[->+<] <

    multiply total by 'a'
    [- < [-<+<+>>] < [->+<] >>]

    copy over total
    < [-] << [->>+<<]

    move back to b
    >>>>>>
]

print result
<<<<;