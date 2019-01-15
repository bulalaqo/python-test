# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 01:42:11 2019

@author: Administrator
"""
import matplotlib.pyplot as plt
import numpy as np

###------------------------------------------静态图函数------------------------------------------
###-----------1.1 基本静态图---------
def scatterplot(x_data, y_data, x_label="", y_label="", title="", color = "r", yscale_log=False):  
    # 散点图
    # Create the plot object  
    _, ax = plt.subplots()    # Plot the data, set the size (s), color and transparency (alpha)  
    # of the points  
    ax.scatter(x_data, y_data, s = 10, color = color, alpha = 0.75)    
    if yscale_log == True:  
        ax.set_yscale('log')    # Label the axes and provide a title  
        ax.set_title(title)  
        ax.set_xlabel(x_label)  
        ax.set_ylabel(y_label)

def lineplot(x_data, y_data, x_label="", y_label="", title=""):  
    # Create the plot object  
    _, ax = plt.subplots()    # Plot the best fit line, set the linewidth (lw), color and  
    # transparency (alpha) of the line  
    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)    # Label the axes and provide a title  
    ax.set_title(title)  
    ax.set_xlabel(x_label)  
    ax.set_ylabel(y_label)   

def histogram(data, n_bins, cumulative=False, x_label = "", y_label = "", title = ""):  
    _, ax = plt.subplots()  
    ax.hist(data, n_bins = n_bins, cumulative = cumulative, color = '#539caf')  
    ax.set_ylabel(y_label)  
    ax.set_xlabel(x_label)  
    ax.set_title(title) 

# Overlay 2 histograms to compare them
def overlaid_histogram(data1, data2, n_bins = 0, data1_name="", data1_color="#539caf", data2_name="", data2_color="#7663b0", x_label="", y_label="", title=""):  
    # Set the bounds for the bins so that the two distributions are fairly compared  
    max_nbins = 10  
    data_range = [min(min(data1), min(data2)), max(max(data1), max(data2))]  
    binwidth = (data_range[1] - data_range[0]) / max_nbins    
    if n_bins == 0:  
        bins = np.arange(data_range[0], data_range[1] + binwidth, binwidth)    
    else:   
        bins = n_bins    # Create the plot  
    _, ax = plt.subplots()  
    ax.hist(data1, bins = bins, color = data1_color, alpha = 1, label = data1_name)  
    ax.hist(data2, bins = bins, color = data2_color, alpha = 0.75, label = data2_name)  
    ax.set_ylabel(y_label)  
    ax.set_xlabel(x_label)  
    ax.set_title(title)  
    ax.legend(loc = 'best')     

def barplot(x_data, y_data, x_label="", y_label="", title=""):
#def barplot(x_data, y_data, error_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()
    # Draw bars, position them in the center of the tick mark on the x-axis
    ax.bar(x_data, y_data, color = '#539caf', align = 'center')
    # Draw error bars to show standard deviation, set ls to 'none'
    # to remove line between points
    #ax.bar(x_data, y_data, color = '#297083', ls = 'none', lw = 2, capthick = 2)
    #ax.errorbar(x_data, y_data, yerr = error_data, color = '#297083', ls = 'none', lw = 2, capthick = 2)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.xticks(rotation=20)
    
def stackedbarplot(x_data, y_data_list, colors, y_data_names="", x_label="", y_label="", title=""):
    _, ax = plt.subplots()
    # Draw bars, one category at a time
    print(len(y_data_list))
    for i in range(0, len(y_data_list)):
        if i == 0:
            ax.bar(x_data, y_data_list[i], color = colors[i], align = 'center', label = y_data_names[i])
        else:
            # For each category after the first, the bottom of the
            # bar will be the top of the last category
            ax.bar(x_data, y_data_list[i], color = colors[i], bottom = y_data_list[i - 1], align = 'center', label = y_data_names[i])
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(loc = 'upper right')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % float(height))
def autolabel_percent(rects,rects1):
    for rect,rect1 in zip(rects,rects1):
        
        height = rect.get_height()
        height1 = rect1.get_height()
        height0 = max(height,height1)
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height0, '%s%%' % round((height1/height-1)*100,2))

        
def groupedbarplot(x_data, y_data_list, colors, y_data_names="", x_label="", y_label="", title=""):
    _, ax = plt.subplots()
    ind = np.arange(len(x_data))  # the x locations for the groups
    # Total width for all bars at one x location
    total_width = 0.8
    # Width of each individual bar
    ind_width = total_width / len(y_data_list)
    # This centers each cluster of bars about the x tick mark
    alteration = np.arange(-(total_width/2), total_width/2, ind_width)

    # Draw bars, one category at a time
    ax_=[[],[]]
    for i in range(0, len(y_data_list)):
        # Move the bar to the right on the x-axis so it doesn't
        # overlap with previously drawn ones
        ax_[i] = ax.bar(ind  + alteration[i], y_data_list[i], color = colors[i], label = y_data_names[i], width = ind_width)
    
    autolabel_percent(ax_[0],ax_[1])
    plt.xticks(ind,x_data)
    plt.xticks(rotation=45)
    
    
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(loc = 'upper right')    

def boxplot(x_data, y_data, base_color="#539caf", median_color="#297083", x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    # Draw boxplots, specifying desired style
    ax.boxplot(y_data
               # patch_artist must be True to control box fill
               , patch_artist = True
               # Properties of median line
               , medianprops = {'color': median_color}
               # Properties of box
               , boxprops = {'color': base_color, 'facecolor': base_color}
               # Properties of whiskers
               , whiskerprops = {'color': base_color}
               # Properties of whisker caps
               , capprops = {'color': base_color})

    # By default, the tick label starts at 1 and increments by 1 for
    # each box drawn. This sets the labels to the ones we want
    ax.set_xticklabels(x_data)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)

###-----------1.2 升级静态图---------
def scatterplot_multi(x_data, y_data, x_label="", y_label="", title="", color = ["r",'b','y'],marker=['+','.','0'], yscale_log=False):  
    # 多组散点合并
    # Create the plot object  
    _, ax = plt.subplots()    # Plot the data, set the size (s), color and transparency (alpha)  
    # of the points
    plt.grid()
    for i in range(len(x_data)): 
        ax.scatter(x_data[i], y_data[i], s = 8,  color = color[i], alpha = 0.4,marker=marker[i]) 
    ax.set_yscale('log')    # Label the axes and provide a title  
    ax.set_title(title)  
    ax.set_xlabel(x_label)  
    ax.set_ylabel(y_label)
    
    
###------------------------------------------动态图函数------------------------------------------

###-----------1.1 基本动态图---------
###示例 1-------------------------------------
def dynamic_plot():
    '''
    放在函数中调用函数，动态图无法达到动态效果
    '''
    from matplotlib.animation import FuncAnimation  # 动图的核心函数
    import seaborn as sns  # 美化图形的一个绘图包
    sns.set_style("whitegrid")  # 设置图形主图
    # 创建画布
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    
    # 画出一个维持不变（不会被重画）的散点图和一开始的那条直线。
    x = np.arange(0, 20, 0.1)
    y = x + np.random.normal(0, 3.0, len(x))
    ax.scatter(x, y)
    line, = ax.plot(x, x - 5, 'r-', linewidth=2)
    #plt.savefig('fig.png',bbox_inches='tight')
    
    
    def update(i):
        label = 'timestep {0}'.format(i)
        print(label)
        # 更新直线和x轴（用一个新的x轴的标签）。
        # 用元组（Tuple）的形式返回在这一帧要被重新绘图的物体
        line.set_ydata(x - 5 + i)  # 这里是重点，更新y轴的数据
        #ax.set_xlabel(label)    # 这里是重点，更新x轴的标签
    
        return line, ax
    
    # FuncAnimation 会在每一帧都调用“update” 函数。
    # 在这里设置一个10帧的动画，每帧之间间隔200毫秒
    anim = FuncAnimation(fig, update, frames=np.arange(0, 10), interval=200)

###示例 2-------------------------------------
'''   
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import seaborn as sns
sns.set_style("whitegrid")


def randn_point():
    # 产生随机散点图的x和y数据
    x=np.random.randint(1,100,3)
    y=np.random.randint(1,2,3)
    return x,y

# 创建画布，包含2个子图
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

# 先绘制初始图形，每个子图包含1个正弦波和三个点的散点图
x = np.arange(0, 2*np.pi, 0.01)

line1, = ax1.plot(x, np.sin(x)) # 正弦波
x1,y1=randn_point()
sca1 = ax1.scatter(x1,y1)   # 散点图

line2, = ax2.plot(x, np.cos(x))  # 余弦波
x2,y2=randn_point()
sca2 = ax2.scatter(x2,y2)   # 散点图

def init():
    # 构造开始帧函数init
    # 改变y轴数据，x轴不需要改
    line1.set_ydata(np.sin(x))
    line1.set_ydata(np.cos(x))
    # 改变散点图数据
    x1, y1 = randn_point()
    x2, y2 = randn_point()
    data1 = [[x,y] for x,y in zip(x1,y1)]
    data2 = [[x,y] for x,y in zip(x2,y2)]
    sca1.set_offsets(data1)  # 散点图
    sca2.set_offsets(data2)  # 散点图
    label = 'timestep {0}'.format(0)
    ax1.set_xlabel(label)
    return line1,line2,sca1,sca2,ax1  # 注意返回值，我们要更新的就是这些数据

def animate(i):
    # 接着，构造自定义动画函数animate，用来更新每一帧上各个x对应的y坐标值，参数表示第i帧
    # plt.cla() 这个函数很有用，先记着它
    line1.set_ydata(np.sin(x + i/10.0))
    line2.set_ydata(np.cos(x + i/10.0))
    x1, y1 = randn_point()
    x2, y2 = randn_point()
    data1 = [[x,y] for x,y in zip(x1,y1)]
    data2 = [[x,y] for x,y in zip(x2,y2)]
    sca1.set_offsets(data1)  # 散点图
    sca2.set_offsets(data2)  # 散点图
    label = 'timestep {0}'.format(i)
    ax1.set_xlabel(label)
    return line1,line2,sca1,sca2,ax1


# 接下来，我们调用FuncAnimation函数生成动画。参数说明：
# fig 进行动画绘制的figure
# func 自定义动画函数，即传入刚定义的函数animate
# frames 动画长度，一次循环包含的帧数
# init_func 自定义开始帧，即传入刚定义的函数init
# interval 更新频率，以ms计
# blit 选择更新所有点，还是仅更新产生变化的点。应选择True，但mac用户请选择False，否则无法显示动画

ani = FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              init_func=init,
                              interval=200,
                              blit=False)
plt.show()

'''

###示例 3-------------------------------------
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
class AnimatedScatter(object):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	def __init__(self, numpoints=50):
		self.numpoints = numpoints
		self.stream = self.data_stream()
 
 
		# Setup the figure and axes...
		self.fig, self.ax = plt.subplots()
		# Then setup FuncAnimation.
		self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
										   init_func=self.setup_plot, blit=True)
 
 
	def setup_plot(self):
		"""Initial drawing of the scatter plot."""
		x, y, s, c = next(self.stream)
		self.scat = self.ax.scatter(x, y, c=c, s=s, animated=True)
		self.ax.axis([-10, 10, -10, 10])
 
 
		# For FuncAnimation's sake, we need to return the artist we'll be using
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,
 
 
	def data_stream(self):
		"""Generate a random walk (brownian motion). Data is scaled to produce
		a soft "flickering" effect."""
		data = np.random.random((4, self.numpoints))
		xy = data[:2, :]
		s, c = data[2:, :]
		xy -= 0.5
		xy *= 10
		while True:
			xy += 0.03 * (np.random.random((2, self.numpoints)) - 0.5)
			s += 0.05 * (np.random.random(self.numpoints) - 0.5)
			c += 0.02 * (np.random.random(self.numpoints) - 0.5)
			yield data
 
 
	def update(self, i):
		"""Update the scatter plot."""
		data = next(self.stream)
 
 
		# Set x and y data...
		self.scat.set_offsets(data[:2, :])
		# Set sizes...
		self.scat._sizes = 300 * abs(data[2])**1.5 + 100
		# Set colors..
		self.scat.set_array(data[3])
 
 
		# We need to return the updated artist for FuncAnimation to draw..
		# Note that it expects a sequence of artists, thus the trailing comma.
    
		return self.scat,
 
 
	def show(self):
		plt.show()
 
'''
if __name__ == '__main__':
	a = AnimatedScatter()
	a.show()
'''    

###-----------1.2 升级动态图---------
###示例 1------------------------------------- 
"""
import pandas as pd
import matplotlib.pyplot as plt

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

