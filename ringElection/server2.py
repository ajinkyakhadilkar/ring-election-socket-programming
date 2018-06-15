import socket
import pickle
from time import sleep
from thread import start_new_thread

processes=[9000,9001,9002,9003,9004,9005]
n=len(processes)
myID=1
failure='false'

s = socket.socket()
r = socket.socket()

r.bind(('0.0.0.0',processes[myID]))
r.listen(2)

while True:
	try:
		s.connect(('localhost', processes[(myID+1)%n]))
	except:
		print("FAILED. Sleep briefly & try again")
		sleep(1)
		continue
	
	break



'''
s.send('handshake')#'Handshake from process '+str(myID))
print s

'''
print('HELLO')

#c,addr = r.accept()
#print 'Got connection from' ,addr
#print c

initiatorFlag=False


def client_thread(c):
	global s, electionFlag, initiatorFlag
	try:
		while True:
		
			data= c.recv(1024)
			#c.close()
			if data=='handshake':
				print 'handshake received'
				c.send(failure)
				s.send('handshake')
				data=s.recv(1024)
				
			if data=='false':
				print data
				
			elif data == 'true':
				s.close()
				s=socket.socket()
				print 'Initiating Election'
				s.connect(('localhost',processes[(myID+2)%n]))
				lst=[myID]
				lst=pickle.dumps(lst)
				s.send('election')
				sleep(2)
				s.send(lst)
				print "SENT"
		
			
			elif data == 'election':
				if not initiatorFlag:
					print("HELLO")
					#c,addr=s.accept()
					data=c.recv(1024)
					
					print('election list received')
					

					
					data2=pickle.loads(data)
					#data2=list(data2)
					print data2
					if myID in data2:
						initiatorFlag=True
					if not initiatorFlag:
						data2.append(myID)
						data=pickle.dumps(data2)
						s.send('election')
						sleep(1)
						s.send(data)
					
					
		
					elif initiatorFlag:
				
						print "election data received"
						#data=c.recv(1024)
						#data2=pickle.loads(data)
						print(data2)
					
						coordinator=max(data2)
						print(str(coordinator)+' is the coordinator')
						s.send('leader')
						sleep(1)
						s.send(str(coordinator))
					
					#electionFlag = not electionFlag
					
			elif data=='leader' and not initiatorFlag:
				data=c.recv(1024)
				print(data+'is the coordinator')
				s.send('leader')
				sleep(1)
				s.send(str(data))
			
			elif data=='leader' and initiatorFlag:
				initiatorFlag=False
				
				
	except KeyboardInterrupt:
		c.close()
		s.close()
		r.close()
		
while True:
	c,addr = r.accept()
	start_new_thread(client_thread,(c,))
#s.close()
