from flask import Flask, jsonify, Response
import json
import block_model_proccesor
import requests
app = Flask(__name__)



@app.route('/')
def Index():
    return 'Hello World'

@app.route('/api/block_models/', methods=['GET'])
def get_block_models_names():
    feature_flags_json = get_feature_flags()
    data = block_model_proccesor.get_model_names_to_dictionary()
    if feature_flags_json["restful_response"]:
        data = {"block_models": data}
    response = Response(json.dumps(data))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def get_block_model_blocks(name=None):
    feature_flags_json = get_feature_flags()
    data = block_model_proccesor.get_block_list(name)
    if feature_flags_json["restful_response"]:
        data = {"block_model": {"blocks": data}}
    response = Response(json.dumps(data))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/api/block_models/<name>/blocks/<index>', methods=['GET'])
def get_block_model_blocks_info(name, index):
    feature_flags_json = get_feature_flags()
    if not feature_flags_json["block_info"]:
        return "block_info flag is disabled"
    else:
        #TODO return more structured version of the block info
        data = {"block": block_model_proccesor.get_block_info_by_index(name, int(index))}
        response = Response(json.dumps(data))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


def get_feature_flags():
    #TODO change this url to https://dry-brushlands-69779.herokuapp.com/api/feature_flags for the delivery
    feature_flags_service_url = "http://localhost:8001/api/feature_flags"
    response = requests.get(feature_flags_service_url)
    feature_flags_json = response.json()
    return feature_flags_json

if __name__ == '__main__':
    app.run()
