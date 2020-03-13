from bs4 import BeautifulSoup
import requests
import queue
import string
from html.parser import HTMLParser
# coding=utf-8

count=0
q=queue.Queue(maxsize=1000)

f2=open("text.txt","w")

start = "chainstoreage.com"
links = []
docid = 1
q.put(start)
while (q.qsize()>0 and not queue.Queue.full(q)):
	url = q.get()
	if count==0:	
		r  = requests.get("http://"+url)
		
	elif url.startswith('/') and url not in links:
		url2="http://"+start+url
		r  = requests.get(url2)
		
	else:
		continue
		
	data = r.text
	soup = BeautifulSoup(data,'lxml')
	content_urls = []
	for link in soup.find_all('a'):
		no1=link.get('href')

		if no1 != None and no1.startswith('/') and '/cdn-cgi/l/email-protection' not in no1 and len(no1) != 1 and len(no1) > 20:

			content_url = "http://" + start + no1
			
			if content_url not in content_urls:
				print('---------- url ----------')
				print(content_url)
				r  = requests.get(content_url)
				soup = BeautifulSoup(r.text, 'html.parser')
				data = soup.select('div.field-paragraph--field-text-area')
				
				for x in data:
					# print('---------- x ----------')
					# print(x)
					content = x.findAll('p')
					if content != None:
						
						# print('---------- content ----------')
						# print(content)
						print()
						# print('---------- text ----------')
						# article = ''
						
						for p in content:
							if p != None:
								paragraph = p.text
								print()
								print('---------- paragraph ----------')
								print(paragraph.replace('\n', '').replace('\r', ''))
								print()
								refined = paragraph.replace('\n', '').replace('\r', '')
								refined = refined.replace('\'', '').replace('\"', '').replace('	', ' ')
								id = 'doc' + str(docid)
								f2.write('{\"id\": \"' + id + '\", \"text\": \"' + refined +'\"}\n')
								docid = docid + 1
							
						print()
				content_urls.append(content_url)

			if no1.startswith('/') and no1 not in q.queue and not queue.Queue.full(q):
				q.put(no1)
				count+=1
	links.append(url)

print('----- DONE -----')

