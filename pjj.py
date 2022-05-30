
import re
import json

class Pjj:
    class TooManyResults(Exception):
        pass

    @staticmethod
    def _split(split_string):
        if len(split_string) == 0:
            return '', None
        split_list = split_string.split('.')
        res = ''
        for item in split_list:
            res += item
            if item[-1] != '\\':
                break
            res += '.'
        return res, None if res == split_string else split_string[len(res)+1:]

    # @staticmethod
    def _get_re_key(self, key, tmp_obj):
        '''
        匹配key中的通配符 ['?', '*']
        '''
        re_key = ['?', '*']
        for rk in re_key: # 匹配通配符  ['?', '*']
            re_match_count = 0
            re_start_index = [i.start() for i in re.finditer('\\'+rk, key)] # 获取通配符起始位
            for rk_index in re_start_index:
                if key[rk_index-1] == '\\': # 不匹配转义
                    continue
                key = key[:rk_index+re_match_count] + r'\S' + key[rk_index+re_match_count:]
                re_match_count += 2
        _ = list(filter(lambda x: re.fullmatch(key, x) is not None,tmp_obj.keys())) # 匹配所有key
        if len(_) == 0:
            # raise IndexError('key not found：{}/{}'.format(key, tmp_obj.keys()))
            return None
        elif len(_) > 1:
            raise self.TooManyResults('{}'.format(_))
        return _[0]
    
    @staticmethod
    def _judge_eval_params(params:str, tmp_obj):
        '''
        只能使用比较方法，且只能用tmp_obj的key作比较
        #(count>=5 && name=="huian")
        #(tail>15&&tail!=22||tail==11)

        eval(params)不够安全
        '''
        logical = [r'[&&]+', r'[||]+']
        comparison = [r'[>,<][=]?', r'[!,=]?=']
        pp = [params,]
        cache = list()
        new_pp = list()
        for operator in logical + comparison: # 先处理逻辑运算符，再处理比较运算符54
            new_pp = list()
            for i in pp:
                re_list = re.findall(operator, i)
                if len(re_list) == 0:
                    new_pp.append(i)
                    continue
                for j in re_list:
                    cache = i.split(j)
                new_pp += cache
            pp = new_pp
            cache = list()
        f_string = list(filter(lambda x:x not in list(tmp_obj.keys()),pp))
        for p in f_string:
            try:
                float(p)
            except ValueError:
                if not (p[0] == '"' and p[-1] == '"' or p[0] == "'" and p[-1] == "'"):
                    raise ValueError(p)

        for key in tmp_obj.keys():
            params = params.replace(key, 'tmp_obj["{}"]'.format(key))
        params = params.replace('&&', ' and ').replace('||', ' or ')
        return eval(params)

    def _get_value(self, key, tail, tmp_obj):
        if isinstance(tmp_obj, list):
            
            if key == '#':
                if tail is None:
                    return len(tmp_obj)
                return tmp_obj
            try:
                return tmp_obj[int(key)]
            except IndexError:
                return None
            except ValueError: # key 不为整型
                try:
                    if re.fullmatch(r'#(\S+)', key):
                        exec_string = re.fullmatch(r'#(\S*)', key).group()[2:-1]
                        tmp_obj = [i for i in tmp_obj if self._judge_eval_params(exec_string, i)]
                        return tmp_obj
                    return [ i[self._get_re_key(key, i)] for i in tmp_obj]
                except KeyError:
                    return None
        
        re_key = self._get_re_key(key, tmp_obj)
        try:
            return tmp_obj[re_key]
        except KeyError:
            return None

    def make_res(self):
        head, tail = self._split(self.base_string)
        tmp_obj = json.loads(self.json_obj)
        self._json = json.loads(self.json_obj)
        while True:
            res = self._get_value(head, tail, tmp_obj)
            if tail is None:
                break
            head, tail = self._split(tail)
            tmp_obj = res
            
        self.res = res

    def __init__(self, search_s, json_obj):
        self.base_string = search_s
        self.json_obj = json_obj
        self.make_res()

    
