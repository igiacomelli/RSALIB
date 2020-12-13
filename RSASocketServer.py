import socket
import RSALIB as rsa

HOST = '127.0.0.1'
PORT = 65432

keys = rsa.genKeys(20) #generates public and private key
myPublicKey, myPrivateKey = keys #seperates keys into public and private
bytesMyPublicKey = rsa.convertToBytes(myPublicKey)  #converts public key from tuple to bytes
x = 1   #for ending server loop

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #start socket server
    s.bind((HOST, PORT))    #bind port and host
    s.listen()              #listen for connections
    conn, addr = s.accept() #accept connection
    with conn:              #with connection
        print('Connected by', addr) #For testing connection
        while x == 1:               #while loop for connection
            data = conn.recv(1024)  #get sent data
            if not data:            #if it sends something else or nothing break
                break
            bytesClientPublicKey = data    #get client public key, not really used
            conn.sendall(bytesMyPublicKey)  #send server public key in bytes
            encryptedbytes = conn.recv(1024)    #receive encrypted message in bytes
            if not data:                    #kill if nothing or not data
                break
            encryptedMessage = rsa.convertFromBytes(encryptedbytes) #convert encrypted bytes to a list
            decryptedMessage = rsa.RSADec(myPrivateKey, encryptedMessage)   #decrypt message
            x += 1  #break from while loop
        print("Decrypted Message: " + decryptedMessage) #print the decrypted message
        conn.sendall(b'Message Successfully Decrypted') #send confirmation message back to client
