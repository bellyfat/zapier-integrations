'''
Python Zap App code to add Harvest Time Entries for
Google Calendar event created
version 1.2
'''
import json
import requests

# Configure the settings
HARVEST_ACCOUNT_ID = "****"
HARVEST_BASE_URL = "https://api.harvestapp.com/v2"
HARVEST_TOKEN = "****"
HEADERS = {
    "User-Agent": "Python Harvest API Sample",
    "Authorization": "Bearer " + HARVEST_TOKEN,
    "Harvest-Account-ID": HARVEST_ACCOUNT_ID,
    "Content-Type": "application/json"
}
# HARVEST_PROJECTS_PAGES default page = 1 contains 100 projects
HARVEST_PROJECTS_PAGES = 10
# HARVEST_TASKS_PAGES default page = 1 contains 100 tasks
HARVEST_TASKS_PAGES = 10

# Get the Google Calendar Data
EVENT_DESCRIPTION = input_data['event_description']
EVENT_ATTENDEE_EMAILS = input_data['event_emails']
EVENT_DURATION_HOURS = float(input_data['event_duration_hours'])
EVENT_DATE = input_data['event_date']

# Get Harvest User IDs by Calendar attendee emails
def get_harvest_user_details():
    """ List Harvest emails and user IDs """
    harvest_api_url = HARVEST_BASE_URL + "/users"
    response = requests.get(url=harvest_api_url, headers=HEADERS)
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    json_harvest_response = json.loads(response.text)
    return json_harvest_response

def filter_harvest_user_ids(json_updated_response):
    """ Filter the user IDs of Calendar attendee emails """
    calender_emails = EVENT_ATTENDEE_EMAILS.split(',')
    harvest_request_user_ids = []

    for user in json_updated_response["users"]:
        for calender_email in calender_emails:
            if user["email"] == calender_email:
                harvest_request_user_ids.append(user["id"])
    return harvest_request_user_ids

def get_harvest_project_id(harvest_project_code):
    """ Get Harvest Projects """
    for pageno in range(HARVEST_PROJECTS_PAGES):
        pageno += 1
        harvest_api_url = HARVEST_BASE_URL + "/projects?page="+str(pageno)
        response = requests.get(url=harvest_api_url, headers=HEADERS)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        json_projects_response = json.loads(response.text)

        # Filter the Harvest Project ID
        harvest_project_id = 0
        for project in json_projects_response['projects']:
            if harvest_project_code == project['code']:
                harvest_project_id = project['id']
                print(harvest_project_id)
                return harvest_project_id

def get_harvest_task_id(harvest_project_id, task_name):
    """ Get Harvest Project assigned task list """
    for pageno in range(HARVEST_TASKS_PAGES):
        pageno += 1
        harvest_api_url = HARVEST_BASE_URL + "/projects/"+str(harvest_project_id)+"/task_assignments?page="+str(pageno)
        response = requests.get(url=harvest_api_url, headers=HEADERS)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        json_tasks_response = json.loads(response.text)

        # Filter the Harvest Project Task ID
        task_id = 0
        task_name = task_name.strip()
        task_name = task_name.lower()
        for task in json_tasks_response['task_assignments']:
            response_task_name = task['task']['name'].strip()
            response_task_name = response_task_name.lower()
            # print(task_name)
            if task_name == response_task_name:
                task_id = task['task']['id']
                # print(task_id)
                return task_id

def add_harvest_time_entries(harvest_user_ids):
    """ Add the Harvest time entry """
    harvest_api_url = HARVEST_BASE_URL + "/time_entries"
    event_date = EVENT_DATE.split("T")[:-1]
    event_date = event_date[0]
    event_description_details = EVENT_DESCRIPTION.splitlines()
    harvest_time_entry_project_code = event_description_details[0].split(":")
    harvest_time_entry_project_code = harvest_time_entry_project_code[1].strip()
    harvest_time_entry_task_name = event_description_details[1].split(":")
    harvest_time_entry_task_name = harvest_time_entry_task_name[1].strip()
    harvest_time_entry_description = event_description_details[2].split(":")
    harvest_time_entry_description = harvest_time_entry_description[1].strip()

    harvest_time_entry_project_id = get_harvest_project_id(harvest_time_entry_project_code)
    if harvest_time_entry_project_id is None:
        print('Harvest project ID not found for '+harvest_time_entry_project_code)
        # print(harvest_time_entry_project_id)
    else:    
        harvest_time_entry_task_id = get_harvest_task_id(harvest_time_entry_project_id, harvest_time_entry_task_name)
        # print(harvest_time_entry_task_id)
        if harvest_time_entry_task_id is None:
            print('Harvest Task ID not found for '+str(harvest_time_entry_task_name))
        else:
            for harvest_user_id in harvest_user_ids:
                data = {
                    "user_id": harvest_user_id,
                    "project_id": harvest_time_entry_project_id,
                    "task_id": harvest_time_entry_task_id,
                    "spent_date": event_date,
                    "hours": EVENT_DURATION_HOURS,
                    "notes":harvest_time_entry_description
                    }
                json_data = json.dumps(data).encode('utf8')
                response = requests.post(
                    url=harvest_api_url,
                    headers=HEADERS,
                    data=json_data
                    )
                print(json.dumps(
                    json.loads(response.text),
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": ")))
    
json_response = get_harvest_user_details()
harvest_response_user_ids = filter_harvest_user_ids(json_response)
add_harvest_time_entries(harvest_response_user_ids)
