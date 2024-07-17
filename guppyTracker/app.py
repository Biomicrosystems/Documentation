import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from generate_data import save_json, generate_graphs, save_csv, save_excel, generate_dataframe  # Import the functions
from processVideoYolo import start_video_processing, stop_video_processing  # Import the functions
import tempfile
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify(success=False), 400

    video_file = request.files['video']
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_file.save(temp_file.name)

    return jsonify(success=True, video_path=temp_file.name)

@app.route('/upload_json', methods=['POST'])
def upload_json():
    if 'json' not in request.files:
        return jsonify(success=False), 400

    json_file = request.files['json']
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    json_file.save(temp_file.name)

    graphs = generate_graphs(temp_file.name)
    return jsonify(success=True, graphs=graphs, json_path=temp_file.name)

@app.route('/save_file', methods=['POST'])
def save_file():
    if 'json' not in request.files or 'format' not in request.form:
        return jsonify(success=False), 400

    json_file = request.files['json']
    format = request.form['format']
    original_json_name = json_file.filename
    base_name = os.path.basename(original_json_name).replace('.json', '')

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    json_file.save(temp_file.name)

    df = generate_dataframe(temp_file.name)

    if format == 'csv':
        path = save_csv(df, base_name)
    elif format == 'excel':
        path = save_excel(df, base_name)
    else:
        return jsonify(success=False), 400

    return jsonify(success=True, path=path)

@socketio.on('start_video')
def start_video(data):
    video_path = data['video_path']
    start_video_processing(video_path, socketio, emit)

@socketio.on('stop_video')
def stop_video():
    frames_data = stop_video_processing()
    json_path = save_json(frames_data)
    graphs = generate_graphs(json_path)

    df = generate_dataframe(json_path)
    base_name = os.path.basename(json_path).replace('.json', '')

    csv_path = save_csv(df, base_name)
    excel_path = save_excel(df, base_name)

    emit('saved', {
        'message': f'Data saved to {json_path}, {csv_path}, and {excel_path}',
        'graphs': graphs
    })

@app.route('/graphs/<filename>')
def send_graph(filename):
    return send_from_directory('Generated_data', filename)

if __name__ == '__main__':
    socketio.run(app, debug=True)
