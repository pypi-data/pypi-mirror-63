<pre width="1000">
                                                              __
█▀▀ █▀▀▄ █▀▀█ █░█ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀ █▀▀       _______    /*_>-<
▀▀█ █░░█ █▄▄█ █▀▄ █▀▀ ▀▀█ █░░█ █▄▄█ █░░ █▀▀   ___/ _____ \__/ /
▀▀▀ ▀░░▀ ▀░░▀ ▀░▀ ▀▀▀ ▀▀▀ █▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀  <____/     \____/
</pre>

[![Actions Status](https://github.com/cmrfrd/SnakeSpace/workflows/pypi/badge.svg)](https://github.com/cmrfrd/SnakeSpace/actions)
[![codecov](https://codecov.io/gh/cmrfrd/SnakeSpace/branch/master/graph/badge.svg)](https://codecov.io/gh/cmrfrd/SnakeSpace)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snakespace)
[![PyPI version](https://badge.fury.io/py/snakespace.svg)](https://badge.fury.io/py/snakespace)

# SnakeSpace

`SnakeSpace` is a module for building label namespaces from [attribute chaining](https://en.wikipedia.org/wiki/Method_chaining) and args/kwargs

### Why

Creating a good label for a file or a key is [hard](https://xkcd.com/1459/). In Python, `str` labels are usually either made via [format strings](https://www.python.org/dev/peps/pep-0498/) or string concatenation. First and foremost, format strings are great! However they are so dynamic, if you are not careful you can end up with a complicated expression, you also have to include those pesky `f` and `{}` characters. String concatenation can also get very messy as putting strings together can turn into a complicated algebraic expression. Now there is an alternative with `SnakeSpace`!

With `SnakeSpace` you type just what you want as a chain of attributes! The expression `S.yo.hey.woohoo` is totally valid! Now labels can be created with ease! Or at least in a different style...

### Installing

This repo uses setup.py, so it follows the standard Python install routine

``` shell
pip install -U snakespace
```

Or if you want to install from source

``` shell
git clone https://github.com/cmrfrd/SnakeSpace.git
cd SnakeSpace
python3 setup.py install
```

### Examples and Behavior

With `SnakeSpace` you can create label namespaces from chaining attributes.

``` python
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.super.duper.cool) # -> 'super.duper.cool'
```

You can also use the `s` function to supply custom arguments

``` python
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.my.favorite.number.s(1301)) # -> 'my.favorite.number.1301'

print(S.yay.kwargs.s(1, 2, third=3)) # -> 'yay.kwargs.1.2.3'

print(S.shoop.s('da').whoop) # -> 'shoop.da.whoop'
```

If you don't like using periods as the default separator, you can change it using the *special* attribute `separator`

``` python
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.a.b.c)    # -> 'a.b.c'
S.separator = '/'
print(S.a.b.c)    # -> 'a/b/c'
```

~Note!~ You can't chain attributes with `.separator`


### Namespacing

`SnakeSpace` behaves in between a `str`, and it's own custom object.

`SnakeSpace` will behave like a `str` when being operated on with another `str` ex: `S.a + 'woop' # -> 'awoop`. However `SnakeSpace` have slightly different behavior when being operated on by other `SnakeSpace`s to support common namespacing operations

`SnakeSpace` can be used for composing and comparing other `SnakeSpace`s.

You can see if a `SnakeSpace` is a subspace of another by using `in`

``` python
from snakespace import SnakeSpace
S = SnakeSpace()

print(S.a.b.c in S.a)           # -> True
print(S.potato in S.a)          # -> False
print(S.data.s(1,2) in S.data)  # -> True
```

`SnakeSpace`s can be compared, composed, and operated on

``` python
from snakespace import SnakeSpace
S = SnakeSpace()

# order (lexicographic)
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
print(S.a % S.a.b.c)               # -> True
print(S.a.b.c.d % S.a.b.c)         # -> False
```

`Snakespace` also comes with multiple common python `str` methods that are applied element wise in a `Snakespace` opposed to being operated on the whole resulting string.

### Limitations

`SnakeSpace` objects have some reserved attributes that cannot be used to building namespace labels.

1. Any [dunder methods/attributes](https://stackoverflow.com/questions/1418825/where-is-the-python-documentation-for-the-special-methods-init-new) (It's best just to avoid building anything with a start of a double underscore)
2. Any of these common string attributes

<pre>
['capitalize', 'casefold', 'count', 'encode', 'endswith',
 'find', 'index', 'isalnum', 'isalpha', 'isdecimal',
 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable',
 'isspace', 'istitle', 'isupper', 'ljust', 'lower',
 'lstrip', 'partition', 'replace', 'rfind', 'rindex',
 'rjust', 'rpartition', 'rstrip', 's', 'separator',
 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
</pre>

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

make a bunch of files with a name schema, then easily filter them

``` python
from uuid import uuid4
from pathlib import Path as Pth
import tempfile as tmpf
from snakespace import SnakeSpace

S = SnakeSpace(separator='/')
tmp_dir = tmpf.TemporaryDirectory()

## Make some files
for i in range(10):
    Pth(S.s(tmp_dir.name,uuid4())).touch()

for f in Pth(tmp_dir.name).iterdir():
    if S.a < S(f.parts[-1]) < S.z:
        print(f)
```

### Releasing

1. `bump2version`
2. push tag release
3. check gha
