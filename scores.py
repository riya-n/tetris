"""
Handles the functionality related to displaying the scores on
a simple flask server.
"""
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn'

@app.route("/", methods=["GET"])
def display_scores():
  """
  Displays the top 5 scores on a server.

  Args:
    None

  Returns:
    flask.render_template: the template rendered with the top scores
  """
  scores = []
  with open("scores.txt", "r") as f:
    for line in f:
      scores.append(int(line.rstrip("\n")))
  most_recent = scores[len(scores) - 1]
  scores.sort(reverse=True)

  return render_template("scores_template.html", top_scores=scores[0:5], most_recent=most_recent)

if __name__ == "__main__":
  app.run(port=5000, debug=True)
