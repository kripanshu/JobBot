"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from getlist import GetList
from util import Util
import json
import pandas as pd

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Call the Gmail API
list_obj = GetList()
list_messages = list_obj.ListMessagesMatchingQuery(service,'me')


# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])
# if not labels:
#     print('No labels found.')
# else:
#     print('Labels:')
#     for label in labels:
#         print(label['name'])
if not list_messages:
    print('error in getting list messages')

else:
    msg_ob = GetList()
    msg_list = {}
    count = 0
    for ids in list_messages:
        count += 1
        id_val = ids['id']
        msg_val = msg_ob.GetMessage(service,'me',id_val)
        # print("msg val : ", msg_val)
        msg_list[id_val]= msg_val
        if count>1000:
            break;
    # print("list of messages", list_messages)
    key_val = {}
    util_obj = Util()
    for val in msg_list:
        for sub in msg_list[val]['payload']['headers']:
                if sub['name'] == 'Subject' and 'You applied for Software' in sub['value']:
                    key_val[val]= {"date":util_obj.conver_to_date(float(msg_list[val]['internalDate'])),
                       "message":msg_list[val]['snippet'].split("!")[1].split("Applied")[0]}
    with open('data.json', 'w') as outfile:
        json.dump(msg_list, outfile, indent= 4)

    data_frame = pd.DataFrame.from_dict(key_val, orient='index')
    print(data_frame)
    file_name = 'data.csv'
    data_frame.to_csv(file_name, sep=',', float_format='%.2f')
