import re
import requests
from datetime import datetime
import argparse

def main(facebook_data_dir, name):
    print 'fb dataset parser'
    security = True
    friends = True

    if security:
        security_file_path = facebook_data_dir + "/html/security.htm"
        parse_security_file(security_file_path, name)

    if friends:
        friends_file_path = facebook_data_dir + "/html/friends.htm"
        parse_friends_file(friends_file_path, name)

def parse_security_file(security_file_path, name):
    ip_geo_file_name = 'ip_geo_%s.csv' % name
    active_sessions_file_name = 'active_sessions_%s.csv' % name
	
    ip_geo_csv = open(ip_geo_file_name, 'w')
    active_sessions_csv = open(active_sessions_file_name, 'w')

    with open(security_file_path, 'r') as security_file:
        lines = security_file.read().split('\n')

        all_html = lines[-1]

        active_sessions_section = all_html.split('Account Activity')[0]
        parse_active_sessions(active_sessions_csv, active_sessions_section)

        ip_section = all_html.split('IP Addresses')[1]
        parse_all_ips(ip_geo_csv, ip_section)


def parse_active_sessions(active_sessions_csv, active_sessions_section):
    sessions = active_sessions_section.split('</p>')
    active_sessions = []

    active_sessions_csv.write('session_title,created,ip_addr,os\n')

    for s in sessions[1:-1]:
        #active_sessions_csv.write(s + '\n\n')
        session_title = s.split('<p')[0]
        
        created = s.split('Created: ')[1].split('<br />')[0]
        created = created[created.find(' '):created.find('at')-1].lstrip().replace(',', '')

        created = __fix_created_date(created)

        ip_addr = s.split('IP Address: ')[1].split('<br />')[0]
        browser = s.split('Browser: ')[1].split('<br />')[0].replace(',', '')

        if 'iOS' in browser or 'iPhone' in browser:
            os = 'iPhone'
        elif 'Windows' in browser:
            os = 'Windows'
        elif 'Android' in browser or 'samsung' in browser:
            os = 'Android'
        elif 'Verizon' in browser or 'Sprint' in browser:
            os = 'Unknown-Mobile'
        else:
            os = 'Unknown-OS'

        if created:
            active_sessions_csv.write('%s,%s,%s,%s\n' % (session_title, created, ip_addr, os))
            pass
        

def parse_all_ips(ip_geo_csv, ip_section):
    ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ip_section )

    coords = []
    cities = []

    api_key = 'ae85b106f6467c47e4508945e1007038'
    ip_geo_csv.write('ip-addr,latitude,longitude\n')

    for ip_addr in ips:
        url = 'http://api.ipstack.com/%s?access_key=%s&format=1' % (ip_addr, api_key)

        response = requests.get(url)
        response_data = response.json()
        
        latitude = response_data['latitude']
        longitude = response_data['longitude']
        city = response_data['city']

        coords.append((latitude, longitude))
        cities.append(city)

        print '(%s, %s): %s' % (latitude, longitude, city)
        ip_geo_csv.write('%s,%s,%s\n' % (ip_addr, latitude, longitude))

def parse_friends_file(friends_file_path, name):
    friends_file_name = 'friends_%s.csv' % name
    sent_friend_requests_file_name = 'sent_friends_requests_%s.csv' % name
    declined_friend_requests_file_name = 'declined_friends_requests_%s.csv' % name
    removed_friends_file_name = 'removed_friends_%s.csv' % name

    friends_csv = open(friends_file_name, 'w')
    sent_friend_requests_csv = open(sent_friend_requests_file_name, 'w')
    declined_friend_requests_csv = open(declined_friend_requests_file_name, 'w')
    removed_friends_csv = open(removed_friends_file_name, 'w')

    with open(friends_file_path, 'r') as friends_file:
        lines = friends_file.read().split('\n')

        all_html = lines[-1]

        friends_section = all_html.split('<h2>Friends')[1]
        parse_friends(friends_csv, friends_section)

        friends_section = all_html.split('<h2>Sent Friend Requests')[1]
        parse_friends(sent_friend_requests_csv, friends_section)

        friends_section = all_html.split('<h2>Declined Friend Requests')[1]
        parse_friends(declined_friend_requests_csv, friends_section)

        friends_section = all_html.split('<h2>Removed Friends')[1]
        parse_friends(removed_friends_csv, friends_section)

def parse_friends(friends_csv, friends_section):
    friends_csv.write('name,date\n')
    friends_section = friends_section.split('<h2>')[0]
    friends = friends_section.split('<li>')
    print len(friends)

    for f in friends:
        if '</li>' not in f:
            continue
        data = f.split('</li>')[0]
        name, date_added = data.split('(')

        name = name.rstrip().replace('&#039;', "'")
        date_added = date_added.replace(')', '').replace(',', '')
        date_added = __fix_date_added(date_added)

        friends_csv.write('%s,%s\n' % (name, date_added))

def __fix_date_added(date_added):
    if len(date_added.split(' ')) == 3:
        dt = datetime.strptime(date_added, '%b %d %Y')
        return dt.strftime('%m/%d/%Y')

    elif len(date_added.split(' ')) == 2:
        currentYear = __get_current_year()
        dt_str = str(date_added) + " " + str(currentYear)
        dt = datetime.strptime(dt_str, '%b %d %Y')
        return dt.strftime('%m/%d/%Y')

    elif len(date_added.split(' ')) == 1:
        return datetime.now().strftime("%m/%d/%Y")

    else:
        return 'error parsing date'

def __fix_created_date(created):
    if created:
        dt = datetime.strptime(created, '%B %d %Y')
        return dt.strftime('%m/%d/%Y')
    else:
        return ''

def __get_current_year():
    return datetime.now().year

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dir", required=True, help="name of the directory containing your Facebook data")
	args = vars(ap.parse_args())

	dir_name = args['dir']
	user_name = dir_name.split('facebook-')[1]

	main(dir_name, user_name)