import uvicorn

if __name__ == "__main__":
    uvicorn.run("config:app", host="0.0.0.0", port=8001 ,reload=True) # in production change it to False
