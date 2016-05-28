import socket

def get_hddtemp(ip, port):
    s = socket.socket()
    s.connect((ip, port))
    buf = s.recv(2048)
    s.close()
    return buf[1:]

def parse_hddtemp(line):

    hddtemps = {}

    for device in line.split('||'):
        parts = device.split('|')

        hddtemps[parts[0]] = {
            'value': parts[2],
            'unit': parts[3]
        }

    return hddtemps
