# -*- coding: utf-8 -*-
import pandas as pd
import os,glob

import numpy as np

from s1_huaxian_dataprocess import *
from s2_huaxian_plot import *
from my_plot import *

## 3.2 可视数据准备

f1 =r'C:\test_biu\data\df410526005.csv'  #优化组
f2 =r'C:\test_biu\data\df410526008.csv'  #对照组
df005_3,df008_3 =readin_10min(f1,f2,'005','008')
y_data_names = ['8#','5#']

## 提取需要变量
def extract_df(df005_3):
    df_refer = pd.DataFrame()
    df_refer['DateTime'] =  df005_3['WTUR.Tm.Rw.Dt']
    df_refer['power']     =  df005_3['WTUR.PwrAt.Ra.F32.Side']
    df_refer['rpm1']     =  df005_3['WGEN.Spd.Ra.F32.overspblade2']
    df_refer['pitch1']   =  df005_3['WTPS.Ang.Ra.F32.blade1']
    df_refer['temperature']   =  df005_3['WTUR.Temp.Ra.F32']
    df_refer['wd']       =  df005_3['WYAW.Posi.Ra.F32.TrueNorth_mod']
    
    return df_refer
    
df_refer  = extract_df(df008_3)   
df_test   = extract_df(df005_3)



train_time1 = '2018-05-01 00:10:00' # '2018-2-01 00:10:00'#注意日期全部两位不足补零
train_time2 = '2018-10-15 00:10:00' 
test_time1  = '2018-10-16 00:10:00' 
test_time2  = '2018-12-26 00:10:00' 
df_refer_train = df_refer[(df_refer['DateTime']>train_time1)  &(df_refer['DateTime']<train_time2)]
df_test_train  = df_test[(df_test['DateTime']  >train_time1)  &(df_test['DateTime'] <train_time2)]
df_refer_test = df_refer[(df_refer['DateTime'] >test_time1)   &(df_refer['DateTime']<test_time2)]
df_test_test  = df_test[(df_test['DateTime']   >test_time1)   &(df_test['DateTime'] <test_time2)]


sum_r_1= df_refer_train.power.sum()
sum_t_1= df_test_train.power.sum()
per1 = sum_t_1/sum_r_1-1
sum_r_2= df_refer_test.power.sum()
sum_t_2= df_test_test.power.sum() 
per2 = sum_t_2/sum_r_2-1  
        


df_groupby=df2groupby(df_refer)
df_dynamic_scatter(df_groupby,'8#')
df_groupby=df2groupby(df_test)
#df_dynamic_scatter(df_groupby,'5#')


#x_data = [df_refer_train.power,df_refer_test.power]
#y_data = [df_refer_train.pitch1,df_refer_test.pitch1]
#y_data1 = [df_refer_train.rpm1,df_refer_test.rpm1]
#scatterplot_multi(x_data, y_data)
#scatterplot_multi(x_data, y_data1)



#x_data = [df_test_train.power,df_test_test.power]
#y_data = [df_test_train.pitch1,df_test_test.pitch1]
#y_data1 = [df_test_train.rpm1,df_test_test.rpm1]
#scatterplot_double(x_data, y_data)
#scatterplot_double(x_data, y_data1)



#
#df005_sum  = df005_3.resample ('m', label='right').sum()
#df008_sum  = df008_3.resample ('m', label='right').sum()
#df005_sum['WTUR.Tm.Rw.Dt'] = df005_sum.index
#df008_sum['WTUR.Tm.Rw.Dt'] = df008_sum.index
##    
#x_t =  df008_sum['WTUR.Tm.Rw.Dt']  
#y_t =  df005_sum['WTUR.Tm.Rw.Dt']
#x_data = df008_sum['TotEgy10min']
#y_data = df005_sum['TotEgy10min']
#
#
#
##stackedbarplot(x_t,[x_data,y_data],colors = ['b','r'])
##
#y_x_data = (y_data-x_data)/x_data
##
#colors = ['b','r']
#groupedbarplot(x_t,[x_data,y_data],colors,y_data_names)
#barplot(x_t,y_x_data)