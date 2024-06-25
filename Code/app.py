from flask import Flask, render_template, request
from query_manager import (
    query_delete, query_update_age, query_insert_giocatore,
    query_update_height_weight, query_by_nationality_and_position,
    query_by_min_and_gols, query_by_age_and_position, query_all_players
)
from query_manager import query_top_scorers, query_top_assists, query_minutes_played_data, query_yellow_red_cards_data

from pymongo import MongoClient

app = Flask(__name__)

# Configurazione del database MongoDB
mongo_uri = 'mongodb://localhost:27017/PremierLegue'
client = MongoClient(mongo_uri)
db = client['PremierLegue']
giocatori_collection = db['Players']
stagioni_collection = db['Seasons']

class PlayerNotFoundError(Exception):
    pass

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET'])
def query():
    return render_template('query.html')

@app.route('/players', methods=['GET'])
def players():
    try:
        players = query_all_players()
        if not players:
            raise PlayerNotFoundError("Players not found")
        return render_template('Players.html', players=players)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/query_delete', methods=['POST'])
def handle_query_delete():
    try:
        full_name = request.form.get('full_name')
        position = request.form.get('position')  # Ottieni la posizione
        risultato = query_delete(full_name, position)
        if risultato is None:
            raise PlayerNotFoundError("Player not found")
        return render_template('risultato_delete.html', oggetto=risultato)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/query_update_age', methods=['POST'])
