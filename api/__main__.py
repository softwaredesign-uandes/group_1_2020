from flask import Flask, jsonify, Response, request
import json
import block_model_proccesor, api_verification, load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME
app = Flask(__name__)

@app.route('/')
def Index():
    return 'Hello World'

@app.route('/api/block_models/', methods=['GET'])
def get_block_models_names():
    response = Response(json.dumps(block_model_proccesor.get_model_names_to_dictionary()))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def get_block_model_blocks(name=None):
    response = Response(json.dumps(block_model_proccesor.get_block_list(name)))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/api/block_models/<name>/reblock', methods=['POST'])
def reblock_block_model(name=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    data = request.get_json()
    valid_information = api_verification.verificate_reblock_information(data, name, json_file_name)
    if valid_information:
        block_model = load_block_model.get_block_model_object(name)
        block_model.reblock(data["rx"], data["ry"], data["rz"], data["continuous_attributes"], data["proportional_attributes"], data["categorical_attributes"], data["columns_with_mass"])
    return

if __name__ == '__main__':
    app.run()
