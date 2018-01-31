#!/usr/bin/env python
# encoding: utf-8

import os,sys
import json,getopt
import urllib2,threading
sys.path.append('/etc/dAppCluster')
import dpool_lib

def usage():
	print '# This is check the URI of the script  #'
	print 'Usage:'
	print "      %s -u URL; default is '/'" %sys.argv[0]
	print '      %s -a; Open the alarm function, for example Email,SMS. default is off' %sys.argv[0]

def Detect_url(ip,uri):
	sing = 0
	urllib2.socket.setdefaulttimeout(5)
	request = urllib2.Request('http://%s/%s' %(ip,uri))
	request.add_header('Host','v5.weibo.com')
	try:
		ret = urllib2.urlopen(request)
#		print ret.info()
	except Exception:
		ips_port.append(ip)
		sing = 1
	if sing != 1:
		print ret.code
		if ret.code != 200:
			print 'error: %s' %ip
		
def Get_iplist():	 
	Slist = []
        List = {"weibo":{"180.149.134.18":"be-dpool-weibo-cookie-v5-ug","123.125.104.197":"pool_weibo.com_v3.6_v4"}}
        for key in List['weibo']:
		response = os.popen("curl -s 'http://dpadmint.grid.sina.com.cn/api/lbapi_getfe.php?vip=%s&groupby=node_ip&port=80&pool=%s'" %(key,List['weibo'][key])).readline()
		s = json.read(response)
		for re in s:
			Slist.append(re['node_ip'])
	return Slist

def send_alatrm(type,sb,msg,es):
	if es == 'sms':	
		os.popen("/etc/dAppCluster/send_alert.pl --sv DPool --service 'web'  --object %s --subject %s --content %s --mailto 'zhangbo3' --msgto 'zhangbo3'" %(type,sb,msg))
	else:	
		os.popen("/etc/dAppCluster/send_alert.pl --sv DPool --service 'web'  --object %s --subject %s --content %s --mailto 'zhangbo3'" %(type,sb,msg))

def main():
	n = 0
	sign = 0
	plist = ['10.73.31.40','10.73.31.42','10.73.13.66','10.55.22.21']
#	plist = Get_iplist()
	lastnu = len(plist)%50

	while 1:

		threads = []
		if n + 50 > len(plist):
			nloops = range(n,len(plist))
			sign = 1
		else:
			nloops = range(n,n+50)
		
		for i in nloops:
			t = threading.Thread(target=Detect_url,args=(plist[i],''))
			threads.append(t)
		if sign == 1:
			th_nu = lastnu
		else:
			th_nu = 50

		for i in range(th_nu):
			threads[i].start()

		for i in range(th_nu):
			threads[i].join()

		n = n + 50

		if sign == 1:
			break

	if ips_port:
		content = ",".join(ips_port)
		send_alatrm('httpport','weibo','IPS:\ %s\ port\ 80\ Unavailable' %content,'')
		


if __name__=='__main__':
	try:
		opts,args=getopt.getopt(sys.argv[1:],"hu:x:a")
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	ips_port = []
	ips_code = []

	if opts:
		for opt,arg in opts:
			if opt == '-h':
				usage()
				sys.exit()
			if opt == '-u':
				duri = arg
			if opt == '-a':
				alarm = 1
				
	else:
		main()
	


