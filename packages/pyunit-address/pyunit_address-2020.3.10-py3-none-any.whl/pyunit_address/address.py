#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
try:
    from collections.abc import Iterable
except ModuleNotFoundError:
    from collections import Iterable
from .TreeAlgorithm import dict_create_tree
from collections import Counter
import bz2
import os
import json
import re


class Address:

    def __init__(self, is_max_address=False):
        """初始化

        :param is_max_address: 满足最长地址
        """

        # 加载精准匹配的词库，共40万 、  顺序表
        self.address_data, self.sequential_address = self._unzip()
        self.length_all = len(self.address_data)

        # 加载模糊匹配的词库
        self.vague = [w.strip() for w in open(os.path.dirname(__file__) + os.sep + 'CAT.txt', encoding='UTF-8')]
        self.length_vague = len(self.vague)

        self.is_max_address = is_max_address
        self._auto_length()
        self.Tree = dict_create_tree(self.sequential_address)

    def _auto_length(self):
        """自动寻找地址的最长度"""
        self.max_data = len(max(self.address_data, key=lambda x: len(x)))
        self.max_vague = len(max(self.vague, key=lambda x: len(x)))
        self.max_address = self.max_data if self.max_data >= self.max_vague else self.max_vague

    def set_vague_text(self, text):
        """重新加载模糊匹配的文本数据

        数据格式1： ['地址1','地址2',....] 并且排序。默认是：sorted()

        数据格式2： 词库的地址，文本默认格式是UTF-8
        """
        if isinstance(text, list):
            self.vague = text
        elif isinstance(text, str) and os.path.exists(text):
            ls = set()
            with open(text, encoding='UTF-8')as fp:
                for f in fp:
                    ls.add(f.strip())
            self.vague = list(sorted(ls))
        else:
            raise TypeError('格式异常！')
        self.length_vague = len(self.vague)
        self._auto_length()

    def delete_vague_text(self, words):
        """删除默认词库

        格式1：删除一个词，传入字符串

        格式2：删除一列词，传入列表
        """
        if isinstance(words, str):
            word = words.strip()
            if word in self.vague:
                self.vague.remove(word)
                self.length_vague -= 1

            if word in self.address_data:
                self.address_data.remove(word)
                self.length_all -= 1
        elif isinstance(words, Iterable):
            for word in words:
                word = word.strip()
                if word in self.vague:
                    self.vague.remove(word)
                if word in self.address_data:
                    self.address_data.remove(word)
            else:
                self.length_vague = len(self.vague)
                self.length_all = len(self.address_data)
        else:
            raise ValueError('增加值错误')
        self._auto_length()

    def add_vague_text(self, words):
        """增加地址词语

        格式1： 只增加一个词

        格式2：增加一个列表
        """
        if isinstance(words, str) and (words not in self.vague):
            self.vague.append(words.strip())
            self.vague = list(sorted(self.vague))
            self.length_vague += 1
        elif isinstance(words, Iterable):
            for word in words:
                word = word.strip()
                if word not in self.vague:
                    self.vague.append(word)
            else:
                self.vague = list(sorted(self.vague))
                self.length_vague = len(self.vague)
        else:
            raise ValueError('增加值错误')
        self._auto_length()

    @staticmethod
    def _unzip() -> (list, dict):
        """解压地址数据包"""
        name = 'address'
        bz = bz2.BZ2File(os.path.dirname(__file__) + os.sep + name + '.bz2')
        lines = bz.read().decode('utf-8')
        address = json.loads(lines[512:-1134], encoding='utf8')
        ls = []
        for one_k, one_v in address.items():
            ls.append(one_k)
            for two_k, two_v in one_v.items():
                ls.append(two_k)
                for three_k, three_v in two_v.items():
                    ls.append(three_k)
                    for four_k, four_v in three_v.items():
                        ls.append(four_k)
                        for five_k in four_v:
                            ls.append(five_k)
        return list(sorted(ls)), address

    @staticmethod
    def _bisect_right(a, x, lo, hi):
        """二分法算法"""
        while lo < hi:
            mid = (lo + hi) // 2
            mid_value = a[mid]
            if x < mid_value:
                hi = mid
            elif x == mid_value:
                return lo, mid_value
            else:
                lo = mid + 1
        return lo

    def _vague(self, values):
        """模糊匹配"""
        value = self._bisect_right(self.vague, values, 0, self.length_vague)
        if isinstance(value, tuple):
            return value[1]
        return None

    def find_address(self, data: str, is_max_address=None, ignore_special_characters=True) -> list:
        """查找地址

        :param data: 查找地址数据
        :param is_max_address: 是否查找最长地址
        :param ignore_special_characters: 是否去掉特殊字符
        :return: 地址列表
        """
        is_max_address = self.is_max_address if is_max_address is None else is_max_address
        if ignore_special_characters:
            data = re.sub(r"[!#$%&'()*+,-./:：，。？！；‘’、《》;<=>?@[\]^_`{|}~\s]", '', data)
        i, ls, length = 0, [], len(data)
        while i + 1 < length:
            width = self.max_address if length - i > self.max_address else (length - i)  # 补差位数
            for j in range(2, width + 1):  # 精准匹配
                n = data[i:i + j]
                value = self._bisect_right(self.address_data, n, 0, self.length_all)
                if isinstance(value, tuple):
                    flag = value[1]
                    index = data.find(flag, i)
                    i = index + len(flag)  # 跳过选择后的地址
                    ls.append(flag)
                    break
            else:  # 进行模糊匹配
                for j in range(2, width + 1):
                    n = data[i:i + j]
                    value = self._bisect_right(self.address_data, n, 0, self.length_all)
                    if isinstance(value, int):
                        v = self._vague(n)
                        if v:
                            index = data.find(v, i)
                            i = index + len(v)  # 跳过选择后的地址
                            ls.append(v)
                            break
                else:
                    i += 1
        if is_max_address:
            max_address = []
            match = re.sub('|'.join(ls), lambda x: '*' * len(x.group()), data)
            for addr in re.finditer(r'[*]+', match):
                max_address.append(data[addr.start():addr.end()])
            return max_address
        return ls

    def supplement_address(self, address_name, is_max_address=False, is_order=False, is_remove_subset=True):
        """补全地址

        输入零碎的地址信息。补全地址，比如输入：山西孝义,补全为：山西省-吕梁市-文水县-孝义镇

        当参数：is_max_address=False时。默认补全最短地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_max_address=True。补全最长地址。比如：山西孝义，补全为：山西省-吕梁市-文水县-孝义镇-孝义村委会

        当参数：is_order=False。补全的地址是无序的，比如：孝义山西，也能补全为：山西省-吕梁市-文水县-孝义镇
        当参数：is_order=True。补全的地址是有序的，比如：孝义山西，则补全不出。无法在孝义下面找到关于山西的地址字眼。

        :param address_name: 要补全的地址，比如：山西孝义
        :param is_max_address: 是否是最大补全地址，默认是否。
        :param is_order: 地址补全，是否遵守顺序。默认是：无序
        :param is_remove_subset: 是否移除地址中含有的地址子集，比如：[山西省-吕梁市,山西省,吕梁市]-->[山西省-吕梁市]
        """
        obj = max if is_max_address else min
        ls, finds_address = [], self.find_address(address_name, is_max_address=False)
        ls = [addr for address in finds_address for addr in self.Tree.search_tree_value(address)]
        match = list(filter(self.satisfy_filter(finds_address, is_order), ls))
        if match:
            ls = obj(match, key=lambda x: len(x))
        elif ls:
            temporary = []
            for temp in finds_address:
                temporary.append(obj(filter(lambda x: temp in x, ls), key=lambda x: len(x)))
            ls = temporary
        if is_remove_subset:
            return self.remove_subset(ls)
        return ls

    @staticmethod
    def remove_subset(ls: list) -> list:
        """去除列表中的子集

        比如：['aa','a','ab'] --> ['aa','ab']

        :param ls: 字符串列表
        :return: 返回去重后的结果
        """
        ls = sorted(ls, key=lambda x: len(x), reverse=True)
        total = []
        for subset in ls:
            if subset not in total:
                flag = True
                for word in total:
                    if subset in word:
                        flag = False
                        break
                if flag:
                    total.append(subset)
        return total

    @staticmethod
    def satisfy_filter(finds_address, is_order):
        """满足条件的过滤算法

        算法流程：满足每一个地址提取的实体
        """

        def _(x):
            order = []
            for address in finds_address:
                if address not in x:
                    return False
                else:
                    order.append(x.find(address))
            else:
                if is_order:
                    return True if order == list(sorted(order)) else False
                return True

        return _
