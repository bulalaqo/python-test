# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:08:04 2018

@author: 32963

function: 筛选scada7秒数据并且转换为10min频率

使用说明：需要查看具体的变量协议，来修来、确定最终的筛选标准
"""

import pandas as pd
import os,glob





def data_resample(file,WTGnum):
    '''
    数据筛选和预处理：
        数据剔除
        真北标定

    求10min平均值：
        本文采用先求平均，再判断状态是否为整数比如可用状态1
        也可先剔除不合格数据再求平均
        
    求完平均值开始：偏航位置取余mod
    
    '''
    df = pd.read_csv (f,header =0)
    df.index = pd.to_datetime (df[ 'WTUR.Tm.Rw.Dt' ])
    
    ####  转换下数据 
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
    
    # 真北方向转换(增加一列)
    if WTGnum=='005':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-0.9928*df['WYAW.Posi.Ra.F32']+52.028).tolist()
    elif WTGnum=='006':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-0.9974*df['WYAW.Posi.Ra.F32']+56.01).tolist()
    elif WTGnum=='008':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-1.0098*df['WYAW.Posi.Ra.F32']+47.12).tolist()
    elif WTGnum=='009':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-1.0165*df['WYAW.Posi.Ra.F32']+109.35).tolist()
    elif WTGnum=='025':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-1.0066*df['WYAW.Posi.Ra.F32']+49.5).tolist()
    elif WTGnum=='026':
        df['WYAW.Posi.Ra.F32.TrueNorth'] = (-1.0075*df['WYAW.Posi.Ra.F32']+28.931).tolist()
    

    
    # 求10min内的时间戳最大最小值
    df_TotEgmax  = df[['WTUR.TotEgyAt.Wt.F32']].resample ('10T', label='right').agg ([ 'max' ])  
    df_TotEgmin  = df[['WTUR.TotEgyAt.Wt.F32']].resample ('10T', label='right').agg ([ 'min' ])  

    
    # 求10min均值
    df_meam  = df.resample ('10T', label='right').mean()
    #df_meam  = df.resample ('10T', label='right').agg(['mean'])  #千万注意agg的作用相当于把列表名增加了一列，(WTUR.TotEgyAt.Wt.F32.1,mean)，尽量不要使用这种聚合agg，免得引用时麻烦
    #
    bb =(df['WTUR.TurSt.Rs.S'].resample ('10T', label='right').agg(['count']))
    aa=bb.reset_index(drop=True)['count'].values.tolist()
    df_meam['count'] =aa
    #
    ###df_meam['count'] =df['WTUR.TurSt.Rs.S'].resample ('10T', label='right').agg(['count'])# 少了['count'].values.tolist() 依旧是series，导致df_meam['count']列有问题
    df_meam['TotEgy10min'] =  (df_TotEgmax['WTUR.TotEgyAt.Wt.F32']['max']-df_TotEgmin['WTUR.TotEgyAt.Wt.F32']['min']).values.tolist()

    #  统计
    df_meam_min =df['WTUR.TurSt.Rs.S'].resample ('10T', label='left').agg(['count'])
    www1 =df_meam_min.index.tolist()
    www2 =df_meam.index.tolist()
    
    df_10min_TWGstatus = []  # 统计机组10min可用状态个数
    for i  in range(len(df_meam_min)):
        df_10min_TWGstatus.append (df[(df['WTUR.Tm.Rw.Dt']>str(www1[i]))&(df['WTUR.Tm.Rw.Dt']<=str(www2[i]))&(df['WTUR.TurSt.Rs.S']==5)]['WTUR.TurSt.Rs.S'].count())
        
        
    df_10min_DATAstatus = [] # 统计数据10min可用状态个数
    for i  in range(len(df_meam_min)):
        df_10min_DATAstatus.append (df[(df['WTUR.Tm.Rw.Dt']>str(www1[i]))&(df['WTUR.Tm.Rw.Dt']<=str(www2[i]))&(df['WTUR.State.Rn.I8']==1)]['WTUR.State.Rn.I8'].count())
        
    df_meam['countTWGstatus']  =df_10min_TWGstatus
    df_meam['countDATAstatus'] =df_10min_DATAstatus
    
    # 取mod，真北方向转化到0-360
    list00 = []
    for i in df_meam['WYAW.Posi.Ra.F32.TrueNorth']:
        if (i>=360)|(i<0) :
            list00.append(i-(i//360)*360)      
        else: 
            list00.append(i)
    df_meam['WYAW.Posi.Ra.F32.TrueNorth_mod'] = list00    


                 
    savepath = Mainpath+'_extract_'+Hz+'\\'+Mainpath.split ('\\')[-1]+WTGnum
    #print(savepath)
    savefilename = file.split ('\\')[ -1 ].replace ('.csv', '_extract'+Hz+'.csv')    
    if not os.path.exists (savepath):
        os.makedirs (savepath)
    df_meam.to_csv (os.path.join (savepath, savefilename))  
    del df    
    
    
# 0.基础信息
 # 需要调整参数
Bin_amount  = 40
Bin_percent = 0.90  # 可以保证每10min至少36个数据
#Mainpath     = r'D:\test\103001\test'  
Mainpath     = r'C:\test_biu\data\410526'                         # 目录到数据类型一级便可
WTGnums_ = [5,6,8,9,25,26]   # 需要提取数据的机组
Hz       = '10min'      # 提取的数据频率
 # 无需调整参数
WTGnums  = [(('00' + str(i)) if len(str(i))==1 else ('0'+str(i))) for i in list(range(1,100))] # 小于99台都可用,此行不需要修改





# 1.数据筛选
for WTGnum in WTGnums_:
    WTGnum = WTGnums[WTGnum-1]
    filepath = '\\'.join ([Mainpath,Mainpath.split ('\\')[-1]+WTGnum])

    F = glob.glob (os.path.join (filepath, r'*.csv'))
    for f in F:
        try:
            data_resample(f,WTGnum)
        except:
            
            continue
        
        
#        if WTGnum=='005':
#            break    
#    if WTGnum=='005':
#        break






