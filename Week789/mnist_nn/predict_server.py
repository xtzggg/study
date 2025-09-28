from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from neural_network import NeuralNetwork
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nn = NeuralNetwork(input_size=784, hidden_size=100, output_size=10)
weights = np.load("weights.npy", allow_pickle=True).item()
nn.W1 = weights["W1"]
nn.b1 = weights["b1"]
nn.W2 = weights["W2"]
nn.b2 = weights["b2"]

def preprocess_image(file):
    img = Image.open(file).convert('L')
    img = img.resize((28,28))
    img_array = np.array(img)
    img_array = 255 - img_array
    img_array = img_array / 255.0
    img_array = img_array.flatten().reshape(1, -1)

    print("图片处理后 shape:", img_array.shape)
    return img_array

#1
# @app.route("/api/predict_digit", methods=["POST"])
# def predict_digit():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
#     file = request.files["file"]
#     img_array = preprocess_image(file)
#     pred = nn.predict(img_array)[0]
#     return jsonify({"result": int(pred)})

@app.route("/api/predict_digit", methods=["POST"])
def predict_digit():
    if "file" not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    file = request.files["file"]
    img_array = preprocess_image(file)
    pred = nn.predict(img_array)[0]

    print("预测结果:", pred)  # 调试用
    # return jsonify({"result": int(pred)})
    return jsonify({"result": int(pred)}), 200



if __name__ == "__main__":
    app.run(port=5001, debug=True)
