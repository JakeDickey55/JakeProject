import subprocess
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": " WOW WI IDID IT"}

@app.get("/test")
async def test():
    return {"message": " WOW test"}

if __name__ == "__main__":
    subprocess.run(["fastapi", "dev","cheese.py",])