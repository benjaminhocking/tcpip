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
	if(_options>4294967296):
		print("ERROR 002: Options MSS must be max 32 bits")
		return format(0, "032b")

	if(_options==0):
		_mss = 536
		mss = format(_mss, "032b")
		optionsArr.append(mss)
		return mss
	else:
		_mss = _options
		mss = format(_mss, "032b")
		return mss

def createTCPHead(_sourcePort, _destinationPort, _sequenceNumber, _flagBitN, _windowSize, _urgentPointer):
	headerInitArr = [0]*10
	_headerLength = 5
	if(_sourcePort>65536):
		return "ERROR 003: Source Port must be 16 bit"
	if(_destinationPort>65536):
		return "ERROR 004: Destination Port must be 16 bit"
	if(_sequenceNumber>4294967296):
		return "ERROR 005: Sequence number must be 32 bit"
	if(_headerLength>16):
		return "ERROR 006: Header Length must be 4 bit"
	if(_flagBitN>64):
		return "ERROR 007: Flag Bits must only be 6 bits"
	if(_windowSize>65536):
		return "ERROR 008: Window Size must be 16 bits"
	if(_urgentPointer>65536):
		return "ERROR 009: Urgent pointer must be 16 bits"


	sourcePort = format(_sourcePort, "016b")
	destinationPort = format(_destinationPort, "016b")
	sequenceNumber = format(_sequenceNumber, "032b")
	acknowledgementN = format(_sequenceNumber+1, "032b")
	headerLength = format(5, "04b")
	reservedField = format(0, "06b")
	flagBitN = format(_flagBitN, "06b")
	windowSize = format(_windowSize, "016b")
	checksum = format(0, "016b")
	urgentPointer = format(_urgentPointer, "016b")
	headerInitArr[0] = sourcePort
	headerInitArr[1] = destinationPort
	headerInitArr[2] = sequenceNumber
	headerInitArr[3] = acknowledgementN
	headerInitArr[4] = headerLength
	headerInitArr[5] = reservedField
	headerInitArr[6] = flagBitN
	headerInitArr[7] = windowSize
	headerInitArr[8] = checksum
	headerInitArr[9] = urgentPointer

	_checksum = checksumTCPHeader(headerInitArr)

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
	return format(0, "016b")

dataEx = format(1203, "014b")

print(createTCP(1,1,1,1,1,1,0,dataEx))