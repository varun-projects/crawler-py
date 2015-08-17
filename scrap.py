from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import string
import re

meriList=[];
mainlink="";

def traverselink(link):
		pageFile = urllib2.urlopen(link)
		pageHtml = pageFile.read()
		pageFile.close()
		soup = BeautifulSoup(pageHtml)
		a=soup.findAll("a")
		verifyappend(a,'href',link)
		img=soup.findall("img")
		verifyappend(img,"src",link)
		script=soup.findall("script")
		verifyappend(script,"src",link)
		lnk=soup.findall("link")
		verifyappend(lnk,"href",link)
		form=soup.findall("form")
		verifyappend(form,"action",link)
		
def verifyappend(tag,attr,link):
		global mainlink
		l=len(mainlink)
		for x in tag:
				try:
						#if(x[attr][-1:] != "/"): 
						#x[attr] += "/"
							
						if (x[attr] == "/") :
							continue
							
						if x[attr][:8]=='https://':
							continue
							
						if  x[attr][:7] == 'http://' :
							if(((not [x[attr],0] in meriList) and ( not [x[attr],1] in meriList) and (not '#' in x[attr]))) :
								if(getresponsecode(x[attr])==200 and (x[attr])[:l]==mainlink):
									meriList.append([x[attr],0])
									print '1'+x[attr]
		
						elif x[attr][:3]=='www':
							if(((not ['http://'+x[attr],0] in meriList) and (not ['http://'+x[attr],1] in meriList)and (not '#' in x[attr]))) :
								if(getresponsecode('http://'+x[attr])==200 and ('http://'+x[attr])[:l]==mainlink):
									meriList.append(['http://'+x[attr],0])
									print '2'+'http://'+x[attr]
									
						elif x[attr][:1]=='/' :
							x[attr] =  x[attr][1:]					
							if((( not [mainlink+x[attr],0] in meriList) and ( not [mainlink+x[attr],1] in meriList)and (not '#' in x[attr]))) :
								if(getresponsecode(mainlink+x[attr])==200):
									meriList.append([mainlink+x[attr],0])	
									print '3'+mainlink+x[attr]
									
						elif ((( not [mainlink+'/'+x[attr],0] in meriList) and ( not [mainlink+'/'+x[attr],1] in meriList)and (not '#' in x[attr]))) :							
							if(getresponsecode(link+'/'+x[attr])==200 ):
								meriList.append([mainlink+'/'+x[attr],0])
								print '4'+mainlink+'/'+x[attr]
								
						else:
							continue
				except :
					continue
		print "----------------------------------------------------------"
		
def printlist():
	
		for x in meriList:
			try:
				if(x[1]!=1):
					print x[0]
					print "========================================================="
					traverselink(x[0])
					x[1]=1		
			except:
				continue
			

def getresponsecode(url):
		try:
			connection = urllib2.urlopen(url,timeout=20)
			return connection.getcode()
		except urllib2.HTTPError, e:
			return e.getcode()
		
def main():
		link="http://lucideus.com/"
		global mainlink
		mainlink=link
		print getresponsecode(link)
		if(getresponsecode(link)==200):
			meriList.append([link,0]);		
			printlist()
		else:
			print "Page doesn't exist"
		for x in meriList:
			print x[0]+"--------*---------*----------*"
		
if __name__ == "__main__":
    main()
