import os, json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    sourcePlaylistID = input("\nEnter the link of the playlist here: ")
    sourcePlaylistID = sourcePlaylistID.split("list=")[1]
    if "&index=" in sourcePlaylistID:
        sourcePlaylistID = sourcePlaylistID.split("&index=")[0]
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"      #OAuth credentials client secret id goes here

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(
        host='localhost',
        port=8088,
        authorization_prompt_message='Please visit this URL: {url}',
        success_message='The auth flow is complete; you may close this window and check the console.',
        open_browser=True
    )
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    print("\nWorking on it...")
    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = sourcePlaylistID,
        maxResults = 100
    )

    retrievePlayList = request.execute()
    for key, value in retrievePlayList.items():
        if(key=="items"):
            videoID = [elements['snippet']['resourceId']['videoId'] for elements in value if elements['snippet']['resourceId']['kind']=='youtube#video']

    createRequest = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
            "title": "Python Created List"
          }
        }
    )
    createdList = createRequest.execute()
    PlaylistID = createdList['id']

    for videos in videoID:
        addElements = youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': PlaylistID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': videos
                    }
                    #'position': 0
                }
            }
        )
        addElements.execute()

if __name__ == "__main__":
    main()
    print("Playlist created successfully..")
