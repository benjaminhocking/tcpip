import computer1
import computer2

def representMac(_binaryMacAddres):
    macPartsBin = []
    macPartsHex = []
    for x in range(0,6):
        macPartsBin.append(_binaryMacAddres[x*8:x*8+8])
    for x in range(0,6):
        macPartsHex.append(str(format(int(macPartsBin[x], 2), 'x')))
    return ":".join(macPartsHex)

def representIP(_binaryIPAddress):
    ipPartsBin = []
    ipPartsDec = []
    for x in range(0,4):
        ipPartsBin.append(_binaryIPAddress[x*8:x*8+8])
    for x in range(0,4):
        ipPartsDec.append(str(int(ipPartsBin[x], 2)))
    return ".".join(ipPartsDec)

def translateMessage(_message):
    charArrBin = []
    charArrDec = []
    charArr = []
    for i in range(0, int(len(_message)/7)):
        charArrBin.append(_message[i*7:i*7+7])
    for x in range(0, len(charArrBin)):
        charArrDec.append(int(charArrBin[x], 2))
    for y in range(0,len(charArrDec)):
        charArr.append(chr(charArrDec[y]))
    demultiplexedString = "".join(charArr)
    return demultiplexedString

def demultiplexer(_ipAdress):
    packet = ""
    if _ipAdress == computer1.settings[0]:
        packet = computer1.readWire2()
    elif _ipAdress == computer2.settings[0]:
        packet = computer2.readWire1()
    else:
        print("Ip Address not recognised")
        return
    destinationMac = packet[0:48]
    sourceMac = packet[48:96]
    type = packet[96:112]
    iPVersion = packet[112:116]
    headerLength = packet[116:120]
    typeOfService = packet[120:128]
    totalLength = packet[128:144]
    identification = packet[144:160]
    flagsIP = packet[160:163]
    fragmentOffset = packet[163:176]
    timeToLive = packet[176:184]
    protocol = packet[184:192]
    headerChecksum = packet[192:208]
    sourceIp = packet[208:240]
    destinationIp = packet[240:272]
    sourcePortNumber = packet[272:288]
    destinationPortNumber = packet[288:304]
    sequenceNumber = packet[304:336]
    acknowledgementNumber = packet[336:368]
    headerLength = packet[368:372]
    reservedField = packet[372:378]
    flagsTCP = packet[378:384]
    windowSize = packet[384:400]
    checksum = packet[400:416]
    urgentPointer = packet[416:432]
    options = packet[432:464]
    data = packet[464:len(packet)-32]
    crc = packet[len(packet)-32: len(packet)]

    representMac("110011001001011000010000000101100101011101100110")

    if int(type,2)==800:
        type="IP Datagram"
    if int(typeOfService,2)==0:
        typeOfService ="TCP"

    data = translateMessage(data)

    packetArr = [destinationMac, sourceMac, type, iPVersion, headerLength, typeOfService, totalLength,identification, flagsIP, fragmentOffset, timeToLive, protocol, headerChecksum, sourceIp, destinationIp, sourcePortNumber, destinationPortNumber, sequenceNumber, acknowledgementNumber, headerLength, reservedField, flagsTCP, windowSize, checksum, urgentPointer, options, data, crc]
    packetArr[0] = "Destination MAC address: " + str(representMac(packetArr[0]))
    packetArr[1] = "Source MAC address: " + str(representMac(packetArr[1]))
    packetArr[2] = "Type of ethernet frame: " + packetArr[2]
    packetArr[3] = "IP type: IPv" + str(int(packetArr[3], 2))
    packetArr[4] = "Ip header length: " + str(int(packetArr[4], 2)*4) + " bytes"
    packetArr[5] = "Type of service: " + str(packetArr[5])
    packetArr[6] = "Total IP datagram length: " + str(int(packetArr[6],2)) + " bytes"
    packetArr[7] = "IP identification: " + str(packetArr[7])
    packetArr[8] = "IP flags : " + str(packetArr[8])
    packetArr[9] = "Fragment offset: " + str(packetArr[9])
    packetArr[10] = "Time to live: " + str(int(packetArr[10],2))
    packetArr[11] = "Transport protocol: " + str(int(packetArr[11]))
    packetArr[12] = "IP Header Checksum: " + str(int(packetArr[12], 2))
    packetArr[13] = "Source IP Address: " + str(representIP(packetArr[13]))
    packetArr[14] = "Destination Ip Address: " + str(representIP(packetArr[14]))
    packetArr[15] = "Source Port Number: " + str(int(packetArr[15], 2))
    packetArr[16] = "Destination Port Number: " + str(int(packetArr[16], 2))
    packetArr[17] = "Sequence Number: " + str(int(packetArr[17], 2))
    packetArr[18] = "Acknowledgement Number: " + str(int(packetArr[18]))
    packetArr[19] = "TCP Header length: " + str(int(packetArr[19], 2))
    packetArr[20] = "(Reserved Field): " + str(packetArr[20])
    packetArr[21] = "TCP Flags: " + str(packetArr[21])
    packetArr[22] = "Window Size: " + str(int(packetArr[22]))
    packetArr[23] = "TCP Header checksum: " + str(int(packetArr[23], 2))
    packetArr[24] = "TCP Urgent Pointer: " + str(int(packetArr[24], 2))
    packetArr[25] = "TCP Options (mss): " + str(int(packetArr[25], 2))
    packetArr[26] = "Application Data: " + data
    packetArr[27] = "CRC value: " + str(int(packetArr[27], 2))
    return packetArr
