# pjj
PJJ provides a fast and simple way to retrieve values from JSON documents.
    

## feature
点连接字符串解析json
支持：    
- 点连接查询     
- 通配符 ['?', '*'] 模糊查询      
- # 符返回字典keys列表、列表长度      
- 字典条件查询     


## use

```
from pjj import Pjj

test_json = '''
{
    "top":"a", 
    "mid":{"m":1, "i":2, "d":3}, 
    "tail":[11,22,33], 
    "test.abc":"success", 
    "mmm":[{"a1":"A", "b1":"B"}, {"a1":"C", "b1":"D"}],
    "filter": [
        {"name":"judy", "age":24},
        {"name":"tom", "age":30},
        {"name":"jerry", "age":28}
    ]
}
''' 

# ------------basis-------------
print(Pjj('top', test_json).res)
# result: "a"

print(Pjj('mid', test_json).res)
# result: {"m":1, "i":2, "d":3}

print(Pjj('#', test_json).res)
# result: ['top', 'mid', 'tail', 'test.abc', 'mmm', 'filter']

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

# ---------list query-----------
print(Pjj('filter.#(name=="judy").age', test_json).res)
# result: "[24]"

print(Pjj('filter.#(age>26).name', test_json).res)
# result: ['tom', 'jerry']

print(Pjj('filter.#(age>26&&name=="tom")', test_json).res)
# result: [{'name': 'tom', 'age': 30}]

print(Pjj('filter.#(age>29||age<=25)', test_json).res)
# result: [{'name': 'judy', 'age': 24}, {'name': 'tom', 'age': 30}]
```

## TODO
- ~~空输入返回完整对象~~    
- ~~字典列表筛选~~  
- 数字列表筛选  
- ~~下划线搭配通配符匹配不了、多个通配符匹配不了~~     
- 条件查询时如果匹配对象带比较运算符或者逻辑运算符会异常

## BUG

## reference
https://github.com/tidwall/jj
