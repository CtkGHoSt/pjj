# pjj
Pjj可以从json文档或dict、list中快速检索返回内容，支持模糊查询

PJJ provides a fast and simple way to retrieve values from JSON documents.
    

## Feature
点连接字符串解析json
支持：    
- 点连接查询     
- 通配符 ['?', '*'] 模糊查询      
- #符返回字典keys列表、列表长度      
- 字典条件查询     
- 双引号强制字符串查询（列表内对象key和索引冲突时，默认返回索引的对象，[双引号后返回该key的列表](https://github.com/CtkGHoSt/pjj/blob/main/README.md#%E8%BD%AC%E4%B9%89%E5%AD%97%E7%AC%A6%E5%92%8C%E5%BC%BA%E5%88%B6%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%A3%80%E7%B4%A2)）


## Usage

```
from pjj import Pjj

test_json = '''
{
    "top":"a", 
    "mid":{"m":1, "i":2, "d":3}, 
    "tail":[11,22,33], 
    "test.abc":"success", 
    "mmm":[{"a1":"A", "b1":"B"}, {"a1":"C", "b1":"D"}],
    "force_string":[{"1":"a1", "2":"a2"}, {"1":"b1", "2":"b2"}],
    "filter": [
        {"name":"judy", "age":24},
        {"name":"tom", "age":30},
        {"name":"jerry", "age":28},
        {"name":"\\"<c>\\"", "age":24}
    ]
}
''' 
```
#### **基础使用**：点连接返回值、#符号返回字典keys列表
```
# ------------basis-------------
print(Pjj('top', test_json).res)
# result: "a"

print(Pjj('mid', test_json).res)
# result: {"m":1, "i":2, "d":3}

print(Pjj('mid.m', test_json).res)
# result: 1

print(Pjj('#', test_json).res)
# result: ['top', 'mid', 'tail', 'test.abc', 'mmm', 'force_string', 'filter']
``` 
#### **通配符**
```
#  ----------wildcard-----------
print(Pjj('t?p', test_json).res)
# result: "a"

print(Pjj('to*', test_json).res)
# result: "a"

print(Pjj('f*r', test_json).res)
# result: [{'name': 'judy', 'age': 24}, {'name': 'tom', 'age': 30}, {'name': 'jerry', 'age': 28}, {'name': '"<c>"', 'age': 24}]
```
#### **列表**（索引和对象key冲突使用双引号强制字符串检索）
```
# ---------index based----------
print(Pjj('tail.0', test_json).res)
# result: 11

# ----------list length---------
print(Pjj('mmm.#', test_json).res)
# result: 2

print(Pjj('mmm.#.a1', test_json).res)
# result: ["A", "C"]

print(Pjj('mmm.1.a1', test_json).res)
# result: "C"

# -----------wildcard-----------
print(Pjj('mmm.b?', test_json).res)
# result: ["B", "D"]
```
#### **转义字符和强制字符串检索**
```
#  ---------string escape-------
print(Pjj('test\.abc', test_json).res)
# result: "success"

# ---------force string--------
print(Pjj('"test.abc"', test_json).res)
# result: "success"

print(Pjj('force_string.1',test_json).res)
# result: {'1': 'b1', '2': 'b2'}

print(Pjj('force_string."1"',test_json).res)
# result: ['a1', 'b1']
```
#### **字典条件筛选**
```
# ---------list query-----------
print(Pjj('filter.#(name=="judy").age', test_json).res)
# result: "[24]"

print(Pjj('filter.#(age>26).name', test_json).res)
# result: ['tom', 'jerry']

print(Pjj('filter.#(age>26&&name=="tom")', test_json).res)
# result: [{'name': 'tom', 'age': 30}]

print(Pjj('filter.#(age>29||age<=25)', test_json).res)
# result: [{'name': 'judy', 'age': 24}, {'name': 'tom', 'age': 30}, {'name': '"<c>"', 'age': 24}]

print(Pjj('fil*.#(name!="judy").#(age>=30)', test_json).res)
# result: [{'name': 'tom', 'age': 30}]

print(Pjj('fil*.#(name=="\\"<c>\\"")', test_json).res)
# result: [{'name': '"<c>"', 'age': 24}]
```

## TODO
- ~~空输入返回完整对象~~    
- ~~字典列表筛选~~  
- 数字列表筛选  
- 可以对对象赋值
 


## BUG
- ~~下划线搭配通配符匹配不了、多个通配符匹配不了~~    
- ~~如果对象带反斜杠会异常~~
- ~~条件查询时如果匹配对象带比较运算符或者逻辑运算符会异常~~    
- ~~如果列表下的对象key为整数，只能返回索引对象不能返回列表key对应的value列表~~ 使用双引号强制字符串    
- ~~条件筛选：如果对象key为浮点数会异常~~ 使用双引号强制字符串     
## Reference
https://github.com/tidwall/jj
