#!/usr/bin/env python3
"""
YouTube Publisher - Upload automation
Publishes videos to YouTube Shorts
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import Config

class YouTubePublisher:
    def __init__(self):
        self.youtube = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = Credentials(
            token=Config.YOUTUBE_TOKEN.get('token'),
            refresh_token=Config.YOUTUBE_TOKEN.get('refresh_token'),
            token_uri=Config.YOUTUBE_TOKEN.get('token_uri'),
            client_id=Config.YOUTUBE_TOKEN.get('client_id'),
            client_secret=Config.YOUTUBE_TOKEN.get('client_secret'),
            scopes=Config.YOUTUBE_TOKEN.get('scopes')
        )
        
        return build('youtube', 'v3', credentials=creds)
    
    def publish(self, video_path, content):
        """Upload video to YouTube as Short"""
        body = {
            'snippet': {
                'title': f"{content['title']} #Shorts",
                'description': f"{content['script']}\n\n#spirituality #meditation #consciousness",
                'tags': ['spirituality', 'meditation', 'shorts'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            str(video_path),
            mimetype='video/mp4',
            resumable=True
        )
        
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        return response['id']
