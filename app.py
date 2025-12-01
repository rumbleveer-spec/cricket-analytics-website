from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Database Models
class BBLMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_no = db.Column(db.Integer)
    date = db.Column(db.String(20))
    venue = db.Column(db.String(100))
    team1 = db.Column(db.String(50))
    score1 = db.Column(db.String(20))
    team2 = db.Column(db.String(50))
    score2 = db.Column(db.String(20))
    result = db.Column(db.String(50))
    winner = db.Column(db.String(50))
    margin = db.Column(db.String(30))
    player_of_match = db.Column(db.String(50))

class BBLBatting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    player_name = db.Column(db.String(100))
    team = db.Column(db.String(50))
    matches = db.Column(db.Integer)
    runs = db.Column(db.Integer)
    average = db.Column(db.Float)
    strike_rate = db.Column(db.Float)
    high_score = db.Column(db.String(10))
    hundreds = db.Column(db.Integer)
    fifties = db.Column(db.Integer)
    fours = db.Column(db.Integer)
    sixes = db.Column(db.Integer)

class BBLBowling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    player_name = db.Column(db.String(100))
    team = db.Column(db.String(50))
    matches = db.Column(db.Integer)
    wickets = db.Column(db.Integer)
    best_figures = db.Column(db.String(10))
    average = db.Column(db.Float)
    economy = db.Column(db.Float)
    strike_rate = db.Column(db.Float)

# Routes
@app.route('/')
def index():
    # Get top stats for dashboard
    top_batsmen = BBLBatting.query.order_by(BBLBatting.runs.desc()).limit(5).all()
    top_bowlers = BBLBowling.query.order_by(BBLBowling.wickets.desc()).limit(5).all()
    recent_matches = BBLMatch.query.order_by(BBLMatch.match_no.desc()).limit(10).all()

    return render_template('index.html', 
                         top_batsmen=top_batsmen,
                         top_bowlers=top_bowlers,
                         recent_matches=recent_matches)

@app.route('/bbl/matches')
def bbl_matches():
    matches = BBLMatch.query.order_by(BBLMatch.match_no).all()
    return render_template('bbl_matches.html', matches=matches)

@app.route('/bbl/batting')
def bbl_batting():
    players = BBLBatting.query.order_by(BBLBatting.rank).all()
    return render_template('bbl_batting.html', players=players)

@app.route('/bbl/bowling')
def bbl_bowling():
    players = BBLBowling.query.order_by(BBLBowling.rank).all()
    return render_template('bbl_bowling.html', players=players)

@app.route('/api/stats/batting')
def api_batting_stats():
    players = BBLBatting.query.order_by(BBLBatting.runs.desc()).limit(10).all()
    data = {
        'labels': [p.player_name for p in players],
        'runs': [p.runs for p in players],
        'sixes': [p.sixes for p in players],
        'strike_rates': [p.strike_rate for p in players]
    }
    return jsonify(data)

@app.route('/api/stats/bowling')
def api_bowling_stats():
    players = BBLBowling.query.order_by(BBLBowling.wickets.desc()).limit(10).all()
    data = {
        'labels': [p.player_name for p in players],
        'wickets': [p.wickets for p in players],
        'economy': [p.economy for p in players]
    }
    return jsonify(data)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
