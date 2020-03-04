import messenger
import threading
settings = ["192.168.8.8", "4c:e6:76:2e:f2:64"]
outWrite = ""
inRead = ""
wire2 = ""
listening = False

def readWire1():
    f = open("Wires/wire1.txt", "r")
    wire1 = f.read()
    #print(wire1)
    return wire1

def writeLo(_output):
    f = open("Wires/loComp2.txt", "w")
    f.write(_output)
    f.close()

def readLo():
    f = open("Wires/loComp2", "r")
    x = f.read()
    return x

def writeWire2(_output):
    f = open("Wires/wire2.txt", "w")
    f.write(_output)
    f.close()

def isIP(_ipAddress):
    arr = _ipAddress.split(".")
    if len(arr) != 4:
        return False
    for x in arr:
        if int(x) >255:
            return False
    return True

def demultiplexPacket():
    _packet = readWire1()
    appData = _packet[464:len(_packet)-32]
    charArrBin = []
    charArrDec = []
    charArr = []
    for i in range(0, int(len(appData)/7)):
        charArrBin.append(appData[i*7:i*7+7])
    for x in range(0, len(charArrBin)):
        charArrDec.append(int(charArrBin[x], 2))
    for y in range(0,len(charArrDec)):
        charArr.append(chr(charArrDec[y]))
    demultiplexedString = "".join(charArr)
    return demultiplexedString

def message(_queryString):
    #in format : message {desination IP} {message}
    arr = _queryString.split(" ")
    if arr[0] != "message":
        print("non-logical query")
        return
    if isIP(arr[1])!= True:
        print("IP format incorrect")
        return
    fullMessage = arr[3:len(arr)]
    fullMessageStr = " ".join(fullMessage)
    frame = messenger.createFrame(settings[0], arr[1], fullMessageStr)
    if arr[1] == settings[0]:
        writeLo(frame)
        print("written to loopback interface")
    else:
        writeWire2(frame)
        print("written to wire2")
