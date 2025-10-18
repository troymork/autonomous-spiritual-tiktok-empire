import json
import os
import requests

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
JSON_FILE = "kyrios_codex_trend_protocol.json"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_or_update_database():
    with open(JSON_FILE, "r") as f:
        schema = json.load(f)

    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"

    # Title & emoji update
    body = {
        "title": [{"type": "text", "text": {"content": schema['title']}}],
        "icon": {"emoji": "🌌"},
        "properties": {}
    }

    for key, value in schema['schema'].items():
        prop_type = value.get('type', 'rich_text')

        # Skip invalid or pre-existing title props
        if key.lower() in ["title", "name"]:
            continue
        if key in ["Codex Reference", "Product or Offering"]:
            continue

        # Map supported property types
        if prop_type == "multi_select":
            body["properties"][key] = {
                "multi_select": {
                    "options": [{"name": o} for o in value.get("options", [])]
                }
            }
        elif prop_type == "select":
            body["properties"][key] = {
                "select": {
                    "options": [{"name": o} for o in value.get("options", [])]
                }
            }
        elif prop_type == "number":
            body["properties"][key] = {"number": {"format": "number"}}
        elif prop_type == "date":
            body["properties"][key] = {"date": {}}
        elif prop_type == "rich_text":
            body["properties"][key] = {"rich_text": {}}
        elif prop_type == "formula":
            body["properties"][key] = {
                "formula": {"expression": value.get("expression", "0")}
            }
        else:
            body["properties"][key] = {"rich_text": {}}

    response = requests.patch(url, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        print("✅ Notion sync complete — Trend Protocol database updated successfully.")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    create_or_update_database()
