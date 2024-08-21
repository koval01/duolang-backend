import uvicorn

from application.src.app import create_app
# from application.src.utils.dummy_data import create_dummy_data

app = create_app()


# Create dummy data on startup
@app.on_event("startup")
async def startup():
    # await create_dummy_data()
    pass

if __name__ == "__main__":
    app_port = 8000
    uvicorn.run(app, host="localhost", port=app_port)
