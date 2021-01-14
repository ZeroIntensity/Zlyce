from flask import Flask, render_template
from threading import Thread

app = Flask(__name__, template_folder='pages')
@app.route('/')
def main():
  return render_template('home.html')

@app.route('/invite')
def invite():
  return render_template('invite.html')

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

