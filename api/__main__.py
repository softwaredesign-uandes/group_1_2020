from flask import Flask, Response, request
from werkzeug.utils import secure_filename
import json, requests, os
from block_model_cli.__main__ import check_neccesary_files_existence
import block_model_proccesor, api_verification, load_block_model
from constants import LOADED_MODELS_INFORMATION_FILE_NAME, DB_NAME, SPAN_TRACING_ID_FILE_NAME, \
    MINERAL_GRADES_INFORMATION_FILE_NAME, ACTUAL_SPAN_APP_ENVIRONMENT


UPLOAD_FOLDER = 'prec_files'
ALLOWED_EXTENSIONS = {"prec"}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def Index():
    return 'Hello World 2'


@app.route('/api/block_models/<name>/precedence', methods=['POST'])
def load_block_model_precedence(model_prec=None, name=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME):
    response = Response()
    verify_name = api_verification.verify_model_exists(name, json_file_name)
    if not verify_name:
        response.status_code = 400
        return response
    if not model_prec:
        if 'file' not in request.files:
            response.status_code = 400
            return response
        model_prec = request.files['file']
    if model_prec.filename == '':
        response.status_code = 400
        return response
    if model_prec and allowed_file(model_prec.filename):
        filename = secure_filename(model_prec.filename)
        path = os.path.join(os.getcwd(),app.config["UPLOAD_FOLDER"], filename)
        model_prec.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        response.status_code = 200
        try:
            post_span_to_trace("block_model_precedences_loaded", name)
        except:
            pass
        return response


@app.route('/api/block_models/<name>/blocks/<index>/extract')
def extract_block(name=None, index=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME,
                json_mineral_grades_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME, db_name=DB_NAME):
    response = Response()
    verify_name = api_verification.verify_model_exists(name, json_file_name)
    if not verify_name:
        response.status_code = 400
        return response
    block_model = load_block_model.get_block_model_object(name, json_file_name, db_name, json_mineral_grades_file_name)
    if not block_model.has_precedence():
        response.status_code = 400
        return response
    blocks_to_extract = block_model.extract(index)
    response = Response(json.dumps(blocks_to_extract))
    try:
        coordinates_tuple = block_model_proccesor.get_block_coordinates_by_index(block_model, int(index))
        if coordinates_tuple:
            x, y, z = coordinates_tuple
            post_span_to_trace("block_extracted", "{},{},{}".format(x, y, z))
    except:
        pass
    return response


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
        try:
            increase_span_id()
            post_span_to_trace("block_model_loaded", block_json["name"])
        except:
            pass
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
        try:
            post_span_to_trace("blocks_requested", name)
        except:
            pass
    else:
        response.status_code = 400
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/api/block_models/<name>/blocks/<index>', methods=['GET'])
def get_block_info(name, index, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME, json_mineral_grades_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    feature_flags_json = get_feature_flags()
    if not feature_flags_json["block_info"]:
        response = Response()
        response.status_code = 501
        return response
    else:
        status_code = 200
        final_data = {}
        try:
            block_data = block_model_proccesor.get_block_info_by_index(name, int(index), json_file_name, db_name, json_mineral_grades_file_name)
            if block_data is None:
                status_code = 400
            else:
                final_data = {"block": block_data}
                try:
                    x = block_data["x"]
                    y = block_data["y"]
                    z = block_data["z"]
                    post_span_to_trace(event_name="block_info_requested", event_data="{},{},{}".format(x, y, z))
                except:
                    pass
        except:
            status_code = 500
        response = Response(json.dumps(final_data))
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.status_code = status_code
        return response


@app.route('/api/block_models/<name>/reblock', methods=['POST'])
def reblock_block_model(name=None, data=None, json_file_name=LOADED_MODELS_INFORMATION_FILE_NAME, db_name=DB_NAME, json_mineral_grades_file_name=MINERAL_GRADES_INFORMATION_FILE_NAME):
    if not data:
        data = request.get_json()
    response = Response()
    valid_information = api_verification.verify_reblock_information(data, name, json_file_name)
    if valid_information:
        block_model = load_block_model.get_block_model_object(name, json_file_name, db_name, json_mineral_grades_file_name)
        try:
            reblock_model = block_model.reblock(data["rx"], data["ry"], data["rz"], data["continuous_attributes"],
                                data["proportional_attributes"],
                                data["categorical_attributes"], data["columns_with_mass"])
            if load_block_model.load_block_model_object(reblock_model, db_name, json_file_name, json_mineral_grades_file_name):
                response.status_code = 200
                try:
                    post_span_to_trace("block_model_reblocked", name)
                except:
                    pass
            else:
                response.status_code = 500
        except:
            response.status_code = 500
    else:
        response.status_code = 400
    return response


def get_feature_flags():
    feature_flags_service_url = "https://dry-brushlands-69779.herokuapp.com/api/feature_flags" #"http://localhost:8001/api/feature_flags"
    response = requests.get(feature_flags_service_url)
    feature_flags_json = response.json()
    return feature_flags_json


def post_span_to_trace(event_name, event_data):
    try:
        trace_app_id = {"dev": "e824d2cb6fe313706126ad7d49b70f4b", "production": "dd6c385e8e294557673d35675f0f0c96"}
        tracing_endpoint_url = "https://gentle-coast-69723.herokuapp.com/api/apps/{}/traces/".format(trace_app_id[ACTUAL_SPAN_APP_ENVIRONMENT])
        actual_span_id = get_actual_span_id()
        data = {"trace": {"span_id": actual_span_id, "event_name": event_name, "event_data": event_data}}
        headers = {'Content-Type': 'application/json'}
        post = requests.post(tracing_endpoint_url, data=json.dumps(data), headers=headers)
        return post
    except:
        return None


def get_actual_span_id():
    with open(SPAN_TRACING_ID_FILE_NAME, "r") as span_id_file:
        data = json.load(span_id_file)
    return data["span_id"]


def increase_span_id():
    with open(SPAN_TRACING_ID_FILE_NAME, "r") as span_id_file:
        data = json.load(span_id_file)
    data["span_id"] += 1
    with open(SPAN_TRACING_ID_FILE_NAME, 'w') as span_id_file:
        json.dump(data, span_id_file)


if __name__ == '__main__':
    check_neccesary_files_existence()
    app.run(debug=True)
