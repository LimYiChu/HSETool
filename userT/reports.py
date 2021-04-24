import matplotlib.pyplot as plt
import base64
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

def showPie(dataAct,labelsAct,Title):
    plt.switch_backend('AGG')
    #plt.style.use("fivethirtyeight") #- used in Coreyvideo, not sure why its better but leave it first
    
    data = dataAct
    labels =labelsAct
    colors = ["#9BBFE0", "#E8A09A", "#D3EDEE","#FBE29F",  "#C6D68F","#5E6565","#91CACC", "#C0A8A3",]
    radius = 1.0
    
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
    fig.suptitle(Title, fontsize=21, fontweight='bold', wrap=True)
    plt.rcParams['font.size'] = 18.0
    plt.rcParams['font.weight'] = "bold"
    #strdisplay = '%.1f %%'
    #strdisplay ='%d'
    #lamda is just an inline function - nothing fancy
    plt.pie(data,colors=colors, radius = radius, startangle = 90,  explode = explodeslice, shadow=True,autopct=lambda pct: func(pct, data), wedgeprops ={'edgecolor':'black'})

    plt.legend(labels, bbox_to_anchor=(1,1), loc="upper left")
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
    x_indexes = np.arange(len(labels_x_axes))
    width=0.25
    #x_index
    plt.bar(x_indexes, data_y_axes, label=label1, width=width, color="#91CACC")
    plt.bar(x_indexes-width, totalcountbyDisSub, label=label2, width=width, color="#5E6565")
    plt.legend()
    plt.title (title)
    plt.xticks (ticks=x_indexes-(width/2) , labels=labels_x_axes)
    plt.xlabel (generalxlabel)
    plt.tight_layout()
    graph =get_graph()
    return graph