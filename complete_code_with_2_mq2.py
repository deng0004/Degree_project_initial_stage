import ujson
import usocket
import ussl
import _thread
import time

class FIREBASE_GLOBAL_VAR:
    GLOBAL_URL=None
    GLOBAL_URL_ADINFO=None
    SLIST={}

class INTERNAL:
  def connect(id):
      LOCAL_ADINFO=usocket.getaddrinfo(FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"], FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["port"], 0, usocket.SOCK_STREAM)[0]
      FIREBASE_GLOBAL_VAR.SLIST["S"+id] = usocket.socket(LOCAL_ADINFO[0], LOCAL_ADINFO[1], LOCAL_ADINFO[2])
      FIREBASE_GLOBAL_VAR.SLIST["S"+id].connect(LOCAL_ADINFO[-1])
      if FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["proto"] == "https:":
          try:
            FIREBASE_GLOBAL_VAR.SLIST["SS"+id] = ussl.wrap_socket(FIREBASE_GLOBAL_VAR.SLIST["S"+id], server_hostname=FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"])
          except:
            print("ENOMEM, try to restart. If you make to many id's (sokets) simultaneously (bg=1 and id=x), try to use less or use a board with more ram!\nSome emulation software limits the RAM.")
            FIREBASE_GLOBAL_VAR.SLIST["S"+id].close()
            FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=None
            FIREBASE_GLOBAL_VAR.SLIST["S"+id]=None
            raise MemoryError
            
      else:
          FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=FIREBASE_GLOBAL_VAR.SLIST["S"+id]
  def disconnect(id):
      FIREBASE_GLOBAL_VAR.SLIST["SS"+id].close()
      FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=None
      FIREBASE_GLOBAL_VAR.SLIST["S"+id]=None
        
  def put(PATH, DATA, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(2)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"PUT /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      LOCAL_DUMMY=LOCAL_SS.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  


  def patch(PATH, DATATAG, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"PATCH /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATATAG))+"\r\n\r\n")
      LOCAL_SS.write(DATATAG)
      LOCAL_DUMMY=LOCAL_SS.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  

  def get(PATH, DUMP, id, cb, limit):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+ujson.dumps(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_OUTPUT=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      INTERNAL.disconnect(id)
      globals()[DUMP]=LOCAL_OUTPUT
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")      
  def getfile(PATH, FILE, bg, id, cb, limit):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"GET /"+PATH+b".json?shallow="+ujson.dumps(limit)+b" HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      while not LOCAL_SS.readline()==b"\r\n":
        pass
      LOCAL_FILE=open(FILE, "wb")
      if bg:
        while True:
          LOCAL_LINE=LOCAL_SS.read(1024)
          if LOCAL_LINE==b"":
            break
          LOCAL_FILE.write(LOCAL_LINE)
          time.sleep_ms(1)
      else:
        while True:
          LOCAL_LINE=LOCAL_SS.read(1024)
          if LOCAL_LINE==b"":
            break
          LOCAL_FILE.write(LOCAL_LINE)
      LOCAL_FILE.close()
      LOCAL_DUMMY=LOCAL_SS.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  

  def delete(PATH, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"DELETE /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n\r\n")
      LOCAL_DUMMY=LOCAL_SS.read()
      del LOCAL_DUMMY
      INTERNAL.disconnect(id)
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
      
  def addto(PATH, DATA, DUMP, id, cb):
      try:
        while FIREBASE_GLOBAL_VAR.SLIST["SS"+id]:
          time.sleep(1)
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      except:
        FIREBASE_GLOBAL_VAR.SLIST["SS"+id]=True
      INTERNAL.connect(id)
      LOCAL_SS=FIREBASE_GLOBAL_VAR.SLIST["SS"+id]
      LOCAL_SS.write(b"POST /"+PATH+b".json HTTP/1.0\r\n")
      LOCAL_SS.write(b"Host: "+FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO["host"]+b"\r\n")
      LOCAL_SS.write(b"Content-Length: "+str(len(DATA))+"\r\n\r\n")
      LOCAL_SS.write(DATA)
      LOCAL_OUTPUT=ujson.loads(LOCAL_SS.read().splitlines()[-1])
      INTERNAL.disconnect(id)
      if DUMP:
        globals()[DUMP]=LOCAL_OUTPUT["name"]
      if cb:
        try:
          cb[0](*cb[1])
        except:
          try:
            cb[0](cb[1])
          except:
            raise OSError("Callback function could not be executed. Try the function without ufirebase.py callback.")  
    
def setURL(url):
    FIREBASE_GLOBAL_VAR.GLOBAL_URL=url
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
        
    FIREBASE_GLOBAL_VAR.GLOBAL_URL_ADINFO={"proto": proto, "host": host, "port": port}

def put(PATH, DATA, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.put, [PATH, ujson.dumps(DATA), str(id), cb])
    else:
      INTERNAL.put(PATH, ujson.dumps(DATA), str(id), cb)

def patch(PATH, DATATAG, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.patch, [PATH, ujson.dumps(DATATAG), str(id), cb])
    else:
      INTERNAL.patch(PATH, ujson.dumps(DATATAG), str(id), cb)

def getfile(PATH, FILE, bg=False, id=0, cb=None, limit=False):
    if bg:
      _thread.start_new_thread(INTERNAL.getfile, [PATH, FILE, bg, str(id), cb, limit])
    else:
      INTERNAL.getfile(PATH, FILE, bg, str(id), cb, limit)

def get(PATH, DUMP, bg=False, cb=None, id=0, limit=False):
    if bg:
      _thread.start_new_thread(INTERNAL.get, [PATH, DUMP, str(id), cb, limit])
    else:
      INTERNAL.get(PATH, DUMP, str(id), cb, limit)
      
def delete(PATH, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.delete, [PATH, str(id), cb])
    else:
      INTERNAL.delete(PATH, str(id), cb)
    
def addto(PATH, DATA, DUMP=None, bg=True, id=0, cb=None):
    if bg:
      _thread.start_new_thread(INTERNAL.addto, [PATH, ujson.dumps(DATA), DUMP, str(id), cb])
    else:
      INTERNAL.addto(PATH, ujson.dumps(DATA), DUMP, str(id), cb)




#Put Tag1
# put("testtag", "1234", bg=0)

# put("lolval/testval", {"somenumbers": [1,2,3], "something": "lol"}, bg=0)


###########################################################################################################################################################
from machine import Pin, ADC
from micropython import const
import utime
from math import exp, log

class BaseMQ(object):
    ## Measuring attempts in cycle
    MQ_SAMPLE_TIMES = const(5)

    ## Delay after each measurement, in ms
    MQ_SAMPLE_INTERVAL = const(500)

    ## Heating period, in ms
    MQ_HEATING_PERIOD = const(60000)

    ## Cooling period, in ms
    MQ_COOLING_PERIOD = const(90000)

    ## This strategy measure values immideatly, so it might be inaccurate. Should be
    #  suitable for tracking dynamics, raither than actual values
    STRATEGY_FAST = const(1)

    ## This strategy measure values separatelly. For a single measurement
    #    MQ_SAMPLE_TIMES measurements are taken in interval MQ_SAMPLE_INTERVAL.
    #    I.e. for multi-data sensors, like MQ2 it would take a while to receive full data
    STRATEGY_ACCURATE = const(2)    

    ## Initialization. 
    #  @param pinData Data pin. Should be ADC pin
    #  @param pinHeater Pass -1 if heater connected to main power supply. Otherwise pass another pin capable of PWM
    #  @param boardResistance On troyka modules there is 10K resistor, on other boards could be other values
    #  @param baseVoltage Optionally board could run on 3.3 Volds, base voltage is 5.0 Volts. Passing incorrect values
    #  would cause incorrect measurements
    #  @param measuringStrategy Currently two main strategies are implemented:
    #  - STRATEGY_FAST = 1 In this case data would be taken immideatly. Could be unreliable
    #  - STRATEGY_ACCURATE = 2 In this case data would be taken MQ_SAMPLE_TIMES times with MQ_SAMPLE_INTERVAL delay
    #  For sensor with different gases it would take a while
    def __init__(self, pinData, pinHeater=-1, boardResistance = 10, baseVoltage = 3.3, measuringStrategy = STRATEGY_ACCURATE):

        ## Heater is enabled
        self._heater = False
        ## Heater is enabled
        self._cooler = False
        ## Base resistance of module         
        self._ro = -1

        self._useSeparateHeater = False
        self._baseVoltage = baseVoltage

        ## @var _lastMeasurement - when last measurement was taken
        self._lastMesurement = utime.ticks_ms()
        self._rsCache = None
        self.dataIsReliable = False
        self.pinData = ADC(Pin(pinData, Pin.IN))
        self.measuringStrategy = measuringStrategy
        self._boardResistance = boardResistance
        if pinHeater != -1:
            self.useSeparateHeater = True
            self.pinHeater = Pin(pinHeater, Pin.OUTPUT)
            pass

    ## Abstract method, should be implemented in specific sensor driver.
    #  Base RO differs for every sensor family
    def getRoInCleanAir(self):
        raise NotImplementedError("Please Implement this method")

    ## Sensor calibration
    #  @param ro For first time sensor calibration do not pass RO. It could be saved for
    #  later reference, to bypass calibration. For sensor calibration with known resistance supply value 
    #  received from pervious runs After calibration is completed @see _ro attribute could be stored for 
    #  speeding up calibration
    def calibrate(self, ro=-1):
        if ro == -1:
            ro = 0
            print("Calibrating:")
            for i in range(0,MQ_SAMPLE_TIMES + 1):        
                print("Step {0}".format(i))
                ro += self.__calculateResistance__(self.pinData.read_u16())
                utime.sleep_ms(MQ_SAMPLE_INTERVAL)
                pass            
            ro = ro/(self.getRoInCleanAir() * MQ_SAMPLE_TIMES )
            pass
        self._ro = ro
        self._stateCalibrate = True    
        pass

    ## Enable heater. Is not applicable for 3-wire setup
    def heaterPwrHigh(self):
        #digitalWrite(_pinHeater, HIGH)
        #_pinHeater(1)
        if self._useSeparateHeater:
            self._pinHeater.on()
            pass
        self._heater = True
        self._prMillis = utime.ticks_ms()


    ## Move heater to energy saving mode. Is not applicable for 3-wire setup
    def heaterPwrLow(self):
        #analogWrite(_pinHeater, 75)
        self._heater = True
        self._cooler = True
        self._prMillis = utime.ticks_ms()


    ## Turn off heater. Is not applicable for 3-wire setup
    def heaterPwrOff(self):
        if self._useSeparateHeater:
            self._pinHeater.off()
            pass
        #digitalWrite(_pinHeater, LOW)
        _pinHeater(0)
        self._heater = False


    ## Measure sensor current resistance value, ere actual measurement is performed
    def __calculateResistance__(self, rawAdc):
        vrl = rawAdc*(self._baseVoltage / 65535)
        rsAir = (self._baseVoltage - vrl)/vrl*self._boardResistance
        return rsAir


    ## Data reading     
    # If data is taken frequently, data reading could be unreliable. Check @see dataIsReliable flag
    # Also refer to measuring strategy
    def __readRs__(self):
        if self.measuringStrategy == STRATEGY_ACCURATE :            
                rs = 0
                for i in range(0, MQ_SAMPLE_TIMES + 1): 
                    rs += self.__calculateResistance__(self.pinData.read_u16())
                    utime.sleep_ms(MQ_SAMPLE_INTERVAL)

                rs = rs/MQ_SAMPLE_TIMES
                self._rsCache = rs
                self.dataIsReliable = True
                self._lastMesurement = utime.ticks_ms()                            
                pass
        else:
            rs = self.__calculateResistance__(self.pinData.read_u16())
            self.dataIsReliable = False
            pass
        return rs


    def readScaled(self, a, b):        
        return exp((log(self.readRatio())-b)/a)


    def readRatio(self):
        return self.__readRs__()/self._ro


    ## Checks if sensor heating is completed. Is not applicable for 3-wire setup
    def heatingCompleted(self):
        if (self._heater) and (not self._cooler) and (utime.ticks_diff(utime.ticks_ms(),self._prMillis) > MQ_HEATING_PERIOD):
            return True
        else:
            return False

    ## Checks if sensor cooling is completed. Is not applicable for 3-wire setup 
    def coolanceCompleted(self):
        if (self._heater) and (self._cooler) and (utime.ticks_diff(utime.ticks_ms(), self._prMillis) > MQ_COOLING_PERIOD):
            return True
        else:
            return False

    ## Starts sensor heating. @see heatingCompleted if heating is completed
    def cycleHeat(self):
        self._heater = False
        self._cooler = False
        self.heaterPwrHigh()
    #ifdef MQDEBUG
        print("Heated sensor")
    #endif #MQDEBUG
        pass

    ## Use this to automatically bounce heating and cooling states
    def atHeatCycleEnd(self):
        if self.heatingCompleted():
            self.heaterPwrLow()
    #ifdef MQDEBUG
            print("Cool sensor")
    #endif #MQDEBUG
            return False

        elif self.coolanceCompleted():
            self.heaterPwrOff()
            return True

        else:
            return False

###########################################################################################################################################################
class MQ2(BaseMQ):
	## Clean air coefficient
	MQ2_RO_BASE = float(9.83)

	def __init__(self, pinData, pinHeater=-1, boardResistance = 10, baseVoltage = 3.3, measuringStrategy = BaseMQ.STRATEGY_ACCURATE):
		# Call superclass to fill attributes
		super().__init__(pinData, pinHeater, boardResistance, baseVoltage, measuringStrategy)
		pass

	## Measure liquefied hydrocarbon gas, LPG
	def readLPG(self):
		return self.readScaled(-0.45, 2.95)
		
	## Measure methane	
	def readMethane(self):
		return self.readScaled(-0.38, 3.21)

	## Measure smoke
	def readSmoke(self):
		return self.readScaled(-0.42, 3.54)

	## Measure hydrogen
	def readHydrogen(self):
		return self.readScaled(-0.48, 3.32)

    ##  Base RO differs for every sensor family
	def getRoInCleanAir(self):
		return self.MQ2_RO_BASE





###########################################################################################################################################################






import utime
import time
def calibaration_testing_mq2(pin):
    Smoke = []
    LPG = []
    Methane = []
    Hydrogen = []
#     pin=26
    print("this is pin: ", pin)
    sensor = MQ2(pinData=pin, baseVoltage = 3.3)
    print("Calibrating")
    sensor.calibrate()
    print("Calibration completed")
    print("Base resistance:{0}".format(sensor._ro))
    start = time.ticks_ms()
    while True:
        smoke = "{:.1f}".format(sensor.readSmoke())
        print("Smoke: " + smoke  +" - ", end="")
        Smoke.append(smoke)
        lpg = "{:.1f}".format(sensor.readLPG())
        print("LPG: " + lpg +" - ", end="")
        LPG.append(lpg)
        methane = "{:.1f}".format(sensor.readMethane())
        print("Methane: " + methane +" - ", end="")
        Methane.append(methane)
        hydrogen = "{:.1f}".format(sensor.readHydrogen())
        print("Hydrogen: " + hydrogen)
        Hydrogen.append(hydrogen)
        print(Smoke)
        print(LPG)
        print(Methane)
        print(Hydrogen)

        if time.ticks_ms()-start > 60000:
            break
    dict = {
    "Smoke": Smoke,
    "LPG": LPG,
    "Methane": Methane,
    "Hydrogen": Hydrogen
    }
    return dict
 

   

dict1 = calibaration_testing_mq2(25) # gas senor 1
dict2 = calibaration_testing_mq2(26) # gas senor 2
# dict3 = calibaration_testing_mq2(27) # gas senor 3



# print("dict: ", dict1)
# print("type of dict: ", type(dict1))

import os as MOD_OS
import network as MOD_NETWORK
import time as MOD_TIME

#Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
# GLOB_WLAN.connect(ssid, password)


while not GLOB_WLAN.isconnected():
  pass

url = "url link from real time databe in firebase"
print(url)

FIREBASE_GLOBAL_VAR()
INTERNAL()

setURL(url)

put("sensor1/data", dict1, bg=0)
put("sensor2/data", dict2, bg=0)
class HTML:

    def __init__(self, Header, tableStyles = {}, trStyles = {}, thStyles = {}):
        self.tableStyles = HTML._styleConverter(tableStyles)
        trStyles = HTML._styleConverter(trStyles)
        thStyles = HTML._styleConverter(thStyles)
        self.rows = []
        self.Header= f'<tr {trStyles} >'
        for th in Header:
            self.Header += f'\n<th {thStyles} >{th}</th>'
        self.Header += '\n</tr>'

    @staticmethod
    def _styleConverter(styleDict : dict):
        if styleDict == {}:
            return ''
        styles = ''
        for [style, value] in styleDict.items():
            styles +=f'{style}: {value};'
        return f'style="{styles}"'

    def addRow(self, row, trStyles = {}, tdStyles = {}):
        trStyles = HTML._styleConverter(trStyles)
        tdStyles = HTML._styleConverter(tdStyles)
        temp_row = f'\n<tr {trStyles} >'
        for td in row:
            temp_row += f'\n<td {tdStyles} >{td}</td>'
        temp_row += '\n</tr>'
        self.rows.append(temp_row)


    def __str__(self):


        return \
f'''
<table {self.tableStyles} >
{self.Header}
{''.join(self.rows)}
</table>
'''

def dictionaryToHTMLTable(dict : dict):
    html = HTML(Header = dict.keys(),
                tableStyles={'margin': '3px'},
                trStyles={'background-color': '#7cc3a97d'},
                thStyles={ 'color': 'white'})
    for i, row in enumerate(zip(*dict.values())):
        print(row)
        if i%2 == 0:
            BGC = 'aliceblue'
        else:
            BGC = '#c2d4e4'
        html.addRow(row, trStyles={'background-color' : BGC}, tdStyles={'padding': '1rem'})
    return html

# print(type(dictionaryToHTMLTable(myDict)))
html_table = ""
gpio_state = ""
html_table_dict1 = str(dictionaryToHTMLTable(dict1))
html_table_dict2 = str(dictionaryToHTMLTable(dict2))
# print(html_table)

html_table_dict1 = ""
html_table_dict2 = ""
gpio_state = ""

def web_page(html_table_dict1, html_table_dict2):
    if led.value() == 1:
        gpio_state="ON"
    else :
        gpio_state="OFF"
    
    html = """
    <html>
       <head>
          <title>Data From Database</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="icon" href="data:,">
          <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
             h1{color: #0F3376; padding: 2vh;}
             p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
             border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
             .button2{background-color: #4286f4;}
          </style>
       </head>
       <body>
          <h1>Gas Sensors Data</h1>
          <p><a href="/?html"><button class="button">SHOW TABLE</button></a></p> """ + """<h2>Gas Sensor 1 </h2>"""+ html_table_dict1 +  """<h2>Gas Sensor 2 </h2>""" + html_table_dict2 + """
       </body>
    </html>
    """
    return html

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'SSID'
password = 'PASSWORD'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(32, Pin.OUT)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    html = request.find('/?html')
    print("html: ", html)
    if html == 6:
        print('HTML')
        html_table_dict1 = str(dictionaryToHTMLTable(dict1))
        html_table_dict2 = str(dictionaryToHTMLTable(dict2))
        
        
        
    response = web_page( html_table_dict1, html_table_dict2 )
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()


