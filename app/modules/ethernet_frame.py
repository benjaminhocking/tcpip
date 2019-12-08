import ip_header as ip
import zlib
import binascii
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
    destinationIp = _ipDatagram[128:160]
    ethernetFrameWithoutIpDatagram = [checkForIpInARPCache(destinationIp), convertMacToBin(_sourceMac), format(800, "016b")]
    ethernetFrameWithoutIpDatagramBin = "".join(ethernetFrameWithoutIpDatagram)
    crc = calcCRC(ethernetFrameWithoutIpDatagramBin)
    ethernetFrame = [checkForIpInARPCache(destinationIp), convertMacToBin(_sourceMac), format(800, "016b"), _ipDatagram]
    ethernetFrame.append(crc)
    ethernetFrame = "".join(ethernetFrame)
    return ethernetFrame

def checkForIpInARPCache(_ipAdress):
    readArpCache()
    ipAddBin = _ipAdress
    macAdress = "0"
    ipAddArr = []
    for x in range(0, 4):
        ipAddArr.append(ipAddBin[x*8:(x*8)+8])
    print(ipAddArr)
    for x in range(0,4):
        ipAddArr[x] = str(int(ipAddArr[x], 2))
    ipAddStr = ".".join(ipAddArr)
    for x in range(0, len(arpCacheEntries)):
        if arpCacheEntries[x][0] == ipAddStr:
            macAdress = arpCacheEntries[x][1]
    if macAdress != "0":
        macAdress = convertMacToBin(macAdress)
    else:
        print("Mac Adress not found")
    return macAdress

def calcCRC(_ethernetFrameWithoutIPDatagram):
    testBytes = int(_ethernetFrameWithoutIPDatagram, 2) #convert to integer
    ethernetFrameBytes = testBytes.to_bytes(14, byteorder="little") #convert integer to bytes
    crcValue = format(binascii.crc32(ethernetFrameBytes), "032b") #calculate crc-32 from bytes
    return crcValue #return calculated crc value

def convertMacToBin(_macAdd):
    macAdressArr = _macAdd.split(':')
    for x in range(0, 6):
        macAdressArr[x] = format(int(macAdressArr[x],16), "08b")
    macAdress = "".join(macAdressArr)
    return macAdress


#print(createEthernetFrame(thisMac, ip.ipPacket1))
