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

    risultato = giocatori_collection.delete_one(query)
    if risultato.deleted_count == 0:
        return None

    return risultato


def query_update_age(full_name, new_age):
    giocatori_collection.update_many(
        {'full_name': full_name},
        {"$set": {"age": new_age}}
    )
    oggetti_modificati = giocatori_collection.find_one({'full_name': full_name})
    return oggetti_modificati


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
    giocatori_collection.insert_one(nuovo_giocatore)
    stagione_id = stagione.get('_id')
    if not stagione_id:
        stagione_id = stagioni_collection.insert_one(stagione).inserted_id
    giocatori_collection.update_one(
        {"_id": nuovo_giocatore["_id"]},
        {"$set": {"stagione_id": stagione_id}}
    )
    oggetto_inserito = giocatori_collection.find_one({"_id": nuovo_giocatore["_id"]})
    return oggetto_inserito


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
