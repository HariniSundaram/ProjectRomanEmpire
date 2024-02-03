from flask import Flask, render_template, request, jsonify, url_for
from routes import all_routes


app = Flask(__name__)

# Home page that renders the map view
@app.route('/')
def index():
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    csv_url = url_for('static', filename='truckDeliveries_rows.csv')
    return render_template('map_view.html', csv_url=csv_url)
@app.route('/api/routes/<int:route_index>')
def route_details(route_index):
    if 0 <= route_index and route_index < len(all_routes):
        return jsonify(all_routes[route_index])
    else:
        return jsonify({"error": "Route not found"}), 404

# # Route for displaying information for a specific route
@app.route('/route-info')
def route_info():
    return render_template('route_info.html')

@app.route('/api/routes')
def routes():
    return jsonify(all_routes)

@app.route('/scheduler')
def scheduler(): 
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    return render_template('scheduler.html')

@app.route('/send_schedule')
def make_schedule(): 
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    return render_template('scheduler.html')

@app.route('/route_0')
def route_0(): 
    # Fetch your routes data from your data source here
    csv_url = url_for('static', filename='dataset1.csv')
    return render_template('route_0.html', csv_url=csv_url)

@app.route('/route_1')
def route_1(): 
    # Fetch your routes data from your data source here
    csv_url = url_for('static', filename='dataset2.csv')
    return render_template('route_1.html', csv_url=csv_url)

@app.route('/route_2')
def route_2(): 
    # Fetch your routes data from your data source here
    csv_url = url_for('static', filename='dataset3.csv')
    return render_template('route_2.html', csv_url=csv_url)

@app.route('/route_3')
def route_3(): 
    # Fetch your routes data from your data source here
    csv_url = url_for('static', filename='dataset4.csv')
    return render_template('route_3.html', csv_url=csv_url)



if __name__ == '__main__':  
    app.run(debug=True)

