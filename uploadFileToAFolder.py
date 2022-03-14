from __future__ import print_function
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import credentials, service_account

# Scopes required by this endpoint -> https://developers.google.com/drive/api/v3/reference/files/create
SCOPES = ['https://www.googleapis.com/auth/drive']
"""
To upload/create a file in to a 'Shared with me' folder this script has the following configured:

1. Project:
    * Create project 
    * Enable the Google Workspace API the service account will be using:     https://developers.google.com/workspace/guides/create-project

2.Consent screen:
    * Configure the consent screen for the application 
    * Create credentials for your service account depending on the type of application to be used with https://developers.google.com/workspace/guides/create-credentials#create_a_service_account 
    Once your Service Account is created you are taken back to the credentials list (https://console.cloud.google.com/apis/credential) click on the created Service Account, next click on ‘Advanced settings’ and copy your client ID

3. Scopes
    * Collect the scopes needed for your service account/application
     https://developers.google.com/identity/protocols/oauth2/scopes

4. Grant access to user data to a service account in Google Workspace https://admin.google.com/ac/owl/domainwidedelegation
    * In the "Client ID" field, paste the client ID  from your service account
    * In the "OAuth Scopes" field, enter a comma-delimited list of the scopes required by your application. This is the same set of scopes you defined when configuring the OAuth consent screen.
    * Click Authorize.

5. In your code you need to impersonate the account the folder was shared with, if it was your account, you add your account here:
    credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_creds = credentials.with_subject('user@domain.info')
"""

def main():

    SERVICE_ACCOUNT_FILE = 'drive.json' #Service Account credentials from Step 2

    credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_creds = credentials.with_subject('user@domain.xyz')

    service = build('drive', 'v3', credentials=delegated_creds)


    media = MediaFileUpload(
        'xfiles.jpg',
        mimetype='image/jpeg',
        resumable=True
        )
    request = service.files().create(
        media_body=media,
        body={'name': 'xfile new pic', 'parents': ['1Gb0BH1NFz30eaxxxxxE']} #In here 1Gb0BH1NFz3xxxxxxxxxxx is the 'Shared With ME'FolderID to upload this file to
        )

    response = None
    while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")


if __name__ == '__main__':
    main()
