from ArmManager import DataManager

data = DataManager(115200, 'COM4')

data.startConnection()

str = input("Number: ")

data.sendData(str)

data.stopConnection()