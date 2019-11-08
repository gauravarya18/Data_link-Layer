import socket		 	 
import sys
import binascii
import time

def xor(a, b): 
   
    
    result = [] 
   
     
    for i in range(1, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
   
    return ''.join(result) 
   
   

def mod2div(divident, divisor): 
   
     
    pick = len(divisor) 
   
    tmp = divident[0 : pick] 
   
    while pick < len(divident): 
   
        if tmp[0] == '1': 
   
            tmp = xor(divisor, tmp) + divident[pick] 
   
        else:  
            tmp = xor('0'*pick, tmp) + divident[pick] 
   
        
        pick += 1
   
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
   
    checkword = tmp 
    return checkword 
   
def decodeData(data, key): 
   
    l_key = len(key)  
    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
   
    return remainder 
  
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def ReverseApplicationLayer(Data):
    print("In Reverse Application layer")
    print("Header LH5 removed to the data")
    
    idx=0
    for i in range(len(Data)):
        if (Data[i]=='-'):
            idx=i
            break
    
    AppData=Data[idx+1:]
    time.sleep(5)
    print(AppData)
    return AppData

def ReverseTransportLayer(AppData):
    print("In Reverse Transport Layer")
    print("Header LH4 removed to the data")
    
    idx=0
    for i in range(len(AppData)):
        if (AppData[i]=='-'):
            idx=i
            break
    
    TransData=AppData[idx+1:]
    time.sleep(5)
    print(TransData)
    return TransData

def ReverseNetworkLayer(TransData):
    print("In Reverse Network Layer")
    print("Header LH3 removed to the data")

    idx=0
    for i in range(len(TransData)):
        if (TransData[i]=='-'):
            idx=i
            break
    
    NetData=TransData[idx+1:]

    time.sleep(5)
    print(NetData)
    return NetData

def Org_ReverseApplicationLayer(Data):
    
    idx=0
    for i in range(len(Data)):
        if (Data[i]=='-'):
            idx=i
            break
    
    AppData=Data[idx+1:]
    print(AppData)
    return AppData

def Org_ReverseTransportLayer(AppData):
    
    idx=0
    for i in range(len(AppData)):
        if (AppData[i]=='-'):
            idx=i
            break
    
    TransData=AppData[idx+1:]
    print(TransData)
    return TransData

def TempNetworkLayer(TransData):

    idx=0
    for i in range(len(TransData)):
        if (TransData[i]=='-'):
            idx=i
            break
    
    NetData=TransData[idx+1:]
    return NetData

def Redundancy_Bit(Data,key):
    r1=int(Data[7],2)^int(Data[6],2)^int(Data[4],2)^int(Data[3],2)^int(Data[1],2)^int(key[3],2)
    r2=int(Data[5],2)^int(Data[4],2)^int(Data[7],2)^int(Data[2],2)^int(Data[1],2)^int(key[2],2)
    r4=int(Data[4],2)^int(Data[5],2)^int(Data[6],2)^int(Data[0],2)^int(key[1],2)
    r8=int(Data[0],2)^int(Data[1],2)^int(Data[2],2)^int(Data[3],2)^int(key[0],2)

    ans=r1*8+r2*4+r4*2+r8*1
    # print(ans+"\n")
    if ans>8:
        return 12-ans
    elif ans>4:
        return 11-ans
    elif ans>2:
        return 10-ans
    else:
        return -1

s = socket.socket() 	  		 # Create a socket object
host = socket.gethostname()                    # Get local machine name
port = int(4444)
s.bind((host, port)) 			 # Bind to the port
s.listen(5) 			         # Now wait for client connection.
print("Server is up and running")


while True:
     c, addr = s.accept() 		# Establish connection with client.
     print('Got connection from', addr)
     print(" '~'  is corrsponding to the errorneous bit")

     Num=0
     while True:
        #recieve the final string (error induced)
        message=c.recv(1024).decode()
        Technique=message[0]+message[1]
        Tech=int(Technique, 2)
        # print(Tech)
        data=message[2:]
        # print(data)
        print("-----------------------**********************************************************-------------------------")
        if message == "quit":
            c.send("Quit".encode())
            break
        else:

            if(Tech==0):
                #recieve the xor string
                parity=c.recv(1024).decode()
                AnsStr=""
                flag=True
                #roving over the parity string
                for j in range(0,len(parity)):

                    #to store the number
                    Num=0

                    #to store the corresponding temp. xor
                    tmp=0

                    #roving over the corresponding message string
                    for i  in  range(j*8,j*8+8):
                        if(data[i]=="1"):
                            tmp^=1
                        else:
                            tmp^=0
                    
                    tempChar=text_from_bits(data[j*8:j*8+8])
                    if(parity[j]!=str(tmp)):
                        #corresponding to the erroreneous bit
                        flag=False
                        AnsStr+="~"
                        AnsStr+=str(tempChar)
                    else:
                        AnsStr+=str(tempChar)
                
                print(AnsStr)
                
                AnsStr=ReverseNetworkLayer(AnsStr)
                print("---------------------------------------------")

                AnsStr=ReverseTransportLayer(AnsStr)
                print("---------------------------------------------")

                AnsStr=ReverseApplicationLayer(AnsStr)

                if flag: 
                    c.send(("THANK you Data ->"+data + " Received No error FOUND").encode())
                else: 
                    c.send(("Error in data").encode())

            elif(Tech==1):
                Crc=c.recv(1024).decode()
                key = "1001"
                temp = "0" * (len(key) - 1)
                flag=True
                
                AnsStr=""
                #roving over the parity string
                for i in range(0,len(data)//8):

                    #to store the number
                    Num=0

                    #to store the corresponding temp. xor
                    tmp=0
                    
                    tempChar=text_from_bits(data[i*8:i*8+8])
                    ans = decodeData(data[i*8:i*8+8]+Crc[i*3:i*3+3], key)
                    if(ans!=temp):
                        AnsStr+="~"
                        flag=False
                    AnsStr+=str(tempChar)
            

                
                print(AnsStr)
                AnsStr=ReverseNetworkLayer(AnsStr)

                print("---------------------------------------------")

                AnsStr=ReverseTransportLayer(AnsStr)
            
                print("---------------------------------------------")

                AnsStr=ReverseApplicationLayer(AnsStr)
                

                # If remainder is all zeros then no error occured 
                 
                if flag: 
                    c.send(("THANK you Data ->"+data + " Received No error FOUND").encode())
                else: 
                    c.send(("Error in data").encode())
            else:
                Redundancy_Code=c.recv(1024).decode()
                flag=True
                AnsStr=""
                Correct_Str=""
                #roving over the parity string
                for i in range(0,len(data)//8):

                    #to store the number
                    Num=0

                    #to store the corresponding temp. xor
                    tmp=0
                    
                    tempChar=text_from_bits(data[i*8:i*8+8])
                    AnsStr+=str(tempChar)
                    temp_str=""
                    ans = Redundancy_Bit(data[i*8:i*8+8],Redundancy_Code[i*4:i*4+4])
                    
                    if(ans!=-1):
                        strInBinary=data[i*8:i*8+8]
                        x=int(strInBinary[int(8-ans)])
                        x=(x+1)%2
                        # print(ans)
                        strToSend=strInBinary[:int(8-ans)]+str(x)+strInBinary[int(8-ans)+1:]
                        # print(strToSend)
                        # print(strInBinary)
                        # print(text_to_bits("H"))
                        orgchar=text_from_bits(strToSend)
                        Correct_Str+=str(orgchar)
                        flag=False
                    else:
                        Correct_Str+=str(tempChar)
            

                
                print(AnsStr)
                AnsStr=ReverseNetworkLayer(AnsStr)
                Correct_Str=TempNetworkLayer(Correct_Str)
                print("---------------------------------------------")

                AnsStr=ReverseTransportLayer(AnsStr)
                Correct_Str=TempNetworkLayer(Correct_Str)
            
                print("---------------------------------------------")

                AnsStr=ReverseApplicationLayer(AnsStr)
                Correct_Str=TempNetworkLayer(Correct_Str)
                

                # If remainder is all zeros then no error occured 
                 
                if flag: 
                    c.send(("THANK you Data ->"+data + " Received No error FOUND").encode())
                else: 
                    print("Correct Message::"+Correct_Str)
                    c.send(("Error Dectected").encode())

            
     c.close() 			# Close the connection.
     
