from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from boggle import Boggle

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)



boggle_game = Boggle()
app.config["SECRET_KEY"] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
csrf = CSRFProtect(app)

@app.route("/")
def homepage():
    """Home page that shows gameboard"""

    board = boggle_game.make_board()
    session["board"] = board
    return render_template("index.html", board=board)

@app.route("/check-word", methods=["GET"])
def check_word():
    """Check if word is in dictionary and on current board state"""
    print (request)
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score",methods=["POST","GET"])
def post_score():
    """Receive score, update nplays, update high score if appropriate"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)