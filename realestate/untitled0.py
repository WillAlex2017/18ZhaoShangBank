# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:21:59 2018

@author: willalex
"""

import pandas as pd

Xtest = pd.read_excel('X序列_test.xls')
Xtrain = pd.read_excel('X序列_train.xls')
Ytrain = pd.read_excel('Y序列_train.xls')
IronXtrain = pd.read_excel('钢铁X_train.xlsx')
Irontest = pd.read_excel('钢铁数据_test.xlsx')
sample = pd.read_csv('submit_sample.txt')

