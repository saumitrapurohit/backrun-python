from flask import Flask
import backrun_sdk.flask

app = Flask(__name__)

backrun_sdk.init(api_url="http://localhost:5001", api_key="test-api-key")
app.add_url_rule("/backrun/", view_func=backrun_sdk.flask.serve)


@backrun_sdk.task
def author_count():
    return 1


@backrun_sdk.task
def exception_raiser():
    raise Exception("This is an exception from exception_raiser")


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/schedule")
def schedule():
    author_count.delay()
    return "done"
