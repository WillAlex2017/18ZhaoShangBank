# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:05:27 2018

@author: willalex
"""

import pandas as pd
import numpy as np

test1 = pd.read_csv('test_input.txt', sep=',', nrows = 180000, header = None, names = ['UserID', 'Bal', 'Date', 'Balance']) 
test2 = pd.read_csv('test_input.txt', sep=',', skiprows = 180000, header = None , 
                    names =['UserID', 'Trx', 'CardID', 'Date', '2GAbstract', 'TranscationName', 'Classify', 'Amount'])
#处理错位问题，处理的方法不是很好，以后还得学习
test2.loc[ test2['Amount'].isnull(), 'Amount'] = test2['Classify']
test2.loc[ test2['Amount'] == test2['Classify'], 'Classify' ] = test2['TranscationName']
test2.loc[ test2['Classify'] == test2['TranscationName'], 'TranscationName'] = None
test2['Amount'] = test2['Amount'].astype(float)

train1 = pd.read_csv('train.txt', sep=',', nrows = 3638790, header = None, names = ['UserID', 'Bal', 'Date', 'Balance'])
train2 =pd.read_csv('train.txt', sep=',', skiprows = 3638790, header = None, 
                     names =['UserID', 'Trx', 'CardID', 'Date', '2GAbstract', 'TranscationName', 'Classify', 'Amount'])

train2.loc[ train2['Amount'].isnull(), 'Amount'] = train2['Classify']
train2.loc[ train2['Amount'] == train2['Classify'], 'Classify' ] = train2['TranscationName']
train2.loc[ train2['Classify'] == train2['TranscationName'], 'TranscationName'] = None
train2['Amount'] = test2['Amount'].astype(float)

#Merge
testdata = pd.merge(test1, test2, how = 'left', on = ['UserID', 'Date'], suffixes = ['_bal', '_trx'])
traindata = pd.merge(train1, train2, how = 'left', on = ['UserID', 'Date'])

#取出最后一天
newdf = test1.groupby('UserID')
newdf2 = newdf['Date'].max()
#sortedbyBalance = grouped['Date']

newddf = pd.DataFrame({'UserID': newdf2.index, 'Date':newdf2.values})
newddf.drop(3000, inplace = True)

temp = pd.merge(test1, newddf, how = 'inner', on = ['UserID', 'Date'])
temp['Date'] = temp['Date'] + 7

#submission
temp.to_csv('demo.txt',sep = ',',index = False, header = False)
