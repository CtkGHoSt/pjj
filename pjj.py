
import re
import json
import copy

class Pjj:
    class TooManyResults(Exception):
        pass

    @staticmethod
    def _split(split_string):
        if len(split_string) == 0:
            return '', None
        split_list = split_string.split('.')
        if split_list[0][0] == '"': # 是否强制字符串
            if split_list[0][-1] != '"':
                try: # 拼合左引号
                    idx = list(map(lambda x:x[-1]=='"', split_list[0:])).index(True)
                    split_list = ['.'.join(split_list[:idx+1]),] + split_list[idx+1:]
                except ValueError: # 没有匹配的引号
                    pass
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
        try:
            _ = list(filter(lambda x: re.fullmatch(key, x) is not None,tmp_obj.keys())) # 匹配所有key
        except AttributeError:
            return None
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

        # 先处理空字符串 
        pp = list()
        string_idx = 0
        count = 0
        string_params_list = list()
        # i=0
        for i in re.finditer(r'[^\\]""', params):
            if count%2 != 1:
                # pp.append(params[string_idx:i.start()+1]+'string_params_list[{}]'.format(len(string_params_list)))
                pp.append(params[string_idx:i.start()+1]+'{{{}}}'.format(len(string_params_list)))
                string_params_list.append('""')
            string_idx = i.end()
            count +=1
            pp.append(params[i.end():])
        if len(pp)!=0:
            params = ''.join(pp)
        # 处理非空字符串
        pp = list()
        string_idx = 0
        count = 0
        if re.search(r'[^\\"]"', params) is not None:
            for i in re.finditer(r'[^\\]"', params):
                if count%2 != 1:
                    pp.append(params[string_idx:i.start()+1]) # 没问题
                    string_idx = i.start()+1
                else:
                    string_params_list.append(params[string_idx:i.end()])# 没问题
                    pp.append('{{{}}}'.format(len(string_params_list)-1))
                    string_idx = i.end()
                count +=1
            if count %2 != 1:
                pp.append(params[i.end():])
            else:
                string_params_list.append(params[i.end()+1:])
                pp.append('{{{}}}'.format(len(string_params_list)-1))
            params = ''.join(pp)
        # 以运算符分割params
        pp = list()
        last_start = 0
        for i in re.finditer('([|]{2})|([&]{2})|(([!,=]=)|([>,<]=?))', params):
            pp.append(params[last_start:i.start()])
            pp.append(params[i.start():i.end()])
            last_start = i.end()
        pp.append(params[i.end():])
        f_string = list(filter(lambda x:x not in list(tmp_obj.keys()),pp))
        # 判断输入的参数是否只为运算符、tmp_obj key、字符串
        for p in f_string:
            try:
                float(p)
            except ValueError:
                if re.match(r'{\d}', p) is None and  re.match('([|]{2})|([&]{2})|(([!,=]=)|([>,<]=?))', p) is None:
                    raise ValueError(p)
        # 格式化params为可执行语句
        for key in tmp_obj.keys():
            params = params.replace(key, 'tmp_obj["{}"]'.format(key))
        params = params.replace('&&', ' and ').replace('||', ' or ')
        params = params.format(*string_params_list)
        return eval(params)

    def __get_list_value(self, key, tail, tmp_obj):
        '''处理对象为列表的'''
        if key == '#':
            if tail is None:
                return len(tmp_obj)
            return tmp_obj
        try:
            if re.fullmatch(r'^".*"$', key): # 判断是否强制输入字符串
                key = key[1:-1]
                raise ValueError # 强制输入为字符串
            return tmp_obj[int(key)] # 返回索引下的对象
        except IndexError:
            return None
        except ValueError: # key不为整形
            try:
                if re.fullmatch(r'#(\S+)', key): # 列表条件筛选
                    exec_string = re.fullmatch(r'#(\S*)', key).group()[2:-1]
                    tmp_obj = [i for i in tmp_obj if self._judge_eval_params(exec_string, i)]
                    return tmp_obj
                return [ i[self._get_re_key(key, i)] for i in tmp_obj] # 返回列表下对象key对应的value
            except KeyError:
                return None

    def _get_value(self, key, tail, tmp_obj):
        if isinstance(tmp_obj, list):
            return self.__get_list_value(key, tail, tmp_obj)
        if re.fullmatch(r'^".*"$', key): # 处理强制字符串
            key = key[1:-1]
        if key == '#':
            return list(tmp_obj.keys())
        re_key = self._get_re_key(key, tmp_obj)
        if re_key is None:
            return None
        try:
            return tmp_obj[re_key]
        except KeyError:
            return None

    def search(self, search_s=None):
        if search_s is None:
            search_s = self.base_string
        head, tail = self._split(search_s)
        tmp_obj = copy.deepcopy(self._json)
        if len(search_s) == 0:
            self.res = self._json
            return self.res
        while True:
            res = self._get_value(head, tail, tmp_obj)
            if tail is None:
                break
            head, tail = self._split(tail)
            tmp_obj = res
        self.res = res
        return self.res

    def __init__(self,json_or_dict, search_s=None):
        self.base_string = search_s if search_s is not None else ''
        if isinstance(json_or_dict, str):
            self.json_obj = json_or_dict
            self._json = json.loads(json_or_dict)
        elif isinstance(json_or_dict, dict) or isinstance(json_or_dict, list):
            self._json = json_or_dict
        else:
            raise TypeError('json_or_dict must be str or dict or list')
        self.search()
