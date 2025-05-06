from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Konfigurasi Database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="",  
    database="flask_db"
)
cursor = db.cursor()

# Halaman Pembuka 
@app.route("/")
def welcome():
    return render_template("welcome.html")  # Tampilkan laman pembuka

# Halaman CV Utama
@app.route("/home")
def home():
    return render_template("index.html")  # Laman utama CV

# Endpoint GET: Ambil Semua Pengguna
@app.route("/api/users", methods=["GET"])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(users)

# Endpoint POST: Tambah Pengguna Baru
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (data["name"],))
    db.commit()
    return jsonify({"message": "User Ditambahkan!"}), 201

#  Endpoint PUT: Edit Nama Pengguna
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    cursor.execute("UPDATE users SET name=%s WHERE id=%s", (data["name"], user_id))
    db.commit()
    return jsonify({"message": "User Berhasil di ganti!"})

# Endpoint DELETE: Hapus Pengguna
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    return jsonify({"message": "User Berhasil Dihapus!"})

@app.route("/")
def index():
    return render_template("index.html") 

if __name__ == "__main__":
    app.run(debug=True)
