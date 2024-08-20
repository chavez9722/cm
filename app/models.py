from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=True)
    cloud_account_number = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(255), nullable=True)
    usage_type = db.Column(db.String(255), nullable=True)
    price_book = db.Column(db.String(255), nullable=True)
    seller_cost = db.Column(db.Numeric(10, 2), nullable=True)
    customer_cost = db.Column(db.Numeric(10, 2), nullable=True)
    margin = db.Column(db.Numeric(10, 2), nullable=True)
    usage_quantity = db.Column(db.Numeric(10, 2), nullable=True)
    user_version = db.Column(db.String(255), nullable=True)
    user_solicitante = db.Column(db.String(255), nullable=True)
    user_proyecto = db.Column(db.String(255), nullable=True)
    user_capa = db.Column(db.String(255), nullable=True)
    user_centro_costos = db.Column(db.String(255), nullable=True)
    user_entorno = db.Column(db.String(255), nullable=True)
    user_nombre_objeto = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=True)
