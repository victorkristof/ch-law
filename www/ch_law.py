import pickle
from flask import Flask, render_template, json, request
app = Flask(__name__)

with open('../data/droit-interne/laws.pkl', 'rb') as f:
    laws = pickle.load(f)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/data')
def data_page():
    return ""


@app.route('/search', methods=["POST"])
def search():
    query = request.form.get('search', None)
    law = laws.get(query, None)
    if law:
        law['law_id'] = query
        return json.dumps(law), 200
    else:
        return "Law %s doesn't exist" % query, 400


if __name__ == '__main__':
    app.run(debug=True)