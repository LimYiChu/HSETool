import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import base64
import math
from io import BytesIO
import numpy as np

def get_graph():
    #copied from youtube - cant explain much but basically it buffers into some base 64 sort of image
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def showPie(dataAct,labelsAct,title):
    plt.switch_backend('AGG')
    #plt.style.use("fivethirtyeight") #- used in Coreyvideo, not sure why its better but leave it first
    
    data = dataAct
    labels =labelsAct
    colors = ["#9BBFE0", "#E8A09A", "#D3EDEE","#FBE29F",  "#C6D68F","#5E6565","#91CACC", "#C0A8A3",]
    radius = 1.0 #yhs changed to 0.8 from 1.0
    
    def explode(dataslice):
    
        explodel = [0.1]*len(dataslice) #- Just explode all based on fed in data instead of hard coding
        return explodel
    
    #get the explosion effect
    explodeslice = explode(data)
    #Taken from mathplot lib site to get both values and percenatge and lable it accordingly
    #using numpy to calculate
    def func(pct, allvals):
        
        absolute = int(round(pct/100.*np.sum(allvals)))
        return "{:.0f} %\n({:d})".format(pct, absolute) #"{:.0f} %\n({:d} Actions)".format(pct, absolute)

    fig = plt.figure()
    fig.suptitle(title, fontsize=21, fontweight='bold', wrap=True)
    #plt.title (title,fontsize=20, fontweight='bold', wrap=True)
    plt.rcParams['font.size'] = 15.0
    plt.rcParams['font.weight'] = "bold"
    plt.rcParams["figure.figsize"] = (6,6)
    #strdisplay = '%.1f %%'
    #strdisplay ='%d'
    #lamda is just an inline function - nothing fancy
    plt.pie(data,colors=colors, radius = radius, startangle = 90,  explode = explodeslice, shadow=True,autopct=lambda pct: func(pct, data), wedgeprops ={'edgecolor':'black'})

    plt.legend(labels, bbox_to_anchor=(0.90,1.2), loc="upper left") #yhs changed to 0.90 and 1.2
    #plt.title (Title)
    plt.tight_layout()
    
    # plt.figure(figsize=(10,5))
    # plt.title('Test ing')
    # plt.plot(x,y)
    
    # plt.xticks(rotation=45)
    # plt.xlabel('item')
    # plt.ylabel('test')
    # plt.tight_layout()
    graph =get_graph()
    return graph

def showbar (listcountbyDisSub,totalcountbyDisSub,listlablebyDisSub, label1,label2,generalxlabel, title):

    plt.switch_backend('AGG') #- must do for django rendering but in the process cant show in python direct

    data_y_axes = listcountbyDisSub
    labels_x_axes =listlablebyDisSub
    
    maxcount = max(totalcountbyDisSub) #the following is to adjust the y axes ranges
    stepcount = 1
    if maxcount >= 5:

        stepcount = math.ceil(maxcount/5)
        print(stepcount)
    x_indexes = np.arange(len(labels_x_axes))
    #y_indexes = np.arange(0, maxcount,stepcount)
    #y_indexes = np.arange(0, 2,0.5)
    width=0.40
    #x_index
    plt.bar(x_indexes, data_y_axes, label=label1, width=width, color="#91CACC")
    plt.bar(x_indexes-width, totalcountbyDisSub, label=label2, width=width, color="#5E6565")
    
    #fig = plt.figure()
    #fig.suptitle(title, fontsize=15, fontweight='bold', wrap=True)
    #plt.rcParams['font.size'] = 15.0
    #plt.rcParams['font.weight'] = "bold"
    plt.rcParams["figure.figsize"] = (6,6)
    #plt.rcParams['axes.autolimit_mode'] = 'round_numbers'

    plt.legend()
    plt.title (title,fontsize=20, fontweight='bold', wrap=True)
    plt.xticks (ticks=x_indexes-(width/2) , labels=labels_x_axes, fontsize='12',fontweight='bold')
    #plt.yticks(y_indexes)
    #plt.gca().yax
    plt.xlabel (generalxlabel)
    plt.tight_layout()
    graph =get_graph()
    return graph