# To Generate a new token key
# https://accounts.zoho.com/apiauthtoken/nb/create?SCOPE=ZohoCRM/crmapi&EMAIL_ID=email@email.com&PASSWORD=****&DISPLAY_NAME=Test-Prototype
# version 1.0.0

#https://accounts.zoho.com/developerconsole
#https://www.zoho.com/crm/developer/docs/api/auth-request.html
#scope=ZohoCRM.modules.ALL

import json
import requests
from datetime import datetime, timedelta

# API methods - https://www.zoho.com/crm/developer/docs/api/api-methods.html

SLACK_BASE_URL = "https://slack.com/api"
SLACK_TOKEN = "****"
SLACK_HEADERS = {
    'Content-Type': 'application/json;charset=iso-8859-1',
   'Authorization': 'Bearer '+SLACK_TOKEN
}

ZOHO_TOKEN ='****'

class Zohocrm(object):

   def get_records(self, module_name, start_record = "1", end_record = "200"):

       api_url = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRecords?authtoken="+ZOHO_TOKEN+"&scope=crmapi&fromIndex="+str(start_record)+"&toIndex="+str(end_record)
       print(api_url)
    #    API_HEADERS = {
    #        "Authorization": "Zoho-oauthtoken "+ZOHO_TOKEN
    #    }
       # GET Request
       request_response = requests.get(
           url=api_url
           )
    #    print(json.dumps(json.loads(request_response.text), sort_keys=True, indent=4, separators=(",", ": ")))
       json_response = json.loads(request_response.text)
       return json_response

   def get_related_records(self, module_name, parent_module, module_id, start_record = "1", end_record = "200"):

       # Get 2 hours earlier modified records
       # Date time calculation
       AEDT_utc_timegap = 11 # UTC + 11
       AEDT_time_zone = datetime.utcnow() + timedelta(hours=+AEDT_utc_timegap)
       #print('AEDT_time_zone now : ')
       #print(AEDT_time_zone)
       #now = datetime.now()
       now = AEDT_time_zone
       #print("now =", now)

       datetime_format = "%Y-%m-%d %H:%M:%S"
       current_datetime = now.strftime(datetime_format)
       current_datetime = datetime.strptime(current_datetime, datetime_format)
       #print("current_datetime =", current_datetime)	
       hourEarlier = (datetime.now() + timedelta(hours=-2))
       datetime_hourearlier = hourEarlier.strftime(datetime_format)
       schedule_datetime = datetime.strptime(datetime_hourearlier, datetime_format)

       api_url = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRelatedRecords?authtoken="+ZOHO_TOKEN+"&scope=crmapi&fromIndex="+str(start_record)+"&toIndex="+str(end_record)+"&version=4&parentModule="+parent_module+"&id="+module_id+"&lastModifiedTime="+str(schedule_datetime)
       print(api_url) 
    #    API_HEADERS = {
    #        "Authorization": "Zoho-oauthtoken "+ZOHO_TOKEN
    #    }
       # GET Request
       request_response = requests.get(
           url=api_url
           )
       #print(json.dumps(json.loads(request_response.text), sort_keys=True, indent=4, separators=(",", ": ")))
       json_response = json.loads(request_response.text)
       return json_response

   def get_notes(self, parent_module, parent_module_record_id, start_record = "1", end_record = "200"):

       #parent_module_record_id = str(****)
       module_name = 'Notes'
       parent_module = parent_module
       module_id = parent_module_record_id
       account_notes = self.get_related_records(module_name, parent_module, module_id, start_record, end_record)
       return account_notes
    

