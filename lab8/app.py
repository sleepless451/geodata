from flask import Flask, jsonify
import json
import os
# підглядав у Менчинського

app = Flask(__name__)
	
@app.route('/')
def hello():
  return 'Hello, World!'

@app.route('/get_json/<string:filename>', methods=['GET'])
def get_json(filename):
  try:
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, filename + '.json')
    with open(filename, 'r') as file:
      json_data = file.read()
      return jsonify(json_data)
  except FileNotFoundError:
    return jsonify({'error': 'File not found'})

@app.route('/field/<string:field_name>', methods=['GET'])
def get_field(field_name):
    with open('../dataset2/dataset_output.json') as f:
        dataset = json.load(f)

    found_object = None
    for feature in dataset:
        properties = feature['properties']
        if properties['name'] == field_name:
            found_object = feature
            break

    if not found_object:
        return jsonify({'message': 'Field not found.'})

    return found_object

if __name__ == '__main__':
    app.run(debug=True)