from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = "data.json"

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        data = json.load(f)
else:
    data = {}  # serial -> {pdu, port, comment}

def load_pdus():
    with open("pdu_list.txt") as f:
        return [line.strip() for line in f if line.strip()]

pdu_options = load_pdus()

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}  # return empty dict if file doesn't exist

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/device', methods=['POST'])
def get_device_by_body():
    req_data = request.get_json()

    if not req_data or 'serial' not in req_data:
        return jsonify({"error": "Missing 'serial' in request body"}), 400

    serial = req_data['serial']
    data = load_data()
    device = data.get(serial)

    if device:
        return jsonify({serial: device})
    else:
        return jsonify({"error": "Device not found"}), 404

@app.route('/api/device/<serial>', methods=['GET'])
def get_device(serial):
    data = load_data()
    device = data.get(serial)
    if device:
        return jsonify({serial: device})
    else:
        return jsonify({"status": "error", "message": "Device not found"}), 404

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
@app.route('/add', methods=['GET', 'POST'])
def add():
    error = None
    if request.method == 'POST':
        serial = request.form.get('serial', '').strip()
        pdu = request.form.get('pdu', '').strip()
        port = request.form.get('port', '').strip()
        comment = request.form.get('comment', '').strip()

        # Validate required fields
        if not serial or not pdu or not port:
            error = "Serial, PDU, and Port are required."
        elif pdu not in pdu_options:
            error = f"PDU must be one of: {', '.join(pdu_options)}"
        elif serial in data:
            error = "Serial already exists."
        else:
            data[serial] = {'pdu': pdu, 'port': port, 'comment': comment}
            save_data()
            return redirect(url_for('index'))

    return render_template('add.html', pdu_options=pdu_options, error=error)

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