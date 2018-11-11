# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:09:28 2018

@author: willalex
"""
import heapq
import pandas as pd
#sample = pd.read_table('sample.txt',sep = '\t', header = None, error_bad_lines= False) 
#Skipping line 4: expected 2 fields, saw 21\n' No use
rowname = ['date', 'abstract', 'lendingcode', 'moneycode', 'AmountTransaction', 'balance', 'customID']
train_dataset = pd.read_csv('train_dataset.txt', sep = '\t') #2349384
train_dataset.columns = rowname
descriptein = train_dataset.describe()

Americandata = train_dataset[ train_dataset['moneycode'] == 32] #2187430
lendingcodeC = Americandata [Americandata ['lendingcode'] == 'C'] #864593
lendingcodeD = Americandata [Americandata ['lendingcode'] == 'D'] #1322837

# lendingcodeC['abstract'].unique() 24
# array(['SSWA', 'ISIR', 'FFM2', 'GALO', 'DPBC', 'DPBF', 'SSW5', 'FFT2',
#       'DPBD', 'IINT', '8001', 'SSW8', 'ISFT', 'SSW6', 'EXME', 'FEZZ',
#       'ONFC', 'TRRA', 'AGRD', 'EXVF', 'FFS2', 'EXVN', 'FEEE', '8003'], dtype=object)

#lendingcodeD['abstract'].unique()  25
#array(['QRTA', 'FEZZ', 'SSWA', 'FENC', 'FEZ1', 'FEIS', 'FFM2', 'ISCP',
#       'GALO', '8001', 'DPBC', 'AGPY', 'SSW5', 'DPBD', 'ISOR', 'ISIR',
#       'FFT2', 'DPBF', 'SSW8', 'SSW6', 'FEEE', 'FFS2', 'ACTF', 'ONFC',
#       'IINT'], dtype=object)

ISIRdata = lendingcodeC[ lendingcodeC['abstract'] == 'ISIR'] #750671
QRTAdata = lendingcodeD[ lendingcodeD['abstract'] == "QRTA"] #601691

#ISIRave = len(ISIRdata) / len(ISIRdata['date'].unique()) #360
ISIRave = len(ISIRdata) / 366 #按照一年来算，这样它的值会稍有减少,事实证明效果又好了一点点
QRTAave = len(QRTAdata) / len(QRTAdata['date'].unique()) #366

positivevalue = QRTAdata[ QRTAdata['AmountTransaction'] > 0]  #8993
# ISIRneg = ISIRdata[ ISIRdata['AmountTransaction'] < 0] 0, 这种数据才是正确数据

#QRTAaveamount = ( sum(QRTAdata['AmountTransaction']) - 2 * sum(positivevalue['AmountTransaction']) )  / len(QRTAdata['date'].unique())

QRTAaveamount = sum(QRTAdata['AmountTransaction']) / len(QRTAdata['date'].unique()) #这样效果更好，说明不用多此一举减去正数

# Top 20
grouped = Americandata.groupby(Americandata['customID']) #29399
sortedbyBalance = grouped['balance'].max()

df = pd.DataFrame({'customID':sortedbyBalance.index, 'maxbalance': sortedbyBalance.values})
dic = sortedbyBalance.to_dict()
Top20Dict = sorted(dic.items(), key=lambda item: item[1], reverse = True)
Top20Dict = Top20Dict[:20]
# 取键
keys =[]
for i in range(20):
    keys.append( Top20Dict[i][0])
#Top20 = heapq.nlargest(20, df['maxbalance'])
#Top20ID = df[ df['maxbalance'] in Top20]

result = pd.DataFrame({'QRTA': QRTAave, 
                       'ISIR': ISIRave,
                       'VOLUME': -QRTAaveamount,
                       'TOP20': keys})
dictresult = dict({'QRTA': QRTAave, 
                   'ISIR': ISIRave,
                   'VOLUME': -QRTAaveamount,
                   'TOP20': keys})


#Write to txt file
file=open('third.txt','w')
file.write('QRTA\t'+str(QRTAave))
file.write('\nISIR\t'+str(ISIRave))
file.write('\nVOLUME\t'+str(-QRTAaveamount))
file.write('\nTOP20')
for i in range(20):
    file.write('\t'+str(keys[i]))
file.close()


 












