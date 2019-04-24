'''
Call JIRA & Harvest APIs
Version 1.0
'''
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth

# JIRA Configurations
JIRA_EMAIL = "****"
JIRA_TOKEN = "****"
BASE_URL = "https://****.atlassian.net"
BASIC_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
JIRA_HEADERS = {'Content-Type' : 'application/json;charset=iso-8859-1'}

JIRA_TASK_ID = input_data['issue_key']

# Harvest Configurations
HARVEST_ACCOUNT_ID = "****"
HARVEST_BASE_URL = "https://api.harvestapp.com/v2"
HARVEST_TOKEN = "****"
HARVEST_HEADERS = {
    "User-Agent": "Python Harvest API Sample",
    "Authorization": "Bearer " + HARVEST_TOKEN,
    "Harvest-Account-ID": HARVEST_ACCOUNT_ID,
    "Content-Type": "application/json"
}
# default page = 1 contains 100 records
HARVEST_CLIENT_PAGES = 5
HARVEST_PROJECT_PAGES = 10
HARVEST_PROJECT_CODES = []
HARVEST_INCREMENT_NUMBERS = []
HARVEST_FORMATTED_PROJECT_CODES = []

class JIRA(object):
# JIRA Class

    def get_issue_details(self, jira_issue_id):
        # Get JIRA issue details by issue key
        api_url = "/rest/api/3/issue/"+str(jira_issue_id)
        api_url = BASE_URL+api_url
        request_response = requests.get(
            url=api_url,
            headers=JIRA_HEADERS,
            auth=BASIC_AUTH
            )
        # print(json.dumps(json.loads(request_response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        json_response = json.loads(request_response.text)
        return json_response

    def update_issue_details(self, jira_issue_id, json_payload):
        # Update JIRA issue details by issue key
        ''' 
        # Payload sample
        """{ "fields": {"summary": "new summary"} }"""
        '''
        api_url = "/rest/api/2/issue/"+str(jira_issue_id)
        api_url = BASE_URL+api_url
        print(api_url)
        request_response = requests.put(
            url=api_url,
            data=json_payload,
            headers=JIRA_HEADERS,
            auth=BASIC_AUTH
            )
        print(request_response)    
        # print(json.dumps(json.loads(request_response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return request_response

class Harvest(object):
# Harvest Class

    def get_client_list(self, page_no):
        harvest_api_url = HARVEST_BASE_URL + "/clients?page="+str(page_no)
        response = requests.get(
            url=harvest_api_url,
            headers=HARVEST_HEADERS
            )
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        json_response = json.loads(response.text)
        return json_response

    def get_project_list(self, page_no):
        # Get Harvest project list
        harvest_api_url = HARVEST_BASE_URL + "/projects?page="+str(page_no)
        response = requests.get(
            url=harvest_api_url,
            headers=HARVEST_HEADERS
            )
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        json_response = json.loads(response.text)
        return json_response

    def get_client_id(self, client_name):
        # Get Harvest client list
        for pageno in range(HARVEST_CLIENT_PAGES):
            pageno += 1
            json_response = self.get_client_list(pageno)

            # Filter the Harvest Project ID
            harvest_client_id = 0
            if client_name is None:
                print('Client name is not defined!')
            else:
                for client in json_response['clients']:
                    if client_name == client['name']:
                        harvest_client_id = client['id']
                        # print(harvest_client_id)
                        return harvest_client_id

    def get_latest_project_code(self, project_key, client_name):
        # Get latest Harvest project increment code

        if client_name is None or project_key is None:
            print('Client Name or Project Key is not defined!')
        else:
            for pageno in range(HARVEST_PROJECT_PAGES):
                pageno += 1
                json_response = self.get_project_list(pageno)

                # Filter the Harvest Project Codes related to Client Name
                for project in json_response['projects']:
                    project_code = project['code']
                    project_client_name = project['client']['name']
                    # print(project_code)
                    # print(project_client_name)
                    # Filter the Harvest Project Codes related to Project Key
                    if client_name == project_client_name:
                        filtered_project_key = str(project_code)[:3]
                        # print(filtered_project_key)
                        if project_key == filtered_project_key:
                            HARVEST_PROJECT_CODES.append(project_code)

            # Generate the new increment number
            for harvest_code in HARVEST_PROJECT_CODES:
                increment_number = str(harvest_code)[-4:]
                # print('increment_number : '+str(increment_number))
                HARVEST_INCREMENT_NUMBERS.append(increment_number)

            # print(HARVEST_INCREMENT_NUMBERS)
            HARVEST_INCREMENT_NUMBERS.sort(reverse=True)
            generated_increment_number = int(HARVEST_INCREMENT_NUMBERS[0]) + 1
            # print(generated_increment_number)
            return generated_increment_number

    def generate_harvest_code(self, project_key, client_name):
        # Generate new Harvest Project code
        current_date = datetime.datetime.now()
        current_year = current_date.year
        formatted_year = str(current_year)[-2:]
        increment_number = self.get_latest_project_code(project_key, client_name)
        old_harvest_code = str(project_key)+str(formatted_year)+str(int(increment_number)-1)
        new_harvest_code = str(project_key)+str(formatted_year)+str(increment_number)
        # print('old harvest code : '+str(old_harvest_code))
        # print('new harvest code : '+str(new_harvest_code))
        HARVEST_FORMATTED_PROJECT_CODES.append(old_harvest_code)
        HARVEST_FORMATTED_PROJECT_CODES.append(new_harvest_code)
        return HARVEST_FORMATTED_PROJECT_CODES


