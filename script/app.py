from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
@app.route('/update-url', methods=['POST'])
def update_url():
    data = request.json
    if 'href' in data:
        global api_url
        api_url = data['href']
        return jsonify({'message': 'URL updated successfully'})
    else:
        return jsonify({'error': 'Invalid data'})
    
@app.route('/launch-script', methods=['POST'])
def launch_script():
    subprocess.run(['python', 'led.py'])  # Replace with the actual path to your script
    return jsonify({'message': 'Script launched'})
@app.route('/')
def hello():
    return "Hello, Flask!"
if __name__ == '__main__':
    app.run(host='134.209.18.82/python', port=5000)  # Replace with your desired host and port
#file_path = "/home/itroot/Téléchargements/Nouveau dossier/minecraft.xml"