class Slack(object):

   def send_message(self,channel_name, message):
       #print(channel_name)
       #print(message)
       slack_url = SLACK_BASE_URL+"/chat.postMessage"
       slack_jsondata = {
           'channel': channel_name,
           'text': message
           }
       slack_channel_response =\
           requests.post(slack_url, json=slack_jsondata, headers=SLACK_HEADERS)
       #print(json.dumps(
       #    json.loads(slack_channel_response.text),
       #    sort_keys=True, indent=4, separators=(",", ": ")
       #    ))

   def get_channel_list(self):
       # Get all the slack channel list
       # Require channels:read permission to Slack App
       slack_url = SLACK_BASE_URL+"/channels.list"
       slack_response = requests.get(
         url=slack_url,
         headers=SLACK_HEADERS
       )
       #print(json.dumps(json.loads(slack_response.text), sort_keys=True, indent=4, separators=(",", ": ")))
       json_response = json.loads(slack_response.text)
       return json_response

   def filter_channel_id_by_name(self, channel_name):
       # Get the slack channel id by its name
       channel_list = self.get_channel_list()
       for channel in channel_list['channels']:
         slack_channel_name = channel['name']
         # print(channel_name)
         if slack_channel_name == channel_name:
           slack_channel_id = channel['id']
           return slack_channel_id

   def get_channel_history(self,channel_id,count):
       #print(channel_id)
       slack_url = SLACK_BASE_URL+"/channels.history?channel="+channel_id+"&count="+count
       slack_channel_response =\
           requests.get(slack_url,headers=SLACK_HEADERS)
       #print(json.dumps(
       #    json.loads(slack_channel_response.text),
       #    sort_keys=True, indent=4, separators=(",", ": ")
       #    ))
       json_response = json.loads(slack_channel_response.text)
       return json_response

   def get_channel_last_bot_message(self, channel_name, count):
       slack_channel_id = slackObj.filter_channel_id_by_name(channel_name)
       #print('slack_channel_id')
       #print(slack_channel_id)
       channel_messages = self.get_channel_history(slack_channel_id, count)
       channel_messages_list = []
       #print('channel_messages')
       #print(channel_messages) 
       if 'messages' in channel_messages:
         for channel_message in channel_messages['messages']:
           if 'subtype' in channel_message:
             #print('channel message: ')
             #print(channel_message['text'])
             channel_messages_list.append(channel_message['text'])
       return channel_messages_list

# Objectives

zohoObj = Zohocrm()
slackObj = Slack()

# Get 2 hours earlier modified records
# Date time calculation
AEDT_utc_timegap = 11 # UTC + 11
AEDT_time_zone = datetime.utcnow() + timedelta(hours=+AEDT_utc_timegap)
#print('AEDT_time_zone now : ')
#print(AEDT_time_zone)
#now = datetime.now()
now = AEDT_time_zone
#print("now =", now)

datetime_format = "%Y-%m-%d %H:%M:%S"
current_datetime = now.strftime(datetime_format)
current_datetime = datetime.strptime(current_datetime, datetime_format)
#print("current_datetime =", current_datetime)	
hourEarlier = (datetime.now() + timedelta(hours=-2))
datetime_hourearlier = hourEarlier.strftime(datetime_format)
schedule_datetime = datetime.strptime(datetime_hourearlier, datetime_format)

# Testing
#zohoaccounts = zohoObj.get_records(record_module_name);
#all_zoho_accounts = zohoaccounts['response']['result']['Accounts']['row']

#print('all_zoho_accounts')
#print(len(all_zoho_accounts))

# Testing an account notes
# account_id = '****'
# module = 'Accounts'
# zohonotes = zohoObj.get_notes(module, account_id)
# print('zoho notes')
# print(zohonotes)

all_messages_array = []

# =======================================
# process zoho account module

record_module_name = 'Accounts'
items_per_page = 200
total_records = 400
total_pages = total_records / items_per_page
total_pages = int(total_pages)
current_page = 1
start_record = 1
slack_channel_account_messages_array = {}

#print('total_pages : '+str(total_pages))

all_accounts_array = []

