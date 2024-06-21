from bson import ObjectId
from pymongo import MongoClient
from flask import request, render_template

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/PremierLegue'
client = MongoClient(mongo_uri)
db = client['PremierLegue']
giocatori_collection = db['Players']
stagioni_collection = db['Seasons']

class PlayerNotFoundError(Exception):
    pass

def query_delete(full_name, age, position):
    try:
        query = {
            "full_name": full_name,
            "age": int(age),
            "position": position
        }
        print(f"Attempting to delete player with query: {query}")

        # Check if the player exists
        player = giocatori_collection.find_one(query)
        if player is None:
            error_message = f"Player not found for query: {query}"
            print(error_message)
            raise PlayerNotFoundError(error_message)

        # Delete the player
        risultato = giocatori_collection.delete_one(query)
        if risultato.deleted_count == 0:
            error_message = f"No documents deleted for query: {query}"
            print(error_message)
            raise PlayerNotFoundError(error_message)

        print(f"Player deleted successfully: {query}")
        return risultato

    except PlayerNotFoundError as e:
        print(f"PlayerNotFoundError in query_delete: {str(e)}")
        raise e
    except Exception as e:
        print(f"Unexpected error in query_delete: {str(e)}")
        raise PlayerNotFoundError(str(e))

def query_update_age(full_name, new_age):
    try:
        giocatori_collection.update_many(
            {'full_name': full_name},
            {"$set": {"age": new_age}}
        )
        oggetti_modificati = giocatori_collection.find_one({'full_name': full_name})
        if oggetti_modificati is None:
            raise PlayerNotFoundError("Player not found")
        return oggetti_modificati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_all_players():
    try:
        giocatori = list(giocatori_collection.find())
        if len(giocatori) == 0:
            raise PlayerNotFoundError("Players not found")

        for giocatore in giocatori:
            player_id = giocatore.get("player_id")
            if player_id is not None:
                stagioni = list(stagioni_collection.find({"player_id": player_id}))
                giocatore["stagioni"] = stagioni

        return giocatori
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_update_height_weight(full_name, new_height, new_weight):
    try:
        giocatori_collection.update_many(
            {'full_name': full_name},
            {"$set": {"height": new_height, "weight": new_weight}}
        )
        oggetti_modificati = giocatori_collection.find_one({'full_name': full_name})
        if oggetti_modificati is None:
            raise PlayerNotFoundError("Player not found")
        return oggetti_modificati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_insert_giocatore(nuovo_giocatore, stagione):
    try:
        giocatori_collection.insert_one(nuovo_giocatore)
        stagione_id = stagione.get('_id')
        if not stagione_id:
            stagione_id = stagioni_collection.insert_one(stagione).inserted_id
        giocatori_collection.update_one(
            {"_id": nuovo_giocatore["_id"]},
            {"$set": {"stagione_id": stagione_id}}
        )
        oggetto_inserito = giocatori_collection.find_one({"_id": nuovo_giocatore["_id"]})
        if oggetto_inserito is None:
            raise PlayerNotFoundError("Player not inserted")
        return oggetto_inserito
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_nationality_and_club(nationality, current_club):
    try:
        query = {
            "nationality": nationality,
            "current_club": current_club
        }
        risultati = list(giocatori_collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_league_and_season(league, season):
    try:
        stagione = stagioni_collection.find_one({"league": league, "season": season})
        if stagione is None:
            raise PlayerNotFoundError("Season not found")

        stagione_id = stagione["_id"]
        risultati = list(giocatori_collection.find({"stagione_id": stagione_id}))

        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_age_and_position(min_age, max_age, position):
    try:
        query = {
            "age": {"$gte": min_age, "$lte": max_age},
            "position": position
        }
        risultati = list(giocatori_collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_age_and_nationality(min_age, max_age, nationality):
    try:
        query = {
            "age": {"$gte": min_age, "$lte": max_age},
            "nationality": nationality
        }
        risultati = list(giocatori_collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))
