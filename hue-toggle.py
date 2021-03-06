#!/usr/bin/env python
 
from scapy.all import *
import requests,json
import MySQLdb
import time
import datetime
from states import *
 
bridgeIP = "192.168.1.2"
user = "VaA-1-uG7zUmFzZHhXIjinA-I-Dr2IUjvtz-O9Pj"

# tideBtn = "f0:27:2d:a7:db:b3"	# RIP tide button
allBtn = "74:c2:46:a8:f3:b8"
slimjimBtn = "74:c2:46:b2:88:4d"
gatoradeBtn = "f0:27:2d:a2:2c:f1"
enjoylifeBtn = "44:65:0d:a0:b2:b9"
onBtn = "44:65:0d:d5:40:29"

lightIDs = ["1", "2", "3", "4", "5"]

bedroomLightIDs = ["1", "2", "3"]
livingroomLightIDs = ["4", "5"]

# "Adam-Bookshelf" Is light ID:  1
# "Adam-Nightstand" Is light ID:  2
# "Adam-Overhang" Is light ID:  3

# "Livingroom - Adam's side" is lightID: 4
# "Livingroom - Chris's side" is lightID: 5


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

def lights_off(lights):
	# print "\tlights_off()"
	for lightID in lights:
		url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		#r = requests.put(url+"/state",json.dumps({'bri': 0}))
		r = requests.put(url+"/state",json.dumps({'on':False}))

def set_state(state, lights):
	# print "\tset_state(" + str(state) + ")"
	for lightID in lights:
		url = "http://"+bridgeIP+"/api/"+user+"/lights/"+lightID
		s = requests.put(url+"/state",json.dumps({'on':True}))
		r = requests.put(url+"/state",json.dumps(state[lightID]))
		# s = requests.put(url+"/state",json.dumps({'on':True}))

#-----------------
# light control
#-----------------

def get_light_state(id):
	url = "http://"+bridgeIP+"/api/"+user+"/lights/"+id
	print url
	r = requests.get(url)
	data = json.loads(r.text)
	return data

def test_light_state(id, scene):
	data = get_light_state(id)
	state = data["state"]
	thresh = 5

	# print "id: " + id
	# print "test - hue: " + str(abs(state["hue"] - scene[id]["hue"]))
	# print "*state: " + str(state["hue"])
	# print "*scene: " + str(scene[id]["hue"])
	# print "test - sat: " + str(abs(state["sat"] - scene[id]["sat"]))
	# print "*state: " + str(state["sat"])
	# print "*scene: " + str(scene[id]["sat"])
	# print "test - bri: " + str(abs(state["bri"] - scene[id]["bri"]))
	# print "*state: " + str(state["bri"])
	# print "*scene: " + str(scene[id]["bri"])

	hue = True if abs(state["hue"] - scene[id]["hue"]) < (thresh *3) else False
	sat = True if abs(state["sat"] - scene[id]["sat"]) < thresh else False
	bri = True if abs(state["bri"] - scene[id]["bri"]) < thresh else False
	on = True if state["on"] == True else False

	# print "hue: " + str(hue)
	# print "sat: " + str(sat)
	# print "bri: " + str(bri)
	# print "on: " + str(on)

	result = hue and sat and bri and on

	return result


def toggle_low():
	first = True

	for lightID in bedroomLightIDs:
		data = get_light_state(lightID)

		print 'data["state"]["on"]: ' + str(data["state"]["on"])

		if data["state"]["on"] == True:
			# print "on==True"
			if first != False:
				first = test_light_state(lightID, firstState)
		else:
			# print "on==False"
			first = False
			
	# print "first==" + str(first)
	if first == True:
		print "\t*****set state off"
		lights_off(bedroomLightIDs)
	else: 
		print "\t*****set state first"
		set_state(firstState, bedroomLightIDs)

def toggle_bright():
	mid = True
	bright = True

	for lightID in bedroomLightIDs:
		data = get_light_state(lightID)

		if data["state"]["on"] == True:
			if mid != False:
				mid = test_light_state(lightID, midState)
			# print "\ttest mid-" + str(lightID) + ": " + str(mid)
			if bright != False:
				bright = test_light_state(lightID, brightState)
			# print "\ttest bright-" + str(lightID) + ": " + str(bright)

	if mid == False and bright == False:
		print "\t*****set state mid"
		set_state(midState, bedroomLightIDs)
	if mid == True and bright == True:
		print "\t*****set state mid"
		set_state(midState, bedroomLightIDs)
	if mid == True and bright == False:
		print "\t*****set state bright"
		set_state(brightState, bedroomLightIDs)
	if mid == False and bright == True:
		print "\t*****set state mid"
		# lights_off(bedroomLightIDs)
		lights_off(bedroomLightIDs)

def toggle_livingroom():
	livingroom_normal = True
	livingroom_movie = True

	for lightID in livingroomLightIDs:
		data = get_light_state(lightID)

		if data["state"]["on"] == True:
			if livingroom_normal != False:
				livingroom_normal = test_light_state(lightID, livingroom_normalState)
			# print "\ttest mid-" + str(lightID) + ": " + str(mid)
			if livingroom_movie != False:
				livingroom_movie = test_light_state(lightID, livingroom_movieState)
			# print "\ttest livingroom_movie-" + str(lightID) + ": " + str(livingroom_movie)

	if livingroom_normal == False and livingroom_movie == False:
		print "\t*****set state livingroom_normal"
		set_state(livingroom_normalState, livingroomLightIDs)
	if livingroom_normal == True and livingroom_movie == True:
		# this should be off for living room lights
		print "\t*****set state livingroom_normal"
		set_state(livingroom_normalState, livingroomLightIDs)
	if livingroom_normal == True and livingroom_movie == False:
		print "\t*****set state livingroom_movie"
		set_state(livingroom_movieState, livingroomLightIDs)
	if livingroom_normal == False and livingroom_movie == True:
		# this should be off for living room lights
		print "\t*****set state livingroom_normal"
		# lights_off(bedroomLightIDs)
		lights_off(livingroomLightIDs)



	return

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
	# connectDB()
	# insertMsgInDb(pkt[ARP].psrc, pkt[ARP].hwsrc)
	# db.commit()
	# closeDB()
	if pkt[ARP].op == 1:
		print "*****"
		print "\thwsrc: " + pkt[ARP].hwsrc
		print "\tpsrc: " + pkt[ARP].psrc
		# if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
		if pkt[ARP].hwsrc == enjoylifeBtn:
			print "\tpkt[ARP].hwsrc == enjoylifeBtn"
			toggle_low()
		if pkt[ARP].hwsrc == gatoradeBtn:
			print "\tpkt[ARP].hwsrc == gatoradeBtn"
			toggle_bright()
		if pkt[ARP].hwsrc == onBtn:
			print "\tpkt[ARP].hwsrc == onBtn"
			toggle_livingroom()

print "start"
print sniff(prn=arp_display, filter="arp", store=0, count=0)
print "stop"