while current_page <= total_pages:
    end_record = int(current_page) * int(items_per_page)
    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohoaccounts = zohoObj.get_records(record_module_name, start_record, end_record);
    #print('zohoaccounts : ')
    #print(zohoaccounts)
    if 'result' in zohoaccounts['response']:
        all_zoho_accounts = zohoaccounts['response']['result']['Accounts']['row']

        # print('response all_zoho_accounts')
        # print(len(all_zoho_accounts))

        # Zoho Account data
        for account_row in all_zoho_accounts:
            account_content_array = account_row['FL']
            #print('account_content_array')
            #print(account_content_array)
            dictionary_account_array = {}
            
            for account in account_content_array:
                
                # check array index order
                #print(account)
                
                if account['val'] == 'ACCOUNTID':
                    account_id = account['content']
                
                if account['val'] == 'Account Name':
                    account_name = account['content']
                
                if account['val'] == 'Last Activity Time':
                    account_last_activity_time = account['content']

                if account['val'] == 'Slack Channel':
                    account_channel = account['content']
                    #print(account_channel)
                    #check latest activity time
                    activity_datetime = datetime.strptime(account_last_activity_time, datetime_format)
                    if schedule_datetime <= activity_datetime <= current_datetime:
                        #print('added account info..')
                        dictionary_account_array.update({'accountname': account_name})
                        dictionary_account_array.update({'account_slack_channel': account_channel})
                        dictionary_account_array.update({'accountid': account_id})
                        #print('account ID: ')
                        #print(account_id)
                        all_accounts_array.append(dictionary_account_array)
                
        # print('all_accounts_array')
        # print(all_accounts_array)

    # next page
    start_record = end_record + 1 
    current_page += 1

#print('account name list')
#print(all_accounts_array)

# call zoho notes of each accounts
counter = 0
for account in all_accounts_array:
    counter += 1
    # print(account)
    account_id = account['accountid']
    #print('Account Count : '+str(counter))
    #print('current page : '+str(current_page)+' : total_pages : '+str(total_pages))
    #print('account ID : '+str(account_id))
    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohonotes = zohoObj.get_notes(record_module_name, account_id, 1, 30)
    #print('zohonotes')
    #print(zohonotes)
    if 'result' in zohonotes['response']:
        all_zoho_notes = zohonotes['response']['result']['Notes']['row']
        
        if not isinstance(all_zoho_notes, list): # verify single note available account also an array
            all_zoho_notes = [all_zoho_notes]
        #print('all_zoho_notes before loop')
        #print(all_zoho_notes)
        # Notes data
        all_notes_array = []
        dictionary_notes_array = {}

        for note_row in all_zoho_notes:
            #print('note_row')
            #print(note_row)    
            if 'FL' in note_row:
                note_content_array = note_row['FL']
                #print('note_content_array')  
                #print(note_content_array)
                for note in note_content_array:
                    if note['val'] == 'Note Content':
                        note_content = note['content']
                        dictionary_notes_array = {'note': note_content}
                    
                    if note['val'] == 'Modified Time':
                        modified_date_time = note['content']  
                        dictionary_notes_array.update({'datetime': modified_date_time})
                        all_notes_array.append(dictionary_notes_array)

        #print('notes result')
        #print(all_notes_array)
        desc_all_zoho_notes = list(reversed(all_notes_array)) #reverse the array order
    
        #print('desc_all_zoho_notes')
        #print(desc_all_zoho_notes)

        for note_data in desc_all_zoho_notes:
            #print(note_data['datetime'])
            #print(note_data['note'])
            note_datetime = datetime.strptime(note_data['datetime'], datetime_format)
            #print('current_datetime : '+str(current_datetime))
            #print('note_datetime : '+str(note_datetime))
            #print('schedule_datetime : '+str(note_datetime))
            if schedule_datetime <= note_datetime <= current_datetime:
                print('ZOHO Accounts Module - within past 2 hours')
                #print('account id')
                #print(account['accountid'])
                note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                print(note_message)
                # check previous slack channel messages
                if 'account_slack_channel' in account:
                    slack_channel_name = account['account_slack_channel']
                    slack_channel_account_messages_array = {'account_slack_channel': slack_channel_name}
                    slack_channel_account_messages_array.update({'message': note_message})
                    all_messages_array.append(slack_channel_account_messages_array)
                else:
                    print('No account slack channel for '+str(account['accountname']))

            # else:
                #print('past')  
                #note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                #print(note_message)
            #     print('account name')
            #     print(account['accountname'])
            #     print('account id')
            #     print(account['accountid'])
            #     print(record_module_name+' : '+note_data['note'])
            #     print('No notes to post in channel within last hour!')

