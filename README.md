# pjj
PJJ provides a fast and simple way to retrieve values from JSON documents.
    

## feature
点连接字符串解析json
支持：    
- 点连接查询     
- 通配符 ['?', '*'] 模糊查询      
- #符返回字典keys列表、列表长度      
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
```
**基础使用**：点连接返回值、#符号返回字典keys列表
```
# ------------basis-------------
print(Pjj('top', test_json).res)
# result: "a"

print(Pjj('mid', test_json).res)
# result: {"m":1, "i":2, "d":3}

print(Pjj('mid.m', test_json).res)
# result: 1

print(Pjj('#', test_json).res)
# result: ['top', 'mid', 'tail', 'test.abc', 'mmm', 'filter']
``` 
**通配符**
```
#  ----------wildcard-----------
print(Pjj('t?p', test_json).res)
# result: "a"

print(Pjj('top*', test_json).res)
# result: "a"

print(Pjj('f*', test_json).res)
# result: [{'name': 'judy', 'age': 24}, {'name': 'tom', 'age': 30}, {'name': 'jerry', 'age': 28}]
```
**列表**
```
# ---------index based----------
print(Pjj('tail.0', test_json).res)
# result: 11

# ----------list length---------
print(Pjj('mmm.#', test_json).res)
# result: 3

print(Pjj('mmm.#.a1', test_json).res)
# result: ["A", "C"]

print(Pjj('mmm.1.a1', test_json).res)
# result: "C"

# -----------wildcard-----------
print(Pjj('mmm.b?', test_json).res)
# result: ["B", "D"]
```
**转义字符**
```
#  ---------string escape-------
print(Pjj('test\.abc', test_json).res)
# result: "success"
```
**字典条件筛选**
```
# ---------list query-----------
print(Pjj('filter.#(name=="judy").age', test_json).res)
# result: "[24]"

print(Pjj('filter.#(age>26).name', test_json).res)
# result: ['tom', 'jerry']

print(Pjj('filter.#(age>26&&name=="tom")', test_json).res)
# result: [{'name': 'tom', 'age': 30}]

print(Pjj('filter.#(age>29||age<=25)', test_json).res)
# result: [{'name': 'judy', 'age': 24}, {'name': 'tom', 'age': 30}]

print(Pjj("fil*.#(name!='judy').#(age>=30)", test_json).res)
# result: [{'name': 'tom', 'age': 30}]
```

## TODO
- ~~空输入返回完整对象~~    
- ~~字典列表筛选~~  
- 数字列表筛选  
 


## BUG
- ~~下划线搭配通配符匹配不了、多个通配符匹配不了~~    
- **条件查询时如果匹配对象带比较运算符或者逻辑运算符会异常**
- **条件查询时如果对象带反斜杠会异常**
## reference
https://github.com/tidwall/jj
