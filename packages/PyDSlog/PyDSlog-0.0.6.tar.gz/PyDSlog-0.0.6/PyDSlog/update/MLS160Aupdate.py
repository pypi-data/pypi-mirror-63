"""
  ____          ____   ____   _                         ____  ____ __     __ 
 |  _ \  _   _ |  _ \ / ___| | |  ___    __ _          / ___|/ ___|\ \   / / 
 | |_) || | | || | | |\___ \ | | / _ \  / _` |  _____  \___ \\___ \ \ \ / /  
 |  __/ | |_| || |_| | ___) || || (_) || (_| | |_____|  ___) |___) | \ V / 
 |_|     \__, ||____/ |____/ |_| \___/  \__, |         |____/|____/   \_/ 
         |___/                          |___/                     

"""
import serial
from PyDSlog.crc8 import crc8
import struct
import os
import time

class MLS160A_update:
    
    def __init__(self, directory_path=".", port="COM16", baudrate = 115200):
        
        self.directory_path = directory_path
        self.port = port
        self.baudrate = baudrate
        
               
    def find_files(self, slot):
    
        for file in os.listdir(self.directory_path):
            if file.endswith(".bin"):
                if "slot"+str(slot) in file:
                    f_bin = file

        for file in os.listdir(self.directory_path):
            if file.endswith(".bin.hash"):
                if "slot"+str(slot) in file:
                    f_hash = file
    
        return f_bin, f_hash

        
    def update(self):
        
        success = 0

        try:

            con = serial.Serial(self.port, self.baudrate)  

            for i in range(0,512): 
                con.write(b"\x5A")

            time.sleep(0.1) 

            con.write("U".encode())

            while(True):

                r = con.read(9)

                if(r[0] == 0x52): 

                    hash = crc8()
                    hash.update(r)

                    if(hash.hexdigest() == "00"):

                        slot_rx =   struct.unpack("<B", r[1:2])[0]
                        offset_rx = struct.unpack("<L", r[2:6])[0]
                        len_rx =   struct.unpack("<H", r[6:8])[0]
                        
                        f_bin, f_hash = self.find_files(slot_rx)

                        f_sz = os.path.getsize(f_bin)
                        with open(f_bin, "rb") as f:

                            if(offset_rx > f_sz):
                                b_arr = b""
                            else:
                                f.seek(offset_rx)
                                b_arr = f.read(len_rx)

                        len_ = len(b_arr)

                        slot_tx = struct.pack("<B", slot_rx)
                        offset_tx = struct.pack("<L", offset_rx)
                        len_tx = struct.pack("<H", len_)

                        frame = bytearray([ord("P")])
                        frame += slot_tx
                        frame += offset_tx
                        frame += len_tx
                        frame += b_arr

                        hash = crc8()
                        hash.update(frame)  
                        crc_val = hash.digest() 

                        frame += crc_val 
                        con.write(frame)

                        len_ = len(b_arr)
                        if(len_ < len_rx):
                            break


            time.sleep(0.1)    
            r = con.read(1)

            if(r[0] == 0x56):

                fb = open(f_hash,"rb").read()        
                frame = bytearray([ord("H")])
                frame += fb

                hash = crc8()
                hash.update(frame)  
                crc_val = hash.digest() 

                frame += crc_val
                con.write(frame)  

                time.sleep(0.1)
                r = con.read(1) 
                
                if(r.decode("utf-8") == "Y"):
                    success = 1

                #print("success: ", r.decode("utf-8"))         

        finally:

            for i in range(0,512): 
                con.write(b"\x5A")
                
            con.close()
            
            return success
            
def main():
    
    print("starting update")

    u = MLS160A_update()
    s = u.update()
    
    print(s)
    
    print("done")
        

if __name__ == "__main__":

    main()
