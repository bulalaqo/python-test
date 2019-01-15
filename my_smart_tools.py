# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 02:19:03 2019

@author: Administrator

常用小工具汇总
"""

def codes_copy_err_correct(file):
    '''
    小工具，网页拷贝代码时有时会出现缩进问题。直接拷贝代码时容易出现问题，删除一些不规则字符
    '''
    file =r'test2.py'
    f = open(file)
    lines =f.readlines()
    lines_new = [i.replace('聽 聽 ','\t').replace('聽',' ') for i in lines]
    f1 = open('codes_copy_err_correct.py','w')
    for i in lines_new:
        f1.write(i)