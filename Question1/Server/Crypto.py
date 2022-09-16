class crypto:

    def __init__(self, mode:str):
        self.mode = mode
    
    def encrypt(self, msg:str):
        if self.mode == 'plain':
            return msg.encode('utf-8')
    
        elif self.mode == 'substitute':
            self.offset = 2
            encrptyed_str =''
            for char in msg:
                if(char.isalnum()):
                    if(char.isupper()):
                        encrptyed_str += chr((ord(char)+self.offset-65)%26+65)
                    elif(char.islower()):
                        encrptyed_str += chr((ord(char)+self.offset-97)%26+97)
                    else:
                        encrptyed_str += chr((ord(char)+self.offset-48)%10+48)
                else:
                    encrptyed_str += char
            return encrptyed_str.encode('utf-8')
        elif self.mode == 'transpose':
            encrptyed_str = ''
            for word in msg.split():
                encrptyed_str += word[::-1] + ' '
            return encrptyed_str[:-1].encode('utf-8')

    def decrypt(self, msg:bytes):
        if self.mode == 'plain':
            return msg.decode('utf-8')
        
        elif self.mode == 'substitute':
            self.offset = -2
            decrptyed_str =''
            msg = msg.decode('utf-8')
            for char in msg:
                if(char.isalnum()):
                    if(char.isupper()):
                        decrptyed_str += chr((ord(char)+self.offset-65)%26+65)
                    elif(char.islower()):
                        decrptyed_str += chr((ord(char)+self.offset-97)%26+97)
                    else:
                        decrptyed_str += chr((ord(char)+self.offset-48)%10+48)
                else:
                    decrptyed_str += char
            return decrptyed_str

        elif self.mode == 'transpose':
            encrptyed_str = ''
            msg = msg.decode('utf-8')
            for word in msg.split():
                encrptyed_str += word[::-1] + ' '
            return encrptyed_str[:-1]

