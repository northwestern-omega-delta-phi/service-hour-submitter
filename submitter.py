# For google
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# For ODPhi site
import requests
from bs4 import BeautifulSoup

# For development 
import json

# Global Variables
with open('config.json') as json_file:  
    config = json.load(json_file)["installed"]

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = config["sheets_id"]
RANGE_NAME = 'Hours!A:Z'

# Could be done a lot better, this is just a quick fix
def dateFormatter(date):
    d_m_y = date.split("/")

    if len(d_m_y[0]) == 1:
        d_m_y[0] = "0" + d_m_y[0] + "/"
    else:
        d_m_y[0] = d_m_y[0] + "/"

    if len(d_m_y[1]) == 1:
        d_m_y[1] = "0" + d_m_y[1] + "/"
    else:
        d_m_y[1] = d_m_y[1] + "/"
    
    date = ""
    for n in d_m_y:
        date += n

    return date

def main():

    ##########################################
    ###### GOOGLE SHEETS AUTHENTICATION ######
    ##########################################

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # ##########################################
    # ######### CALL GOOGLE SHEETS API #########
    # ##########################################

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found was found in the google sheet. Please make sure the ID that was provided for the service sheet in config.json is correct and that you have access to the sheet.')
    else:
        # Constructing the service object for user
        service_hours = []
        for i, row in enumerate(values):
            if (i == 1):
                for date in row[4:]:
                    service_hours.append({"date": date})
            elif (i == 2):
                for j, event in enumerate(row[4:]):
                    service_hours[j]["event"] = event
            elif (row[1] == config["name_on_service_sheet"]):
                offset = 0
                for j, hours in enumerate(row[4:]):
                    if hours != "0":
                        service_hours[j - offset]["hours"] = float(hours)
                    else:
                        del service_hours[j - offset]
                        offset += 1

        # Example of what the data might look like:
        # service_hours = [   
        #     {'date': '1/19/2019', 'event': 'FSL: Recruitment & Support', 'hours': 1.0},
        #     {'date': '1/19/2019', 'event': 'SHPE Jr', 'hours': 2.5},
        #     {'date': '1/21/2019', 'event': 'MLKDOS', 'hours': 3.0},
        #     {'date': '1/26/2019', 'event': 'SHPE Jr', 'hours': 2.5},
        #     {'date': '2/2/2019', 'event': 'SHPE Jr', 'hours': 2.0},
        #     {'date': '2/9/2019', 'event': 'SHPE Jr', 'hours': 2.0},
        #     {'date': '2/16/2019', 'event': 'SHPE Jr', 'hours': 1.0},
        #     {'date': '2/23/2019', 'event': 'EPL', 'hours': 2.0},
        #     {'date': '2/23/2019', 'event': 'SHPE Jr', 'hours': 2.0},
        #     {'date': '3/2/2019', 'event': 'SHPE Jr', 'hours': 2.0},
        #     {'date': '3/9/2019', 'event': 'SHPE Jr Competition', 'hours': 8.0}
        # ]

        ##########################################
        ############ LOGIN TO MYODPHI ############
        ##########################################

        login_url = 'https://myodphi.com/login/'
        login_action = 'https://myodphi.com/wp-login.php'

        # Start session
        session = requests.session()

        # Not entirely sure, but I think we need this get request for the cookies and headers
        r = session.get(login_url)

        # Set username and password as the form wants it
        payload = {
            "log":config["odphi_username"],
            "pwd":config["odphi_password"]
        }

        # Login
        r = session.post(login_action, data = payload)

        ###########################################
        ######### SUBMIT HOURS TO MYODPHI #########
        ###########################################

        service_url = 'https://myodphi.com/servicehours/'

        # Navigate to service page and get basic info
        r = session.get(service_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        official_name = soup.find("input", id="input_5_1")["value"]
        official_email = soup.find("input", id="input_5_2")["value"]
        official_username = soup.find("input", id="input_5_3")["value"]

        is_submit = soup.find("input", {"name":"is_submit_5"})["value"]
        gform_submit = soup.find("input", {"name":"gform_submit"})["value"]
        state5 = soup.find("input", {"name":"state_5"})["value"]
        gform_target = soup.find("input", {"name":"gform_target_page_number_5"})["value"]
        gform_source = soup.find("input", {"name":"gform_source_page_number_5"})["value"]

        # Submit all hours, making a get request for a new form for each event
        for service_event in service_hours:
            r = session.get(service_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            _gform_submit_nonce = soup.find("input", {"name":"_gform_submit_nonce_5"})["value"]
            unique_id = soup.find("input", {"name":"gform_unique_id"})["value"]
            gform_field = soup.find("input", {"name":"gform_field_values"})["value"]
            
            service_details = [
                ("input_11", (None, official_username)),
                ("input_1", (None, official_name)),
                ("input_12", (None, official_email)),
                ("input_2", (None, official_email)),
                ("input_3", (None, official_username)),
                ("input_4", (None, config["region"])),
                ("input_5", (None, config["school"])),
                ("input_6", (None, config["semester"])),
                ("input_7", (None, config["year"])),
                ("input_8", (None, dateFormatter(service_event["date"]))),
                ("input_9", (None, str(service_event["hours"]))),
                ("input_10", (None, service_event["event"])),
                ("_gform_submit_nonce_5", (None, _gform_submit_nonce)),
                ("_wp_http_referer", (None, "/servicehours/")),
                ("is_submit_5", (None, is_submit)),
                ("gform_submit", (None, gform_submit)),
                ("gform_unique_id", (None, unique_id)),
                ("state_5", (None, state5)),
                ("gform_target_page_number_5", (None, gform_target)),
                ("gform_source_page_number_5", (None, gform_source)),
                ("gform_field_values", (None, gform_field))
            ]

            r = session.post(service_url, files = service_details)
            print("\n\nThe following has been submitted:")
            print("  Event: ", service_event["event"])
            print("  Date: ", dateFormatter(service_event["date"]))
            print("  Hours: ", service_event["hours"])
        
        print("All done submitting! Check the service report page to make sure they're all there!")

if __name__ == '__main__':
    main()