#!/usr/bin/env python
 
from scapy.all import *
import requests,json
import MySQLdb
import time
import datetime
 
bridgeIP = "192.168.1.2"                    #IP Address of your Bridge
user = "VaA-1-uG7zUmFzZHhXIjinA-I-Dr2IUjvtz-O9Pj"    #Username you generated
# tideBtn = "10:0d:7f:79:46:86"                #MAC address of your Dash button
tideBtn = "f0:27:2d:a7:db:b3"
allBtn = "74:c2:46:a8:f3:b8"
slimjimBtn = "74:c2:46:b2:88:4d"
gatoradeBtn = "f0:27:2d:a2:2c:f1"
# lightID = "3"                                #ID of the light you want to control
lightIDs = ["1", "2", "3"]

# "Adam-Bookshelf" Is light ID:  1
# "Adam-Overhang" Is light ID:  3
# "Adam-Nightstand" Is light ID:  2

firstState = {
	'1': {  
		# 'on':True,
		'hue':47125,
		'colormode':'xy',
		'effect':'none',
		'alert':'none',
		'xy':[  
		 0.1684,
		 0.0416
		],
		'reachable':True,
		'bri':37,
		'ct':153,
		'sat':253
	},
	'2': {  
      # 'on':True,
      'hue':64488,
      'colormode':'xy',
      'effect':'none',
      'alert':'none',
      'xy':[  
         0.6451,
         0.3062
      ],
      'reachable':True,
      'bri':38,
      'ct':153,
      'sat':253
	},
	'3': {
      # 'on':True,
      'hue':47125,
      'colormode':'xy',
      'effect':'none',
      'alert':'none',
      'xy':[  
         0.1684,
         0.0416
      ],
      'reachable':True,
      'bri':37,
      'ct':153,
      'sat':253
	}
}

midState = {
	'1': {  
		# 'on':True,
		'bri':48,
		'hue':566,
		'sat':228,
		'effect':'none',
		'xy':[  
			0.6395,
			0.3315
		],
		'ct':153,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	},
	'2': {  
		# 'on':True,
		'bri':128,
		'hue':44173,
		'sat':252,
		'effect':'none',
		'xy':[  
			0.2014,
			0.1073
		],
		'ct':153,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	},
	'3': {
		# 'on':True,
		'bri':136,
		'hue':54526,
		'sat':209,
		'effect':'none',
		'xy':[  
			0.3732,
			0.1931
		],
		'ct':239,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	}
}

brightState = {
	'1': {
		# 'on':True,
		'bri':254,
		'hue':33129,
		'sat':52,
		'effect':'none',
		'xy':[  
			0.3689,
			0.3714
		],
		'ct':231,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	},
	'2': {
		# 'on':True,
		'bri':254,
		'hue':33129,
		'sat':52,
		'effect':'none',
		'xy':[  
			0.3689,
			0.3714
		],
		'ct':231,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	},
	'3': {
		# 'on':True,
		'bri':254,
		'hue':33129,
		'sat':52,
		'effect':'none',
		'xy':[  
			0.3689,
			0.3714
		],
		'ct':231,
		'alert':'none',
		'colormode':'xy',
		'reachable':True
	}
}


#-----------------
# database stuff
#-----------------

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="robot", # your username
                      passwd="r0b0t!", # your password
                      db="21newbury") # name of the data base
cur=db.cursor()
db.close()

def connectDB():
    global db
    global cur
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                                             user="robot", # your username
                                              passwd="r0b0t!", # your password
                                              db="21newbury") # name of the data base
    cur=db.cursor()

def closeDB():
    global db
    db.close()

def insertMsgInDb(ip, mac, os=""):
    cur.execute("INSERT INTO dash_watch (ip, mac, os) VALUES (\'" + str(ip) + "\', \'" + str(mac) + "\', \'" + str(os) + "\')")


#-----------------
# light states
#-----------------

def all_off():
	print "\tall_off()"
	for lightID in lightIDs:
		url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		r = requests.put(url+"/state",json.dumps({'bri': 0}))
		r = requests.put(url+"/state",json.dumps({'on':False}))

def set_state(state):
	# print "\tset_state(" + str(state) + ")"
	for lightID in lightIDs:
		url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		s = requests.put(url+"/state",json.dumps({'on':True}))
		r = requests.put(url+"/state",json.dumps(state[lightID]))
		# s = requests.put(url+"/state",json.dumps({'on':True}))

#-----------------
# light control
#-----------------

def get_light_state(id):
	url = "http://"+bridgeIP+"/api/"+user+"/lights/"+id
	r = requests.get(url)
	data = json.loads(r.text)
	return data

def test_light_state(id, scene):
	data = get_light_state(id)
	state = data["state"]
	thresh = 5

	hue = True if abs(state["hue"] - scene[id]["hue"]) < (thresh *3) else False
	sat = True if abs(state["sat"] - scene[id]["sat"]) < thresh else False
	bri = True if abs(state["bri"] - scene[id]["bri"]) < thresh else False

	result = hue and sat and bri

	return result


def toggle_low():
	first = True

	for lightID in lightIDs:
		data = get_light_state(lightID)

		if data["state"]["on"] == True:
			if first != False:
				first = test_light_state(lightID, midState)

	if first == True:
		print "\tset state first"
		set_state(firstState)
	else: 
		print "\tset state off"
		all_off()

def toggle_bright():
	mid = True
	bright = True

	for lightID in lightIDs:
		data = get_light_state(lightID)

		if data["state"]["on"] == True:
			if mid != False:
				mid = test_light_state(lightID, midState)
			print "\ttest mid-" + str(lightID) + ": " + str(mid)
			if bright != False:
				bright = test_light_state(lightID, brightState)
			print "\ttest bright-" + str(lightID) + ": " + str(bright)

	if mid == False and bright == False:
		print "\tset state mid"
		set_state(midState)
	if mid == True and bright == True:
		print "\tset state mid"
		set_state(midState)
	if mid == True and bright == False:
		print "\tset state bright"
		set_state(brightState)
	if mid == False and bright == True:
		print "\tset state off"
		# all_off()
		set_state(midState)

#-----------------
# packet sniffing
#-----------------
 
def arp_display(pkt):
	print "*****"
	print "pkt"
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print st
	# print dir(pkt)
	# print dir(pkt[ARP])
	connectDB()
	insertMsgInDb(pkt[ARP].psrc, pkt[ARP].hwsrc)
	db.commit()
	closeDB()
	if pkt[ARP].op == 1:
		print "*****"
		print "\thwsrc: " + pkt[ARP].hwsrc
		print "\tpsrc: " + pkt[ARP].psrc
		if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
			if pkt[ARP].hwsrc == slimjimBtn:
				print "\tpkt[ARP].hwsrc == slimjimBtn"
				toggle_low()
			if pkt[ARP].hwsrc == gatoradeBtn:
				print "\tpkt[ARP].hwsrc == gatoradeBtn"
				toggle_bright()
 
print "start"
print sniff(prn=arp_display, filter="arp", store=0, count=0)
print "stop"

