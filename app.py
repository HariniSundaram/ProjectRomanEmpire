from flask import Flask, render_template, request, jsonify
from routes import all_routes


app = Flask(__name__)

# Home page that renders the map view
@app.route('/')
def index():
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    return render_template('map_view.html')

@app.route('/api/routes/<int:route_index>')
def route_details(route_index):
    if 0 <= route_index and route_index < len(all_routes):
        return jsonify(all_routes[route_index])
    else:
        return jsonify({"error": "Route not found"}), 404

# Route for displaying information for a specific route
@app.route('/route-info')
def route_info():
    return render_template('route_info.html')

@app.route('/api/routes')
def routes():
    return jsonify(all_routes)

if __name__ == '__main__':  
    app.run(debug=True)

