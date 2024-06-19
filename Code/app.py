from flask import Flask, render_template, request
from query_manager import (
    query_delete, query_update_age, query_insert_giocatore,
    query_update_height_weight, query_by_nationality_and_club,
    query_by_nationality_and_club_and_position, query_by_assists_and_clean_sheets,
    query_by_goals_assists_clean_sheets, query_all_players, PlayerNotFoundError
)

app = Flask(__name__)

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

@app.route('/query_delete', methods=['GET', 'POST'])
def handle_query_delete():
    if request.method == 'POST':
        id_player = request.form['id_player']
        try:
            risultato = query_delete(id_player)
            return render_template('risultato_delete.html', id_player=id_player)
        except PlayerNotFoundError as e:
            return render_template('player_not_found.html', error=str(e))
    return render_template('query_delete.html')

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
        "id": request.form.get('id'),
        "full_name": request.form.get('full_name'),
        "age": request.form.get('age'),
        "position": request.form.get('position'),
        "current_club": request.form.get('current_club'),
        "nationality": request.form.get('nationality'),
        "appearances_overall": request.form.get('appearances_overall'),
        "goals_overall": request.form.get('goals_overall'),
        "assists_overall": request.form.get('assists_overall'),
        "clean_sheets_overall": request.form.get('clean_sheets_overall'),
        "yellow_cards_overall": request.form.get('yellow_cards_overall'),
        "red_cards_overall": request.form.get('red_cards_overall'),
        "minutes_played_overall": request.form.get('minutes_played_overall'),
        "rating_overall": request.form.get('rating_overall')
    }
    try:
        risultato = query_insert_giocatore(nuovo_giocatore)
        return render_template('query_insert.html', oggetto=risultato)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_update_height_weight', methods=['POST'])
def handle_query_update_height_weight():
    full_name = request.form['full_name']
    new_height = request.form['new_height']
    new_weight = request.form['new_weight']
    try:
        oggetto = query_update_height_weight(full_name, new_height, new_weight)
        return render_template('query_update_height_weight.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_by_nationality_and_club', methods=['POST'])
def handle_query_by_nationality_and_club():
    nationality = request.form['nationality']
    current_club = request.form['current_club']
    try:
        oggetto = query_by_nationality_and_club(nationality, current_club)
        return render_template('query_by_nationality_and_club.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_by_nationality_and_club_and_position', methods=['POST'])
def handle_query_by_nationality_and_club_and_position():
    nationality = request.form['nationality']
    current_club = request.form['current_club']
    position = request.form['position']
    try:
        oggetto = query_by_nationality_and_club_and_position(nationality, current_club, position)
        return render_template('query_by_nationality_and_club_and_position.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_by_assists_and_clean_sheets', methods=['POST'])
def handle_query_by_assists_and_clean_sheets():
    assists_overall = float(request.form['assists_overall'])
    clean_sheets_overall = float(request.form['clean_sheets_overall'])
    try:
        oggetto = query_by_assists_and_clean_sheets(assists_overall, clean_sheets_overall)
        return render_template('query_by_assists_and_clean_sheets.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

@app.route('/query_by_goals_assists_clean_sheets', methods=['POST'])
def handle_query_by_goals_assists_clean_sheets():
    goals_overall = float(request.form['goals_overall'])
    assists_overall = float(request.form['assists_overall'])
    clean_sheets_overall = float(request.form['clean_sheets_overall'])
    try:
        oggetto = query_by_goals_assists_clean_sheets(goals_overall, assists_overall, clean_sheets_overall)
        return render_template('query_by_goals_assists_clean_sheets.html', oggetto=oggetto)
    except PlayerNotFoundError as e:
        return render_template('player_not_found.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
