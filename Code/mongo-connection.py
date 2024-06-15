from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configura la connessione a MongoDB con Flask-PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Players'  # Sostituisci con l'URI del tuo database
mongo = PyMongo(app)

# Verifica la connessione a MongoDB
try:
    mongo.db.command('ping')  # Esegue un comando per verificare la connessione
    print("Connessione al database MongoDB avvenuta con successo.")
except Exception as e:
    print(f"Errore di connessione al database MongoDB: {str(e)}")

# Rotte per interagire con il database
@app.route('/api/documents', methods=['GET'])
def get_documents():
    # Seleziona il database e la collezione
    database = mongo.db  # Usa il database impostato in PyMongo
    collection = database['Giocatori']  # Sostituisci con il nome della tua collezione

    # Recupera tutti i documenti nella collezione
    documenti = collection.find()

    # Converte i documenti in una lista di dizionari (JSON serializzabile)
    documenti_list = [documento for documento in documenti]

    # Restituisci i documenti come JSON
    return jsonify(documenti_list)

if __name__ == '__main__':
    app.run(debug=True)