# Get JIRA details
JIRAOBJ = JIRA()
JSON_RESPONSE = JIRAOBJ.get_issue_details(JIRA_TASK_ID)

SOW_CLIENT_CARD_KEY = JSON_RESPONSE['fields']['issuelinks'][0]['inwardIssue']['key']
SOW_CLIENT_SUMMARY = JSON_RESPONSE['fields']['issuelinks'][0]['inwardIssue']['fields']['summary']
SOW_SUMMARY = JSON_RESPONSE['fields']['summary']
SOW_SUMMARY_TITLE = "SOW Description"
SOW_SPLIT_ARRAY = SOW_SUMMARY.split("-")
for summary in SOW_SPLIT_ARRAY:
    SOW_SUMMARY_TITLE = summary
# Processing the client card task
JSON_RESPONSE = JIRAOBJ.get_issue_details(SOW_CLIENT_CARD_KEY)
CLIENT_CARD_KEY = JSON_RESPONSE['key']
CLIENT_NAME = JSON_RESPONSE['fields']['summary']
# Get Harvest details
# Get Harvest client ID
HARVESTOBJ = Harvest()
HARVEST_CLIENT_ID = HARVESTOBJ.get_client_id(CLIENT_NAME)
# Get generated harvest code
HARVEST_CODE_KEY = 'MID'
HARVEST_CODES = HARVESTOBJ.generate_harvest_code(HARVEST_CODE_KEY, CLIENT_NAME)
# print(HARVEST_CODES)
HARVEST_OLD_CODE = HARVEST_CODES[0]
HARVEST_NEW_CODE = HARVEST_CODES[1]
JIRA_ISSUE_SUMMARY = '"'+HARVEST_NEW_CODE+" - "+SOW_SUMMARY_TITLE+'"'
# Update the JIRA task summary
JSON_PAYLOAD = """{ "fields": {"summary": """+JIRA_ISSUE_SUMMARY+"""} }"""
JIRAOBJ.update_issue_details(JIRA_TASK_ID, JSON_PAYLOAD)

output = [{'client_key': CLIENT_CARD_KEY, 'client_name': CLIENT_NAME, 'new_harvest_code': HARVEST_NEW_CODE, 'old_harvest_code': HARVEST_OLD_CODE, 'sow_summary': SOW_SUMMARY_TITLE, 'harvest_client_id': HARVEST_CLIENT_ID}]
