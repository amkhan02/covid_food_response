from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1JaTm6_w0_aX_inMRZcq0w91HRcPZiW0KPhSbSIBObOI'
RANGES = {'time_name':'A2:B', 'city':'E2:E', 'group':'F2:F'}
RANGE_NAMES = [RANGES['time_name'], RANGES['city'], RANGES['group']]
value_render_option = 'UNFORMATTED_VALUE'
date_time_render_option = 'SERIAL_NUMBER'

def main():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
			
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
		
	service = build('sheets', 'v4', credentials=creds)
	
	sheet = service.spreadsheets()
	result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,
								ranges=RANGE_NAMES,
								valueRenderOption=value_render_option,
								dateTimeRenderOption=date_time_render_option).execute()
	valueRanges = result.get('valueRanges',[])
	
	values = 'values'
	
	# Check to see if data is returned
	if not valueRanges:
		print('No data found.')
	else:
		# Parse data into separate lists
		groups = valueRanges[2][values] + [[-1] for x in range(len(valueRanges[1][values])-len(valueRanges[2][values]))]
		for item in groups:
			groups[groups.index(item)] = item[0]
		max_group = max(groups)
		
		city = valueRanges[1][values][:]
		for item in city:
			if len(item) is not 0:
				city[city.index(item)] = item[0].lower().strip()
			else:
				city[city.index(item)] = 'null'
		
		time = valueRanges[0][values][:]
		name = valueRanges[0][values][:]
		for item in valueRanges[0][values]:
			time[time.index(item)] = item[0]
			name[name.index(item)] = item[1]
		
		
		# Group ungrouped users
		for index, item in enumerate(city):			
			citygroups = list(zip(city,groups))
			# If there are 5 or more ungrouped requests in the same city...
			if citygroups.count((item,-1)) >= 5 and groups[index] is -1:
				# ...find the next five and add them to the next group
				indices = [i for i, x in enumerate(city) if x == item and i >= index]
				for ii in range(5):
					groups[indices[ii]] = max_group + 1
				max_group += 1
		
		# for number in range(len(time)):
			# print('%s, %s, %s, %s' % (time[number], name[number], city[number], groups[number]))
		# print(groups)
		
		# Upload Changes to Sheet
		upload_values = [[i] for i in groups]
		data = [
			{
				'range': RANGES['group'],
				'values': upload_values
			}
		]
		body = {
			'valueInputOption': "USER_ENTERED",
			'data': data
		}
		upload_result = service.spreadsheets().values().batchUpdate(
			spreadsheetId=SPREADSHEET_ID, body=body).execute()
		print('{0} cells updated.'.format(upload_result.get('totalUpdatedCells')))
		
def push(group, email):
	pass
		
if __name__ == '__main__':
	main()
								