# =======================================
# process zoho contacts module

record_module_name = 'Contacts'
items_per_page = 200
total_records = 2000
total_pages = total_records / items_per_page
total_pages = int(total_pages)
current_page = 1
start_record = 1
slack_channel_contact_messages_array = {}
all_contacts_array = []

#print('total_pages : '+str(total_pages))

while current_page <= total_pages:
    end_record = current_page * items_per_page
    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohocontacts = zohoObj.get_records(record_module_name, start_record, end_record);
    #print('zohocontacts : ')
    #print(zohocontacts)
    if 'result' in zohocontacts['response']:
        all_zoho_contacts = zohocontacts['response']['result']['Contacts']['row']

        #print('response all_zoho_contacts')
        #print(len(all_zoho_contacts))

        # Zoho Contacts data
        dictionary_contact_array = {}

        for contact_row in all_zoho_contacts:
            contact_content_array = contact_row['FL']
            #print('contact_content_array')
            #print(contact_content_array)
            for contact in contact_content_array:
                # check array index order
                #print('contact:')
                #print(contact)
                if contact['val'] == 'CONTACTID':
                    contact_id = contact['content']

                if contact['val'] == 'ACCOUNTID':
                    account_id = contact['content']

                if contact['val'] == 'Last Activity Time':
                    account_last_activity_time = contact['content']

                    activity_datetime = datetime.strptime(account_last_activity_time, datetime_format)
                    if schedule_datetime <= activity_datetime <= current_datetime:
                        #print('added contact info..')
                        # get the account slack channel name
                        account_slack_channel = ''
                        account_name = ''
                        for account_info in all_accounts_array:
                            if (account_id == account_info['accountid']):
                                if 'account_slack_channel' in account_info:
                                    account_slack_channel = account_info['account_slack_channel']
                                else:    
                                    account_slack_channel = ''
                        
                        for account_info in all_accounts_array:
                            if (account_id == account_info['accountid']):
                                account_name = account_info['accountname']
                        
                        if account_slack_channel != '':
                            dictionary_contact_array = {'contactid': contact_id}
                            dictionary_contact_array.update({'accountid': account_id})
                            dictionary_contact_array.update({'accountname': account_name})
                            dictionary_contact_array.update({'account_slack_channel': account_slack_channel})
                            all_contacts_array.append(dictionary_contact_array)

    # next page
    start_record = end_record + 1 
    current_page += 1

#print('contacts module - all_contacts_array')
#print(all_contacts_array)

