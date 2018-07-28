#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from copy import deepcopy


class JsonDict(object):

    __slots__ = ['action', 'actionId', 'params', 'sleep', '__data__']
    __setText = 'setText'
    __initVariable = 'initVariable'
    __click = 'click'
    __plugin = 'plugin'

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
    def get_setText_param_value(action):
        action = JsonDict(action)
        if action.action == JsonDict.__setText:
            for param in action.params:
                if param.key == JsonDict.__setText:
                    return JsonDict.__setText + " " + param.value
        return ''

    def get_param_name_value(self):
        if self.is_setText():
            for param in self.params:
                if param.key == 'setText' and param.name:
                    return param.name, param.value
        elif self.is_plugin():
            for param in self.params:
                if param.key == 'param' and param.name:
                    name = param.name
                    _value = param.value.split(' ', 1)
                    value = _value[-1] if len(_value) == 2 else ''
                    return name, value
        else:
            return '', ''

    def set_param_name(self, name):
        for param in self.params:
            if param.key == 'setText':
                param.name = name

    def set_param_value(self, dataset):
        if self.is_setText() or self.is_plugin():
            for param in self.params:
                if (param.key == 'setText' or param.key == 'param') and param.name is not None:
                    name = param.name
                    value
                    param.value = value
                    self.is_expanded = True
                    return
        elif self.is_initVariable():
            self.expected = value
            self.is_expanded = True
            return
        else:
            pass


    @staticmethod
    def __new_one_or_origin(item):
        if isinstance(item, dict):
            return JsonDict(item)
        return item

    def is_setText(self):
        return True if self.action == self.__setText else False

    def is_plugin(self):
        return True if self.action.startswith(self.__plugin) else False

    def is_initVariable(self):
        return True if self.action == self.__initVariable else False

    def _normalize(self, action_item, index, global_var):
        def _expand_param_value(action, index):
            if action.get('action') == 'setText':
                name_dict = {item['name']: item for item in action_config.get('plugins', []) if 'path' not in item and 'name' in item}
                for param in action.get('params', []):
                    _p = name_dict.get(param.get('name'), {})
                    if param.get('key') == 'setText' and param.get('name') is not None and _p:
                        if _p['name'] in global_var:
                            param['value'] = global_var[_p['name']]
                        else:
                            # 防止index超过setText数组长度,下同
                            param['value'] = _p['setText'][index] if index < len(_p['setText']) else _p['originValue']
                        action['is_expanded'] = True
            elif action.is_plugin():
                name_dict = {item['name']: item for item in action_config.get('plugins', []) if
                             'path' in item and 'name' in item}
            elif action.is_initVariable():
                name_dict = {ocrArea['name']: ocrArea for ocrArea in action_config.get('ocrAreas', [])}
                _a = name_dict.get(action.variableName, {})
                # 如果index超过期望值长度，默认超过的期望值为'*'
                if _a['name'] in global_var:
                    action.expect = global_var[_a['name']]
                else:
                    action.expect = _a.get('expect')[index] if index < len(_a['expect']) else '*'
                if _a.get('regExp'):
                    action.variableRegex = _a['regExp']
                action.is_expanded = True

            for param in act.params:
                _p = name_dict.get(param.name, {})
                if _p and param.key == 'setText' and param.name is not None :

                    p_value, originValue, = ['', 'originValue'] if act.is_setText() else [os.path.basename(_p.get('path', '')), 'originTextValue']
                    _value = _p['setText'][index] if index < len(_p['setText']) else _p[originValue]

                    if _p.get('setText'):
                        if _p['name'] in global_var:
                            param.value = ' '.join([p_value, global_var[_p['name']]]).lstrip()
                        else:
                            param.value = ' '.join([p_value, _value]).lstrip()
                        act.is_expanded = True

                    if act.is_plugin():
                        if _p.get('originTextValue'):
                            param.value = ' '.join([p_value, _p.get('originTextValue')]).lstrip()
                        else:
                            param.value = p_value

        action = deepcopy(action_item)
        action_config = expanded_snapshots_json_dict_without_suffix.get(action.get('actionId', ''))
        if action_config:
            # 截图上配置了忽略此步骤，把该截图对应的所有action块都置为None，将在最后剔除为None的，不发送给tc
            if action_config.get('ignoreAction', False):
                return None

            if index is not None:
                _expand_param_value(action, index)
                return action
            else:
                return action
        else:
            return action


if __name__ == '__main__':
    m = {
         'action': [100, 111, 105]
         }

    print id(m['action'])
    j = JsonDict(m)
    print id(j.action)
    j.action.sort()

    print j.action
    print j.get_data()

