from pymongo import MongoClient
from bson import ObjectId

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/PremierLegue'
client = MongoClient(mongo_uri)
db = client['PremierLegue']
giocatori_collection = db['Players']
stagioni_collection = db['Seasons']


class DuplicatePlayerError(Exception):
    pass


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def query_delete(full_name, position):
    query = {"full_name": full_name, "position": position}  # Aggiungi la posizione alla query
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

    existing_player = giocatori_collection.find_one({
        "full_name": nuovo_giocatore["full_name"],
        "position": nuovo_giocatore["position"]
    })
    if existing_player:
        raise DuplicatePlayerError("Duplicate player found.")

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


def query_by_nationality_and_position(nationality, position):
    query = {
        "nationality": nationality,
        "position": position
    }
    giocatori = list(giocatori_collection.find(query))
    for giocatore in giocatori:
        stagioni = list(stagioni_collection.find({"player_id": giocatore["player_id"]}))
        giocatore["stagioni"] = stagioni
    return giocatori


def query_by_min_and_gols(min_minutes, min_goals):
    risultati = []

    # Trova tutte le stagioni che soddisfano i criteri di gol e minutaggio
    stagioni = stagioni_collection.find({
        "minutes_played_overall": {"$gt": min_minutes},
        "goals_overall": {"$gt": min_goals}
    })

    # Itera su tutte le stagioni trovate
    for stagione in stagioni:
        player_id = stagione.get("player_id")
        if player_id:
            # Trova il giocatore corrispondente utilizzando player_id
            giocatore = giocatori_collection.find_one({"player_id": player_id})
            if giocatore:
                # Aggiungi le informazioni delle stagioni al giocatore
                stagioni_giocatore = list(stagioni_collection.find({"player_id": player_id}))
                giocatore["stagioni"] = stagioni_giocatore
                risultati.append(giocatore)

    return risultati


def query_by_age_and_position(min_age, max_age, position):
    try:
        query = {
            "age": {"$gte": min_age, "$lte": max_age},
            "position": position
        }

        risultati = []

        # Trova i giocatori che soddisfano i criteri
        giocatori = giocatori_collection.find(query)

        for giocatore in giocatori:
            # Recupera le stagioni associate al giocatore
            player_id = giocatore.get("player_id")
            stagioni = []
            if player_id:
                stagioni = list(stagioni_collection.find({"player_id": player_id}))
                giocatore["stagioni"] = stagioni
            risultati.append(giocatore)

        return risultati

    except Exception as e:
        # Gestione generale delle eccezioni
        print(f"Errore nella query_by_age_and_position: {str(e)}")
        return []


def query_top_scorers():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "Seasons",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "seasons_data"
                }
            },
            {
                "$unwind": "$seasons_data"
            },
            {
                "$sort": {"seasons_data.goals_overall": -1}
            },
            {
                "$limit": 10
            },
            {
                "$lookup": {
                    "from": "Players",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "player_data"
                }
            },
            {
                "$unwind": "$player_data"
            },
            {
                "$project": {
                    "_id": 0,
                    "full_name": 1,
                    "club": "$player_data.Current Club",
                    "goals_overall": "$seasons_data.goals_overall"
                }
            }
        ]
        top_scorers = list(giocatori_collection.aggregate(pipeline))

        # Stampa il risultato ottenuto
        print("Risultato di query_top_scorers():", top_scorers)

        return top_scorers

    except Exception as e:
        print(f"Errore durante la query_top_scorers: {str(e)}")
        raise e


def query_top_assists():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "Seasons",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "seasons_data"
                }
            },
            {
                "$unwind": "$seasons_data"
            },
            {
                "$sort": {"seasons_data.assists_overall": -1}
            },
            {
                "$limit": 10
            },
            {
                "$lookup": {
                    "from": "Players",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "player_data"
                }
            },
            {
                "$unwind": "$player_data"
            },
            {
                "$project": {
                    "_id": 0,
                    "full_name": 1,
                    "club": "$player_data.Current Club",
                    "assists_overall": "$seasons_data.assists_overall"
                }
            }
        ]
        top_assists = list(giocatori_collection.aggregate(pipeline))

        # Stampa il risultato ottenuto
        print("Risultato di query_top_assists():", top_assists)

        return top_assists

    except Exception as e:
        print(f"Errore durante la query_top_assists: {str(e)}")
        raise e




def query_minutes_played_data():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "Seasons",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "seasons_data"
                }
            },
            {
                "$unwind": "$seasons_data"
            },
            {
                "$project": {
                    "_id": 0,
                    "full_name": 1,
                    "season": "$seasons_data.season",
                    "minutes_played_overall": "$seasons_data.minutes_played_overall",
                    "minutes_played_home": "$seasons_data.minutes_played_home",
                    "minutes_played_away": "$seasons_data.minutes_played_away"
                }
            }
        ]

        players_minutes = list(giocatori_collection.aggregate(pipeline))

        return players_minutes

    except Exception as e:
        print(f"Errore durante la query_minutes_played_data: {str(e)}")
        raise e


def query_yellow_red_cards_data():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "Seasons",
                    "localField": "player_id",
                    "foreignField": "player_id",
                    "as": "seasons_data"
                }
            },
            {
                "$unwind": "$seasons_data"
            },
            {
                "$group": {
                    "_id": {
                        "league": "$seasons_data.league",
                        "season": "$seasons_data.season"
                    },
                    "total_yellow_cards": {"$sum": "$seasons_data.yellow_cards_overall"},
                    "total_red_cards": {"$sum": "$seasons_data.red_cards_overall"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "league": "$_id.league",
                    "season": "$_id.season",
                    "total_yellow_cards": 1,
                    "total_red_cards": 1
                }
            }
        ]

        yellow_red_cards_data = list(giocatori_collection.aggregate(pipeline))

        # Stampa il risultato ottenuto
        print("Risultato di query_yellow_red_cards_data():", yellow_red_cards_data)

        return yellow_red_cards_data

    except Exception as e:
        print(f"Errore durante la query_yellow_red_cards_data: {str(e)}")
        raise e

