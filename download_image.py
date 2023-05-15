import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import requests
from pathlib import Path
import shutil

import pandas as pd
from datetime import date, timedelta, datetime
import json
import argparse
import sys


class GooglePhotosApi:
    def __init__(self,
                 api_name='photoslibrary',
                 client_secret_file=r'./credentials/client_secret.json',
                 api_version='v1',
                 scopes=['https://www.googleapis.com/auth/photoslibrary']):
        '''
        Args:
            client_secret_file: string, location where the requested credentials are saved
            api_version: string, the version of the service
            api_name: string, name of the api e.g."docs","photoslibrary",...
            api_version: version of the api
        '''

        self.api_name = api_name
        self.client_secret_file = client_secret_file
        self.api_version = api_version
        self.scopes = scopes
        self.cred_pickle_file = f'./credentials/token_{self.api_name}_{self.api_version}.pickle'

        self.cred = None

    def run_local_server(self):
        # is checking if there is already a pickle file with relevant credentials
        if os.path.exists(self.cred_pickle_file):
            with open(self.cred_pickle_file, 'rb') as token:
                self.cred = pickle.load(token)

        # if there is no pickle file with stored credentials, create one using google_auth_oauthlib.flow
        if not self.cred or not self.cred.valid:
            if self.cred and self.cred.expired and self.cred.refresh_token:
                self.cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, self.scopes)
                self.cred = flow.run_local_server()

            with open(self.cred_pickle_file, 'wb') as token:
                pickle.dump(self.cred, token)
        return self.cred


def get_response_from_medium_api(year, month, day, creds):
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    payload = {"pageSize": 100,
               "filters": {
                   "dateFilter": {
                       "dates": [
                           {
                               "day": day,
                               "month": month,
                               "year": year
                           }
                       ]
                   },
                   "mediaTypeFilter": {"mediaTypes": ["PHOTO"]},
                   "contentFilter": {"includedContentCategories": ["PEOPLE"]}
               }
               }
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(creds.token)
    }

    try:
        res = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)
    except:
        print('Request error')

    return (res)


def list_of_media_items(year, month, day, creds):
    '''
    Args:
        year, month, day: day for the filter of the API call 
    Return:
        items_df: media items uploaded on specified date
    '''

    items_list_df = pd.DataFrame()

    # create request for specified date
    response = get_response_from_medium_api(year, month, day, creds)

    try:
        for item in response.json()['mediaItems']:
            items_df = pd.DataFrame(item)
            items_df = items_df.rename(
                columns={"mediaMetadata": "creationTime"})
            items_df.set_index('creationTime')
            items_df = items_df[items_df.index == 'creationTime']

            # append the existing media_items data frame
            items_list_df = pd.concat([items_list_df, items_df])
            items_list_df.set_index("id")
    except Exception:
        print(response.text)
    return items_list_df


def download(date_str):
    google_photos_api = GooglePhotosApi()
    creds = google_photos_api.run_local_server()

    download_dir = f'./downloads/{date_str}'
    # download_image(date_str, download_dir)
    year, month, day = date_str.split("-")
    DATE = date(int(year), int(month), int(day))
    items_list_df = list_of_media_items(DATE.year, DATE.month, DATE.day, creds)
    print(f"Number of images to download {len(items_list_df)}")

    try:
        shutil.rmtree(download_dir)
    except:
        print(f"{download_dir} not exists")

    Path(download_dir).mkdir(parents=True, exist_ok=True)

    if len(items_list_df) > 0:
        for index, item in items_list_df.iterrows():
            # Download full resolution images
            url = item.baseUrl + "=d"

            response = requests.get(url)

            file_name = item.filename

            # convert heic file to jpeg file
            if file_name.lower().endswith('.heic'):
                file_name = os.path.splitext(file_name)[0] + '.jpg'

            with open(os.path.join(download_dir, file_name), 'wb') as f:
                f.write(response.content)
                
        print(f'Downloaded items found for date_str: {DATE.year}/{DATE.month}/{DATE.day}')
    else:
        print(f'No media items found for date_str: {DATE.year}/{DATE.month}/{DATE.day}')
        sys.exit(1)
    

# if __name__ == "__main__":
#     download_images(date_str)