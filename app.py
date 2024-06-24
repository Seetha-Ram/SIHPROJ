from flask import Flask, request, render_template
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

# Load the CSV data
csv_path = 'data/minerals.csv'  # Adjust this path to the actual CSV location
data = pd.read_csv(csv_path)

# Function to query by latitude and longitude
def query_by_lat_lon(latitude, longitude):
    result = data[(data['latitude'] == latitude) & (data['longitude'] == longitude)]
    if not result.empty:
        return result[['ore', 'gangue', 'work_type', 'names', 'ore_ctrl', 'hrock_type', 'arock_type']]
    else:
        nearest = data.iloc[((data['latitude'] - latitude)**2 + (data['longitude'] - longitude)**2).idxmin()]
        return nearest[['ore', 'gangue', 'work_type', 'names', 'ore_ctrl', 'hrock_type', 'arock_type']].to_frame().T

# Function to query by city name
def query_by_city(city_name):
    result = data[data['site_name'].str.contains(city_name, case=False, na=False)]
    if not result.empty:
        return result[['commod1','commod2','commod3','ore', 'gangue', 'work_type', 'names', 'ore_ctrl', 'hrock_type', 'arock_type']]
    else:
        return "No matching records found."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_type = request.form['query_type']
        if query_type == 'latlon':
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            result = query_by_lat_lon(latitude, longitude)
        elif query_type == 'city':
            city_name = request.form['city_name']
            result = query_by_city(city_name)
        else:
            result = "Invalid query type."
        return render_template('index.html', result=result.to_html(index=False))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
