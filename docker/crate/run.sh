#!/usr/bin/python
import consul
from crate import client
import time
import signal
import os
import socket
import subprocess

#handle sigterm to gracefully shutdown processes.
def handler(signum, frame):
	print 'Signal handler called with signal', signum
	conn = client.connect()
	curs = conn.cursor()

	curs.execute("select name from sys.cluster")
	
	clustername = curs.fetchone()[0]	
	curs.close()
	consulhandle = consul.Consul()
	consulhandle.agent.service.deregister(clustername)
	subprocess.call(["consul", "leave"])
	subprocess.call(["/etc/init.d/crate", "graceful-stop"])

	raise IOError("Data Store Shutdown.")

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGILL, handler)
signal.signal(signal.SIGFPE, handler)
signal.signal(signal.SIGABRT, handler)
signal.signal(signal.SIGSEGV, handler)

clustername = "crate"

if os.environ.has_key("CLUSTER_NAME"):
	clustername = os.environ["CLUSTER_NAME"]
else:
	os.environ["CLUSTER_NAME"]="crate"
	
os.environ['NODE_NAME'] = os.environ['HOSTNAME']
consulMaster = os.environ["CONSUL_MASTERS"]

subprocess.call(["/etc/init.d/crate", "restart"])
subprocess.Popen(["/usr/bin/consul", "agent"
		#,  "-config-file", "crateNode.json"
		, "-data-dir", "/consul-data"
		, "-config-dir", "/consul-data"
		,"-join", consulMaster])

time.sleep(30)

# loop forever
while True:
		
	conn = client.connect()
	curs = conn.cursor()

	try:
			
		# Get the name of the Crate Cluster
		curs.execute("select name from sys.cluster")
		
		clustername = curs.fetchone()[0]	
		
		# Get the list of tables from the cluster.	
		curs.execute("select table_name from information_schema.tables where schema_name = 'doc'")
		
		tags = []
		for table in curs.fetchall():
			tags.append(table[0])
		curs.close()
		
		# Now register the Service with the consul cluster.
		consulhandle = consul.Consul()
		services = consulhandle.agent.services()
		if services.has_key(clustername):
			serviceInfo = services[clustername]
		else:
			serviceInfo = None

		tableList = None
		if serviceInfo != None:
			tableList = serviceInfo["Tags"]
		if tableList != tags:
			consulhandle.agent.service.register(name=clustername, port=4200, tags=tags)
			consulhandle.kv.put(clustername+"-type", "crate")
	except:
		consulhandle = consul.Consul()
		consulhandle.agent.service.deregister(clustername)
		
	# Sleep 15 seconds and do it again.
	time.sleep(15)
