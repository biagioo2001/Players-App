from bson import ObjectId
from pymongo import MongoClient

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
        print(f"Deleting player with full_name: {full_name}, age: {age}, position: {position}")
        print(f"Query to MongoDB: {query}")
        risultato = collection.delete_one(query)
        if risultato.deleted_count == 0:
            raise PlayerNotFoundError(f"Player not found for query: {query}")
        return risultato
    except Exception as e:
        print(f"Error in query_delete: {str(e)}")
        raise PlayerNotFoundError(str(e))


def query_update_age(full_name, new_age):
    try:
        risultati = collection.update_many(
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
        risultati = collection.update_many(
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
        oggetto_inserito = collection.find_one({"id": nuovo_giocatore["id"]})
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
