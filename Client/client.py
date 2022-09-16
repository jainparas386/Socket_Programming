import socket
import os

from Crypto import crypto

#object of crypto class
#pass mode in the object
crypto_obj = crypto('substitute')

s = socket.socket()

s.connect(('localhost',9999))

msg = s.recv(1024)
print(crypto_obj.decrypt(msg))
#Taking input from client
print('Enter the command')
request_cmd = input()
print(request_cmd)

s.send(crypto_obj.encrypt(request_cmd))

if(request_cmd == 'CWD'):
    working_dir = s.recv(1024)
    print(crypto_obj.decrypt(working_dir))

if(request_cmd == 'LS'):
    dir_list = s.recv(1024)
    print(crypto_obj.decrypt(dir_list))

if(request_cmd[0:2] == 'CD'):
    try:
        new_directory = s.recv(1024)
        print(crypto_obj.decrypt(new_directory))
        print('status-OK')
    except:
        print('status-NOK')
if(request_cmd[0:3]=='DWD'):
    try:
        file_name = request_cmd[4:]
        # print("./"+file_name)
        file_size = s.recv(1024)
        file_size = crypto_obj.decrypt(file_size)
        # print(type(file_size))
        # print(file_size)
        # print(os.getcwd())
        with open("./"+file_name,"w") as file:
            data_received = 0

            while data_received <= int(file_size):
                packet = None
                packet = s.recv(1024)
                packet = crypto_obj.decrypt(packet)
                
                if not (packet):
                    print('break')
                    break
                file.write(packet)
                data_received += len(packet)
                # print(data_received)
                
            file.close()
        # print(os.path.getsize(file_name))
        print("receieved file", file_name)
        print('status-OK')
    except:
        print('Status-NOK')

if(request_cmd[0:3]=='UPD'):
    try:
        file_name = request_cmd[4:]
        file_size = os.path.getsize(file_name)
        # print(file_name,file_size)
        s.send(crypto_obj.encrypt(str(file_size)))
        
        with open(file_name, "r") as file:
            data_transfered = 0

            while data_transfered <= int(file_size):
                packet =  file.read(1024)
                if not (packet):
                    print('break')
                    break
                s.send(crypto_obj.encrypt(packet))
                data_transfered += len(packet) 
        print('file_uploaded',file_name)
        print('status-OK')
    except:
        print('status-NOK')
s.close()