#dependencies:
#		
#
#
#
print("working")


while True:
	userData = input("String of four characters: ")
	if len(userData)==4:
		break
asciiCodes = []
for x in range(0,len(userData)):
	asciiCodes.append(ord(userData[x]))


print(asciiCodes)

def fillTcpHeaderOptions(_mss, _windowScaling, _selectiveAck)
	#mss = 32 bits
	#window scaling = 30 bits
	#SACK = 2 x 16 bits = 32 bits

def createTcpHead(_sourcePort, _destinationPort, _sequenceNumber, _headerLength, _flagBitN, _windowSize, _urgentPointer, _options, _appData):
	headerInit = bytearray()
	if(_sourcePort>65536):
		return "Source Port must be 16 bit"
	if(_destinationPort>65536):
		return "Destination Port must be 16 bit"
	if(_sequenceNumber>4294967296):
		return "Sequence number must be 32 bit"
	if(_headerLength>16):
		return "Header Length must be 4 bit"
	if(_flagBitN>512):
		return "Flag Bits must only be 9 bits"
	if(_windowSize>65536):
		return "Window Size must be 16 bits"
	if(_urgentPointer>65536):
		return "Urgent pointer must be 16 bits"
	if(len(_options)>40):
		return "Options must be less than or equal to 320 bits/40 bytes"
	communicationMSS = _options[:4]

	headerInit.append(_sourceIp)
	print(len(headerInit))
	print(headerInit)
	acknowledgementN = _sequenceNumber + 1

createTcpHead(1,1,1,1,1,1,1,1,1)