#dependencies:
#
#notes
#	no window scaling option, only mss


def createTCP(_sourcePort, _destinationPort, _sequenceNumber, _flagBitN, _windowSize, _urgentPointer, _options, _data):
	#top level function
	header = createTCPHead(_sourcePort, _destinationPort, _sequenceNumber, _flagBitN, _windowSize, _urgentPointer)
	mss = fillTCPHeaderOptions(_options)
	data = _data
	completeTCPPacket = []
	completeTCPPacket.append(header)
	completeTCPPacket.append(mss)
	completeTCPPacket.append(data)
	tcpPacket = "".join(completeTCPPacket)
	if(len(tcpPacket)>int(mss)):
		print("ERROR 001: TCP is attempting to transmit a greater data size than MSS allows for")
		return

	return tcpPacket


def fillTCPHeaderOptions( _options):
	#mss = 32 bits long
	optionsArr = []

	if(len(_options)!=32):
		print("ERROR 002: Options MSS must be max 32 bits")
		return format(0, "032b")

	if(int(_options)==0):
		_mss = 536
		mss = format(_mss, "032b")
		optionsArr.append(mss)
		return mss
	else:
		_mss = _options
		mss = format(int(_mss), "032b")
		return mss

def createTCPHead(_sourcePort, _destinationPort, _sequenceNumber, _flagBitN, _windowSize, _urgentPointer):
	headerInitArr = [0]*10
	_headerLength = 5
	if(len(_sourcePort)!=16):
		return "ERROR 003: Source Port must be 16 bit"
	if(len(_destinationPort)!=16):
		return "ERROR 004: Destination Port must be 16 bit"
	if(len(_sequenceNumber)!=32):
		return "ERROR 005: Sequence number must be 32 bit"
	if(len(_flagBitN)!=6):
		return "ERROR 007: Flag Bits must only be 6 bits"
	if(len(_windowSize)!=16):
		return "ERROR 008: Window Size must be 16 bits"
	if(len(_urgentPointer)!=16):
		return "ERROR 009: Urgent pointer must be 16 bits"
	acknowledgementN = format(int(_sequenceNumber)+1, "032b")
	reservedField = format(0, "06b")
	checksum = format(0, "016b")
	headerInitArr[0] = _sourcePort
	headerInitArr[1] = _destinationPort
	headerInitArr[2] = _sequenceNumber
	headerInitArr[3] = acknowledgementN
	headerInitArr[4] = format(5, "04b")
	headerInitArr[5] = reservedField
	headerInitArr[6] = _flagBitN
	headerInitArr[7] = _windowSize
	headerInitArr[8] = checksum
	headerInitArr[9] = _urgentPointer

	_checksum = checksumTCPHeader("".join(headerInitArr))

	headerInitArr[8] = _checksum
	separator = ""
	header = separator.join(headerInitArr)
	if(len(header)/32!=int(len(header)/32)):
		print("ERROR 010: TCP header is not multiple of 32")
	headerLength = format(int(len(header)/32), "04b")
	headerInitArr[4] = headerLength
	header = separator.join(headerInitArr)
	return header

def checksumTCPHeader(tcpArray):
		tcpHeader16bits = []
		for i in range(0,int(len(tcpArray)/16)):
			tcpHeader16bits.append(tcpArray[i*16:(i*16)+16])
		counter = "0"
		for x in range(0, len(tcpHeader16bits)):
			thisAddition = int(counter,2)+int(tcpHeader16bits[x], 2)
			sumBin = format(thisAddition, "017b")
			if(sumBin[0]=="1"):
				sumBinArr = list(sumBin)
				sumBinArr[0] = "0"
				sumBinArr[16] = "1"
				sumBin = "".join(sumBinArr)
			counter = sumBin
		countArr = list(counter)
		del countArr[0]
		for x in range(0, len(countArr)):
			if countArr[x] == "0":
				countArr[x]="1"
			else:
				countArr[x]="0"
		counter = "".join(countArr)
		return counter

dataEx = format(1203, "014b")

#print(createTCP(format(1, "016b"), format(1, "016b"), format(1, "032b"), format(1, "06b"), format(1, "016b"), format(1, "016b"), format(0, "032b"), format(1203, "014b")))
