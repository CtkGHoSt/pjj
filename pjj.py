
import re
import json

class Pjj:
    @staticmethod
    def _split(split_string):
        split_list = split_string.split('.')
        res = ''
        for item in split_list:
            res += item
            if item[-1] != '\\':
                break
            res += '.'
        return res, None if res == split_string else split_string[len(res)+1:]

    def _get_value(self, key, tail, tmp_obj):
        if isinstance(tmp_obj, list):
            if key == '#':
                if tail is None:
                    return len(tmp_obj)
                return tmp_obj
            try:
                return tmp_obj[int(key)]
            except ValueError:
                return [ i[key] for i in tmp_obj]
        
        re_key = ['?', '*']
        for rk in re_key:
            if key.find(rk) > 0 and key[key.find(rk)-1]!='\\':
                rk_index = key.find(rk)
                key = key[:rk_index] + r'\S' + key[rk_index:]
        _ = list(filter(lambda x: re.fullmatch(key, x) is not None,tmp_obj.keys()))
        if len(_) != 1:
            raise IndexError('key not found：{}/{}'.format(key, tmp_obj.keys()))
        return tmp_obj[_[0]]

    def make_res(self):
        head, tail = self._split(self.base_string)
        tmp_obj = json.loads(self.json_obj)
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

    