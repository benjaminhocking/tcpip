import computer1
import computer2
import threading
import demultiplexer
from time import sleep
computerN = -1
userInput = ""
"""
while True:
    compIP = input("IP adress of computer to control: ")
    if computer1.isIP(compIP):
        print("Connecting...")
        f = open("Network/net.txt", "r")
        allIpAdresses = f.read()
        ipAdressesArr = allIpAdresses.splitlines()
        found = False
        for x in ipAdressesArr:
            if x == compIP:
                found = True
        sleep(2)
        if found:
            print("Success")
            break
        else:
            print("IP Adress not found")

    else:
        print("Please enter valid IP address")
if compIP == "192.168.8.1":
    computerN = 1
elif compIP == "192.168.8.8":
    computerN = 2
"""

def listener():
    while True:
        userInput=  input(">> ")
        userInputArr = userInput.split(" ")
        if userInputArr[0] == "message" and (userInputArr[1]==computer1.settings[0] or userInputArr[1]==computer2.settings[0]) and (userInputArr[2]==computer1.settings[0] or userInputArr[2]==computer2.settings[0]):
            print("sending message from: ", userInputArr[1], " to: " + userInputArr[2])
            if userInputArr[1] == computer1.settings[0]:
                if userInputArr[2] == computer1.settings[0]:
                    print("from computer 1 to computer 1 using lo")
                    computer1.message(userInput)
                elif userInputArr[2] == computer2.settings[0]:
                    print("from computer 1 to computer 2 along SLIP")
                    computer1.message(userInput)
                else:
                    print("IP Address not recognised")
            elif userInputArr[1] == computer2.settings[0]:
                if userInputArr[2] == computer1.settings[0]:
                    print("from computer 2 to computer 1 along SLIP")
                    computer2.message(userInput)
                elif userInputArr[2] == computer2.settings[0]:
                    print("from computer 2 to computer 2 along lo")
                    computer2.message(userInput)
                else:
                    print("IP Address not recognised")
            sleep(0.3)
            print("success")
            sleep(0.7)
            message = " ".join(userInputArr[2:len(userInputArr)])
            print("sent " + message + " to " + str(userInputArr[1]))
        elif userInputArr[0] == "readmessage" and computer1.isIP(userInputArr[1]) :
            targetIP = userInputArr[1]
            if targetIP == computer1.settings[0]:
                result = computer1.demultiplexPacket()
            elif targetIP == computer2.settings[0]:
                result = computer2.demultiplexPacket()
            else:
                result = "ERROR : IP address not found"
            print(result)
        elif userInputArr[0] == "demultiplex" and computer1.isIP(userInputArr[1]):
            result = demultiplexer.demultiplexer(userInputArr[1])
            for x in result:
                print(x)

        else:
            print(userInput, " is not a recognised command or the parameters provided are incorrect")


t = threading.Thread(target=listener)
t.start()
