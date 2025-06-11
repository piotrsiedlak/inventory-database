from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "data.json"

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        data = json.load(f)
else:
    data = {}  # serial -> {pdu, port, comment}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    q = request.args.get('q', '').lower()
    if q:
        filtered = {
            serial: item for serial, item in data.items()
            if q in serial.lower()
            or q in item.get('pdu', '').lower()
            or q in item.get('port', '').lower()
            or q in item.get('comment', '').lower()
        }
    else:
        filtered = data
    return render_template('index.html', items=filtered)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        serial = request.form['serial']
        data[serial] = {
            'pdu': request.form['pdu'],
            'port': request.form['port'],
            'comment': request.form['comment']
        }
        save_data()
        return redirect(url_for('index'))
    return render_template('edit.html', item={})

@app.route('/edit/<serial>', methods=['GET', 'POST'])
def edit(serial):
    if request.method == 'POST':
        data[serial] = {
            'pdu': request.form['pdu'],
            'port': request.form['port'],
            'comment': request.form['comment']
        }
        save_data()
        return redirect(url_for('index'))
    return render_template('edit.html', serial=serial, item=data[serial])

@app.route('/delete/<serial>', methods=['POST'])
def delete(serial):
    if serial in data:
        del data[serial]
        save_data()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)