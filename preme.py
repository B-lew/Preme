#!/bin/env python2.7

# Run anytime before 10:59:59.
# Polling interval isn't important.
# Ghost checkout timer can be changed by 
# adjusting for loop range near bottom.
# Fill out personal data in checkout payload dict.
# Preload item, color and size. Punctuation is key.
# If multiple items make sure to change loop value.

import sys, json, requests, urllib2
from datetime import datetime, time
import time as t

qty='1'

def UTCtoEST():
    current=datetime.now()
    return str(current) + ' EST'
print

def main():
    global ID
    global variant
    global cw
    req = urllib2.Request('http://www.supremenewyork.com/mobile_stock.json')
    req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
    resp = urllib2.urlopen(req)
    data = json.loads(resp.read())
    ID=0
    for i in range(len(data[u'products_and_categories'].values())):
        for j in range(len(data[u'products_and_categories'].values()[i])):
            item=data[u'products_and_categories'].values()[i][j]
            name=str(item[u'name'].encode('ascii','ignore'))
            # SEARCH WORDS HERE
            # if string1 in name or string2 in name:
            if keyword in name:
                # match/(es) detected!
                # can return multiple matches but you're 
                # probably buying for resell so it doesn't matter
                myproduct=name                
                ID=str(item[u'id'])
                print UTCtoEST(),'::',name, ID, 'found ( MATCHING ITEM DETECTED )'
    if (ID == 0):
        # variant flag unchanged - nothing found - rerun
        t.sleep(poll)
        print UTCtoEST(),':: Reloading and reparsing page...'
        main()
    else:
        print UTCtoEST(),':: Selecting',str(myproduct),'(',str(ID),')'
        jsonurl = 'http://www.supremenewyork.com/shop/'+str(ID)+'.json'
        req = urllib2.Request(jsonurl)
        req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
        resp = urllib2.urlopen(req)
        data = json.loads(resp.read())
        found=0
        for numCW in data['styles']:
            # COLORWAY TERMS HERE
            # if string1 in numCW['name'] or string2 in numCW['name']:
            if color in numCW['name'].title():
                for sizes in numCW['sizes']:
                    # SIZE TERMS HERE
                    if str(sizes['name'].title()) == sz: # Medium
                        found=1;
                        variant=str(sizes['id'])
                        cw=numCW['name']
                        print UTCtoEST(),':: Selecting size:', sizes['name'],'(',numCW['name'],')','(',str(sizes['id']),')'
                        
        if found ==0:
            # DEFAULT CASE NEEDED HERE - EITHER COLORWAY NOT FOUND OR SIZE NOT IN RUN OF PRODUCT
            # PICKING FIRST COLORWAY AND LAST SIZE OPTION
            print UTCtoEST(),':: Selecting default colorway:',data['styles'][0]['name']
            sizeName=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['name'])
            variant=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['id'])
            cw=data['styles'][0]['name']
            print UTCtoEST(),':: Selecting default size:',sizeName,'(',variant,')'

gettime=datetime.now()
currenttime= gettime.time()
while currenttime < time(10,59,59):
        gettime=datetime.now()
        sys.stdout.write("\r" +UTCtoEST()+ ' :: Waiting for 10:59:59')
        sys.stdout.flush()
        currenttime=gettime.time()

poll=1
itemlist = ['Incense','Variety','N/A', 'UZI Tactical','Red', '']	
itemnum = 1
mover = 0

