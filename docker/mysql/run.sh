#!/usr/bin/python

import consul
import MySQLdb
import time
import signal
import os
import socket
import subprocess
import json


def graceful_shutdown():
        pass

#handle sigterm to gracefully shutdown processes.
def handler(signum, frame):
        print 'Signal handler called with signal', signum
        try:
                conn = MySQLdb.connect(host=connectobject["host"], user=connectobject["user"]\
                               , passwd=connectobject["passwd"], db=connectobject["database"])
                curs = conn.cursor()
        
                curs.execute("select database()")

                clustername = curs.fetchone()[0]
                curs.close()
                conn.close()
        except:
                clustername = os.environ["DATABASE"]
                
        consulhandle = consul.Consul()
        consulhandle.kv.delete("/datastore/"+clustername, recurse=True)
        consulhandle.agent.service.deregister(clustername)
        subprocess.call(["consul", "leave"])

        raise IOError("Data Store Shutdown.")

os.system("cat /etc/hosts.local >> /etc/hosts")
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGILL, handler)
signal.signal(signal.SIGFPE, handler)
signal.signal(signal.SIGABRT, handler)
signal.signal(signal.SIGSEGV, handler)

connectobject = {}

connectobject["host"] = os.environ["SQLHOST"]
connectobject["user"] = os.environ["USERNAME"]
connectobject["passwd"] = os.environ["PASSWD"]
connectobject["database"] = os.environ["DATABASE"]

consulMaster = os.environ["CONSUL_MASTERS"]

clustername = os.environ["DATABASE"]
subprocess.Popen(["/usr/bin/consul", "agent"\
                #,  "-config-file", "crateNode.json"\
                , "-data-dir", "/consul-data"\
                , "-config-dir", "/consul-data"\
                ,"-join", consulMaster])


time.sleep(3)

# loop forever
while True:

        conn = MySQLdb.connect(host=connectobject["host"], user=connectobject["user"]\
                               , passwd=connectobject["passwd"], db=connectobject["database"])
        curs = conn.cursor()

        try:

                # Get the list of tables from the cluster.
                curs.execute("select table_name from information_schema.tables where table_schema = '%s' " % clustername )

                tags = []
                for table in curs.fetchall():
                        tags.append(table[0])

                # Get the name of the Crate Cluster
                curs.execute("select database();")

                clustername = curs.fetchone()[0]
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
                        consulhandle.agent.service.register(name=clustername, tags=tags)
                        consulhandle.kv.put("/datastore/"+clustername+"-type", "mysql")
                        consulhandle.kv.put("/datastore/"+clustername+"-connect", json.dumps(connectobject))
        except:
                consulhandle = consul.Consul()
                consulhandle.agent.service.deregister(clustername)

        # Sleep 15 seconds and do it again.
        conn.close()
        time.sleep(15)

