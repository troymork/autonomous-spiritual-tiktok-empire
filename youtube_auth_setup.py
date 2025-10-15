#!/usr/bin/env python3
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_token():
    if not os.path.exists('client_secret.json'):
        print("❌ client_secret.json not found!")
        return
    
    print("🔐 Starting authentication...")
    print("📱 Browser will open...")
    
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=8080, prompt='consent')
    
    token_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    print("\n" + "="*70)
    print("✅ COPY THIS JSON TO RENDER AS YOUTUBE_TOKEN:")
    print("="*70)
    print(json.dumps(token_data, indent=2))
    print("="*70)
    
    with open('youtube_token.json', 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print("\n💾 Saved to youtube_token.json")

if __name__ == '__main__':
    get_youtube_token()