for j in range(0, itemnum):

	print mover

	keyword=itemlist[mover]       # hardwire here by declaring keyword as a string
	mover +=1

	print keyword
	print mover
	
        color=itemlist[mover]                # hardwire here by declaring keyword as a string
	mover +=1

	print color
	print mover

        sz=itemlist[mover]                    # hardwire here by declaring keyword as a string
	mover +=1

	print sz
				
	print UTCtoEST(),':: Parsing page...'

	main()

	print
		
	session=requests.Session()
	addUrl='http://www.supremenewyork.com/shop/'+str(ID)+'/add.json'
	addHeaders={
		'Host':              'www.supremenewyork.com',
		'Accept':            'application/json',
		'Proxy-Connection':  'keep-alive',
		'X-Requested-With':  'XMLHttpRequest',
		'Accept-Encoding':   'gzip, deflate',
		'Accept-Language':   'en-us',
		'Content-Type':      'application/x-www-form-urlencoded',
		'Origin':            'http://www.supremenewyork.com',
		'Connection':        'keep-alive',
		'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',
		'Referer':           'http://www.supremenewyork.com/mobile'
	}
	addPayload={
		'size': str(variant),
		'qty':  '1'
	}
	print UTCtoEST() +' :: Adding product to cart...'
	addResp=session.post(addUrl,data=addPayload,headers=addHeaders)

	print UTCtoEST() +' :: Checking status code of response...'

	if addResp.status_code!=200:
		print UTCtoEST() +' ::',addResp.status_code,'Error \nExiting...'
		print
	elif addResp.json()==[]:
		print UTCtoEST() +' :: Response Empty! - Problem Adding to Cart\nExiting...'
		print
     	else:
		print UTCtoEST() +' :: '+str(cw)+' - '+addResp.json()[0]['name']+' - '+ addResp.json()[0]['size_name']+' added to cart!'

		print

		checkoutUrl='https://www.supremenewyork.com/checkout.json'
		checkoutHeaders={
			'host':              'www.supremenewyork.com',
			'If-None-Match':    '"*"',
               		'Accept':            'application/json',
               		'Proxy-Connection':  'keep-alive',
               		'Accept-Encoding':   'gzip, deflate',
               		'Accept-Language':   'en-us',
               		'Content-Type':      'application/x-www-form-urlencoded',
               		'Origin':            'http://www.supremenewyork.com',
               		'Connection':        'keep-alive',
               		'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',
               		'Referer':           'http://www.supremenewyork.com/mobile'
		}



    #################################
    # FILL OUT THESE FIELDS AS NEEDED
    #################################
    checkoutPayload={
        		'store_credit_id':    '',      
        		'from_mobile':              '1',
        		'cookie-sub':               '%7B%22'+str(variant)+'%22%3A1%7D',       # cookie-sub: eg. {"VARIANT":1} urlencoded
        		'same_as_billing_address':  '1',                                    
        		'order[billing_name]':      'First Last',                              # FirstName LastName
        		'order[email]':             'email@gmail.com',                    # email@domain.com
        		'order[tel]':               '000-000-0000',                           # phone-number-here
        		'order[billing_address]':   '00 Street Name',                        # your address
        		'order[billing_address_2]': '',
        		'order[billing_zip]':       '00000',                                  # zip code
        		'order[billing_city]':      'City',                          # city
        		'order[billing_state]':     'St',                                     # state
        		'order[billing_country]':   'USA',                                    # country
        		'store_address':            '1',                                
        		'credit_card[type]':        'visa',                                   # master or visa
        		'credit_card[cnb]':         '0000 0000 0000 0000',                    # credit card number
        		'credit_card[month]':       '00',                                     # expiration month
        		'credit_card[year]':        '2019',                                   # expiration year
        		'credit_card[vval]':        '000',                                    # cvc/cvv
        		'order[terms]':             '0',
        		'order[terms]':             '1'                
        	}
		
		if mover <4:
			# GHOST CHECKOUT PREVENTION WITH ROLLING PRINT
			for i in range(3):
	        		sys.stdout.write("\r" +UTCtoEST()+ ' :: Sleeping for '+str(3-i)+' seconds to avoid ghost checkout...')
                		sys.stdout.flush()
	        		t.sleep(1)
		print 
		print UTCtoEST()+ ' :: Firing checkout request!'
		checkoutResp=session.post(checkoutUrl,data=checkoutPayload,headers=checkoutHeaders)
		try:
			print UTCtoEST()+ ' :: Checkout',checkoutResp.json()['status'].title()+'!'
		except:
			print UTCtoEST()+':: Error reading status key of response!'
			print checkoutResp.json()
		print 
		print checkoutResp.json()
		if checkoutResp.json()['status']=='failed':
			print
			print '!!!ERROR!!! ::',checkoutResp.json()['errors']
		print 
