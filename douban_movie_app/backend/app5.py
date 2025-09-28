from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "test"
}

@app.route("/api/movie_stats", methods=["GET"])
def movie_stats():
    # 查询前10电影评分
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, rating FROM movies ORDER BY rating DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    param = data.get("param", "")
    return jsonify({"message": f"第一个输入框的参数是 {param}"})

@app.route("/api/echo2", methods=["POST"])
def echo2():
    body = request.get_json()
    body_param = body.get("bodyParam", "")
    query_param = request.args.get("param", "")
    return jsonify({"message": f"body中的参数是 {body_param}, param中的参数是 {query_param}"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
