from bson import ObjectId
from pymongo import MongoClient
import pymongo

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/Players'
client = MongoClient(mongo_uri)
db = client['Giocatori']
collection = db['Giocatori']

# Funzione per rimuovere un giocatore in base all'id
def query_delete(id_player):
    query = {"_id": ObjectId(id_player)}
    risultato = collection.delete_one(query)
    return risultato

# Funzione per aggiornare l'età di un giocatore in base al nome
def query_update_age(full_name, new_age):
    risultati = collection.update_many(
        {'full_name': full_name},
        {"$set": {"age": new_age}}
    )
    oggetti_modificati = collection.find_one({'full_name': full_name})
    return oggetti_modificati

# Funzione per aggiornare altezza e peso di un giocatore in base al nome
def query_update_height_weight(full_name, new_height, new_weight):
    risultati = collection.update_many(
        {'full_name': full_name},
        {"$set": {"height": new_height, "weight": new_weight}}
    )
    oggetti_modificati = collection.find_one({'full_name': full_name})
    return oggetti_modificati

# Funzione per inserire un nuovo giocatore
def query_insert_giocatore(nuovo_giocatore):
    collection.insert_one(nuovo_giocatore)
    oggetto_inserito = collection.find_one({"id": nuovo_giocatore["id"]})
    return oggetto_inserito

# Funzione per trovare giocatori per nazionalità e club
def query_by_nationality_and_club(nationality, current_club):
    query = {
        "nationality": nationality,
        "current_club": current_club
    }
    risultati = collection.find(query)
    return risultati

# Funzione per trovare giocatori per nazionalità, club e posizione
def query_by_nationality_and_club_and_position(nationality, current_club, position):
    query = {
        "nationality": nationality,
        "current_club": current_club,
        "position": position
    }
    risultati = collection.find(query)
    return risultati

# Funzione per trovare giocatori per assist e clean sheets
def query_by_assists_and_clean_sheets(assists_overall, clean_sheets_overall):
    query = {
        "assists_overall": assists_overall,
        "clean_sheets_overall": clean_sheets_overall
    }
    risultati = collection.find(query)
    return risultati

# Funzione per trovare giocatori per gol, assist e clean sheets
def query_by_goals_assists_clean_sheets(goals_overall, assists_overall, clean_sheets_overall):
    query = {
        "goals_overall": goals_overall,
        "assists_overall": assists_overall,
        "clean_sheets_overall": clean_sheets_overall
    }
    risultati = collection.find(query)
    return risultati
