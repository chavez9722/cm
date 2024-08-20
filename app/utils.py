import pandas as pd
from datetime import datetime
from .models import db, Data

def process_file(file):
    # Determina si es CSV o XLSX
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return {'status': 'error', 'message': 'File format not supported'}

    # Verifica la estructura del archivo
    required_columns = [
        "Customer Name", "Cloud Account Number", "Product Name", "Usage Type", "Price Book",
        "Seller Cost (USD)", "Customer Cost (USD)", "Margin (USD)", "Usage Quantity",
        "user:Version (tag)", "user:Solicitante (tag)", "user:Proyecto (tag)", "user:Capa (tag)", "user:Centro_Costos (tag)",
        "user:Entorno (tag)", "user:Nombre_Objeto (tag)", "date"
    ]

    if not all(col in df.columns for col in required_columns):
        return {'status': 'error', 'message': 'Missing required columns'}

    # Convertir la columna de fecha con el formato dd/mm/yyyy
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    # Reemplaza NaN con None en todo el DataFrame
    df = df.applymap(lambda x: None if pd.isna(x) else x)

    # Obtener el mes y año de los registros existentes en la base de datos
    existing_dates = db.session.query(db.func.date_format(Data.date, '%Y-%m')).distinct().all()
    existing_dates = [date[0] for date in existing_dates]

    # Crear un conjunto para almacenar las fechas a eliminar
    dates_to_delete = set()

    # Verificar si hay fechas duplicadas
    for _, row in df.iterrows():
        if pd.notna(row['date']):  # Verifica que row['date'] no sea NaT
            record_month_year = row['date'].strftime('%Y-%m')
            if record_month_year in existing_dates:
                record_day = row['date'].strftime('%d')
                id_db_record = (
                    db.session.query(Data.id)
                    .filter(record_month_year == db.func.date_format(Data.date, '%Y-%m'))
                    .first()
                )[0]

                # Obtener la fecha completa del registro
                date_db_record = (
                    db.session.query(Data.date)
                    .filter(Data.id == id_db_record)
                    .first()
                )[0]

                # Verificar si la fecha del registro es más reciente
                existing_day = (
                    db.session.query(db.func.date_format(Data.date, '%d'))
                    .filter(Data.id == id_db_record)
                    .first()
                )[0]
                if int(record_day) <= int(existing_day):
                    return {'status': 'error', 'message': 'Ya se cuenta con registros de fecha más reciente.'}

                # Agregar la fecha a eliminar al conjunto
                dates_to_delete.add(date_db_record)

    # Eliminar todos los registros con las fechas recopiladas
    if dates_to_delete:
        db.session.query(Data).filter(Data.date.in_(dates_to_delete)).delete(synchronize_session='fetch')
        db.session.commit()

    # Inserta los datos en la base de datos
    for _, row in df.iterrows():
        if pd.notna(row['date']):  # Verifica que row['date'] no sea NaT
            data = Data(
                customer_name=row.get('Customer Name'),
                cloud_account_number=row.get('Cloud Account Number'),
                product_name=row.get('Product Name'),
                usage_type=row.get('Usage Type'),
                price_book=row.get('Price Book'),
                seller_cost=round(row.get('Seller Cost (USD)'), 2) if row.get('Seller Cost (USD)') is not None else None,
                customer_cost=round(row.get('Customer Cost (USD)'), 2) if row.get('Customer Cost (USD)') is not None else None,
                margin=round(row.get('Margin (USD)'), 2) if row.get('Margin (USD)') is not None else None,
                usage_quantity=round(row.get('Usage Quantity'), 2) if row.get('Usage Quantity') is not None else None,
                user_version=row.get('user:Version (tag)'),
                user_solicitante=row.get('user:Solicitante (tag)'),
                user_proyecto=row.get('user:Proyecto (tag)'),
                user_capa=row.get('user:Capa (tag)'),
                user_centro_costos=row.get('user:Centro_Costos (tag)'),
                user_entorno=row.get('user:Entorno (tag)'),
                user_nombre_objeto=row.get('user:Nombre_Objeto (tag)'),
                date=row.get('date')
            )
            db.session.add(data)
    db.session.commit()
    
    return {'status': 'success', 'message': 'File processed successfully'}
