from bson import ObjectId
from pymongo import MongoClient
from flask import request, render_template

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/Players'
client = MongoClient(mongo_uri)
db = client['Giocatori']
collection = db['Giocatori']

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
        player = collection.find_one(query)
        if player is None:
            error_message = f"Player not found for query: {query}"
            print(error_message)
            raise PlayerNotFoundError(error_message)

        # Delete the player
        risultato = collection.delete_one(query)
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
        collection.update_many(
            {'full_name': full_name},
            {"$set": {"age": new_age}}
        )
        oggetti_modificati = collection.find_one({'full_name': full_name})
        if oggetti_modificati is None:
            raise PlayerNotFoundError("Player not found")
        return oggetti_modificati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_all_players():
    try:
        risultati = list(collection.find())
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_update_height_weight(full_name, new_height, new_weight):
    try:
        collection.update_many(
            {'full_name': full_name},
            {"$set": {"height": new_height, "weight": new_weight}}
        )
        oggetti_modificati = collection.find_one({'full_name': full_name})
        if oggetti_modificati is None:
            raise PlayerNotFoundError("Player not found")
        return oggetti_modificati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_insert_giocatore(nuovo_giocatore):
    try:
        collection.insert_one(nuovo_giocatore)
        oggetto_inserito = collection.find_one({
            "full_name": nuovo_giocatore["full_name"],
            "age": nuovo_giocatore["age"],
            "position": nuovo_giocatore["position"]
        })
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
        risultati = list(collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_nationality_and_club_and_position(nationality, current_club, position):
    try:
        query = {
            "nationality": nationality,
            "current_club": current_club,
            "position": position
        }
        risultati = list(collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_assists_and_clean_sheets(assists_overall, clean_sheets_overall):
    try:
        query = {
            "assists_overall": assists_overall,
            "clean_sheets_overall": clean_sheets_overall
        }
        risultati = list(collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_goals_assists_clean_sheets(goals_overall, assists_overall, clean_sheets_overall):
    try:
        query = {
            "goals_overall": goals_overall,
            "assists_overall": assists_overall,
            "clean_sheets_overall": clean_sheets_overall
        }
        risultati = list(collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))

def query_by_league_and_season(league, season):
    try:
        query = {
            "league": league,
            "season": season
        }
        risultati = list(collection.find(query))
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
        risultati = list(collection.find(query))
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
        risultati = list(collection.find(query))
        if len(risultati) == 0:
            raise PlayerNotFoundError("Players not found")
        return risultati
    except Exception as e:
        raise PlayerNotFoundError(str(e))