# call zoho notes of each contacts
for contact in all_contacts_array:
    #print(account)
    contact_id = contact['contactid']

    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohonotes = zohoObj.get_notes(record_module_name, contact_id, 1, 30)
    #print('zohonotes')
    #print(zohonotes)
    if 'result' in zohonotes['response']:
        all_zoho_notes = zohonotes['response']['result']['Notes']['row']
        #print('account id : ')
        #print(account_id)
        if not isinstance(all_zoho_notes, list): # verify single note available account also an array
            all_zoho_notes = [all_zoho_notes]
        #print('all_zoho_notes before loop')
        #print(all_zoho_notes)
        # Notes data
        all_notes_array = []
        dictionary_notes_array = {}

        for note_row in all_zoho_notes:
            #print('note_row')
            #print(note_row)    
            if 'FL' in note_row:
                note_content_array = note_row['FL']
                #print('note_content_array')
                #print(note_content_array)
                for note in note_content_array:
                    if note['val'] == 'Note Content':
                        note_content = note['content']
                        dictionary_notes_array = {'note': note_content}
                    
                    if note['val'] == 'Modified Time':
                        modified_date_time = note['content']  
                        dictionary_notes_array.update({'datetime': modified_date_time})
                        all_notes_array.append(dictionary_notes_array)

        #print('notes result')
        #print(all_notes_array)
        desc_all_zoho_notes = list(reversed(all_notes_array)) #reverse the array order
    
        #print('desc_all_zoho_notes')
        #print(desc_all_zoho_notes)

        for note_data in desc_all_zoho_notes:
            #print(note_data['datetime'])
            #print(note_data['note'])
            note_datetime = datetime.strptime(note_data['datetime'], datetime_format)
            #print('current_datetime : '+str(current_datetime))
            #print('note_datetime : '+str(note_datetime))
            #print('schedule_datetime : '+str(note_datetime))
            if schedule_datetime <= note_datetime <= current_datetime:
                print('ZOHO Contacts Module - within past 2 hours')
                #print('account id')
                #print(account['accountid'])
                note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                print(note_message)
                # check previous slack channel messages
                if 'account_slack_channel' in account:
                    slack_channel_name = account['account_slack_channel']
                    slack_channel_contact_messages_array = {'account_slack_channel': slack_channel_name}
                    slack_channel_contact_messages_array.update({'message': note_message})
                    all_messages_array.append(slack_channel_contact_messages_array)
                else:
                    print('No account slack channel for '+str(account['accountname']))

            # else:
                #print('past')  
                #note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                #print(note_message)
            #     print('account name')
            #     print(account['accountname'])
            #     print('account id')
            #     print(account['accountid'])
            #     print(record_module_name+' : '+note_data['note'])
            #     print('No notes to post in channel within last hour!')

# =======================================
# process zoho deals module

record_module_name = 'Deals'
items_per_page = 200
total_records = 400
total_pages = total_records / items_per_page
total_pages = int(total_pages)
current_page = 1
start_record = 1
slack_channel_deal_messages_array = {}
all_deals_array = []
        
#print('total_pages : '+str(total_pages))

while current_page <= total_pages:
    end_record = current_page * items_per_page
    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohodeals = zohoObj.get_records(record_module_name, start_record, end_record);
    #print('zohodeals : ')
    #print(zohodeals)
    if 'result' in zohodeals['response']:
        all_zoho_deals = zohodeals['response']['result']['Deals']['row']

        #print('response all_zoho_deals')
        #print(len(all_zoho_deals))

        # Zoho Deals data
        dictionary_deal_array = {}

        for deal_row in all_zoho_deals:
            deal_content_array = deal_row['FL']
            #print('deal_content_array')
            #print(deal_content_array)
            for deal in deal_content_array:
                #print('deal:')
                #print(deal)
                if deal['val'] == 'DEALID':
                    deal_id = deal['content']
                    dictionary_deal_array = {'dealid': deal_id}

                if deal['val'] == 'ACCOUNTID':
                    account_id = deal['content']

                if deal['val'] == 'Last Activity Time':
                    account_last_activity_time = deal['content']
                    
                    activity_datetime = datetime.strptime(account_last_activity_time, datetime_format)
                    if schedule_datetime <= activity_datetime <= current_datetime:
                        #print('added deal info..')
                        # get the account slack channel name
                        account_slack_channel = ''
                        account_name = ''
                        for account_info in all_accounts_array:
                            if (account_id == account_info['accountid']):
                                if 'account_slack_channel' in account_info:
                                    account_slack_channel = account_info['account_slack_channel']
                                else:    
                                    account_slack_channel = ''
                        
                        for account_info in all_accounts_array:
                            if (account_id == account_info['accountid']):
                                account_name = account_info['accountname']
                        
                        if account_slack_channel != '':
                            dictionary_deal_array.update({'accountid': account_id})
                            dictionary_deal_array.update({'accountname': account_name})
                            dictionary_deal_array.update({'account_slack_channel': account_slack_channel})
                            all_deals_array.append(dictionary_deal_array)
                            #print(dictionary_deal_array)

    # next page
    start_record = end_record + 1 
    current_page += 1

