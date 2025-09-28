from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ✅ 数据库连接（你已经能用了，不改）
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="test"
    )

# ---- API 1: 获取全部电影 ----
@app.route('/api/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT movie_rank, title, rating FROM movies ORDER BY movie_rank")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(movies)

# ---- API 2: 根据条件筛选电影 ----
@app.route('/api/filter_movies', methods=['POST'])
def filter_movies():
    data = request.json
    title = data.get("title", "")
    min_rating = data.get("min_rating", None)
    rank_range = data.get("rank_range", "")

    query = "SELECT movie_rank, title, rating FROM movies WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")

    if min_rating:
        query += " AND rating >= %s"
        params.append(float(min_rating))

    if rank_range and "-" in rank_range:
        start, end = rank_range.split("-")
        query += " AND movie_rank BETWEEN %s AND %s"
        params.append(int(start))
        params.append(int(end))

    query += " ORDER BY movie_rank"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(movies)

# ---- API 3: 接收 param & body ----
@app.route('/api/echo2', methods=['POST'])
def echo2():
    body_data = request.json
    body_param = body_data.get("body_param", "")

    query_param = request.args.get("param", "")

    return jsonify({
        "message": f"body 中的参数是 {body_param}, param 中的参数是 {query_param}"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
