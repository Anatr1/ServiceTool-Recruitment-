#!/usr/bin/python3
import subprocess
import os
import time
import curses

#Execute with superuser privileges
PATH = "/absolute/path/to/file"  #CHANGE THIS BEFORE EXECUTING!

services = open(PATH+"/services.txt", "r").read().split()

scr = curses.initscr()

def display_services():
	global services
	i = 1
	for srv in services:
		scr.addstr(int(i+2), 0, "                                                         ")
		scr.addstr(int(i+2), 0, "\t>"+str(i)+": "+srv+"\t" + "-"+str(get_service_status(srv)), curses.A_BOLD)
		i += 1
	
	scr.addstr(10,0,"")

def execute_command(command, service):
	try:
		command = "systemctl "+str(command).lower()+" "+services[int(service)-1]
		os.system(command)
	except:
		scr.addstr(10, 0, "Error while executing command\n")

def get_service_status(service):
	result = subprocess.run(['systemctl', 'is-active', str(service)], stdout=subprocess.PIPE)
	return str(result.stdout)[2:-3]

def service(user_input):
	fields = str(user_input).split()
	if len(fields) is 2:
		fields[0] = fields[0][2:]
		fields[1] = fields[1][:-1]

	try:
		if len(fields) is not 2 or str(fields[0]).lower() not in ["start", "stop"] or int(fields[1]) not in range(1,len(services)+1):
			scr.addstr(10, 0,"Enter ")
			scr.addstr(10, 6, "Start/Stop", curses.A_BOLD)
			scr.addstr(10, 16, " <service index> to start or stop a service\n")
			return

		else:
			execute_command(fields[0], fields[1])
	except:
		scr.addstr(10, 0, "Some banana happened\n")

scr.addstr(0, 0, "Welcome to ServiceTool!", curses.A_BOLD)
scr.addstr(1, 0, "Services currently monitoring: ")

display_services()

scr.addstr(8, 0, "Enter ")
scr.addstr(8, 6, "Start/Stop", curses.A_BOLD)
scr.addstr(8, 16, " <service index> to start or stop a service\n\n")
scr.refresh()

try:
	while True:
		#service(input())
		service(scr.getstr())
		time.sleep(0.99) # ;)
		display_services()
		scr.clrtoeol()
		scr.refresh()
except KeyboardInterrupt:
    print("Interrupted...")

curses.endwin()
print("Goodbye :-)")
