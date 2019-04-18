# Call JIRA API with HTTPBasicAuth
import json
import requests
from requests.auth import HTTPBasicAuth

JIRA_EMAIL = "****"
JIRA_TOKEN = "****"
BASE_URL = "https://****.atlassian.net"
API_URL = "/rest/api/3/issue/{TASK-KEY}"

API_URL = BASE_URL+API_URL

print("API URL : "+str(API_URL))

BASIC_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {'Content-Type' : 'application/json;charset=iso-8859-1'}

response = requests.get(
    API_URL,
    headers=HEADERS,
    auth=BASIC_AUTH
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
json_response = json.loads(response.text)
# Get issue links summary
print(json_response['fields']['issuelinks'][0]['inwardIssue']['fields']['summary'])
