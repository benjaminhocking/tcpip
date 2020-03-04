import computer1
import computer2
import threading
import demultiplexer
from time import sleep
computerN = -1
userInput = ""
computerList = [["moscow", "192.168.8.1"], ["denver", "192.168.8.8"]]
chosenComputer = ""
global chooseComp
chosenComputerIP = ""


print("Choose a machine to control: ")
for i in range(len(computerList)):
    print(">", computerList[i][0])
chosenComputer = input()
for i in range(len(computerList)):
    if computerList[i][0] == chosenComputer:
        chooseComp = False
if chooseComp:
    print("Please enter a valid machine name.")

for i in range(len(computerList)):
    if chosenComputer == computerList[i][0]:
        print(computerList[i][0], computerList[i][1])
        chosenComputerIP = computerList[i][1]

def listener():
    while True:
        userInput=  input(">> ")
        userInputArr = userInput.split(" ")

#######################################################################################################
        #Formatted as: message {destination ip} {message content}
        if userInputArr[0] == "message" and (userInputArr[1]==computer1.settings[0] or userInputArr[1]==computer2.settings[0]):
            print("sending message from: ", chosenComputerIP, " to: " + userInputArr[1])
            if chosenComputerIP == computer1.settings[0]:
                if userInputArr[1] == computer1.settings[0]:
                    print("from computer 1 to computer 1 using lo")
                    computer1.message(userInput)
                elif userInputArr[1] == computer2.settings[0]:
                    print("from computer 1 to computer 2 along SLIP")
                    computer1.message(userInput)
                else:
                    print("IP Address not recognised")
            elif chosenComputerIP == computer2.settings[0]:
                if userInputArr[1] == computer1.settings[0]:
                    print("from computer 2 to computer 1 along SLIP")
                    computer2.message(userInput)
                elif userInputArr[1] == computer2.settings[0]:
                    print("from computer 2 to computer 2 along lo")
                    computer2.message(userInput)
                else:
                    print("IP Address not recognised")
            sleep(0.3)
            print("success")
            sleep(0.7)
            message = " ".join(userInputArr[2:len(userInputArr)])
            print("Message: ", message)
            print("sent " + message + " to " + str(userInputArr[1]))

#######################################################################################################

        elif userInputArr[0] == "readmessage":
            targetIP = chosenComputerIP
            if targetIP == computer1.settings[0]:
                result = computer1.demultiplexPacket()
            elif targetIP == computer2.settings[0]:
                result = computer2.demultiplexPacket()
            else:
                result = "ERROR : IP address not found"
            print(result)

#######################################################################################################

        elif userInputArr[0] == "demultiplex":
            _ipAddress = chosenComputerIP
            result = demultiplexer.demultiplexer(_ipAddress)
            for x in result:
                print(x)

#######################################################################################################

        else:
            print(userInput, " is not a recognised command or the parameters provided are incorrect")


t = threading.Thread(target=listener)
t.start()