def df_dynamic_scatter(df_groupby):
    '''
    按时序分批动态显示df_groupby
    '''
    import matplotlib.pyplot as plt

    
    fig,ax=plt.subplots()
    fig2,ax2=plt.subplots()
    
    
    x=pd.DataFrame()
    y=pd.DataFrame()
    
    for name, group in df_groupby:
        x=pd.concat([x,group['power']])
        y=pd.concat([y,group['rpm1' ]])
        ax.cla()
#        cla()   # Clear axis即清除当前图形中的当前活动轴。其他轴不受影响。
#        clf()   # Clear figure清除所有轴，但是窗口打开，这样它可以被重复使用。
#        close() # Close a figure window
        ax.set_title("Loss")
        ax.set_xlabel(name)
        ax.set_ylabel("Loss")
        ax.set_xlim(0,2100)
        ax.set_ylim(-1,20)
        ax.grid()
        # 显示方式1：分批次显示
        #ax.scatter(group['power'], group['rpm1'], s = 8,  color = 'r', alpha = 0.4,marker='+') 
        # 显示方式2：起始累计显示
        ax.scatter(x, y, s = 8,  color = 'r', alpha = 0.4,marker='+')
#        ax.plot(y1,label='train')
#        ax.plot(y2,label='test')
        ax.legend(loc='best')
        plt.show()
        plt.pause(0.5)    
    
"""
    