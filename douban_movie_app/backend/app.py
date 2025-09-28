from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "test"
}

# ================= 用户模块 =================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "用户名已存在"}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "注册成功"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"success": True, "message": "登录成功"})
    else:
        return jsonify({"success": False, "message": "用户名或密码错误"})


# ================= 电影数据接口（保留） =================
@app.route("/api/movie_stats", methods=["GET"])
def movie_stats():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, rating FROM movies ORDER BY rating DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# ================= 输入框接口（保留） =================
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
