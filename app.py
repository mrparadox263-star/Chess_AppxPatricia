from flask import Flask, render_template, request, jsonify
import chess
import chess.engine
import os
import platform 
import stat 

app = Flask(__name__)

# Find the exact folder where app.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":
    ENGINE_PATH = os.path.join(BASE_DIR, "patricia.exe")
else:
    ENGINE_PATH = os.path.join(BASE_DIR, "patricia")
    # Force Linux to make the engine executable
    os.chmod(ENGINE_PATH, stat.S_IRWXU) 

# Start the engine
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


@app.route("/")
def home():
    # This serves your HTML webpage when someone visits the site
    return render_template("index.html")


@app.route("/api/move", methods=["POST"])
def get_bot_move():
    # This is the API endpoint the web browser talks to
    data = request.json
    fen = data.get("fen")
    elo = int(data.get("elo", 1200))

    board = chess.Board(fen)

    # Engine Limits based on Elo
    if elo <= 700:
        limit = chess.engine.Limit(depth=1, time=0.05)
    elif elo < 1200:
        limit = chess.engine.Limit(depth=2, time=0.1)
    elif elo < 1600:
        limit = chess.engine.Limit(depth=5, time=0.2)
    elif elo < 2000:
        limit = chess.engine.Limit(depth=10, time=0.5)
    else:
        limit = chess.engine.Limit(depth=15, time=1.0)

    # Get move from Patricia
    result = engine.play(board, limit)
    board.push(result.move)

    # Send the new board state back to the web browser
    return jsonify({
        "move": result.move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over()
    })


if __name__ == "__main__":
    # Runs the local web server on port 5000
    app.run(debug=True, port=5000)
