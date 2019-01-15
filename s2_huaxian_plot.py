# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:02:59 2019

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def df2groupby(df_refer):
    '''
    把df按照特定时间分组
    需要修改：WTUR.Tm.Rw.Dt，改为df的对应时序列
    '''
#    a1 = pd.date_range(start='20180301',end='20181010',freq='W').values
#    a2 = df_refer[a1[0]:a1[1]]
#    a3 = df_refer['20180301':'20180401']
    df_period = df_refer.to_period('W')
    df_period.reset_index( drop=False, inplace=True)
    df_period.rename(columns={"WTUR.Tm.Rw.Dt":"index1"}, inplace=True) 
    df_groupby = df_period.groupby("index1")
    return df_groupby

def df_dynamic_scatter(df_groupby,pngsavepath):
    '''
    按时序分批动态显示df_groupby
    '''
    import matplotlib.pyplot as plt
    
    fig,ax=plt.subplots()
    #设置画布大小 fig = plt.figure(figsize=(16, 16))
    
    x=pd.DataFrame()
    y=pd.DataFrame()
    
    for name, group in df_groupby:
        x=pd.concat([x,group['power']])
        y=pd.concat([y,group['rpm1' ]])
        ax.cla()
        ax.set_title("power-rpm1")
        ax.set_xlabel(name)
        ax.set_ylabel("rpm1")
        ax.set_xlim(0,2100)
        ax.set_ylim(-1,20)
        ax.grid(linestyle='-.')
        # 显示方式1：分批次显示
        ax.scatter(group['power'], group['rpm1'], s = 8,  color = 'b', alpha = 0.4,marker='+') 
        # 显示方式2：起始累计显示
        #ax.scatter(x, y, s = 8,  color = 'r', alpha = 0.4,marker='+')
#        ax.plot(y1,label='train')
#        ax.plot(y2,label='test')
        ax.legend(loc='best')
        plt.pause(0.5) 
    plt.close()
    
    
    # 保存分帧    
    for name, group in df_groupby:
        fig2,ax=plt.subplots()
        x=pd.concat([x,group['power']])
        y=pd.concat([y,group['rpm1' ]])
        ax.cla()
        
        ax.set_title("power-rpm1")
        ax.set_xlabel(name)
        ax.set_ylabel("rpm1")
        ax.set_xlim(0,2100)
        ax.set_ylim(-1,20)
        ax.grid(linestyle='-.')
        # 显示方式1：分批次显示
        ax.scatter(group['power'], group['rpm1'], s = 8,  color = 'b', alpha = 0.4,marker='+') 
        # 显示方式2：起始累计显示
        #ax.scatter(x, y, s = 8,  color = 'r', alpha = 0.4,marker='+')
#        ax.plot(y1,label='train')
#        ax.plot(y2,label='test')
        ax.legend(loc='best')

        plt.pause(0.5) 
        
        if not os.path.exists (pngsavepath):
            os.makedirs (pngsavepath)
        plt.show()
        plt.savefig(pngsavepath+'\\'+str(name).replace('/','_')+'.jpg',bbox_inches='tight',figsize=(20,16))
        
        plt.close()