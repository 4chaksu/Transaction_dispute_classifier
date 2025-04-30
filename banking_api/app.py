from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Numeric, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from decimal import Decimal

# DB Config 
DB_CONFIG = {
    "dbname": "Employee",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# account 
class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Numeric(15, 2), default=0.00)
    updated_at = Column(DateTime, default=datetime.utcnow)

#  create table and account
def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if not session.query(Account).filter(Account.id == "abc123").first():
            account = Account(id="abc123", name="Vinay", balance=1000.00)
            session.add(account)
            session.commit()
            print("Sample account created")
    except:
        session.rollback()
    finally:
        session.close()

app = Flask(__name__)
init_db()

#depbit endpoint
@app.route("/transaction/debit", methods=["POST"])
def debit_account():
    data = request.json
    session = SessionLocal()
    try:
        account = session.query(Account).with_for_update().filter(Account.id == data["account_id"]).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        if account.balance < data["amount"]:
            return jsonify({"error": "Insufficient balance"}), 400

        account.balance -= Decimal(data["amount"])
        account.updated_at = datetime.utcnow()
        session.commit()
        return jsonify({"message": "Debit successful", "balance": float(account.balance)})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

#credit endpoint
@app.route("/transaction/credit", methods=["POST"])
def credit_account():
    data = request.json
    session = SessionLocal()
    try:
        account = session.query(Account).with_for_update().filter(Account.id == data["account_id"]).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404

        account.balance += Decimal(data["amount"])
        account.updated_at = datetime.utcnow()
        session.commit()
        return jsonify({"message": "Credit successful", "balance": float(account.balance)})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# balance endpoint
@app.route("/account/<account_id>/balance", methods=["GET"])
def get_balance(account_id):
    session = SessionLocal()
    try:
        account = session.query(Account).filter(Account.id == account_id).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        return jsonify({"account_id": account.id, "balance": float(account.balance)})
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
