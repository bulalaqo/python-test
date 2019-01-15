# -*- coding: utf-8 -*-
# python3
"""
Created on Wed Sep 19 13:44:14 2018

@author: 32963
"""

import pandas as pd
import sqlite3 as db
import os
import glob
import zipfile


##############################定义基本函数
# arc 解压为data文件，即db
def arc2data(filename):
    '''
    filename=r'E:\AAAAA所有算法开发测试完成归档\python脚本保存\datafile\real_410526001_20180301.arc'

    :param filename:
    :return:
    '''
    filepath = os.path.dirname (filename)
    f = filename.split ('\\')[ -1 ]
    #print (f)
    # 现场7s文件解压缩成DB文件，arc文件解压成data文件，即db文件。
    try:
        z = zipfile.ZipFile (filename, 'r')
        z.extract (f.replace ('.arc', '.data'), filepath)
        z.close ()
    except:
        pass


##############################

#0.基本信息
#main_path=linux重启命令r'A:\PowerPrediction\滑县现场瞬态数据'
main_path=r'C:\test_biu\data\09.11-10.317s'

main_path_list=os.listdir(main_path)
save_path = r'C:\test_biu\data\09.11-10.317s_csv'
NeedCrewNoSwitch = 1 # 为1时，可以选择需要转换的机组
#NeedCrewNo = ['05','06','08','09','25','26']  # 选择需要转换的机组
NeedCrewNo = ['05','06','08','09','25','26']  # 选择需要转换的机组

#1.批量装换
for ML in main_path_list:
    print('正在转换'+ML+'文件夹的arc.....')
    arcfiles  = glob.glob (os.path.join (main_path, ML,r'*.arc'))
    
    for arcfile in arcfiles:
        try:
            CrewNo = arcfile.split ('\\')[-1].split ('_')[-2][-2:]
            if (NeedCrewNoSwitch == 1)& (CrewNo not in NeedCrewNo) :
                continue
                
            # 读arc文件 
            arc2data(arcfile)
            dbfile = arcfile.replace ('.arc', '.data') 
            conn = db.connect (dbfile)
            cursor = conn.cursor()
            #加载全部DB或者ARC数据为DataFrame文件
            sql2 = 'select * from realtimedata'                  
            df = pd.read_sql (sql2, conn)
            List_ = df.columns.values.tolist ()  # 获取原始表头名
            df.index = pd.to_datetime (df[ 'WTUR.Tm.Rw.Dt' ])
            #print (df[:10])
            conn.close() # 关闭数据库
    
    
            if not os.path.exists(save_path+'/'+CrewNo):         
                os.makedirs(save_path+'/'+CrewNo)
            df.to_csv (save_path+'/'+CrewNo+'/'+arcfile.split ('\\')[-1].replace ('.arc', '.csv'), index=None)
            #os.remove(dbfile)
            #os.remove(arcfile)
        except:
            continue
#    ttt = 1
#    if ttt==1:
#        break