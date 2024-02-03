from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home page that renders the map view
@app.route('/')
def map_view():
    # Fetch your routes data from your data source here
    # routes_data = #INSERT ROUTE DATA HERE
    return render_template('map_view.html')

if __name__ == '__main__':
    app.run(debug=True)
