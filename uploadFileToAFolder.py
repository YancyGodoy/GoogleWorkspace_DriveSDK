from __future__ import print_function
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import credentials, service_account

# Found at https://developers.google.com/drive/api/v3/reference/files/create#auth
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():

    #Since we are impersonating a user, we need to get the Service Account credentials.
    SERVICE_ACCOUNT_FILE = 'drive.json'
    
    credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_creds = credentials.with_subject('impersonatedUser@domain')

    service = build('drive', 'v3', credentials=delegated_creds)

    media = MediaFileUpload(
        'snoop.jpg',
        mimetype='image/jpeg',
        resumable=True
        )
    request = service.files().create(
        media_body=media,
        body={'name': 'Snoopy Image', 'parents': ['1Gb0BH1NFz3xxxxxxxxxxx']} #In here 1Gb0BH1NFz3xxxxxxxxxxx is the FolderID to upload this file to
        )

    response = None
    while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")


if __name__ == '__main__':
    main()
