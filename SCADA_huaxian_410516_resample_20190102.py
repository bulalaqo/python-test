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
        本文采用先剔除不合格数据再求平均
        也可先求平均，再判断状态是否为整数比如可用状态1
    求完平均值开始：偏航位置取余mod
    
    '''
    df = pd.read_csv (file,header =0)
    df.index = pd.to_datetime (df[ 'WTUR.Tm.Rw.Dt' ])
    #df_head = df.head(1000)
    #df_head.to_csv (os.path.join (savepath, '103001-103001001-20180101-20180131-realData_extract_head.csv'), index=None)
    #del df 
    #df = df_head
    List_         = df.columns.values.tolist ()  # 获取原始表头名
    dflidartime   = df.iloc[ :, 0 ].resample ('10T', label='right').agg ([ 'max' ])  # 提取lidar每10min的最后一个时间戳，便于与lidar数据对时
    df_count_base = df.iloc[ :, 0 ].resample ('10T', label='right').agg ([ 'count' ])  # 统计源数据每个时间段内的数据个数
    
    # 数据剔除
    # 因为停机模式字改变了，数据需要分开处理
    df1 = df[df['WTUR.Tm.Rw.Dt']<'2019-08-17']
    df2 = df[df['WTUR.Tm.Rw.Dt']>'2019-08-18'] 
    df1=(df1[
      (df1['WTUR.TurSt.Rs.S']==5)  
    & (df1['WTUR.Other.Wn.I16.StopModeWord']==0) 
    & (df1['WTUR.Other.Rn.I16.HaveFault']==0)
    & (df1['WTUR.Other.Rn.I16.LimPow']==0)
    & (df1['WTUR.State.Rn.I8']==1)
    & (df1['WTUR.WSpd.Ra.F32']<=30) 
    & (df1['WTUR.PwrAt.Ra.F32.Side']<=2800)
    & (df1['WTPS.Ang.Ra.F32.blade1']<=40)][List_[1::]].astype('float')) # 提取正常发电状态数据 # 加载完注意是字符，转换为数值类型
    
    df2=(df2[
      (df2['WTUR.TurSt.Rs.S']==5)  
    & (df2['WTUR.Other.Wn.I16.StopModeWord']==81) 
    & (df2['WTUR.Other.Rn.I16.HaveFault']==0)
    & (df2['WTUR.Other.Rn.I16.LimPow']==0)
    & (df2['WTUR.State.Rn.I8']==1)
    & (df2['WTUR.WSpd.Ra.F32']<=30) 
    & (df2['WTUR.PwrAt.Ra.F32.Side']<=2800)
    & (df2['WTPS.Ang.Ra.F32.blade1']<=40)][List_[1::]].astype('float')) # 提取正常发电状态数据 # 加载完注意是字符，转换为数值类型
    df = df1.append(df2)
    df_count = df.iloc[ :, 0 ].resample ('10T', label='right').agg ([ 'count' ])  # 统计筛选后的每个时间段的个数
    
    # 
    
    
    
    
    
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
    

    
    #  求平均值
    df_mean  = df.resample('10T',label='right').mean()                 
    
    #  求10min的累计发电量
    
    # 取mod，真北方向转化到0-360
    list00 = []
    for i in df_meam['WYAW.Posi.Ra.F32.TrueNorth']:
        if (i>=360)|(i<0) :
            list00.append(i-(i//360)*360)      
        else: 
            list00.append(i)
    df_meam['WYAW.Posi.Ra.F32.TrueNorth_mod'] = list00    
    
    
    # 判定时间段内数据量是否充足，筛选后的数据占比90%以上，数据量大于定值（如7秒数据，源数据10min内有77个左右，筛选要求至少65个）
    df_mean  = df_mean[(df_count['count']>=Bin_amount) &(df_count['count']/df_count_base['count']>Bin_percent)]
                
    savepath = Mainpath+'_extract_'+Hz+'\\'+Mainpath.split ('\\')[-1]+WTGnum
    #print(savepath)
    savefilename = file.split ('\\')[ -1 ].replace ('.csv', '_extract'+Hz+'.csv')    
    if not os.path.exists (savepath):
        os.makedirs (savepath)
    df_mean.to_csv (os.path.join (savepath, savefilename))  
    del df    
    
    
# 0.基础信息
 # 需要调整参数
Bin_amount  = 40
Bin_percent = 0.90  # 可以保证每10min至少36个数据
#Mainpath     = r'D:\test\103001\test'  
Mainpath     = r'C:\test_biu\data\410526'                         # 目录到数据类型一级便可
WTGnums_ = [9]   # 需要提取数据的机组
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






