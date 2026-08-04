import os
import datetime
print("=" * 50)
print("     DEVOPS SYSTEM MONITOR")
print("=" * 50)

#Get disk
result = os.popen("df -h").read()
print("Disk size: ", result)
print("=" * 50)
#Get memory
memory = os.popen("free -h").read()
print("Memory size: ",  memory)
print("=" * 50)

#Get uptime
up_time = os.popen("uptime").read()
print("uptime: ", up_time)
print("=" * 50)
#Get processes
processes = os.popen("ps aux --sort=-%cpu |head -6 | tail -5").read()
print("procesess: " , processes)
print("=" * 50)
#Get date and time
now = datetime.datetime.now()
print("Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))
