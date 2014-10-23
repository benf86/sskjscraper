#coding: utf8
#file: sskj.py

#imports:
import urllib.request
import sys
import re
import threading
import os
from pprint import pprint
import time
#magic:

class GetSskj:
	def __init__(self, numreqs = 1, firsthit = 1):
		self.url = 'http://bos.zrc-sazu.si/cgi/a03.exe?name=sskj_testa&expression=*&hs='	#URL of the 1st page, needs to have number of 1st word on page appended
		self.firsthit = firsthit	#number of the first word on the page
		self.numreqs = numreqs		#which of the requests is this
		self.dicfile = 'dict.txt'	#write words to this file
		self.foo = '<li class="nounderline">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font face="Arial Unicode MS"><b>ametísten</b></font>&nbsp; -tna -o <font size=-1>prid.</font> (<font face="Lucida Sans Unicode">ȋ</font>) <b>1.</b> <i>ki je iz ametistov, z ametisti:</i> ametistni prstan; ametistna ogrlica <b>2.</b> <i>po barvi podoben ametistu:</i> ametistno nebo <font face="Lucida Sans Unicode">♪</font>'

	def getSinglePage(self):
		i = self.firsthit
		print('Getting hits %s to %s' % (i, i + 25))
		url = self.url + str(i)
		response = urllib.request.urlopen(url)	#get the page with hits
		response_read = str()
		foo = 1
		for line in response.readlines():
			try:
				response_read += line.decode('utf-8')
				foo += 1
			except:
				print('Error on page with firsthit: %s' % i)
		self.regexSinglePage(response_read)

	def regexSinglePage(self, response):
		onlyResults = response.split('<ol start=%s>' % self.firsthit, 1)[1].split('</ol>', 1)[0]
		f = open('words%s.html' % self.numreqs, 'a')
		f.write(onlyResults)
		f.close()
		self.parseSinglePage() #parse it

	def parseSinglePage(self):
		f2 = open('dict.html', 'a')
		f2.write('<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"></HEAD><BODY>')
		f = open('words%s.html' % self.numreqs)
		i = self.firsthit
		for line in f.readlines():
			if re.search('^<li', line):
				if len(line) > 3:
					word = '%s. %s' % (i, line.split('<b>', 1)[1].split('</b>', 1)[0])
					print('\t\t\t%s' % word)
					word += '<br>'
					f2.write(word)
					i += 1
		f2.write('</BODY></HTML>')
		f2.close()
		f.close()



class MyThreads:
	def __init__(self, lasthit = 25):
		self.threads = lasthit // 25 #number of threads to run
		if lasthit < 26:
			self.threads = 1
		elif lasthit % 25 != 0:
			self.threads += 1
		self.makeThreads()

	def makeThreads(self):
		i = 1
		for thread in range(1, self.threads+1):
			print('Thread %s running\n\n' % thread)
			foo = GetSskj(thread, i)
			t = threading.Thread(target=GetSskj.getSinglePage(foo))
			t.start()
			i += 25

		self.cleanUp()

	def cleanUp(self):
		for i in range(1, self.threads + 1):
			os.remove('words%s.html' % i)
		print('\n\n\nAll clean and done!')

MyThreads(int(sys.argv[1]))

