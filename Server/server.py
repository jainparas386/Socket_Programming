import os
import socket


#importing Crpyto Class
from Crypto import crypto

#object of crypto class
#pass mode in the object
crypto_obj = crypto('substitute')
s = socket.socket()
print("Socket Created")

s.bind(('localhost',9999))

s.listen(5)

while True:
    clientsocket, address  = s.accept()
    print(f"Connected from {address} is established")
    clientsocket.send(crypto_obj.encrypt("Welcome to the server!"))
    req = crypto_obj.decrypt(clientsocket.recv(1024))
    print(req)
    if (req == 'CWD'):
        curr_directory = os.getcwd()
        clientsocket.send(crypto_obj.encrypt(curr_directory))

    if req == 'LS':
        dir_list = os.listdir(os.getcwd())
        clientsocket.send(crypto_obj.encrypt(str(dir_list)))
    
    if req[0:2] == 'CD':
        os.chdir(req[3:])
        new_dir = os.getcwd()
        clientsocket.send(crypto_obj.encrypt(new_dir))
    
    if req[0:3] == 'DWD':
        file_name = req[4:]
        file_size = os.path.getsize(file_name)
        # print(file_name,file_size)
        clientsocket.send(crypto_obj.encrypt(str(file_size)))
        
        with open(file_name, "r") as file:
            data_transfered = 0

            while data_transfered <= int(file_size):
                packet =  file.read(1024)
                if not (packet):
                    print('break')
                    break
                clientsocket.send(crypto_obj.encrypt(packet))
                data_transfered += len(packet)     

    if req[0:3] == 'UPD':
        file_name = req[4:]
        file_size = int(crypto_obj.decrypt(clientsocket.recv(1024)))
        print(file_name,file_size)

        with open("./"+file_name,"w") as file:
            data_received = 0
            while data_received <= file_size:
                
                packet = None
                packet = crypto_obj.decrypt(clientsocket.recv(1024))
                
                if not (packet):
                    print('break')
                    break
                file.write(packet)
                data_received += len(packet)
                print(data_received)
            file.close()

    clientsocket.close()  


    print(req)


