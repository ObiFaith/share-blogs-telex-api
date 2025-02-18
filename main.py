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
