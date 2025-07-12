from Arm.ArmController import dataManager

data = dataManager(115200, 'COM4')

data.startConnection()

str = input("Number: ")

data.sendData(str)

data.stopConnection()