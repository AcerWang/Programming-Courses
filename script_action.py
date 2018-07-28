#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JsonDict(object):

    def __init__(self, data=None):
        self.__data__ = data if data else {}

    def __setattr__(self, key, value):
        if key == '__data__':
            object.__setattr__(self, key, value)
        else:
            self.__data__[key] = value

    def __getattr__(self, item):
        res = self.__data__.get(item)
        if isinstance(res, list):
            res = [] if res == [] else map(self.__new_one_or_origin, res)
            self.__data__[item] = res
        elif isinstance(res, dict):
            res = JsonDict(res)
        return '' if res is None else res

    def get_data(self):
        return self.__data__

    @staticmethod
    def __new_one_or_origin(item):
        if isinstance(item, dict):
            return JsonDict(item)
        return item

    
if __name__ == '__main__':
    m = {
         'action': [100, 111, 105]
         }

    j = JsonDict(m)

    j.action.sort()
    j.action.append(1)

    print j.action
    print j.get_data()
