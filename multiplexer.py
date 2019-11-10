#dependencies:
#		
#
#
#this is a test

while True:
	userData = input("String of four characters: ")
	if len(userData)==4:
		break
asciiCodes = []
for x in range(0,len(userData)):
	asciiCodes.append(ord(userData[x]))


print(asciiCodes)


def tcpHead(_sourcePort, _destinationPort, _sequenceNumber, _headerLength, _flagBitN, _windowSize, _urgentPointer, _options, _appData):
	headerInit = bytearray()
	if(len(_sourceIp)!=2):
		return "Source Port must be 16 bit"
	if(len(_destinationIp)!=2):
		return "Destination Port must be 16 bit"
	if(len(_sequenceNumber)!= 4):
		return "Sequence number must be 32 bit"
	headerInit.append(_sourceIp)
	print(len(headerInit))
	print(headerInit)
	acknowledgementN = _sequenceNumber + _headerLength

tcpHead(1,1,1,1,1,1,1,1,1)