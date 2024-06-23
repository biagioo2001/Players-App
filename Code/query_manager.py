from pymongo import MongoClient
from bson import ObjectId

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/PremierLegue'
client = MongoClient(mongo_uri)
db = client['PremierLegue']
giocatori_collection = db['Players']
stagioni_collection = db['Seasons']


def query_delete(full_name):
    query = {"full_name": full_name}
    player = giocatori_collection.find_one(query)
    if player is None:
        return None

    # Ottieni il player_id
    player_id = player["player_id"]

    # Cancella il giocatore
    risultato_giocatore = giocatori_collection.delete_one(query)
    if risultato_giocatore.deleted_count == 0:
        return None

    # Cancella tutte le stagioni associate al giocatore
    stagioni_collection.delete_many({"player_id": player_id})

    return risultato_giocatore



def query_update_age(full_name, new_age):
    # Aggiorna l'età del giocatore
    giocatori_collection.update_many(
        {'full_name': full_name},
        {"$set": {"age": new_age}}
    )

    # Recupera il documento del giocatore aggiornato
    giocatore = giocatori_collection.find_one({'full_name': full_name})

    if giocatore:
        # Recupera le stagioni del giocatore utilizzando il player_id
        player_id = giocatore.get("player_id")
        stagioni = []
        if player_id:
            stagioni = list(stagioni_collection.find({"player_id": player_id}))
        giocatore["stagioni"] = stagioni

    return giocatore

def query_all_players():
    giocatori = list(giocatori_collection.find())
    for giocatore in giocatori:
        player_id = giocatore.get("player_id")
        if player_id is not None:
            stagioni = list(stagioni_collection.find({"player_id": player_id}))
            giocatore["stagioni"] = stagioni
    return giocatori


def query_update_height_weight(full_name, new_height, new_weight):
    giocatori_collection.update_many(
        {'full_name': full_name},
        {"$set": {"height": new_height, "weight": new_weight}}
    )
    oggetti_modificati = giocatori_collection.find_one({'full_name': full_name})
    return oggetti_modificati


def query_insert_giocatore(nuovo_giocatore, stagione):
    # Ottieni il prossimo ID per il giocatore
    player_id = giocatori_collection.count_documents({})  # Count dei documenti più uno
    nuovo_giocatore["player_id"] = player_id

    # Inserisci il nuovo giocatore
    giocatori_collection.insert_one(nuovo_giocatore)

    stagione["player_id"] = player_id

    # Inserisci la nuova stagione
    stagioni_collection.insert_one(stagione)

    # Recupera il giocatore inserito con le informazioni della stagione
    giocatore_inserito = giocatori_collection.find_one({"player_id": player_id})

    if giocatore_inserito:
        # Recupera tutte le stagioni associate al giocatore
        stagioni = list(stagioni_collection.find({"player_id": player_id}))
        giocatore_inserito["stagioni"] = stagioni

    return giocatore_inserito


def query_by_nationality_and_club(nationality, current_club):
    query = {
        "nationality": nationality,
        "current_club": current_club
    }
    risultati = list(giocatori_collection.find(query))
    return risultati


def query_by_league_and_season(league, season):
    stagione = stagioni_collection.find_one({"league": league, "season": season})
    if stagione is None:
        return None

    stagione_id = stagione["_id"]
    risultati = list(giocatori_collection.find({"stagione_id": stagione_id}))
    return risultati


def query_by_age_and_position(min_age, max_age, position):
    query = {
        "age": {"$gte": min_age, "$lte": max_age},
        "position": position
    }
    risultati = list(giocatori_collection.find(query))
    return risultati


def query_by_age_and_nationality(min_age, max_age, nationality):
    query = {
        "age": {"$gte": min_age, "$lte": max_age},
        "nationality": nationality
    }
    risultati = list(giocatori_collection.find(query))
    return risultati
