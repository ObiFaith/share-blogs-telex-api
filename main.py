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

@app.post('/daily-standup-report')
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
