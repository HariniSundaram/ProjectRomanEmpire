from flask import Flask, render_template, request, jsonify
from routes import all_routes


app = Flask(__name__)

# Home page that renders the map view
@app.route('/')
def map_view():
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    return render_template('map_view.html')


@app.route('/api/routes')
def routes():
    return jsonify(all_routes)

if __name__ == '__main__':
    app.run(debug=True)

