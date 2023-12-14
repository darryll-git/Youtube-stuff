api_key = 'AIzaSyDFvWQqeA62QPwrSNVLlY6w985W_3h6-qM'

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Build the YouTube API service
youtube = build('youtube', 'v3', developerKey=api_key)

# Specify the channel username or ID
channel_username = 'pikachu'

# Get the channel ID from the provided username
channels_response = youtube.channels().list(part='id', forUsername=channel_username).execute()
channel_id = channels_response['items'][0]['id']

# Get the videos from the channel
playlist_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Get the video details from the playlist
videos_response = youtube.playlistItems().list(part='snippet', playlistId=playlist_id).execute()

# Retrieve comments from each video
for video in videos_response['items']:
    video_id = video['snippet']['resourceId']['videoId']
    
    try:
        comments_response = youtube.commentThreads().list(part='snippet', videoId=video_id).execute()
        
        # Print comments
        for comment in comments_response['items']:
            text_display = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            print(text_display)
            
    except HttpError as e:
        # Check if comments are disabled
        error_details = e.error_details[0]
        if 'commentsDisabled' in error_details['reason']:
            print(f"Comments are disabled for the video with ID {video_id}")
        else:
            # Handle other errors
            print(f"Error retrieving comments for video with ID {video_id}: {e}")
