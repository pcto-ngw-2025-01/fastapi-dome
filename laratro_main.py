from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI()

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "esngwpy",
    "auth_plugin": "mysql_native_password"
}


def get_db():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Errore nel collegamento al database: {str(e)}")

@app.get("/posts")
def read_posts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post non trovato")
    return post

@app.post("/posts")
def create_post(title: str, content: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    post_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"message": "Post creato con successo", "post_id": post_id}


@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str, content: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Post aggiornato con successo"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Post eliminato con successo"}


@app.get("/users")
def read_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


@app.get("/users/{user_id}")
def read_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user

@app.post("/users")
def create_user(nome: str, email: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (nome, email) VALUES (%s, %s)", (nome, email))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"message": "Utente creato con successo", "user_id": user_id}


@app.put("/users/{user_id}")
def update_user(user_id: int, nome: str, email: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nome = %s, email = %s WHERE id = %s", (nome, email, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Utente aggiornato con successo"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Utente eliminato con successo"}

@app.patch("/posts/{post_id}/like")
def like_post(post_id: int, user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Post non trovato")
        
        cursor.execute("SELECT id FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Hai già messo mi piace a questo post")

        cursor.execute("INSERT INTO likes (user_id, post_id) VALUES (%s, %s)", (user_id, post_id))
        conn.commit()

        return {"message": "Like aggiunto con successo"}
    finally:
        cursor.close()
        conn.close()


@app.get("/posts/{post_id}/likes")
def get_likes(post_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.username
            FROM likes l
            JOIN users u ON l.user_id = u.id
            WHERE l.post_id = %s
        """, (post_id,))
        
        users = cursor.fetchall()
        usernames = [user[0] for user in users]

        return {"post_id": post_id, "liked_by_users": usernames}
    finally:
        cursor.close()
        conn.close()
