from fastapi import FastAPI
import backrun_sdk.fastapi

app = FastAPI()


backrun_sdk.init(api_url="http://localhost:8001", api_key="test-api-key")
app.add_api_route("/backrun/", backrun_sdk.fastapi.serve, methods=["GET", "POST"])


@backrun_sdk.task
def author_count():
    return 1


@backrun_sdk.task
def exception_raiser():
    raise Exception("This is an exception from exception_raiser")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/schedule")
def schedule():
    author_count.delay()
    return "done"
