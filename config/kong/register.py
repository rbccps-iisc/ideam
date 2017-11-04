from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
app = Flask(__name__)


def post(url, json_data, headers):
    response = requests.post(url, json=json_data, headers=headers)
    response = response.content.decode("utf-8")
    print response
    return response


@app.route('/', methods=['GET'])
def index():
    response = dict()
    services = []
    resource_id = request.headers.get('resourceID')
    service_type = request.headers.get('serviceType')

    response_consumer = post("http://127.0.0.1:8001/consumers/", json_data={"username": resource_id}, headers={})
    response_consumer = json.loads(response_consumer)

    # failure case when user already exists
    if "already exists" in response_consumer["username"]:
        response["status"] = "failure"
        response["Registration"] = "failure"
        response["response"] = "device resourceID " + response_consumer["username"]
        return jsonify(response)
    else:
        response["status"] = "success"
        response["Registration"] = "success"

    response_apikey = post("http://127.0.0.1:8001/consumers/" + resource_id + "/key-auth", json_data={}, headers={})
    response_apikey = json.loads(response_apikey)

    # failure case when api key is not sent by kong
    if "key" in response_apikey:
        response["status"] = "success"
        response["Registration"] = "success"
    else:
        response["status"] = "failure"
        response["Registration"] = "failure"
        response["response"] = response_apikey
        return jsonify(response)

    if "subscribe" in service_type:
        post("http://127.0.0.1:8001/consumers/" + resource_id + "/acls", {"group": "subscribe"}, {})
        services.append("subscribe")
        response_queue = post("http://rabbitmq:8000/queue", {"name": resource_id}, {})
        # failure case when queue is not created in rabbitmq
        if "queue ok" in response_queue:
            response["status"] = "success"
            response["Registration"] = "success"
        else:
            response["status"] = "failure"
            response["Registration"] = "failure"
            response["response"] = response_queue
            return jsonify(response)

    if "publish" in service_type:
        post("http://127.0.0.1:8001/consumers/" + resource_id + "/acls", {"group": "publish"}, {})
        services.append("publish")
    if "historicData" in service_type:
        post("http://127.0.0.1:8001/consumers/" + resource_id + "/acls", {"group": "historicData"}, {})
        services.append("historicData")
    services.append("cat")

    # TODO: Change response format to camelCase
    response["APIKey"] = response_apikey["key"]
    response["ResourceID"] = resource_id
    response["accessEndPoint"] = "https://smartcity.rbccps.org/api/0.1.0/historicData"
    response["publicationEndPoint"] = "https://smartcity.rbccps.org/api/0.1.0/publish"
    response["resourceAPIInfo"] = "https://rbccps-iisc.github.io"
    response["AllowedAPIs"] = ",".join(services)
    response["subscriptionEndPoint"] = "https://smartcity.rbccps.org/api/0.1.0/subscribe"
    response["Subscription Queue Name"] = resource_id

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
