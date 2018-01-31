#!/usr/bin/env python
# encoding: utf-8

#
# Write by Bob
# zhangbo3@

import os,sys
import getopt,re
import socket,threading,urllib2

def usage():
        print '# This is check the URI or Socket of the script  #'
        print 'Usage:'
        print "      %s -d URL; This is Http protocol" %sys.argv[0]
	print "      %s -s socket IP or domain; This is Socket protocol" %sys.argv[0]
	print "      %s -p port; This is Socket port" %sys.argv[0]
	print "      %s -n ; Total number of requests" %sys.argv[0]
	print "      %s -c ; Number of concurrent requests" %sys.argv[0]
	print "      %s -t ; Timeout time(s),socket default is 1s,http default is 5s" %sys.argv[0]
        print "For exampale: %s -d www.weibo.com/index.php -n 200 -c 10 -t 2" %sys.argv[0]
	print "For exampale: %s -s 10.210.214.249 -p 80 -n 200 -c 50 -t 3" %sys.argv[0]

def Detect_url(url,sign):
	if timeout:
		time = int(timeout)
	else:
		time = 5
	urllib2.socket.setdefaulttimeout(time)
	request = urllib2.Request('http://%s' %(url))
	try:
		ret = urllib2.urlopen(request)
	except urllib2.URLError,e:
		if hasattr(e,"reason"):
			port_timeout.append('1')
		elif hasattr(e,"code"):
			if re.findall('^3\d*','%s' %e.code):
				port_normal.append('1')
			if re.findall('^404\d*','%s' %e.code):
				port_404.append('1')
                        if re.findall('^403\d*','%s' %e.code):
                                port_403.append('1')
                        if re.findall('^500\d*','%s' %e.code):
                                port_500.append('1')
			if re.findall('^502\d*','%s' %e.code):
				port_502.append('1')
                        if re.findall('^503\d*','%s' %e.code):
                                port_503.append('1')
		else:		
			port_other.append('1')
	else:
                port_normal.append('1')

def Detect_socket(server,port):
	sign = 0
        if timeout:
                time = int(timeout)
        else:
                time = 1
	   
	socket.setdefaulttimeout(time)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	try:
		ret = s.connect((server, int(port)))
	except socket.error, e:
		if re.findall('^timed\ out*','%s' %e):
			socket_timeout.append('1')
			sign = 1
		else:
			print '%s' %e
			sys.exit(2)
	else:
		socket_normal.append('1')
		sign = 1
	if sign == 0:
		s.close()

def print_out():
	if url_mod:
		print 'URL:'
	        print 'timeout:[%s]' %len(port_timeout)
        	print 'normal:[%s]' %len(port_normal)
        	print '\033[;31mError_403:[%s]\tError_404:[%s]\033[0m' %(len(port_403),len(port_404))
        	print '\033[;31mError_500:[%s]\tError_502:[%s]\tError_503:[%s]\033[0m' %(len(port_500),len(port_502),len(port_503))
		print '\033[;31mError_other:[%s]\033[0m' %len(port_other)
		
	if sock_mod:
		print 'Socket:'
	        print 'timeout:[%s]' %len(socket_timeout)
       	 	print 'normal:[%s]' %len(socket_normal)
				

def main():
	if sock_mod:
		dest_arg1 = sock_mod
		dest_arg2 = dport
		dest_function = Detect_socket		
	elif url_mod:
		dest_arg1 = url_mod
		dest_arg2 = ''
		dest_function = Detect_url
	else:
		sys.exit()
		
	total = int(dcount)
	concurrent = int(dconcurrent)
        n = 0
        sign = 0
	lastnu = total%concurrent


        while 1:

                threads = []
                if n + concurrent > total:
                        nloops = range(n,total)
                        sign = 1
                else:
                        nloops = range(n,n+concurrent)

                for i in nloops:
                        t = threading.Thread(target=dest_function,args=(dest_arg1,dest_arg2))
                        threads.append(t)
                if sign == 1:
                        th_nu = lastnu
                else:
                        th_nu = concurrent

                for i in range(th_nu):
                        threads[i].start()

                for i in range(th_nu):
                        threads[i].join()

                n = n + concurrent

                if sign == 1:
                        break

	print_out()

	
if __name__=='__main__':
	try:
		opts,args=getopt.getopt(sys.argv[1:],"hd:s:p:n:c:t:")
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	port_timeout = []
	port_normal = []
	port_403= []
	port_404 = []
	port_500 = []
	port_502 = []
	port_503 = []
	port_other = []
	socket_normal = []
	socket_timeout = []
	dcount = 0
	url_mod = ''
	sock_mod = ''
	dport = ''
	dconcurrent = 0
	timeout = 0

	if opts:
		for opt,arg in opts:
			if opt == '-h':
				usage()
				sys.exit()
			if opt == '-d':
				url_mod = arg
			if opt == '-s':
				sock_mod = arg
			if opt == '-p':
				dport = arg
			if opt == '-n':
				dcount = arg
			if opt == '-c':
				dconcurrent = arg
			if opt == '-t':
				timeout = arg
		if url_mod and dcount and dconcurrent:
			main()
		elif sock_mod and dport and dcount and dconcurrent:
			main()
		else:
			usage()

        else:
		usage()
		sys.exit()
	
