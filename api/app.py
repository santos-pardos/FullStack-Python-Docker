import os
import json
from flask import Flask, request, jsonify
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fintech:fintechpassword@localhost:5432/fintechdb")

app = Flask(__name__)

def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/accounts")
def list_accounts():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM accounts ORDER BY id")
            rows = cur.fetchall()
            return jsonify(rows)

@app.post("/accounts")
def create_account():
    data = request.get_json(force=True)
    name = data.get("owner_name")
    balance = float(data.get("balance", 0))
    if not name:
        return {"error":"owner_name required"}, 400
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO accounts (owner_name, balance) VALUES (%s, %s) RETURNING *", (name, balance))
            acc = cur.fetchone()
            conn.commit()
            return jsonify(acc), 201

@app.get("/accounts/<int:acc_id>")
def get_account(acc_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM accounts WHERE id=%s", (acc_id,))
            acc = cur.fetchone()
            if not acc: return {"error":"not found"}, 404
            return jsonify(acc)

@app.get("/accounts/<int:acc_id>/transactions")
def list_tx(acc_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM transactions WHERE account_id=%s ORDER BY created_at DESC, id DESC", (acc_id,))
            rows = cur.fetchall()
            return jsonify(rows)

@app.post("/accounts/<int:acc_id>/deposit")
def deposit(acc_id):
    data = request.get_json(force=True)
    amount = float(data.get("amount", 0))
    note = data.get("note")
    if amount <= 0:
        return {"error":"amount must be positive"}, 400
    with get_conn() as conn:
        with conn.cursor() as cur:
            # update balance
            cur.execute("UPDATE accounts SET balance = balance + %s WHERE id=%s RETURNING balance", (amount, acc_id))
            if cur.rowcount == 0:
                return {"error":"account not found"}, 404
            new_balance = cur.fetchone()["balance"]
            cur.execute("INSERT INTO transactions (account_id, amount, kind, note) VALUES (%s,%s,'deposit',%s)", (acc_id, amount, note))
            conn.commit()
            return {"account_id": acc_id, "new_balance": float(new_balance)}, 201

@app.post("/accounts/<int:acc_id>/withdraw")
def withdraw(acc_id):
    data = request.get_json(force=True)
    amount = float(data.get("amount", 0))
    note = data.get("note")
    if amount <= 0:
        return {"error":"amount must be positive"}, 400
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT balance FROM accounts WHERE id=%s", (acc_id,))
            row = cur.fetchone()
            if not row: return {"error":"account not found"}, 404
            if row["balance"] < amount:
                return {"error":"insufficient funds"}, 400
            cur.execute("UPDATE accounts SET balance = balance - %s WHERE id=%s RETURNING balance", (amount, acc_id))
            new_balance = cur.fetchone()["balance"]
            cur.execute("INSERT INTO transactions (account_id, amount, kind, note) VALUES (%s,%s,'withdrawal',%s)", (acc_id, amount, note))
            conn.commit()
            return {"account_id": acc_id, "new_balance": float(new_balance)}, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
