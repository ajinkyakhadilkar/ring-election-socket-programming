import socket
import pickle
from time import sleep
from thread import start_new_thread

processes=[9000,9001,9002,9003,9004,9005] #port number of each process
n=len(processes)
myID=0
failure='false'	# a failure flag which denotes if a process is failed or not

s= socket.socket()
r= socket.socket()
r.bind(('0.0.0.0',processes[myID]))
r.listen(2)
while True:
	try:
		s.connect(('localhost', processes[(myID+1)%n]))
	except:
		print("Waiting for connection...")
		sleep(1)
		continue
	
	break
s.send('handshake')
print s

print('HELLO')

failData=s.recv(1024)


initiatorFlag = False	# a flag to tell if the current node is the one conducting election


def client_thread(c):
	global s, failData ,initiatorFlag
	try:
		while True:
	
			data = c.recv(1024)
			
			if data == 'handshake':
				print 'handshake received'
				c.send(failure)
	
		
			if data == 'false' or failData=='false':
				print 'Failure status of process '+str((myID+1)%n)+' : '+str(failData)
				failData=''
				
				
			elif data == 'true' or failData=='true':
				failData=''
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
					data=c.recv(1024)
					
					print('election list received')
					

					
					data2=pickle.loads(data)
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
						print(data2)
					
						coordinator=max(data2)
						print('Process '+str(coordinator)+' is the coordinator')
						s.send('leader')
						sleep(1)
						s.send(str(coordinator))
					
								
			elif data=='leader' and not initiatorFlag:
				data=c.recv(1024)
				print('Process '+data+' is the coordinator')
				s.send('leader')
				sleep(1)
				s.send(str(data))
			
			elif data=='leader' and initiatorFlag:
				initiatorFlag=False
				
	
	except KeyboardInterrupt:	
		#close the sockets in case of a keyboard interrupt
		c.close()	
		s.close()	
		r.close()
		print "sockets closed"
		
while True:
	c,addr=r.accept()
	start_new_thread(client_thread,(c,))
