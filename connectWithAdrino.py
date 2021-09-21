import serial
import time


serialCom = serial.Serial('/dev/ttyACM0', 9600)
serialCom.timeout = 1

count = 0
while True:
    # i = input("input (on/off):").strip()
    if(count % 2 == 0):
        i = 'on'
    else:
        i = 'off'
    print('i', i)
    count = count + 1
    if i == 'done':
        print('finish the program')
        break
    serialCom.write(i.encode())
    time.sleep(0.5)
    print(serialCom.readline().decode('ascii'))
serialCom.close()


"""adriuno code"""
# String InBytes;
#
# void setup(){
# //  put your setup code here
# Serial.begin(9600);
# pinMode(LED_BUILTIN, OUTPUT);
# }
#
# void loop(){
# //  put your main code here, to run repeatly
#   if(Serial.available() > 0){
#       InBytes = Serial.readStringUntil('\n');
#       if(InBytes == "on"){
#           digitalWrite(LED_BUILTIN, HIGH);
#           Serial.write("Led on");
#         }
#       if(InBytes == "off"){
#           digitalWrite(LED_BUILTIN, LOW);
#           Serial.write("Led off");
#         }
#       else{
#         Serial.write("invalid input");
#         }
#     }
#   }