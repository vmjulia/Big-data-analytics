# the script is set to run every 15 min to download data using .bat file
# data is delivered partially, each return gives token for the next request. date is stored in .txt file in order to fetch the data
# in the next 15 min session starting from the "correct point of time"

import json 
import os
import requests 
from requests.auth import HTTPBasicAuth

f = open(os.path.join('UpdatedData', "Output.txt"))
prev = f.read()
f.close()
url = 'https://..../export/api/jobs/updates/json?date=' + prev

r = requests.get(
  url, 
  auth=HTTPBasicAuth('....', '....')
)

files = r.json()
curr  = files['date']          
data = files['jobs']


while True:
 try:
    url = 'https://..../export/api/jobs/updates/json?token='+ files['token']     
    r = requests.get(url, auth=HTTPBasicAuth('....', '...'))
    files = r.json()
    data.extend(files['jobs'])
   
 except:
   break

def save_jobs(filename, jobs):
   with open(filename, 'w+', encoding='utf8') as f:
      json_formatted_str = json.dumps(jobs, indent=2, ensure_ascii=False)
      f.write(json_formatted_str)
    
import dateutil.parser as dp    

def converttime(t):
    parsed_t = dp.parse(t)
    t_in_seconds = int(parsed_t.timestamp()*1000)
    return (t_in_seconds)


with open(os.path.join('UpdatedData',  "Output.txt" ), "w") as text_file:
    text_file.write(curr.replace(":", "%3A").replace("+", "%2B"))

save_jobs(os.path.join( 'UpdatedData',  '%s.json' % (converttime(curr)) ), data)
