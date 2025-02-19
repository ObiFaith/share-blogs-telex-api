import httpx
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['Authorization', 'Content-Type']
)

@app.get('/api/v1')
def get_integration():
  return {
    "data": {
      "date": {
        "created_at": "2025-02-18",
        "updated_at": "2025-02-18"
      },
      "descriptions": {
        "app_name": "Daily Standup Report",
        "app_description": "This Telex integration sends a scheduled reminder to a channel, prompting team members to submit their daily (or weekly) standup reports. It helps streamline the reporting process, ensuring consistent updates and improved team communication. Users can configure the time and frequency of the reminders.",
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
          "label": "Reminder Frequency",
          "type": "text",
          "required": True,
          "default": "* * * * *"
        },
        {
          "label": "Reminder Message",
          "type": "text",
          "required": True,
          "default": "Reminder: It's time for your daily standup report!  What have you accomplished since the last stand-up? [What you accomplished here]  What are you working on next? [What you will be doing]  Any blockers? [blocked?]"
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
      "tick_url": "https://share-blogs-telex-api.onrender.com/api/v1/integration"
    }
  }

@app.post('/api/v1/integration')
async def daily_standup_report(request: Request):
  try:
    data = await request.json()
    return_url = data.get("return_url")
    settings = data.get("settings")

    if not return_url:
      return JSONResponse(
        content={"error": "Return URL not provided"},
        status_code=status.HTTP_400_BAD_REQUEST,
      )

    mention_type = ""
    reminder_message = ""

    for setting in settings:
      if setting["label"] == "Reminder Message":
        reminder_message = setting.get("default", "Time for standup!")
      elif setting["label"] == "Mention Type":
        mention_type = setting.get("default", "@channel")

    message = f"{mention_type} {reminder_message}"

    payload = {
      "event_name": "Daily Standup Report",
      "message": message,
      "status": "success",
      "username": "TelexBot"
    }

    async with httpx.AsyncClient() as client:
      response = await client.post(return_url, json=payload)

    telex_response = await response.json()
    return {"status": "Message sent", "telex_response": telex_response}

  except Exception as e:
    return JSONResponse(
      content={"error": str(e)},
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
