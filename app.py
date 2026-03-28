from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    role TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS notices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    category TEXT,
                    description TEXT)''')

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                    (user,pwd,role))

        conn.commit()
        conn.close()

        return redirect("/")
    
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (user,pwd))
    
    data = cur.fetchone()
    conn.close()

    if data:
        session["user"] = data[1]
        session["role"] = data[3]

        if data[3] == "admin":
            return redirect("/admin")
        else:
            return redirect("/dashboard")
    else:
        return "Invalid Login"

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM notices")
    notices = cur.fetchall()

    conn.close()
    return render_template("dashboard.html", notices=notices)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        title = request.form["title"]
        cat = request.form["category"]
        desc = request.form["description"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO notices (title,category,description) VALUES (?,?,?)",
                    (title,cat,desc))

        conn.commit()
        conn.close()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM notices")
    notices = cur.fetchall()
    conn.close()

    return render_template("admin.html", notices=notices)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
