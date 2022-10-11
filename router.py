from flask import Flask, request, make_response, has_request_context
from flask.logging import default_handler
import logging
import scrap

app = Flask(__name__)

def configLogger():
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None

            return super().format(record)

    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)
    logging.basicConfig(filename='request.log')

@app.route("/", methods=['GET'])
def gateway():
    return make_response("Connection is fine", 200)

@app.route("/api/scholar/v1/<paperId>", methods=['GET'])
def api_scholar(paperId):
    url = f"https://scholars.cityu.edu.hk/en/publications/{paperId}.html"
    logging.info("%s is being called", url)
    orcid = None
    if request.is_json: 
        print(request.get_json()["orcid"])
        orcid = request.get_json()["orcid"]
    output = scrap.create_scholar(url, orcid)
    resp = make_response(output)
    resp.content_type = "application/json"
    return resp

@app.route("/api/orcid/v1/<orcid>", methods=['GET'])
def api_orcid(orcid):
    output = scrap.create_orcid(orcid)
    resp = make_response(output)
    resp.content_type = "application/json"
    return resp

if __name__ == '__main__':
    configLogger()
    app.run(debug=False, host='0.0.0.0')