from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import credentials, service_account

# Scopes required by this endpoint -> https://developers.google.com/drive/api/v3/reference/files/get
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Service Account Credentials to be used. How to create at https://developers.google.com/workspace/guides/create-credentials#service-account
SERVICE_ACCOUNT_FILE = 'YourServiceAccountCredentials.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes= SCOPES)
delegated_creds = credentials.with_subject("userToBeImpersonated@yourDomain.com")

service = build('drive', 'v3', credentials = delegated_creds)

results = service.files().list(orderBy = 'name', pageSize = 100, corpora= 'user').execute()
items = results.get('files', [])

if not items:
    print("no files found")
else:
    print("Document name + FileID ")
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

