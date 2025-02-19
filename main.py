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

@app.get('/integration.json')
def get_integration(request: Request):
  base_url = str(request.base_url).rstrip("/")
  return {
    "data": {
      "date": {
        "created_at": "2025-02-18",
        "updated_at": "2025-02-18"
      },
      "descriptions": {
        "app_name": "Daily Standup Report",
        "app_description": "This Telex integration sends a scheduled reminder to a channel, prompting team members to submit their daily (or weekly) standup reports.",
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

@app.post('/tick')
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

    if not settings or not isinstance(settings, list):
      return JSONResponse(
          content={"error": "Settings must be a list and cannot be empty"},
          status_code=status.HTTP_400_BAD_REQUEST
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
      try:
        response = await client.post(
          return_url,
          json=payload,
          headers={"Accept": "application/json", "Content-Type": "application/json"}
        )

        response.raise_for_status()

        return response.json()
      except httpx.HTTPStatusError as http_err:
        return JSONResponse(content={"error": str(http_err)}, status_code=response.status_code)
      except httpx.RequestError as req_err:
        return JSONResponse(content={"error": str(req_err)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

  except Exception as e:
    return JSONResponse(
      content={"error": str(e)},
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
