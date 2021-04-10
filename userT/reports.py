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
    #plt.style.use("fivethirtyeight") - used in Coreyvideo, not sure why its better but leave it first
    
    data = dataAct
    labels =labelsAct
    colors = ["#D3EDEE","#91CACC", "#C0A8A3","#5E6565","#E5C0E2"]
    radius = 0.8
    
    
    def explode(dataslice):
    
        explodel = [0.1]*len(dataslice) #- Just explode all based on fed in data instead of hard coding
        return explodel
    
    #get the explosion effect
    explodeslice = explode(data)
    #Taken from mathplot lib site to get both values and percenatge and lable it accordingly
    #using numpy to calculate
    def func(pct, allvals):
        absolute = int(round(pct/100.*np.sum(allvals)))
        return "{:.1f}%\n({:d} Actions)".format(pct, absolute)

    #strdisplay = '%.1f %%'
    #strdisplay ='%d'
    #lamda is just an inline function - nothing fancy
    plt.pie(data,labels=labels,colors=colors, radius = radius, startangle = 90,  explode = explodeslice, shadow=True,autopct=lambda pct: func(pct, data), wedgeprops ={'edgecolor':'black'})

    plt.title (Title)
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

