import time
import serial
import serial.tools.list_ports

## Change the serial if not using PCA10059 (VID:PID=239A:80D9)
SerialPortName = 'COM17'         # Set default serial port Name
################################################################

def enableDataControl(state):
    ## Fix for NRf Circuit Python (Windows) driver errror
    if (state & 1):
        ser.dsrdtr =    bool(state & 1)            
        ser.rtscts   =  bool(state & 2)
        ser.xonxoff  =  bool(state & 3)     
    ####################

def openPort():
    try:
        ser.open()         # Open serial port
        ser.write(b'\x04') # send CTRL-D
        ser.write(b'\x03') # send CTRL-C
        ser.write(b'\x04') # send CTRL-D

        data = ser.read(ser.in_waiting)
        ser.close()
        return True
    except serial.SerialException as error:
        err_str = str(error)
        
        if err_str.startswith("could not open port"):
            print("Unable to connect to comport: " , SerialPortName )
            print("In top of this program, please change the value for SerialPortName")
        else:
            print(error)
        return False    
        
#Find serial port name automaticaly for PAC10059
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    if hwid.startswith("USB VID:PID=239A:80D9"):
        SerialPortName=port
        print("Found nRF52840-Dongle PCA10059 connected at " , port)

ser = serial.Serial()         # Create Serial Obj 
ser.baudrate = 9600
ser.timeout = 0 
ser.port = SerialPortName     # Set Serial port Name

#Enable dsrdtr , rtscts, xonxoff    
enableDataControl(7)
#Disable dsrdtr , rtscts, xonxoff
enableDataControl(0)

if (not openPort()) :
    print("\nPlease reinsert the device and retry")
else:
    print("Circuit Python CDC Serial port sucessfully opened")        
