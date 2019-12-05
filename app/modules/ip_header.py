def createIPHead(_IPVersion, _tos, _identification, _flags, _ttl, _protocol, _sourceIP, _destinationIP, _totalLength):
	#will use IPv4 and TCP protocol
	if(len(_IPVersion)!=4):
		return "ERROR 011: IP version must be 4 bit"
	if(len(_tos)!=8):
		return "ERROR 012: Type of service must be 8 bit"
	if(len(_identification)!=16):
		return "ERROR 013: Identification must be 16 bit"
	if(len(_flags)!=3):
		return "ERROR 014: flags must be 3 bit"
	if(len(_ttl)!=8):
		return "ERROR 015: time to live must be 8 bit"
	if(len(_protocol)!=8):
		return "ERROR 016: protocol must be 8 bit"
	if(len(_sourceIP)!=32):
		return "ERROR 017: souce IP must be 32 bit"
	if(len(_destinationIP)!=32):
		return "ERROR 018: destination IP must be 32 bit"
	iPHead = []
	iPHead.append(_IPVersion) #ip version (ipv4) - 4bit
	iPHead.append(format(0, "04b")) #header length (initially set to 4) - 4bit
	iPHead.append(_tos) #type of service - 8bit
	iPHead.append(format(16, "016b")) #total length (initially set to 16) - 16bit
	iPHead.append(_identification) #identification to identify each datagram sent by a host - 16bit
	iPHead.append(_flags) #flags - 3bit
	iPHead.append(format(0, "013b")) #fragment offset - 13bit
	iPHead.append(_ttl) #time to live (max amount of routers through which the datagram can pass) - 8bit
	iPHead.append(_protocol) #protocol used (TCP) - 8bit
	iPHead.append(format(0, "016b")) #checksum - 16bit
	iPHead.append(_sourceIP) #source IP - 32bit
	iPHead.append(_destinationIP) # destination IP - 32bit
	#still to: CALC HEADER LENGTH - [x] || CALC TOTAL LENGTH || CALC CHECKSUM
	ipHeader = "".join(iPHead)
	if(int(len(ipHeader)/32)!= len(ipHeader)/32):
		return "ERROR 019: IP Header length is not a multiple of 32"
	iPHead[1] = format(int(len(ipHeader)/32), "04b")
	ipHeader = "".join(iPHead)
	return ipHeader

def createIP(_IPVersion, _tos, _identification, _flags, _ttl, _protocol, _sourceIP, _destinationIP, _data):
	ipHeader = createIPHead(_IPVersion, _tos, _identification, _flags, _ttl, _protocol, _sourceIP, _destinationIP, format(0, "016b"))
	ipPacket = ipHeader + _data
	totalLen = format(int(len(ipPacket)/32), "016b")
	ipHeader = createIPHead(_IPVersion, _tos, _identification, _flags, _ttl, _protocol, _sourceIP, _destinationIP, totalLen)
	ipPacket = ipHeader + _data

	return ipPacket

destinationIpT = format(192, "08b") + format(168, "08b") + format(8, "08b") + format(1, "08b")

ipPacket1 = createIP(format(4, "04b"), format(1, "08b"), format(1, "016b"), format(1, "03b"), format(1, "08b"), format(1, "08b"), format(1, "032b"), destinationIpT, format(100, "032b"))

#print(createIP(format(4, "04b"), format(1, "08b"), format(1, "016b"), format(1, "03b"), format(1, "08b"), format(1, "08b"), format(1, "032b"), format(1, "032b"), format(100, "032b")))
