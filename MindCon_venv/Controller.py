import MindCon
import threading
headset = MindCon.Headset(port='COM6')

headset.start()

def printData():
    threading.Timer(1.0, printData).start()
    print(f"{headset.getData()}")

# def plotData():
#     threading.Timer(1.0, plotData).start()
#     plt.show(headset.plotData())
    

printData()




