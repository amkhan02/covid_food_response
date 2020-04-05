import mechanize
import csv
import http.cookiejar
import io
import re
import ast
import json
from flask import Flask, request

br = None

app = Flask(__name__)
@app.route('/', methods=['POST'])
def parse_request():
	data = {'firstname':'', 'lastname':'', 'homeless':0, 'household_total':'', 'street_address':'', 'apartment':'', 'city':'', 'state':'SC', 'zipcode':'', 'phone':'', 'gender':'', 'dob':'', 'race':'', 'cf_guests_f69d4306dd':'1', 'cf_guests_4c0fc7dc8e': '0.00', 'cf_guests_11521eb564':'1', 'cf_guests_48faabaf3f':'1', 'income1':'0.00', 'action':'Save', 'othersHousehold[]':''}
	genders = {'Male':'1', 'Female':'2'}
	races = {'black':'1', 'white':'2', 'asian':'4', 'hispanic':'3', 'native-american':'6', 'pacific-islander':'7'}
	
	for (key, value) in request.form.items():
		value = str(value)
		data['firstname'] = value if key == 'First Name' else data['firstname']
		data['lastname'] = value if key == 'Last Name' else data['lastname']
		data['household_total'] = value if key == 'household-size' else data['household_total']
		data['street_address'] = value if key == 'Street Address' else data['street_address']
		data['apartment'] = value if key == 'Apartment/lot number' else data['apartment']
		data['city'] = value if key == 'City' else data['city']
		data['state'] = 'SC'
		data['zipcode'] = value if key == 'Zip code' else data['zipcode']
		data['phone'] = re.sub(r"\D", "", value) if key == 'Phone Number' else data['phone']
		data['gender'] = genders[value] if key == 'gender' else data['gender']
		data['dob'] = value if key == 'dob' else data['dob']
		data['race'] = races[value] if key == 'race' else data['race']
	
	for i in range(1,int(data['household_total'])):
		data['othersHousehold[' + str(i-1) + '][id]'] = str(i-1)
		for (key, value) in request.form.items():
			if key == 'member' + str(i) + '_name':
				data['othersHousehold[' + str(i-1) + '][name]'] = value
			if key == 'member' + str(i) + '_dob':
				data['othersHousehold[' + str(i-1) + '][age]'] = value
			if key == 'member' + str(i) + '_relationship':
				data['othersHousehold[' + str(i-1) + '][rel]'] = value
			if key == 'member' + str(i) + '_race':
				data['othersHousehold[' + str(i-1) + '][race]'] = races[value]
			if key == 'member' + str(i) + '_gender':
				data['othersHousehold[' + str(i-1) + '][gender]'] = genders[value]
	
	x = returning_guest(data) is None
	print(x)
	if x:
		print(data)
		create_new_guest(data)
	return(request.values)
	
def main():
	#Set up Browser
	global br
	deploy = False
	
	br = mechanize.Browser()
	cj = http.cookiejar.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Chrome')]
	
	#login
	br.open('https://icnareliefusashifafreeclinic.soxbox.co/login')
	br.select_form(nr = 0)
	
	config = json.load(open('/etc/config.json')) if deploy else json.load(open('config.json'))
		
	br.form['username'] = config.get('username')
	br.form['password'] = config.get('password')
	br.submit()
	
	br.open('https://icnareliefusashifafreeclinic.soxbox.co/create-new-visit/')
	br.open('https://icnareliefusashifafreeclinic.soxbox.co/create-new-visit/set-outreach/?id=config_1')
	
	app.run()
	#fam = [{'firstname':'husband', 'lastname':'herfer', 'dob':'1988-01-05', 'relationship':'husband', 'race':'hispanic', 'gender':'Male'}, {'firstname':'son1', 'lastname':'herfer', 'dob':'2013-05-08', 'relationship':'son', 'race':'hispanic', 'gender':'Male'}, {'firstname':'son2', 'lastname':'herfer', 'dob':'2015-09-18', 'relationship':'son', 'race':'hispanic', 'gender':'Male'}, {'firstname':'son3', 'lastname':'herfer', 'dob':'2019-04-26', 'relationship':'son', 'race':'hispanic', 'gender':'Male'}]
	#create_new_guest('Silvia', 'Herfer', '5', '7121 Stall Road lot 31', '31', 'North Charleston', 'SC', '29406', '8438265194', 'Female', '1988-12-31', 'hispanic', fam)
	
	
	
def guest_list():
	global br
	br.open('https://icnareliefusashifafreeclinic.soxbox.co/reports/guests/guests/')
	br.select_form(nr = 0)
	csv_file = br.submit().read()
	csv_file = csv_file.decode('utf-8')
	file = io.StringIO()
	file.write(csv_file)
	file.seek(0)
	csv_reader = csv.reader(file)
	return csv_reader

# Format for family_members
# [{'firstname': 'Robert', 'lastname': 'Fletcher', 'dob': '1968-02-20', 'relationship': 'Husband', 'race': 'white', 'gender': 'Male'}, {'firstname': 'Grayson', 'lastname': 'Fletcher', 'dob': '2015-02-24', 'relationship': 'Son', 'race': 'white', 'gender': 'Male'}, {'firstname': 'Dakota', 'lastname': 'Fletcher', 'dob': '2017-01-15', 'relationship': 'Daughter', 'race': 'white', 'gender': 'Female'}]
# Format dob
# dob = dob.split('/')[2] + '-' + dob.split('/')[0] + '-' + dob.split('/')[1]
# Make sure all elements are str before passing to this function
def create_new_guest(data):
	url = 'https://icnareliefusashifafreeclinic.soxbox.co/create-new-visit/guest/create/'
	x = mechanize.Request(url, data)
	br.open(x)
	
#Not Necessary, Unfinished
def create_new_visit(gid):
	data = {'terms':'2', 'type':'cf_visits_05ffab81ad'}
	br.open(mechanize.Request('https://icnareliefusashifafreeclinic.soxbox.co/signature-panel/type:Guest/id:'+gid, data=data))
	output = '[{"lx":9,"ly":20,"mx":9,"my":19}]'
	
	br.open('https://icnareliefusashifafreeclinic.soxbox.co/signature-panel/type:Guest/id:'+gid)
	
	data = {'output':output}
	x = br.open(mechanize.Request('https://icnareliefusashifafreeclinic.soxbox.co/signature-panel/submit/type:Guest/id:'+gid, data=data))
	
	j_value = x.read().decode('utf-8')
	j_value = ast.literal_eval(j_value)
	data = {'sig':j_value['sig'], 'field':'cf_visits_05ffab81ad'}
	x = br.open('https://icnareliefusashifafreeclinic.soxbox.co/create-new-visit/guest/update-visit/1912/', data=data)	

#Note: Make sure that DOB is in the correct format
#	yyyy-mm-dd
#Make this case insensitive
def returning_guest(data):
	gid = None
	for row in guest_list():
		num = 0
		num = num + 1 if row[1].lower() == data['firstname'].lower() else num
		num = num + 1 if row[3].lower() == data['lastname'].lower() else num
		num = num + 1 if row[4].lower() == data['dob'] else num
		num = num + 1 if row[5].lower() == data['street_address'].lower() else num
		gid = row[0] if num >= 2 else gid
	return gid

if __name__ == '__main__':
	main()
	