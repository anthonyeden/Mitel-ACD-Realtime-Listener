import sys
import socket
import json
import io
import time


HOST = "192.168.201.2"
PORT = 15373


agents = dict()
groups = dict()
paths = dict()
allData = dict()
allData['agents'] = dict()
allData['groups'] = dict()
allData['paths'] = dict()
lastDataWrite = time.time()
lastDataUpdate = 0


def isACDNumber(num):
	try:
		float(num)
		return True
	except ValueError:
		return False




if __name__ == "__main__":
	
	json_data = open('mitel_data.json')
	jsondata = json.load(json_data)
	json_data.close()
	
	agents = jsondata['agents']
	groups = jsondata['groups']
	paths = jsondata['paths']
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	while 1:
		try:
			data = s.recv(1024)
			commandType = data[3:4]
		
			if commandType == "A":
				agents[data[17:21]] = "in"
				lastDataUpdate = time.time()
				print "Agent " + data[17:21] + " Logged In"
			
			elif commandType == "B":
				agents[data[17:21]] = "out"
				lastDataUpdate = time.time()
				print "Agent " + data[17:21] + " Logged Out"
			
			elif commandType == "C":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " enabled DND"
				else:
					print "Extension " + data[10:13] + " enabled DND"
			
			elif commandType == "D":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "idle"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " disabled DND"
				else:
					print "Extension " + data[10:13] + " disabled DND"
			
			elif commandType == "E":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " made busy"
				else:
					print "Extension " + data[10:13] + " made busy"
			
			elif commandType == "F":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "idle"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " unmade busy"
				else:
					print "Extension " + data[10:13] + " unmade busy"
			
			elif commandType == "G":
				agents[data[17:21]] = "busy"
				lastDataUpdate = time.time()
				print "Agent " + data[17:21] + " Answered Call from path " + data[11:14]
			
			elif commandType == "H":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Answered Personal Call"
				else:
					print "Extension " + data[10:13] + " Answered Personal Call"
				
			elif commandType == "I":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Made Call"
				else:
					print "Extension " + data[10:13] + " Made Call"
			
			elif commandType == "J":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "idle"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Idle"
				else:
					print "Extension " + data[10:13] + " Idle"
			
			elif commandType == "L":
				agents[data[17:21]] = "timer"
				lastDataUpdate = time.time()
				print "Agent " + data[17:21] + " Work Timer started"
			
			elif commandType == "M":
				agents[data[17:21]] = "idle"
				lastDataUpdate = time.time()
				print "Agent " + data[17:21] + " Work Timer ended"
			
			elif commandType == "N":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Placed Call on Hold"
				else:
					print "Extension " + data[10:13] + " Placed Call on Hold"
				
			elif commandType == "O":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "busy"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Retreived Call on Hold"
				else:
					print "Extension " + data[10:13] + " Retreived Call on Hold"
				
			elif commandType == "P":
				if isACDNumber(data[17:21]):
					agents[data[17:21]] = "idle"
					lastDataUpdate = time.time()
					print "Agent " + data[17:21] + " Dropped Call on Hold"
				else:
					print "Extension " + data[10:13] + " Dropped Call on Hold"
			
			# not sure about this one? not documented
			elif commandType == "T":
				print "Agent " + data[17:21] + " Sent Call"
			
			
			
			#Group Report - not sure what the trailing zeroes are
			elif commandType == "K":
				if not groups.has_key(data[10:13]):
					groups[data[10:13]] = dict()
				
				groups[data[10:13]]['waiting'] = data[13:16]
				groups[data[10:13]]['agents'] = data[16:19]
				groups[data[10:13]]['longestwait'] = data[19:23]
				lastDataUpdate = time.time()
				
				print "Group Report: " + data[10:13] + ". " + data[13:16] + " Calls Waiting. " + data[16:19] + " Agents Logged In."
				print "Longest Call Held Time: " + data[19:21] + ":" + data[21:23]
			
			
			
			#Path Report
			elif commandType == "Q":
				if not paths.has_key(data[10:13]):
					paths[data[10:13]] = dict()
				
				paths[data[10:13]]['waiting'] = data[13:16]
				paths[data[10:13]]['agents'] = data[16:19]
				paths[data[10:13]]['longestwait'] = data[19:23]
				lastDataUpdate = time.time()
				
				print "Path Report: " + data[10:13] + ". " + data[13:16] + " Calls Waiting. " + data[16:19] + " Agents Logged In."
				print "Longest Call Held Time: " + data[19:21] + ":" + data[21:23]
			
			
			
			elif commandType == "R":
				#keep alive data
				bloopy = "no"
			
			
			
			else:
				print data
				
			
			
			if lastDataWrite < lastDataUpdate:
				#Update the JSON file on disk
				allData['agents'] = agents
				allData['groups'] = groups
				allData['paths'] = paths
				allData['lastUpdate'] = lastDataUpdate
				
				with open('mitel_data.json', 'w') as outfile:
					json.dump(allData, outfile)
					lastDataWrite = time.time()
					print "Wrote to mitel_data.json"
					print
			
		except:
			print "Loop exception"
		
	s.close()





