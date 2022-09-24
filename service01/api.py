from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route('/')
def index():
    return '<p>Este site é um protótipo de API</p>'


@app.route('/teste')
def otherpath():
    return 'This is another path'
app.run(debug=True, host='0.0.0.0')
