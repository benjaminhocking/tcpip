import ip_header as ip
arpCacheEntries = []
macAdress = "0"
f=open("ComputerSettings/settings.txt", "r")
thisMac = f.read()
def readArpCache():
    f = open("Ethernet/ARP/arpcache.txt", "r")
    arpString = f.read()
    arpCacheLines = arpString.splitlines()
    for i in range(0, len(arpCacheLines)):
        arpCacheEntries.append(arpCacheLines[i].split("|"))

def createEthernetFrame(_sourceMac, _ipDatagram):
    ethernetFrame = [checkForIpInARPCache(), convertMacToBin(_sourceMac), format(800, "016b"), _ipDatagram, format(0, "032b")]
    ethernetFrame = "".join(ethernetFrame)
    print(len(_ipDatagram))

def checkForIpInARPCache():
    ipAddBin = ip.ipPacket1[128:160]
    ipAddArr = []
    for x in range(0, 4):
        ipAddArr.append(ipAddBin[x*8:(x*8)+8])
    for x in range(0,4):
        ipAddArr[x] = str(int(ipAddArr[x], 2))
    ipAddStr = ".".join(ipAddArr)
    print(ipAddStr)
    for x in range(0, len(arpCacheEntries)):
        if arpCacheEntries[x][0] == ipAddStr:
            macAdress = arpCacheEntries[x][1]
    if macAdress != "0":
        macAdress = convertMacToBin(macAdress)
    else:
        print("Mac Adress not found")
    return macAdress

def convertMacToBin(_macAdd):
    macAdressArr = _macAdd.split(':')
    for x in range(0, 6):
        macAdressArr[x] = format(int(macAdressArr[x],16), "08b")
    macAdress = "".join(macAdressArr)
    return macAdress

readArpCache()
createEthernetFrame(thisMac, ip.ipPacket1)
