import os
import time

os.system("gnome-terminal --geometry=49x20+460+0 -e 'bash -c \"python server2.py; exec bash\"'")
os.system("gnome-terminal --geometry=49x20+920+0 -e 'bash -c \"python server3.py; exec bash\"'")
os.system("gnome-terminal --geometry=49x20+0+450 -e 'bash -c \"python server4.py; exec bash\"'")
os.system("gnome-terminal --geometry=49x20+460+450 -e 'bash -c \"python server5.py; exec bash\"'")
os.system("gnome-terminal --geometry=49x20+920+450 -e 'bash -c \"python server6.py; exec bash\"'")
os.system("gnome-terminal --geometry=49x20+0+0 -e 'bash -c \"python server1.py; exec bash\"'")

