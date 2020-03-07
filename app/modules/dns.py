#requests in format: identification(16bit), flags(16bit), number of questions(16bit), number of answer RRs (16bit), number of authority RRs(16bit), number of additional RRs(16bit), questions, answers
#flags in form: QR (1bit) - 0 = query; 1 = reply, 11 empty bits, rcode (4bits)
dnsMappings =[["denver", "192.168.8.8"], ["moscow", "192.168.8.1"]]

def writeToComputer1(output):
    f = open("Wires/dns___computer1.txt", "w")
    f.write(output)
    f.close()

def readFromComputer1():
    f = open("Wires/computer1___dns.txt", "r")
    x = f.read()
    f.close()
    return x

def writeToComputer2(output):
    f = open("Wires/dns___computer2.txt", "w")
    f.write(output)
    f.close()

def readFromComputer2():
    f = open("Wires/computer2___dns.txt", "r")
    x = f.read()
    f.close()
    return x


def dnsRequest(packetRead):
    packet = packetRead[208:]
    _identification = packet[0:16]
    _queryResponse = packet[16]
    _rcode = packet[17:21]
    _nameBytes=packet[21:29]
    _nNameBytes = int(_nameBytes, 2)
    _queryName = packet[29:]
    return [_queryResponse, queryNameBinToEng(_queryName), _identification]


def queryNameBinToEng(queryName):
    charArrBin = []
    charArrDec = []
    charArr = []
    for i in range(0, int(len(queryName)/7)):
        charArrBin.append(queryName[i*7:i*7+7])
    for x in range(0, len(charArrBin)):
        charArrDec.append(int(charArrBin[x], 2))
    for y in range(0,len(charArrDec)):
        charArr.append(chr(charArrDec[y]))
    serverName = "".join(charArr)
    return serverName

def checkDnsForServerName(serverName):
    for i in range(len(dnsMappings)):
        if serverName == dnsMappings[i][0]:
            return dnsMappings[i][1]
    return "Server name not found"

def dnsGet(packet):
    info = dnsRequest(packet)
    if info[0] == "0":
        ipAddress = checkDnsForServerName(info[1])
        if ipAddress == "Server name not found":
            return  info[2] + format(0, "032b")
        else:
            return info[2] + ipBinaryValue(ipAddress)

def ipBinaryValue(_ipString):
    ipArr = _ipString.split(".")
    for i in range(0, 4):
        ipArr[i] = format(int(ipArr[i]), "08b")
    return "".join(ipArr)

def replyToRequest(computerName):
    if computerName == "moscow":
        currentPacket = readFromComputer1()
    elif computerName == "denver":
        currentPacket = readFromComputer2()
    output = dnsGet(currentPacket)
    if computerName == "moscow":
        writeToComputer1(output)
    elif computerName == "denver":
        writeToComputer2(output)
