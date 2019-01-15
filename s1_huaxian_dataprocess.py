# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 01:16:13 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
import pandas as pd
import os,glob


# 0.基础信息
 # 需要调整参数

Mainpath = r'C:\test_biu\data\410526_extract_10min'
windfarmId = '410526'   # 目录到数据类型一级便可
WTGnums_ = [5,6,8,9,25,26]   # 需要提取数据的机组
Hz       = '10min'      # 提取的数据频率
 # 无需调整参数
WTGnums  = [(('00' + str(i)) if len(str(i))==1 else ('0'+str(i))) for i in list(range(1,100))] # 小于99台都可用,此行不需要修改




# 1.数据整合
def df_10min_merge(Mainpath,windfarmId):
    '''
    把每天的10min数据整合为一个文件，方便下次加载
    '''
    df = pd.DataFrame()
    for WTGnum in WTGnums_:
        WTGnum = WTGnums[WTGnum-1]
        filepath = '\\'.join ([Mainpath,windfarmId+WTGnum])
    
        F = glob.glob (os.path.join (filepath, r'*.csv'))
        for f in F:
            df_ = pd.read_csv (f,header =0)
            df_.index = pd.to_datetime (df_[ 'WTUR.Tm.Rw.Dt' ])
            df = df_.append(df)
        exec('df'+WTGnum+'=df')
        df.to_csv (os.path.join ('df'+windfarmId+WTGnum+'.csv'))
        del df,df_
        df = pd.DataFrame()


# 2.数据筛选清洗
def df_pro(df,WTGnum):
    '''
    根据可用状态筛选提取数据
    '''
    ## 2.1 可用状态删除
    #WTUR.TurSt.Rs.S;              % ==5 正常发电
    #WTUR.Other.Rn.I16.HaveFault;  % ==0无故障
    #WTUR.Other.Rn.I16.LimPow;     % ==0不限功率
    #WTUR.State.Rn.I8;             % 数据可用状态 ==1
    #WTUR.Bool.Rd.b0.ServiceFlag2; % 维护状态     ==0时未维护
    #WTUR.Other.Wn.I16.StopModeWord ; % 停机状态 ==0时未停机
    #WTUR.Flt.Ri.I32.main;             % 主故障   ==0时无主故障
    df_1 = df[  (df['WTUR.TurSt.Rs.S']==5)
                 & (df['WTUR.Other.Rn.I16.HaveFault']==0)
                 & (df['WTUR.Other.Rn.I16.LimPow']==0)
                 & (df['WTUR.State.Rn.I8']==1)
                 & (df['WTUR.Bool.Rd.b0.ServiceFlag2']==0)
                 & (df['WTUR.Other.Wn.I16.StopModeWord']==0)
                 & (df['WTUR.Flt.Ri.I32.main']==0)]
        
    ## 2.2 扇区剔除
    sectors = [[144.6183, 259.3514, 325.7958, 79.1512],
               [145.7958, 259.2750, 325.3405, 79.3513],
               [145.3388, 259.6656, 324.6204, 78.5876],
               [144.6204, 261.5864, 323.8623, 79.6656],
               [135.4961, 247.9015, 316.2804, 67.8376],
               [131.9256, 248.6354, 314.6983, 70.2624]]   
    
    if   WTGnum == '005':
        sector1 = sectors[0]
    elif WTGnum == '006':
        sector1 = sectors[1]
    elif WTGnum == '008':
        sector1 = sectors[2]
    elif WTGnum == '009':
        sector1 = sectors[3]
    elif WTGnum == '025':
        sector1 = sectors[4]
    elif WTGnum == '026':
        sector1 = sectors[5]    
    df_2 = df_1[((df_1['WYAW.Posi.Ra.F32.TrueNorth_mod']>sector1[0]) & (df_1['WYAW.Posi.Ra.F32.TrueNorth_mod']<sector1[1])) 
                |(df_1['WYAW.Posi.Ra.F32.TrueNorth_mod']>sector1[2])
                |(df_1['WYAW.Posi.Ra.F32.TrueNorth_mod']<sector1[3])]
    return df_2
  

## 2.3 对时选取数据
def readin_10min(f1,f2,num1,num2):
    '''
    加载已经真合并的10min文件
    '''
#    f1 =r'C:\test_biu\data\df410526005.csv'
#    f2 =r'C:\test_biu\data\df410526008.csv'
#    num1 = '005'
#    num2 = '008'
    df005  =   pd.read_csv (f1,header =0) 
    df008  =   pd.read_csv (f2,header =0)
    df005.index = pd.to_datetime (df005[ 'WTUR.Tm.Rw.Dt' ])
    df008.index = pd.to_datetime (df008[ 'WTUR.Tm.Rw.Dt' ])
    
    df005_1 =  df_pro(df005,num1)   
    df008_1 =  df_pro(df008,num2) 
    
    a05 = df005_1['WTUR.Tm.Rw.Dt'].tolist()
    a08 = df008_1['WTUR.Tm.Rw.Dt'].tolist()
    
    a05_a08 =   list(set(a05)  & set(a08))
    
    flag1 = df005_1['WTUR.Tm.Rw.Dt'].isin(a05_a08)
    flag2 = df008_1['WTUR.Tm.Rw.Dt'].isin(a05_a08)
    
    df005_3 = df005_1[flag1]  
    df008_3 = df008_1[flag2]
    return df005_3,df008_3
