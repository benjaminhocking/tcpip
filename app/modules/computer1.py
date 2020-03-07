import messenger
import threading
import dns
import udp_header
import ip_header
from time import sleep
settings = ["192.168.8.1", "cc:96:10:16:57:66", "moscow"]
dnsSeverIP = "192.186.8.9"
wire1 = ""
loWire = ""
listening = False
global identification
identification = 0

def writeToDns(output):
    f = open("Wires/computer1___dns.txt", "w")
    f.write(output)
    f.close()

def readDns():
    f = open("Wires/dns___computer1.txt", "r")
    x = f.read()
    return x

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
    #in format : message {desination IP} {message}
    arr = _queryString.split(" ")
    destinaionIP = ""
    if isIP(arr[1]):
        destinationIP = arr[1]
    else:
        destinationIP = dnsRequest(arr[1])
    if arr[0] != "message":
        print("non-logical query")
        return

    fullMessage = arr[2:len(arr)]
    fullMessageStr = " ".join(fullMessage)
    frame = messenger.createFrame(settings[0], arr[1], fullMessageStr)
    if arr[1] == settings[0]:
        writeLo(frame)
        print("written to loopback interface")
    else:
        writeWire1(frame)
        print("written to wire1")

def ipBinToEng(ipBin):
    ipBinArr = []
    for i in range(4):
        ipBinI = ipBin[i*8: i*8+8]
        ipBinArr.append(str(int(ipBinI, 2)))
    ipEng = ".".join(ipBinArr)
    return ipEng

def ipEngToArpa(ipAddress):
    ipArr = ipAddress.split(".")
    newArr = []
    for i in range(4):
        newArr.append(ipArr[len(ipArr)-i-1])
    newArrStr = ".".join(newArr)
    fqdn =  newArrStr + ".in-addr.arpa."
    return fqdn

def dnsRequest(serverName):
    print("Using DNS server", dnsSeverIP)
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
    fqdn = ipEngToArpa(ipEng)
    print(serverName, ":", ipEng , ",", fqdn)
    return ipEng
