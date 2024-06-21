from flask import Flask, render_template, request
from query_manager import (
    query_delete, query_update_age, query_insert_giocatore,
    query_update_height_weight, query_by_nationality_and_club,
    query_by_league_and_season, query_by_age_and_position, query_all_players,
    PlayerNotFoundError
)
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
        age = request.form.get('age')
        position = request.form.get('position')
        risultato = query_delete(full_name, age, position)
        return render_template('query_delete.html', oggetto=risultato)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/query_update_age', methods=['POST'])
def handle_query_update_age():
    full_name = request.form['full_name']
    new_age = request.form['new_age']
    try:
        oggetto = query_update_age(full_name, new_age)
        return render_template('query_update_age.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_insert', methods=['POST'])
def handle_query_insert_giocatore():
    nuovo_giocatore = {
        "full_name": request.form.get('full_name'),
        "age": int(request.form.get('age')),
        "birthday": int(request.form.get('birthday')),
        "position": request.form.get('position'),
        "current_club": request.form.get('current_club'),
        "nationality": request.form.get('nationality'),
        "appearances_overall": int(request.form.get('appearances_overall')),
        "goals_overall": int(request.form.get('goals_overall')),
        "assists_overall": int(request.form.get('assists_overall')),
        "clean_sheets_overall": int(request.form.get('clean_sheets_overall')),
        "yellow_cards_overall": int(request.form.get('yellow_cards_overall')),
        "red_cards_overall": int(request.form.get('red_cards_overall'))
    }
    stagione = {
        "league": request.form.get('league'),
        "season": request.form.get('season')
    }
    try:
        risultato = query_insert_giocatore(nuovo_giocatore, stagione)
        return render_template('query_insert.html', oggetto=risultato)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/query_nationality_club', methods=['POST'])
def handle_query_nationality_club():
    nationality = request.form['nationality']
    current_club = request.form['current_club']
    try:
        risultati = query_by_nationality_and_club(nationality, current_club)
        return render_template('query_results.html', risultati=risultati)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_league_season', methods=['POST'])
def handle_query_league_season():
    league = request.form['league']
    season = request.form['season']
    try:
        risultati = query_by_league_and_season(league, season)
        return render_template('query_results.html', risultati=risultati)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_age_position', methods=['POST'])
def handle_query_age_position():
    min_age = int(request.form['min_age'])
    max_age = int(request.form['max_age'])
    position = request.form['position']
    try:
        risultati = query_by_age_and_position(min_age, max_age, position)
        return render_template('query_results.html', risultati=risultati)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)