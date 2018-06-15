# ring-election-socket-programming
Implementation of the ring coordinator election algorithm using socket programming

Each server represents a process. Each process first sends a handshake signal to the next process and reads its 'failure flag'. If the next process is a failure, the current process starts the election procedure.

Just execute start.py from the terminal to start the election procedure.
