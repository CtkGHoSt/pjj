# pjj
JJ provides a fast and simple way to retrieve values from JSON documents.
    
## use

```
from pjj import Pjj

test_json = '''
{
    "top":"a", 
    "mid":{"m":1, "i":2, "d":3}, 
    "tail":[11,22,33], 
    "test.abc":"success", 
    "mmm":[{"a1":"A", "b1":"B"}, {"a1":"C", "b1":"D"}]
}
''' 

# ------------basis-------------
print(Pjj('top', test_json).res)
# result: "a"

print(Pjj('mid', test_json).res)
# result: {"m":1, "i":2, "d":3}

#  ----------wildcard-----------
print(Pjj('t?p', test_json).res)
# result: "a"

print(Pjj('top*', test_json).res)
# result: "a"

# -------point connection-------
print(Pjj('mid.m', test_json).res)
# result: 1

# ---------index based----------
print(Pjj('tail.0', test_json).res)
# result: 11

# -------------list-------------
print(Pjj('mmm.#', test_json).res)
# result: 3

print(Pjj('mmm.b?', test_json).res)
# result: ["B", "D"]

print(Pjj('mmm.#.a1', test_json).res)
# result: ["A", "C"]

print(Pjj('mmm.1.a1', test_json).res)
# result: "C"

#  ---------string escape-------
print(Pjj('test\.abc', test_json).res)
# result: "success"
```

## reference
https://github.com/tidwall/jj
