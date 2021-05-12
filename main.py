import paho.mqtt.client as paho ,ssl , json , serial 
from time import sleep

 
connflag = False

ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
ser.flush()
 
def on_connect(client, userdata, flags, rc):                
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      
    print(msg.topic+" "+str(msg.payload))
    

 
mqttc = paho.Client()                                       
mqttc.on_connect = on_connect                             
mqttc.on_message = on_message                             

awshost = "a3fghbd5ko08t3-ats.iot.ap-south-1.amazonaws.com"     
awsport = 8883                                             
clientId = "Rpi"                                   
thingName = "Rpi"                                  
caPath = "./CREDENTIALS/AmazonRootCA1.pem"                                      
certPath = "./CREDENTIALS/942c539fa0-certificate.pem.crt"                          
keyPath = "./CREDENTIALS/942c539fa0-private.pem.key"                         
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               
 
mqttc.loop_start()                                          
 
while 1==1:
    sleep(5)
    if connflag == True:
        temp = "20.01" #sample temp data
        
        if ser.in_waiting > 0:
            temp = ser.readline().decode('utf-8').rstrip()
        
        paylodmsg0="{"
        paylodmsg1 = "\"temp\": \""
        paylodmsg4="\"}"
        paylodmsg = "{} {} {} {}".format(paylodmsg0, paylodmsg1, temp, paylodmsg4)
        paylodmsg = json.dumps(paylodmsg) 
        paylodmsg_json = json.loads(paylodmsg)       
        mqttc.publish("RpiHOME", paylodmsg_json , qos=1)        
        print("msg sent: {}".format(temp) ) 
        print(paylodmsg_json)

    else:
        print("waiting for connection...")                      