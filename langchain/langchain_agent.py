from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/process', methods=['GET'])
def process():
    # Add Langchain processing logic here
    return jsonify({"message": "Processed by Langchain"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
