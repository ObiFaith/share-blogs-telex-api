from fastapi import FastAPI

app = FastAPI()
""" app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_methods=['*'],
  allow_credentials=True,
  allow_headers=['Authorization', 'Content-Type']
) """

@app.get('/')
def index():
  return {"detail": "Welcome to the FastAPI Project"}
