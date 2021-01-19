from flask import Flask, render_template
from threading import Thread

app = Flask(__name__, template_folder='pages')
@app.route('/')
def main():
  return render_template('home.html')

@app.route('/invite')
def invite():
  return render_template('invite.html')

# Changelog starts here
@app.route('/changelog/development/1.19.21')
def development11921():
  return render_template('changelogs/11921.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 404

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()

