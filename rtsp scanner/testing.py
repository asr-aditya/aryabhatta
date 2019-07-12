import re
import os

os.system("arp.exe -a > ip_mac.txt")


f=open("ip_mac.txt", "r")
if f.mode == 'r':
    #ip addresses
    contents =f.read()

    RE1 = '(?:\d{1,3}\.)+(?:\d{1,3})'
    RE2 = '(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)'
#s = '*some string* 100/64h *some string* 120h/90 *some string* abc 200/100 abc *some string* 100h/100f'


    p = re.compile('('+RE2+'|'+RE1+')');
    matches = p.findall(contents)

print(matches)

ips = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})',matches)

print(ips)
