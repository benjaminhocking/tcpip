import tcp_header as tcp
import ip_header as ip
import ethernet_frame as ethernet
f=open("ComputerSettings/settings.txt", "r")
thisMac = f.read()
def messageToASCII(message):
    asciiArr = []
    for x in message:
        asciiArr.append(format(ord(x), "07b"))
    return "".join(asciiArr)
    return ord(message)
def ipBinaryValue(_ipString):
    ipArr = _ipString.split(".")
    for i in range(0, 4):
        ipArr[i] = format(int(ipArr[i]), "08b")
    return "".join(ipArr)

def createFrame(_fromIP, _toIP, _message):
    tcpPacket = tcp.createTCP(format(1, "016b"), format(1, "016b"), format(0, "032b"), format(0,"06b"), format(0,"016b"), format(0, "016b"), format(0, "032b"), messageToASCII(_message)) #send and listen on port 1, sequence number not currently in use, no flags, window size not in use, urgent pointer off, no options in use
    ipPacket = ip.createIP(format(4, "04b"), format(0, "08b"), format(0, "016b"), format(0, "03b"), format(64, "08b"), format(6, "08b"), ipBinaryValue(_fromIP), ipBinaryValue(_toIP), tcpPacket) #IPv4, normal type of service, no identification, 64 hops, protocol field = 6 (TCP), no flags

    ethernetFrame = ethernet.createEthernetFrame(ethernet.checkForIpInARPCache(ipBinaryValue(_fromIP)), ipPacket)
    return ethernetFrame
