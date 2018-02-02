from flask import jsonify, Flask, request, render_template

import PrinterInfo
import os
import config

app = Flask(__name__, static_folder='frontend')


def return_error(e):
  return {"error": e}


def allowed_file(filename: str):
  return '.' in filename and filename.split(".")[1] == 'pdf'


def secure_filename(filename: str):
  tokens = filename.split('.')
  return tokens[0].replace('.', '_').replace('/', '_') + '.' + tokens[1]


@app.route('/api/printer')
def printer_view():
  if request.method == 'GET':
    try:
      return jsonify({"options": PrinterInfo.get_printer_info()})
    except FileNotFoundError as e:
      return jsonify(return_error(e))


@app.route('/api/print', methods=['GET', 'POST'])
def print_it():
  if request.method == 'POST':
    if 'file' not in request.files:
      return return_error("file not found")
    file = request.files['file']
    if file.filename == '':
      return return_error("no selected file")
    if file and allowed_file(file.filename):
      file.save(os.path.join(config.UPLOAD_FOLDER, secure_filename(file.filename)))
      return jsonify({"status": "cool"})


@app.route('/')
def index_page():
  return app.send_static_file('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
