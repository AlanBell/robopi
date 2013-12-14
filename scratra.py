# scratra ~ 0.3
# greatdane ~ easy python implementation with scratch
# inspired by sinatra(sinatrarb.com) ~ code snippets from scratch.py(bit.ly/scratchpy)
import socket
from errno import *
from array import array
import threading

# Errors from scratch.py
class ScratchConnectionError(Exception): pass   
class ScratchNotConnected(ScratchConnectionError): pass
class ScratchConnectionRefused(ScratchConnectionError): pass
class ScratchConnectionEstablished(ScratchConnectionError): pass

class ScratchInvalidValue(Exception): pass

broadcast_map = {}
update_map = {}
start_list = []
end_list = []
scratchSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

runtime_quit = 0
scratchInterface = None

# Implementation for Scratch variables
class RemoteSensors:
    
    sensor_values = {}
    
    def __setitem__(self, sensor_name, value):
        if isinstance(value, str):
            v = Scratch.toScratchMessage('sensor-update "' + sensor_name +'" "'+value+'"')
            self.sensor_valueues[sensor_name] = value
            scratchSocket.send(v)
        elif isinstance(value, int) or isinstance(value, float):
            v = Scratch.toScratchMessage('sensor-update "' + sensor_name +'" ' + str(value))
            self.sensor_valueues[sensor_name] = value
            scratchSocket.send(v)
        else:
            raise ScratchInvalidValue(sensor_name + ': Incorrect attempted value')
        
    def __getitem__(self, sensor_name):
        return self.sensor_values[sensor_name]
        
# For general convenience, scratch interface
class Scratch:
    
    # Variables interface
    sensor = RemoteSensors()
    var_values = {}
    
    # Broadcast interface
    def broadcast(self, *broadcasts):
        for broadcast_name in broadcasts:
            scratchSocket.send(self.toScratchMessage('broadcast "' + broadcast_name + '"'))
        
    # Variable interface
    def var(self, var_name):
        return self.var_values[var_name]
        
    @staticmethod   
    def toScratchMessage(cmd):
        # Taken from chalkmarrow
        n = len(cmd)
        a = array('c')
        a.append(chr((n >> 24) & 0xFF))
        a.append(chr((n >> 16) & 0xFF))
        a.append(chr((n >>  8) & 0xFF))
        a.append(chr(n & 0xFF))
        return a.tostring() + cmd

    @staticmethod
    def atom(msg):
        try:
            return int(msg)
        except:
            try:
                return float(msg)
            except:
                return msg.strip('"')

def run(host='localhost', poll=True, msg="Scratra -> Connected\n-> 'stop' to quit", console=True):
    runClass(host, poll, msg, console).start()

# actual threading process
class runClass(threading.Thread):

    def __init__(self, host, poll, msg, console):
        self.host = host
        self.poll = poll
        self.msg = msg
        self.console = console
        threading.Thread.__init__(self)

    def run(self):
        host = self.host
        poll = self.poll
        port = 42001
        console = self.console
        while 1:
            try: scratchSocket.connect((host, port))
            # Except series from scratch.py
            except socket.error as error:
                (err, msge) = error
                if err == EISCONN:
                    raise ScratchConnectionEstablished('Already connected to Scratch')
                elif poll == True:
                    continue
                elif err == ECONNREFUSED:
                    raise ScratchConnectionRefused('Connection refused, try enabling remote sensor connections')
                else:
                    raise ScratchConnectionError(msge)
            scratchInterface = Scratch()
            break
        if console:
            run_console(self.msg).start()
        for func in start_list:
            func(scratchInterface)
        while not runtime_quit:
            scratchSocket.settimeout(3)
            try:
                msg = scratchSocket.recv(1024)
            except socket.timeout:
                msg = ''#timeouts just mean we listen again, if we never timeout then we can hang whilst shutting down
            except socket.error as (errno, message):
                raise ScratchConnectionError(errno, message)
            if msg:
                # If the message is not a sensor-update, but a broadcast
                if msg.find('sensor-update')==-1 and 'broadcast' in msg:
                    msg = msg[15:-1]
                    if msg in broadcast_map:
                        for func in broadcast_map[msg]:
                            func(scratchInterface)
                # Otherwise, it must be a sensor-update
                else:
                    msg = msg[4:]
                    if 'sensor-update' in msg:
                        msg = msg.split()[1:]
                        i = 0
                        while i < len(msg)-1:
                            if scratchInterface.atom(msg[i]) in update_map:
                                scratchInterface.var_values[scratchInterface.atom(msg[i])] = scratchInterface.atom(msg[i+1])
                                for func in update_map[scratchInterface.atom(msg[i])]:
                                    func(scratchInterface, scratchInterface.atom(msg[i+1]))
                            i+=2
                            
class run_console(threading.Thread):

    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)
        
    def run(self):
        global runtime_quit
        print self.msg
        while not runtime_quit:
            cmd = raw_input('-> ')
            if cmd == 'stop':
                runtime_quit = 1
                print '-> Quitting'
                for func in end_list:
                    func(scratchInterface)
        

# For user convenience, decorator methods

# When Scratch broadcasts this...
# @broadcast('scratch_broadcast')
# def func(scratch): ....
class broadcast:
    
    def __init__(self, broadcast):
        self.b = broadcast
        
    def __call__(self, func):
        if self.b in broadcast_map:
            broadcast_map[self.b].append(func)
        else:
            broadcast_map[self.b] = [func]
        
# When this variable is updated...
# @update('variable')
# def func(scratch, value): ...
class update:
    
    def __init__(self, update):
        self.u = update
        
    def __call__(self, func):
        if self.u in update_map:
            update_map[self.u].append(func)
        else:
            update_map[self.u] = [func]

# When we start listening...
# @start
# def func(scratch): ...
def start(func):
    if func not in start_list:
        start_list.append(func)

# When we stop listening
# @end
# def func(scratch): ...
def end(func):
    if func not in end_list:
        end_list.append(func)
