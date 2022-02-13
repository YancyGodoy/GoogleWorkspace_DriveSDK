from __future__ import print_function
from email.message import EmailMessage
from operator import truediv
from googleapiclient.discovery import build
from google.oauth2 import credentials, service_account

# Scopes required by this endpoint -> https://developers.google.com/drive/api/v3/reference/permissions/create
SCOPES = ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.file"]

# Service Account Credentials to be used. How to create at https://developers.google.com/workspace/guides/create-credentials#service-account
SERVICE_ACCOUNT_FILE = 'yourServiceAccountCredentials.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes= SCOPES)
delegated_creds = credentials.with_subject('UserToBeImpersonated@yourdomain.com')

service = build('drive', 'v3', credentials = delegated_creds)

#If you don't have it you can get it with https://github.com/Yancy-Godoy/GoogleWorkspace_DriveSDK/blob/main/listFilesFromAnotherUser.py
userfileID = 'FileIDfromFileToBeTransferred'

parameters = {
    'sendNotificationEmail': 'True', #Optional to send an email notification
    'emailMessage': 'You are the new owner of file X', #Optional Message to be sent to new owner if the above parameter is set to true
    'moveToNewOwnersRoot':'True',
    'role': 'owner',  
    'type': 'user',
    'emailAddress': 'newOwnerEmailAddress@yourdomain',
}

results = service.permissions().create(fileId=userfileID,body=parameters,transferOwnership=True).execute()

print(results)
