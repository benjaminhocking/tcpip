#source port: Integer, destination port: Integer, data: Binary
def createUDP(sourcePort, destinationPort, data):
    _sourcePort = format(sourcePort, "016b")
    _destinationPort = format(destinationPort, "016b")
    _udpLength = format(len(data), "016b")
    _data = data
    packet = "".join([_sourcePort + _destinationPort + _udpLength + _data])
    return packet