#print('deals module - all_deals_array')
#print(all_deals_array)

# call zoho notes of each deals
for deal in all_deals_array:
    #print(deal)
    deal_id = deal['dealid']

    # call API
    #print('start_record : '+str(start_record)+' | '+' end_record : '+str(end_record)+' | '+' current_page : '+str(current_page))
    zohonotes = zohoObj.get_notes(record_module_name, deal_id, 1, 30)
    #print('zohonotes')
    #print(zohonotes)
    if 'result' in zohonotes['response']:
        all_zoho_notes = zohonotes['response']['result']['Notes']['row']
        #print('account id : ')
        #print(account_id)
        if not isinstance(all_zoho_notes, list): # verify single note available account also an array
            all_zoho_notes = [all_zoho_notes]
        #print('all_zoho_notes before loop')
        #print(all_zoho_notes)
        # Notes data
        all_notes_array = []
        dictionary_notes_array = {}

        for note_row in all_zoho_notes:
            #print('note_row')
            #print(note_row)    
            if 'FL' in note_row:
                note_content_array = note_row['FL']
                #print('note_content_array')
                #print(note_content_array)
                for note in note_content_array:
                    if note['val'] == 'Note Content':
                        note_content = note['content']
                        dictionary_notes_array = {'note': note_content}
                    
                    if note['val'] == 'Modified Time':
                        modified_date_time = note['content']  
                        dictionary_notes_array.update({'datetime': modified_date_time})
                        all_notes_array.append(dictionary_notes_array)

        #print('notes result')
        #print(all_notes_array)
        desc_all_zoho_notes = list(reversed(all_notes_array)) #reverse the array order
    
        #print('desc_all_zoho_notes')
        #print(desc_all_zoho_notes)

        for note_data in desc_all_zoho_notes:
            #print(note_data['datetime'])
            #print(note_data['note'])
            note_datetime = datetime.strptime(note_data['datetime'], datetime_format)
            #print('current_datetime : '+str(current_datetime))
            #print('note_datetime : '+str(note_datetime))
            #print('schedule_datetime : '+str(note_datetime))
            if schedule_datetime <= note_datetime <= current_datetime:
                print('ZOHO Deals Module - within past 2 hours')
                #print('account id')
                #print(account['accountid'])
                note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                print(note_message)
                # check previous slack channel messages
                if 'account_slack_channel' in account:
                    slack_channel_name = account['account_slack_channel']
                    slack_channel_deal_messages_array = {'account_slack_channel': slack_channel_name}
                    slack_channel_deal_messages_array.update({'message': note_message})
                    all_messages_array.append(slack_channel_deal_messages_array)
                else:
                    print('No account slack channel for '+str(account['accountname']))    
                
            # else:
                #print('past')  
                #note_message = 'Zoho '+record_module_name+' : '+account['accountname']+' : '+note_data['note'] 
                #print(note_message)
            #     print('account name')
            #     print(account['accountname'])
            #     print('account id')
            #     print(account['accountid'])
            #     print(record_module_name+' : '+note_data['note'])
            #     print('No notes to post in channel within last hour!')
                
# #print('all_messages_array : ')
# #print(all_messages_array)

slack_messages_count = '20'
for message_data in all_messages_array:
  if 'account_slack_channel' in message_data:
    #print('channel name : ')
    #print(message_data['account_slack_channel'])  
    channel_last_messages_list = slackObj.get_channel_last_bot_message(message_data['account_slack_channel'], slack_messages_count)
    #print('channel_last_messages_list')
    #print(channel_last_messages_list)
    if message_data['message'] not in channel_last_messages_list:
      # post message in slack channel
      print('post message in '+str(message_data['account_slack_channel'])+' : message : '+str(message_data['message']))
      #slackObj.send_message(message_data['account_slack_channel'], message_data['message'])          
  else:
    print('No account slack channel found!')          
  
