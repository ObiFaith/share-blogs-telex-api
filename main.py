import httpx
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status, BackgroundTasks

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['Authorization', 'Content-Type']
)

class Setting(BaseModel):
  label: str
  type: str
  required: bool
  default: str
  options: List[str] = None

class TickPayload(BaseModel):
  channel_id: str
  return_url: str
  settings: List[Setting]

@app.get("/integration.json")
async def get_integration_json(request: Request):
  base_url = str(request.base_url).rstrip("/")
  return {
    "data": {
      "date": {
        "created_at": "2025-02-19",
        "updated_at": "2025-02-19"
      },
      "descriptions": {
        "app_name": "Daily Standup Report",
        "app_description": "This Telex integration sends a scheduled reminder to a channel, prompting team members to submit their daily standup reports.",
        "app_logo": "https://static.thenounproject.com/png/1259527-512.png",
        "app_url": "https://share-blogs-telex-api.onrender.com/",
        "background_color": "#fff"
      },
      "is_active": True,
      "integration_category": "Communication & Collaboration",
      "integration_type": "interval",
      "key_features": [
        "Scheduled reminders",
        "Report template/format guidance in the reminder message."
      ],
      "author": "Faith Obi",
      "settings": [
        {
          "label": "interval",
          "type": "text",
          "required": True,
          "default": "*/5 * * * *"
        },
        {
          "label": "Reminder Message",
          "type": "text",
          "required": True,
          "default": "Reminder: DAILY STAND-UP REPORT\nWhat have you accomplished since the last stand-up?\n[What you accomplished here]\n\nWhat are you working on next?\n[What you will be doing]\n\nAny blockers?\n[blocked?]"
      },
        {
          "label": "Mention Type",
          "type": "dropdown",
          "required": True,
          "default": "@channel",
          "options": [
            "@channel",
            "@here"
          ]
        }
      ],
      "target_url": "''",
      "tick_url": f"{base_url}/tick"
    }
  }

async def send_standup_reminder(payload: TickPayload):
    mention_type = next(
      (s.default for s in payload.settings if s.label == "Mention Type"),
      "@channel",
    )
    reminder_message = next(
      (s.default for s in payload.settings if s.label == "Reminder Message"),
      "Time for standup!",
    )

    message = f"{mention_type} {reminder_message}"

    data = {
      "event_name": "Daily Standup Report",
      "message": message,
      "status": "success",
      "username": "Standup Bot",
    }

    async with httpx.AsyncClient() as client:
      await client.post(payload.return_url, json=data)

@app.post("/tick", status_code=status.HTTP_202_ACCEPTED)
async def tick(payload: TickPayload, background_tasks: BackgroundTasks):
  background_tasks.add_task(send_standup_reminder, payload)
  return {"status": "accepted"}