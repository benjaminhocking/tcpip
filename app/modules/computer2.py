import messenger
import threading
import udp_header
import ip_header
import dns
from time import sleep
dnsSeverIP = "192.168.8.9"
settings = ["192.168.8.8", "4c:e6:76:2e:f2:64", "denver"]
outWrite = ""
inRead = ""
wire2 = ""
listening = False

def writeToDns(output):
    f = open("Wires/computer2___dns.txt", "w")
    f.write(output)
    f.close()

def readDns():
    f = open("Wires/dns___computer2.txt", "r")
    x = f.read()
    return x

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

def messageToASCII(message):
    asciiArr = []
    for x in message:
        asciiArr.append(format(ord(x), "07b"))
    return "".join(asciiArr)
    return ord(message)

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

def ipBinToEng(ipBin):
    ipBinArr = []
    for i in range(4):
        ipBinI = ipBin[i*8: i*8+8]
        ipBinArr.append(str(int(ipBinI, 2)))
    ipEng = ".".join(ipBinArr)
    return ipEng

def dnsRequest(serverName):
    identification = 1
    serverNameBin = messageToASCII(serverName)
    dnsPacket = [format(identification, "016b"), "0", "0000", format(len(serverNameBin), "08b"), serverNameBin]
    dnsPacket = "".join(dnsPacket)
    dnsUDP = udp_header.createUDP(1447, 53, dnsPacket)
    ipPacket = ip_header.createIP(format(4, "04b"), format(0, "08b"), format(0, "016b"), format(0, "03b"), format(64, "08b"), format(6, "08b"), messenger.ipBinaryValue(settings[0]), messenger.ipBinaryValue(dnsSeverIP),dnsUDP)
    dnsPacketBin = "".join(ipPacket)
    writeToDns(dnsPacketBin)
    sleep(0.5)
    dns.replyToRequest(settings[2])
    sleep(0.5)
    returnPacket = readDns()
    ipBin = returnPacket[16:]
    ipEng = ipBinToEng(ipBin)
    print(ipEng)
    return ipEng
