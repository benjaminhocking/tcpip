import messenger
import threading
settings = ["192.168.8.1", "cc:96:10:16:57:66"]
wire1 = ""
loWire = ""
listening = False

def readWire2():
    f = open("Wires/wire2.txt", "r")
    wire2 = f.read()
    return wire2

def writeLo(_output):
    f = open("Wires/loComp1.txt", "w")
    f.write(_output)
    f.close()

def readLo():
    f = open("Wires/loComp1", "r")
    x = f.read()
    return x

def writeWire1(_output):
    f = open("Wires/wire1.txt", "w")
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
    _packet = readWire2()
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
    #in format : message {source IP} {desination IP} {message}
    arr = _queryString.split(" ")
    if arr[0] != "message":
        print("non-logical query")
        return
    if isIP(arr[1])!= True:
        print("IP format incorrect")
        return
    if isIP(arr[2])!= True:
        print("IP format incorrect")
        return
    fullMessage = arr[3:len(arr)]
    fullMessageStr = " ".join(fullMessage)
    frame = messenger.createFrame(arr[1], arr[2], fullMessageStr)
    if arr[2] == arr[1]:
        writeLo(frame)
        print("written to loopback interface")
    else:
        writeWire1(frame)
        print("written to wire1")
