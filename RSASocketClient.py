import socket
import RSALIB as rsa

keys = rsa.genKeys(20)  #generate public and private keys
myPublicKey, myPrivateKey = keys    #seperate into public and private
bytesPublicKey = rsa.convertToBytes(myPublicKey)    #convert public key to bytes for sending over socket
message = "hello world" #message to by encrypted and sent

HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server Port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #launch socket
    s.connect((HOST, PORT)) #connect to server
    s.sendall(bytesPublicKey)      #send public key in bytes as request for public key response
    byteServerPublicKey = s.recv(1024)  #receive server public key
    serverPublicKey = rsa.convertFromBytes(byteServerPublicKey) #convert server public key from bytes to tuple
    encrypted = rsa.RSAEnc(serverPublicKey, message)    #encrypt message using server's public key
    encryptedBytes = rsa.convertToBytes(encrypted)      #convert encrypted message to bytes for sending over socket
    s.sendall(encryptedBytes)   #send bytes over
    confirmation = s.recv(1024) #wait for confirmation of reciept and get it

print('Received', repr(confirmation))   #print confirmation message