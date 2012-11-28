#!/usr/bin/python

import os

cpu=[]
mem=[]
net=[]

def dump(l):
  i=1
  for item in l:
    print("%d:" % i)
    for k in item:
      print("  %s: %s" % (k, item[k]) )
    i+=1
  print("")

def parse(l):
  info={}
  for line in lines:
    t=line.split(": ")
    if len(t) < 2:
      continue
    name=t[0].strip()
    value=t[1].strip()
    info[name]=value
  return info 

data = os.popen("/usr/sbin/dmidecode").read()
sectors=data.split("\n\n")
for sector in sectors:
  lines=sector.split("\n")
  if len(lines) < 3:
    continue
  title=lines[1]
  info=parse(lines)
  if title == 'Processor Information':
    cpu.append({'type':info['Version'],'cores':info['Core Enabled'],'threads':info['Thread Count']})
  if title == 'Memory Device':
    if not info['Size'].startswith('No'):
      mem.append({'size':info['Size']})

data = os.popen("/sbin/ip -o -f inet addr").read()
lines = data.split("\n")
for line in lines:
  items = line.split()
  if len(items) < 4:
    continue
  net.append({'name':items[1],'addr':items[3]})


print("[OS]")
os.system('/bin/uname -nsr')
print(open('/etc/issue.net').readline())

print("[CPU]")
dump(cpu)

print("[Memory]")
lines=open('/proc/meminfo').readlines()
info=parse(lines)
print("total: %s ; swap: %s" % (info['MemTotal'], info['SwapTotal']))
dump(mem)


print("[FS]")
os.system('/bin/df -h')
print("")

print("[Net]")
dump(net)

