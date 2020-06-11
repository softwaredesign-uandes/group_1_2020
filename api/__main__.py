from flask import Flask, jsonify, request
import block_model_proccesor
app = Flask(__name__)

@app.route('/')
def Index():
    return 'Hello World'


@app.route('/api/block_models/', methods=['GET'])
def get_block_models_names():
    return 'block models'


@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def get_block_model_blocks(name=None):
    block_list = block_model_proccesor.get_block_list(name)
    return jsonify(block_list)


@app.route('/api/block_models/post/', methods=['POST'])
def post_block_model_blocks():
    block_json = request.get_json()
    print(block_json)
    return block_json


if __name__ == '__main__':
    app.run(port=3000, debug=True)
