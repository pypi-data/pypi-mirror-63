<pre>
                                                              __
█▀▀ █▀▀▄ █▀▀█ █░█ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀ █▀▀       _______    /*_>-<
▀▀█ █░░█ █▄▄█ █▀▄ █▀▀ ▀▀█ █░░█ █▄▄█ █░░ █▀▀   ___/ _____ \__/ /
▀▀▀ ▀░░▀ ▀░░▀ ▀░▀ ▀▀▀ ▀▀▀ █▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀  <____/     \____/
</pre>

`SnakeSpace` is a module for building for composable namespace identifiers from [attribute chaining](https://en.wikipedia.org/wiki/Method_chaining) and args/kwargs

### Examples and Behavior

With `SnakeSpace` you can create namespace identifiers from chaining attributes.

``` text
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.super.duper.cool) # -> 'super.duper.cool'
```

You can also use the `s` function to supply custom arguments

``` text
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.my.favorite.number.s(1301)) # -> 'my.favorite.number.1301'

print(S.yay.kwargs.s(1, 2, third=3)) # -> 'yay.kwargs.1.2.3'

print(S.shoop.s('da').whoop) # -> 'shoop.da.whoop'
```

If you don't like using periods as the default seperator, you can change it using the *special* attribute `seperator`

``` text
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.a.b.c)    # -> 'a.b.c'
S.seperator = '/'
print(S.a.b.c)    # -> 'a/b/c'
```

### Namespacing

`SnakeSpace` behaves in between a `str`, and it's own custom object.

`SnakeSpace` will behave like a `str` when being operated on with another `str` ex: `S.a + 'woop' # -> 'awoop`. However `SnakeSpace` have slightly different behavior when being operated on by other `SnakeSpace`s to support common namespacing operations

`SnakeSpace` can be used for composing and comparing other `SnakeSpace`s.

You can see if a `SnakeSpace` is a subspace of another by using `in`

``` text
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.a.b.c in S.a)           # -> True
print(S.potato in S.a)          # -> False
print(S.data.s(1,2) in S.data)  # -> True
```

`SnakeSpace`s can be compared and composed

``` text
from snakespace import SnakeSpace
S = SnakeSpace()

# order
print(S.one < S.one.two)           # -> True
print(S.a.b.c > S.a.b > S.a)       # -> True

# equality
print(S.a == S.a)                  # -> True

# addition
print(S.a + S.b)                   # -> 'a.b'

# size
print(len(S.apple.bannana.cherry)) # -> 3

# items
print(S.a.b.c[1])                  # -> 'b'

# superspace
print(S.a.b.c % S.a)               # -> True
print(S.a.b.c % S.a.b.c.d)         # -> False
```

`Snakespace` also comes with multiple common python `str` methods that are applied element wise in a `Snakespace` opposed to being operated on the whole resulting string.


### Fun examples

Easily make a bunch of keys for a `dict`

``` python
from random import randint
from snakespace import SnakeSpace
S = SnakeSpace()
D = {}

for i in range(10):
    D[S.data.s(i)] = randint(0,10)


```

### Limitations

*Special attributes:* SnakeSpace objects have some special attributes that cannot be used to build labels.

    1. `seperator` which is used to configure what string will be used to seperate spaces
    2. Any [dunder methods/attributes](https://stackoverflow.com/questions/1418825/where-is-the-python-documentation-for-the-special-methods-init-new)

It's best just to avoid building anything with a start of a double underscore
