from flask import Flask, request, json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is Server Gate!'

@app.route('/get-history', methods=['GET'])
def get_history():
    url = "http://127.0.0.1:1111/get-all-history"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    history = json.loads(response.text)
    return json.dumps(history)

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    req = request.get_json()

    def search_city_id(city, province, city_type):
        url = f"http://127.0.0.1:2222/search-city?city_name={city}&province_name={province}&city_type={city_type}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        city =json.loads(response.text)
        return city

    city_origin = search_city_id(req["city_origin"], req["province_origin"], req["city_type_origin"])
    city_destination = search_city_id(req["city_destination"], req["province_destination"], req["city_type_destination"])
    
    def get_cost(origin, destination, weight, courier):
        url = "http://127.0.0.1:2222/get-cost"

        payload = json.dumps({
        "origin": origin,
        "destination": destination,
        "weight": weight,
        "courier": courier
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        cost =json.loads(response.text)
        return cost
    
    cost = get_cost(city_origin["city_id"], city_destination["city_id"], req["weight"], req["courier"])

    def save_history(origin, destination, weight, cost, courier):
        url = "http://127.0.0.1:1111/add-history"

        payload = json.dumps({
        "origin": origin,
        "destination": destination,
        "weight": weight,
        "cost": cost,
        "courier": courier
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    save_history(city_origin["city_id"], city_destination["city_id"], req["weight"], cost[0]["costs"][0]["cost"][0]["value"], req["courier"])

    return json.dumps({"city_origin": city_origin, "city_destination": city_destination, "cost": cost})


if __name__ == '__main__':
    app.run(debug=True, port=1212)