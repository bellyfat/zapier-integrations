# Create JIRA shared projects by Harvest create new project trigger
import requests
import json

baseURL = "https://***.atlassian.net"
url = baseURL+"/rest/api/3/project"
username = "***"
password = "***"
sharedProjectID = "10000";
harvestProjectCode = str(input_data['code']).strip()
harvestProjectName = str(input_data['name']).strip()
print('harvestProjectCode : '+harvestProjectCode+' | harvestProjectName :  '+harvestProjectName)
jiraProjectName = harvestProjectCode+" - "+harvestProjectName
jiraProjectLead = "JIRA-USER-NAME"

print('Create a new shared JIRA project')

url = baseURL+"/rest/project-templates/1.0/createshared/"+sharedProjectID
jsonData = {'key':harvestProjectCode,'name':jiraProjectName,'lead':jiraProjectLead}

response = requests.post(url, auth=(username, password), json=jsonData)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
