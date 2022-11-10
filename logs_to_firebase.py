#!/usr/bin/python3

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import datetime
import subprocess


def timeDiffAsSecond(date1,date2):
    delta = date2-date1
    return delta.total_seconds()


# Sservice account key
cred = credentials.Certificate('*.json') # Edit

# Initialize granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://*.firebaseio.com' # Edit
})

# Admin has access to read and write all data without of security rules
ref = db.reference('systems') # Edit: 'systems' = root of the records 
#print(ref.get())

# Get date logged
logDate =  datetime.datetime.now()

# Log CPU load that is five minute statistic (second one)
log = subprocess.getoutput('top -n 1 -b | head -n 1')
cpuLoad = log.split(', ')[-2]
cpuLoad = cpuLoad.replace(',','.',1)
cpuLoad = float(cpuLoad)

# Log GPU informations
log = subprocess.getoutput('nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,temperature.gpu --format=csv,noheader')
log = log.replace("%","")
gpu0 = list(map(float, (log.split("\n")[0].split(", ")[1:4])));
gpu1 = list(map(float, (log.split("\n")[1].split(", ")[1:4])));
gpu2 = list(map(float, (log.split("\n")[2].split(", ")[1:4])));
gpu3 = list(map(float, (log.split("\n")[3].split(", ")[1:4])));
header = ["utilization.gpu [%]", "utilization.memory [%]", "temperature.gpu [C]"]

users_ref = ref.child('core-rl') # Edit : Server name
users_ref.set({ 
    'date': str(logDate),
    'cpuLoad': cpuLoad,
    'gpu': header,
    'gpu0' : gpu0,
    'gpu1' : gpu1,
    'gpu2' : gpu2,
    'gpu3' : gpu3
    })

# Logmessage includes
# date, cpuload; gpu-util, gpu-mem-util and  gpu-temp for each gpu
