# myapp/data_extraction.py
import pandas as pd
from .models import BE, Invoice, Customers
from sklearn.ensemble import IsolationForest
import joblib

def extract_data():
    # Extraire les données des modèles Django
    invoices = Invoice.objects.all().select_related('be__customers')
    data = []

    for invoice in invoices:
        num = invoice.number
        be_num = invoice.be.pk
        sm_eqv = invoice.be.sm_eqv
        total = invoice.total
        client_id = invoice.be.customers.pk
        data.append({'be_num':be_num,'num':num,'sm_eqv': sm_eqv, 'total': total, 'client_id': client_id})

    # Créer un DataFrame Pandas
    df = pd.DataFrame(data)
    
    X = df[['sm_eqv', 'total', 'client_id']]
    


    # Entraîner le modèle Isolation Forest
    model = IsolationForest(contamination=0.1, random_state=42)
    df['is_fraud'] = model.fit_predict(X)
    df['is_fraud'] = df['is_fraud'].apply(lambda x: x == -1)
    
    #print(df)  # Display the dataframe with the new 'is_fraud' column
    invoices_to_update = []
    for invoice,fraud in zip(invoices,df['is_fraud']):
        invoice.is_fraud = fraud
        invoices_to_update.append(invoice)
    Invoice.objects.bulk_update(invoices_to_update, ['is_fraud'])
    joblib.dump(model, 'fraud_detection_model.pkl')