def handle_query_update_age():
    full_name = request.form['full_name']
    new_age = int(request.form['new_age'])  # Converti l'età in intero
    try:
        oggetto = query_update_age(full_name, new_age)
        if oggetto is None:
            raise PlayerNotFoundError("Giocatore non trovato")
        return render_template('query_update_age.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))


def safe_int(value):
    try:
        return int(value) if value is not None else None
    except ValueError:
        raise BadRequest(f"Invalid integer value: {value}")

def safe_float(value):
    try:
        return float(value) if value is not None else None
    except ValueError:
        raise BadRequest(f"Invalid float value: {value}")

@app.route('/query_insert', methods=['POST'])
def handle_query_insert_giocatore():
    nuovo_giocatore = {
        "full_name": request.form.get('full_name'),
        "age": safe_int(request.form.get('age')),
        "birthday": request.form.get('birthday'),
        "birthday_GMT": request.form.get('birthday_GMT'),
        "position": request.form.get('position'),
        "current_club": request.form.get('current_club'),
        "nationality": request.form.get('nationality'),
        "player_id": request.form.get('player_id')
    }
    stagione = {
        "league": request.form.get('league'),
        "season": request.form.get('season'),
        "minutes_played_overall": safe_int(request.form.get('minutes_played_overall')),
        "minutes_played_home": safe_int(request.form.get('minutes_played_home')),
        "minutes_played_away": safe_int(request.form.get('minutes_played_away')),
        "appearances_overall": safe_int(request.form.get('appearances_overall')),
        "appearances_home": safe_int(request.form.get('appearances_home')),
        "appearances_away": safe_int(request.form.get('appearances_away')),
        "goals_overall": safe_int(request.form.get('goals_overall')),
        "goals_home": safe_int(request.form.get('goals_home')),
        "goals_away": safe_int(request.form.get('goals_away')),
        "assists_overall": safe_int(request.form.get('assists_overall')),
        "assists_home": safe_int(request.form.get('assists_home')),
        "assists_away": safe_int(request.form.get('assists_away')),
        "clean_sheets_overall": safe_int(request.form.get('clean_sheets_overall')),
        "clean_sheets_home": safe_int(request.form.get('clean_sheets_home')),
        "clean_sheets_away": safe_int(request.form.get('clean_sheets_away')),
        "conceded_overall": safe_int(request.form.get('conceded_overall')),
        "conceded_home": safe_int(request.form.get('conceded_home')),
        "conceded_away": safe_int(request.form.get('conceded_away')),
        "yellow_cards_overall": safe_int(request.form.get('yellow_cards_overall')),
        "red_cards_overall": safe_int(request.form.get('red_cards_overall')),
        "goals_involved_per_90_overall": safe_float(request.form.get('goals_involved_per_90_overall')),
        "assists_per_90_overall": safe_float(request.form.get('assists_per_90_overall')),
        "conceded_per_90_overall": safe_float(request.form.get('conceded_per_90_overall')),
        "min_per_conceded_overall": safe_float(request.form.get('min_per_conceded_overall')),
        "min_per_match": safe_float(request.form.get('min_per_match')),
        "min_per_card_overall": safe_float(request.form.get('min_per_card_overall')),
        "min_per_assist_overall": safe_float(request.form.get('min_per_assist_overall')),
        "cards_per_90_overall": safe_float(request.form.get('cards_per_90_overall')),
        "rank_in_league_top_attackers": request.form.get('rank_in_league_top_attackers'),
        "rank_in_league_top_midfielders": request.form.get('rank_in_league_top_midfielders'),
        "rank_in_league_top_defenders": request.form.get('rank_in_league_top_defenders'),
        "rank_in_club_top_scorer": request.form.get('rank_in_club_top_scorer'),
        "additional_info": request.form.get('additional_info')
    }
    try:
        # Assuming query_insert_giocatore and PlayerNotFoundError are defined elsewhere
        risultato = query_insert_giocatore(nuovo_giocatore, stagione)
        return render_template('query_insert.html', oggetto=risultato)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except BadRequest as e:
        return render_template('error.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/query_nationality_position', methods=['POST'])
def handle_query_nationality_position():
    nationality = request.form['nationality']
    position = request.form['position']
    try:
        risultati = query_by_nationality_and_position(nationality, position)
        return render_template('Players.html', players=risultati)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/query_by_min_and_gols', methods=['POST'])
def handle_query_by_min_and_gols():
    try:
        # Ottieni i valori di min e goals dal form
        min_minutes = int(request.form['min'])
        min_goals = int(request.form['goals'])

        # Esegui la query per ottenere i risultati
        risultati = query_by_min_and_gols(min_minutes, min_goals)

        # Ritorna i risultati alla pagina Players.html
        return render_template('Players.html', players=risultati)

    except ValueError:
        # Gestione degli errori nel caso di input non validi (es. non numerici)
        error_msg = 'Invalid input, please enter numbers.'
        return render_template('error.html', error=error_msg)

    except Exception as e:
        # Gestione di altre eccezioni non previste
        error_msg = str(e)
        return render_template('error.html', error=error_msg)


@app.route('/query_age_position', methods=['POST'])
def handle_query_age_position():
    try:
        min_age = int(request.form['min_age'])
        max_age = int(request.form['max_age'])
        position = request.form['position']

        # Assicurati che min_age sia minore di max_age
        if min_age > max_age:
            raise ValueError("L'età minima non può essere maggiore dell'età massima.")

        # Esegui la query per ottenere i giocatori con l'età e la posizione specificate
        risultati = query_by_age_and_position(min_age, max_age, position)

        if not risultati:
            raise PlayerNotFoundError("Nessun giocatore trovato con i criteri specificati.")

        return render_template('Players.html', players=risultati)

    except ValueError as ve:
        error_msg = f"Errore: {str(ve)}"
        return render_template('error.html', error=error_msg)

    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

    except Exception as e:
        error_msg = f"Errore imprevisto: {str(e)}"
        return render_template('error.html', error=error_msg)


@app.route('/statistics')
def statistics():
    try:
        top_scorers = query_top_scorers()
        top_assists = query_top_assists()
        minutes_data = query_minutes_played_data()
        yellow_red_cards_data = query_yellow_red_cards_data()

        return render_template('statistics.html', top_scorers=top_scorers, top_assists=top_assists, minutes_data=minutes_data, yellow_red_cards_data=yellow_red_cards_data)

    except Exception as e:
        error_msg = f"Errore durante il recupero delle statistiche: {str(e)}"
        return render_template('error.html', error=error_msg)


if __name__ == '__main__':
    app.run(debug=True)
