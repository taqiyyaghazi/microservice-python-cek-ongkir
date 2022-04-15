from flask import Flask, request, json
import http.client
app = Flask(__name__)


@app.route('/')
def index():
    return 'This is Server 2!'

@app.route('/search-city', methods=['GET'])
def search_city_id():
    city_name = request.args.get('city_name')
    province_name = request.args.get('province_name')
    city_type = request.args.get('city_type')

    if city_name and province_name and city_type:
        conn = http.client.HTTPSConnection("api.rajaongkir.com")
        payload = ''
        headers = {}
        conn.request("GET", "/starter/city?key=8b06b6a059bd1e215464fb7c0d57f74c", payload, headers)
        res = conn.getresponse()
        data = res.read()
        city_data = json.loads(data.decode("utf-8"))['rajaongkir']['results']
        for city in city_data:
            if city_name.lower() in city['city_name'].lower() and province_name.lower() in city['province'].lower() and city_type.lower() in city['type'].lower():
                return json.dumps(city)
        return json.dumps({'city_id': 'Not Found'})
    elif not city_name:
        return 'City Name is required!'
    elif not province_name:
        return 'Province Name is required!'
    elif not city_type:
        return 'City Type is required!'

@app.route('/get-cost', methods=['POST'])
def get_cost():
    req = request.get_json()
    if 'origin' in req.keys() and 'destination' in req.keys() and 'weight' in req.keys() and 'courier' in req.keys():
        conn = http.client.HTTPSConnection("api.rajaongkir.com")
        payload = json.dumps({
        "key": "8b06b6a059bd1e215464fb7c0d57f74c",
        "origin": req["origin"],
        "destination": req["destination"],
        "weight": req["weight"],
        "courier": req["courier"]
        })
        headers = {
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/starter/cost", payload, headers)
        res = conn.getresponse()
        data = res.read()

        cost = json.loads(data.decode("utf-8"))['rajaongkir']['results']
        
        return json.dumps(cost)
    elif 'origin' not in req.keys():
        return 'Origin is required!'
    elif 'destination' not in req.keys():
        return 'Destination is required!'
    elif 'weight' not in req.keys():
        return 'Weight is required!'
    
if __name__ == '__main__':
    app.run(debug=True, port=2222)