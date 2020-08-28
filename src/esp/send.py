
def http_send(temp, humidity, room):
    import socket
    addr = socket.getaddrinfo('192.168.1.110', 5000)[0][-1]
    path = 'esp/submit?temp=' + temp + '&humidity=' + humidity + '&room=' + room
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, "192.168.1.110"), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()