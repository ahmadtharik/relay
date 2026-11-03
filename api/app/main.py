from fastapi import FastAPI, status

app = FastAPI()


@app.get("/api/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}