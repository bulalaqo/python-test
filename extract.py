# -*- coding: utf-8 -*-
#python35
"""
Created on Fri Oct 26 11:05:35 2018

@author: 32963

功能：根绝现场实际采集变量来在各机型保存实时量(1).xlsx中查询变量含义
"""

#1.xlrd主要是用来读取excel文件

import xlrd

workbook = xlrd.open_workbook(r'C:\test_biu\data\各机型保存实时量(1).xlsx')
sheet_names= workbook.sheet_names()
#sheet2 = workbook.sheet_by_name(sheet_names[0])
#rows = sheet2.row_values(3) # 获取第四行内容
#cols = sheet2.col_values(1) # 获取第二列内容

#2.打开一个csv文件在‘各机型保存实时量(1).xlsx’找到全部变量解释
import pandas as pd
import os,glob
 
excelFile = r'C:\test_biu\data\各机型保存实时量(1).xlsx'
sheet_name = sheet_names[0]
dffname=pd.read_excel(excelFile,sheet_name)
dfname = pd.DataFrame(dffname)

savepath_protocol = r'C:\test_biu\data'
savefilename_protocol = r'滑县变量协议.xlsx'
#excelFile1 = r'D:\test\huaxian\滑县提取变量列表.xlsx'
excelFile1 = r'C:\test_biu\data\滑县提取变量列表.xlsx'


WTGnums  = [(('0' + str(i)) if len(str(i))==1 else str(i)) for i in list(range(1,50))]
WTGnums_ = [5,6,8,9,25,26] #需要选定的机组
for WTGnum in WTGnums_:
    WTGnum = WTGnums[WTGnum-1]
    
    #filepath = r'D:\test\huaxian\滑县现场瞬态数据csv'+'\\'+WTGnum
    filepath = r'C:\test_biu\data\09.11-10.317s_csv'+'\\'+WTGnum
    print(filepath)
    F = glob.glob (os.path.join (filepath, r'*.csv'))
    for filepath in F:
        f = open(filepath)
        print (filepath)
        df = pd.read_csv (f,low_memory=False)
        
        #print(df.info())
        typess= df.dtypes

        
        
        #df = df.convert_objects(convert_numeric=True)
        
        #——————————————布尔数据转换————-——————————————————
        # 只使用以下转化代码只能处理整列全部为bool的数据
#        df['WTUR.Bool.Rd.b0.PowerFlag']      =df['WTUR.Bool.Rd.b0.PowerFlag'].astype('int')
#        df['WTUR.Bool.Rd.b0.ServiceFlag2']   =df['WTUR.Bool.Rd.b0.ServiceFlag2'].astype('int')
#        df['WTUR.Bool.Rd.b1.LimPowStopState']=df['WTUR.Bool.Rd.b1.LimPowStopState'].astype('int')
        
        tt = df['WTUR.Bool.Rd.b0.PowerFlag'].values.tolist()
        tt = list( map(lambda x:[x,'0'][x=='False'],tt))
        tt = list( map(lambda x:[x,'0'][x=='false'],tt))
        tt = list( map(lambda x:[x,'1'][x=='True'],tt))
        tt = list( map(lambda x:[x,'1'][x=='true'],tt))
        df['WTUR.Bool.Rd.b0.PowerFlag'] = tt
        
        tt = df['WTUR.Bool.Rd.b0.ServiceFlag2'].values.tolist()
        tt = list( map(lambda x:[x,'0'][x=='False'],tt))
        tt = list( map(lambda x:[x,'0'][x=='false'],tt))
        tt = list( map(lambda x:[x,'1'][x=='True'],tt))
        tt = list( map(lambda x:[x,'1'][x=='true'],tt))
        df['WTUR.Bool.Rd.b0.ServiceFlag2'] = tt
        
        tt = df['WTUR.Bool.Rd.b1.LimPowStopState'].values.tolist()
        tt = list( map(lambda x:[x,'0'][x=='False'],tt))
        tt = list( map(lambda x:[x,'0'][x=='false'],tt))
        tt = list( map(lambda x:[x,'1'][x=='True'],tt))
        tt = list( map(lambda x:[x,'1'][x=='true'],tt))
        df['WTUR.Bool.Rd.b1.LimPowStopState'] = tt
        
        
        #print(df.info())
        df['WTUR.Bool.Rd.b0.PowerFlag']      =df['WTUR.Bool.Rd.b0.PowerFlag'].astype('int')
        df['WTUR.Bool.Rd.b0.ServiceFlag2']   =df['WTUR.Bool.Rd.b0.ServiceFlag2'].astype('int')
        df['WTUR.Bool.Rd.b1.LimPowStopState']=df['WTUR.Bool.Rd.b1.LimPowStopState'].astype('int')
        typess= df.dtypes
        #——————————————布尔数据转换————-——————————————————
        # 将FASLE替换为：0，将TRUE替换为：1
