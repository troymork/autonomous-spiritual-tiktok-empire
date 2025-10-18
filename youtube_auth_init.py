from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

# Define the OAuth scope for YouTube uploads
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    creds = None
    secret_file = "client_secret.json"

    if not os.path.exists(secret_file):
        print("❌ Missing client_secret.json — place it in the same folder as this script.")
        return

    print("🌐 Launching Google OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
    creds = flow.run_local_server(port=8080)

    # Save credentials as token.json
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("✅ OAuth complete! token.json saved successfully.")

if __name__ == "__main__":
    main()
