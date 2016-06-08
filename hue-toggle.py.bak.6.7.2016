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
	print "\tset_state()"
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


def toggle_low():
	first = True
	for lightID in lightIDs:
		# print "*****"
		# print "light ID: " + str(lightID)
		url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		r = requests.get(url)
		data = json.loads(r.text)

		if data["state"]["on"] == True:
			# print "on"
			# print "xy:" + str(data["state"]["xy"])
			# print "x:" + str(data["state"]["xy"][0])
			# print "x test:" + str(str(data["state"]["xy"][0]) != "0.1684")
			# print "y:" + str(data["state"]["xy"][1])
			# print "y test:" + str(str(data["state"]["xy"][1]) != "0.0417")

			if lightID=="1" and (str(data["state"]["xy"][0]) != "0.1684" or str(data["state"]["xy"][1]) != "0.0417"):
				# set_first()
				break
			elif lightID=="2" and (str(data["state"]["xy"][0]) != "0.645" or str(data["state"]["xy"][0]) != "0.3062"):
				# set_first()
				break
			elif lightID=="3" and (str(data["state"]["xy"][0]) != "0.1684" or str(data["state"]["xy"][0]) != "0.0416"):
				# set_first()
				break
			else: 
				first = False

	if first == True:
		# set_first()
		set_state(firstState)
	else: 
		all_off()

def toggle_bright():
	mid = True
	bright = True
	for lightID in lightIDs:
		data = get_light_state(lightID)
		# url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		# r = requests.get(url)
		# data = json.loads(r.text)

		# print data
		print "*****"
		print "midState[" + lightID + "][xy][0]==" + str(midState[lightID]["xy"][0])
		print "midState[" + lightID + "][xy][1]==" + str(midState[lightID]["xy"][1])
		print "brightState[" + lightID + "][xy][0]==" + str(brightState[lightID]["xy"][0])
		print "brightState[" + lightID + "][xy][1]==" + str(brightState[lightID]["xy"][1])
		print "data[state][xy][0]==" + str(data["state"]["xy"][0])
		print "data[state][xy][1]==" + str(data["state"]["xy"][1])

		print ""
		print ""

		print "midState[" + lightID + "][hue]==" + str(midState[lightID]["hue"])
		print "midState[" + lightID + "][sat]==" + str(midState[lightID]["sat"])
		print "midState[" + lightID + "][bri]==" + str(midState[lightID]["bri"])
		print "midState[" + lightID + "][ct]==" + str(midState[lightID]["ct"])
		print "brightState[" + lightID + "][hue]==" + str(brightState[lightID]["hue"])
		print "brightState[" + lightID + "][sat]==" + str(brightState[lightID]["sat"])
		print "brightState[" + lightID + "][bri]==" + str(brightState[lightID]["bri"])
		print "brightState[" + lightID + "][ct]==" + str(brightState[lightID]["ct"])
		print "data[state][hue]==" + str(data["state"]["hue"])
		print "data[state][sat]==" + str(data["state"]["sat"])
		print "data[state][bri]==" + str(data["state"]["bri"])
		print "data[state][ct]==" + str(data["state"]["ct"])


		# test for mid
		if data["state"]["on"] == True:
			if lightID=="1" and (str(data["state"]["xy"][0]) == str(midState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(midState[lightID]["xy"][1])):
				print "mid 1: true"
				# break
			elif lightID=="2" and (str(data["state"]["xy"][0]) == str(midState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(midState[lightID]["xy"][1])):
				print "mid 2: true"
				# break
			elif lightID=="3" and (str(data["state"]["xy"][0]) == str(midState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(midState[lightID]["xy"][1])):
				print "mid 3: true"
				# break
			else: 
				mid = False
		else:
			mid = False

		# test for bright
		if data["state"]["on"] == True:
			if lightID=="1" and (str(data["state"]["xy"][0]) == str(brightState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(brightState[lightID]["xy"][1])):
				print "bright 1: true"
				# break
			elif lightID=="2" and (str(data["state"]["xy"][0]) == str(brightState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(brightState[lightID]["xy"][1])):
				print "bright 2: true"
				# break
			elif lightID=="3" and (str(data["state"]["xy"][0]) == str(brightState[lightID]["xy"][0]) and str(data["state"]["xy"][1]) == str(brightState[lightID]["xy"][1])):
				print "bright 3: true"
				# break
			else: 
				bright = False
		else: 
			bright = False

	print "mid==" + str(mid)
	print "bright==" + str(bright)

	if mid == False and bright == False:
		print "set state mid"
		set_state(midState)
	if mid == True and bright == False:
		print "set state bright"
		set_state(brightState)
	if bright == True:
		print "set state off"
		all_off()

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
			if pkt[ARP].hwsrc == tideBtn:
				print "\tpkt[ARP].hwsrc == tideBtn"
				toggle_low()
			if pkt[ARP].hwsrc == gatoradeBtn:
				print "\tpkt[ARP].hwsrc == allBtn"
				toggle_bright()
 
print "start"
print sniff(prn=arp_display, filter="arp", store=0, count=0)
print "stop"

