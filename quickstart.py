from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '13W5cjUqM7-aB0OxtwMmF-cQGIKjeo8v_aHyOGZzhG1A'
RANGE_NAMES = ['A2:B', 'F2:F', 'Q2:Q']
value_render_option = 'UNFORMATTED_VALUE'
date_time_render_option = 'SERIAL_NUMBER'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,
                                ranges=RANGE_NAMES, 
								valueRenderOption=value_render_option, 
								dateTimeRenderOption=date_time_render_option).execute()
    valueRanges = result.get('valueRanges', [])
	
    values = 'values'
	
    if not valueRanges:
        print('No data found.')
    else:
        # print('%s, %s, %s, %s' % (valueRanges[0][values][0][0], valueRanges[0][values][0][1], valueRanges[1][values][0][0], valueRanges[2][values][0][0]))
        groups = valueRanges[2][values] + [[-1] for x in range(len(valueRanges[1][values])-len(valueRanges[2][values]))]
        for item in groups:
            groups[groups.index(item)] = item[0]
        print(max(groups))
		
        city = valueRanges[1][values]
        for item in city:
            if len(item) is not 0:
               city[city.index(item)] = item[0].lower().strip()
            else:
               city[city.index(item)] = 'null'
        
            
        

if __name__ == '__main__':
    main()