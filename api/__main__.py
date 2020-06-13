from flask import Flask, jsonify, Response, request
import json, requests
import block_model_proccesor, api_verification, load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, TEST_MINERAL_GRADES_INFORMATION_FILE_NAME, \
    MINERAL_GRADES_INFORMATION_FILE_NAME
from block import Block
from block_model import BlockModel


app = Flask(__name__)
@app.route('/')
def Index():
    return 'Hello World 2'


@app.route('/api/block_models/', methods=['GET'])
def get_block_models_names(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    feature_flags_json = get_feature_flags()
    data = block_model_proccesor.get_model_names_to_dictionary(json_file_name)
    if feature_flags_json["restful_response"]:
         data = {"block_models": data}
    response = Response(json.dumps(data))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def block_models_controller(json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    feature_flags_json = get_feature_flags()
    data = block_model_proccesor.get_model_names_to_dictionary(json_file_name)
    if feature_flags_json["restful_response"]:
        data = {"block_models": data}
    response = Response(json.dumps(data))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/api/block_models/', methods=['POST'])
def input_block_model(block_json=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME,
                      json_mineral_grades_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    response = Response()
    if not block_json:
        block_json = request.get_json()
    verify_blocks = api_verification.verify_json_block_post(block_json)
    verify_name = api_verification.verify_model_exists(block_json["name"], json_file_name)
    if not verify_blocks:
        response.status_code = 400
        return response
    if verify_name:
        response.status_code = 400
        return response
    block_loaded = load_block_model.load_block_json(block_json["name"],
                                                    block_json["columns"],
                                                    block_json["minerals"],
                                                    block_json["blocks"],
                                                    db_name,
                                                    json_file_name,
                                                    json_mineral_grades_file_name
                                                    )
    if block_loaded:
        response.status_code = 200
    else:
        response.status_code = 500
    return response
    # return block_json


@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def get_block_model_blocks(name=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME, json_mineral_grades_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    feature_flags_json = get_feature_flags()
    response = Response()
    valid_model = api_verification.verify_model_exists(name, json_file_name)
    if valid_model:
        data = block_model_proccesor.get_block_list(name, json_file_name, db_name, json_mineral_grades_file_name)
        if feature_flags_json["restful_response"]:
            data = {"block_model": {"blocks": data}}
        response = Response(json.dumps(data))
    else:
        response.status_code = 400
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/api/block_models/<name>/blocks/<index>', methods=['GET'])
def get_block_model_blocks_info(name, index):
    feature_flags_json = get_feature_flags()
    if not feature_flags_json["block_info"]:
        return "block_info flag is disabled"
    else:
        #TODO return more structured version of the block info
        status_code = 200
        final_data = {}
        try:
            block_data = block_model_proccesor.get_block_info_by_index(name, int(index))
            if block_data is None:
                status_code = 400
            else:
                final_data = {"block": block_data}
        except:
            status_code = 500
        response = Response(json.dumps(final_data))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.status_code = status_code
        return response


@app.route('/api/block_models/<name>/reblock', methods=['POST'])
def reblock_block_model(name=None, data=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME, json_mineral_grades_file_name=TEST_MINERAL_GRADES_INFORMATION_FILE_NAME):
    if None:
        data = request.get_json()
    response = Response()
    valid_information = api_verification.verify_reblock_information(data, name, json_file_name)
    if valid_information:
        block_model = load_block_model.get_block_model_object(name, json_file_name, db_name, json_mineral_grades_file_name)
        try:
            block_model.reblock(data["rx"], data["ry"], data["rz"], data["continuous_attributes"],
                                data["proportional_attributes"],
                                data["categorical_attributes"], data["columns_with_mass"])
            response.status_code = 200
        except:
            response.status_code = 500
    else:
        response.status_code = 400
    return response


def get_feature_flags():
    #TODO change this url to https://dry-brushlands-69779.herokuapp.com/api/feature_flags for the delivery
    feature_flags_service_url = "https://dry-brushlands-69779.herokuapp.com/api/feature_flags" #"http://localhost:8001/api/feature_flags"
    response = requests.get(feature_flags_service_url)
    feature_flags_json = response.json()
    return feature_flags_json


if __name__ == '__main__':
    app.run()
