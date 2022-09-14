from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route('/')
def index():
    return '<h1>Encontre uma ONG</h1><p>Este site é um protótipo de API para encontrar ONGs pelo Brasil.</p>'


@app.route('/teste')
def otherpath():
    return 'This is another path'
app.run(debug=True, host='0.0.0.0')
