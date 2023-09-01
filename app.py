
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static', static_folder='static'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # Get the form ID value
    form_id = request.form.get('form_id')

    # Execute the script and capture the modified ID
    modified_id = subprocess.run(['python3', 'script.py', form_id], capture_output=True, text=True).stdout.strip()
    
    # Run the led.py script using subprocess
    modified_id2 = subprocess.run(['sudo', 'python3', 'led.py', modified_id])

    # Redirect to the result page with modified ID as a parameter
    return redirect(url_for('result', modified_id=modified_id))

@app.route('/result')
def result():
    # Get the modified ID value from the URL parameter
    modified_id = request.args.get('modified_id')
    return render_template('result.html', modified_id=modified_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
