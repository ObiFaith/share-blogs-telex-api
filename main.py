from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_methods=['*'],
  allow_credentials=True,
  allow_headers=['Authorization', 'Content-Type']
)

@app.get('/api/v1/integration')
def index():
  return {
    "data": {
      "date": {
        "created_at": "2025-02-17",
        "updated_at": "2025-02-17"
      },
      "descriptions": {
        "app_name": "Share Learning Blog Posts",
        "app_description": "This API Integration that share learning blog post to team in an organization based on a specific interval daily.",
        "app_logo": "''",
        "app_url": "https://share-blogs-telex-api.onrender.com/",
        "background_color": "#fff"
      },
      "is_active": True,
      "integration_type": "interval",
      "key_features": [
        "Share Learning Blog Posts"
      ],
      "author": "Faith Obi",
      "settings": [
        {
          "label": "Blog RSS Feed URL",
          "type": "text",
          "required": True,
          "default": "true"
        }
      ],
      "target_url": "''",
      "tick_url": "https://share-blogs-telex-api.onrender.com/api/v1/integration"
    }
}