#        df['WTUR.Bool.Rd.b0.PowerFlag']=df['WTUR.Bool.Rd.b0.PowerFlag'].astype(str)
#        df['WTUR.Bool.Rd.b0.ServiceFlag2']=df['WTUR.Bool.Rd.b0.ServiceFlag2'].astype(str)
#        df['WTUR.Bool.Rd.b1.LimPowStopState']=df['WTUR.Bool.Rd.b1.LimPowStopState'].astype(str)
#        print (df['WTUR.Bool.Rd.b0.PowerFlag'].dtypes)
#        
#        df['WTUR.Bool.Rd.b0.PowerFlag']=df['WTUR.Bool.Rd.b0.PowerFlag'].replace('False',0).astype(int)
#        df['WTUR.Bool.Rd.b0.ServiceFlag2']=df['WTUR.Bool.Rd.b0.ServiceFlag2'].replace('False',0).astype(int)
#        df['WTUR.Bool.Rd.b1.LimPowStopState']=df['WTUR.Bool.Rd.b1.LimPowStopState'].replace('False',0).astype(int)
#        df['WTUR.Bool.Rd.b0.PowerFlag']=df['WTUR.Bool.Rd.b0.PowerFlag'].replace('True',1).astype(int)
#        df['WTUR.Bool.Rd.b0.ServiceFlag2']=df['WTUR.Bool.Rd.b0.ServiceFlag2'].replace('True',1).astype(int)
#        df['WTUR.Bool.Rd.b1.LimPowStopState']=df['WTUR.Bool.Rd.b1.LimPowStopState'].replace('True',1).astype(int)         
#        print (df['WTUR.Bool.Rd.b0.PowerFlag'].dtypes)
    #    List_name = df.columns.values.tolist ()  # 获取原始表头名
    #    in_not= []
    #    for i,name in enumerate(List_name):
    #        list_1 =dfname.iecpath .tolist()
    #        if name in list_1:
    #            in_not.append(list_1.index(name))            
    #    DFsave = dff.ix[in_not, :]
    #    DFsave.to_excel (os.path.join (savepath_protocol, savefilename_protocol), index=None)
        
        print (df['WTUR.Bool.Rd.b0.PowerFlag'].dtypes)
        #3 编辑‘滑县提取变量列表.xlsx’读取需要提取变量
        savepath = '\\'.join (filepath.split ('\\')[ 0:-2 ]) + '\\'+WTGnum+'_extract'
        savefilename = filepath.split ('\\')[ -1 ].replace ('.csv', '_extract.csv')    
        if not os.path.exists (savepath):
            A = os.makedirs (savepath)
        dffname1=pd.read_excel(excelFile1)
        dfname1 = pd.DataFrame(dffname1)
        a = dfname1[(dfname1.extract==1)].index.tolist() 
        a1 = df.iloc[:,a]
        a1.to_csv (os.path.join (savepath, savefilename), index=None)