from flask import Flask, jsonify, Response
import json
import block_model_proccesor
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

if __name__ == '__main__':
    app.run(port=3000, debug=True)
