# Create JIRA task in Harvest by creating JIRA event web hook
import requests
import json
import xml.etree.ElementTree as ET

baseURL = "https://***.harvestapp.com"
username = "****"
password = "****"
jiraProjectCode = str(input_data['issueProjectKey']).strip()
jiraTaskName = str(input_data['issueSummary']).strip()
harvestProjectID = 0;

print('Get all the Harvest Projects')

url = baseURL+"/projects"
headers = {'Content-Type' : 'application/xml', 'Accept' : 'application/xml', 'User-Agent' : 'PHP Wrapper Library for Harvest API'} 

response = requests.get(url, auth=(username, password), headers=headers)

'''
<Element 'id' at 0x7f95b7b02f98>
<Element 'client-id' at 0x7f95b7b02ef8>
<Element 'name' at 0x7f95b7b17048>
<Element 'code' at 0x7f95b7b17228>
<Element 'active' at 0x7f95b7b17278>
<Element 'bill-by' at 0x7f95b7b172c8>
<Element 'budget' at 0x7f95b7b17318>
<Element 'budget-by' at 0x7f95b7b17368>
<Element 'notify-when-over-budget' at 0x7f95b7b173b8>
<Element 'over-budget-notification-percentage' at 0x7f95b7b17408>
<Element 'over-budget-notified-at' at 0x7f95b7b17458>
<Element 'show-budget-to-all' at 0x7f95b7b174a8>
<Element 'created-at' at 0x7f95b7b174f8>
<Element 'updated-at' at 0x7f95b7b17548>
<Element 'starts-on' at 0x7f95b7b17598>
<Element 'ends-on' at 0x7f95b7b175e8>
<Element 'estimate' at 0x7f95b7b17638>
<Element 'estimate-by' at 0x7f95b7b17688>
<Element 'is-fixed-fee' at 0x7f95b7b176d8>
<Element 'billable' at 0x7f95b7b17728>
<Element 'hint-earliest-record-at' at 0x7f95b7b17778>
<Element 'hint-latest-record-at' at 0x7f95b7b177c8>
<Element 'notes' at 0x7f95b7b17818>
<Element 'hourly-rate' at 0x7f95b7b17868>
<Element 'cost-budget' at 0x7f95b7b178b8>
<Element 'cost-budget-include-expenses' at 0x7f95b7b17958>
'''
# Filter the web hook selected project code
xmlTree = ET.ElementTree(ET.fromstring(response.text))
root = xmlTree.getroot()
for child in root:
    print("Harvest Project ID : "+child[0].text+" | Project Code : "+child[3].text)
    if child[3].text == jiraProjectCode:
        harvestProjectID = child[0].text
        print("Selected Harvest Project ID : "+child[0].text+" | Project Code : "+child[3].text+" | Task Name : "+jiraTaskName)
        
print('Create a new task and assign it to the Harvest Project')

url = baseURL+"/projects/"+str(harvestProjectID)+"/task_assignments/add_with_create_new_task"
headers = {'Content-Type' : 'application/xml', 'Accept' : 'application/xml', 'User-Agent' : 'PHP Wrapper Library for Harvest API'} 
xmlData = """<task><name>"""+str(jiraTaskName)+"""</name><billable-by-default>1</billable-by-default><default-hourly-rate>0</default-hourly-rate></task>""";

response = requests.post(url, data=xmlData, auth=(username, password), headers=headers)
print(response)

output = [{'response': 'true'}]
