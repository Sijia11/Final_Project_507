from flask import Flask, render_template, request
app = Flask(__name__)
import json
import requests


import secrets_key
from collections import defaultdict
import create_json
import plotly.graph_objects as go
import read_json_tree

map_find_place_params = {"fields" : "formatted_address,name,rating,opening_hours,geometry,type", "inputtype" : "textquery" }
text_search_params = {'query': 'dark sky park', "type": "park", "radius": "10000"}
weather_params = {}
distance_params = {}
global INFO, LOCATION
@app.route('/')
def index():
    
    return render_template('Home.html') # just the static HTML
    

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    global INFO, LOCATION
    search = request.form["search_type"]
    location = request.form["location"]
    distance = request.form["distance"]
    cloud = request.form["cloud"]
    option = request.form["option"]
    result_list = []
    if distance != "3":
        result_list.extend([search, location, distance,cloud])
    if distance == "3":
        result_list.extend([search, location,cloud])
    # print(result_list)
    answer, final_request = create_json.ask_map(create_json.mapTree, result_list,0)
    create_json.save_json("json_tree.json",answer)
    res,new_tree = read_json_tree.read_json("json_tree.json")
    # print(new_tree)

    if search == "1":
 
        map_find_place_params["input"] = location
       # print(start_location)
        res = make_request_with_cache(map_find_place_url, map_find_place_params, "map")
     
        lat = res["candidates"][0]["geometry"]["location"]["lat"]
        lng = res["candidates"][0]["geometry"]["location"]["lng"]
        text_search_params["location"] = str(lat) + "," + str(lng)
        distance_params["origins"] = str(lat) + "," + str(lng)
   
        result = make_request_with_cache(map_endpoint_url, text_search_params, "map")["results"]
        info = []
        location = []

        for i, val in enumerate(result):
            address = val["formatted_address"]
            name = val["name"]
            info.append(f"address:{address}, park name:{name}")
            location.append([val["geometry"]["location"]["lat"],val["geometry"]["location"]["lng"], i])

        INFO = info
        LOCATION = location

        
        dropped_location = []
        for lat, lng, i in LOCATION:
            distance_params["destinations"] = str(lat) + "," + str(lng)
            result = make_request_with_cache(distance_url, distance_params, "map")["rows"][0]["elements"][0]["distance"]["value"]
          
            INFO[i] += f", distance: {result//1609}"
            if result > 563.27*1000:
                dropped_location.append(i)

   
        if distance == "1":
            for i in range(len(dropped_location)-1,-1,-1):
                LOCATION.pop(dropped_location[i])
                INFO.pop(dropped_location[i])

    if search == "2":

        map_find_place_params["input"] = location
        result = make_request_with_cache(map_find_place_url, map_find_place_params, "map")["candidates"]
        info = []
        location = []
        for i, val in enumerate(result):
            address = val["formatted_address"]
            name = val["name"]
            info += [f"address:{address}, park name:{name}, distance: n/a"]
            location.append([val["geometry"]["location"]["lat"],val["geometry"]["location"]["lng"], i])
        INFO = info
        LOCATION = location

    if cloud == "1":
        cloudiness = 20
    elif cloud == "2":
        cloudiness = 10

    weather_params = {}
    ideal = defaultdict(list)
    print(len(INFO),len(LOCATION),"llllllll")
    for i,v in enumerate(LOCATION):
        print(i)
        weather_params["lat"] = v[0]
        weather_params["lon"] = v[1]

        result = make_request_with_cache(weather_endpoint_url, weather_params, "weather")["list"]

        
        for val in result:
            if val["dt_txt"][11:13] in ["21","00","03"] and val["clouds"]["all"] < cloudiness:
                ideal[INFO[i]].append([val["dt_txt"], val["clouds"]["all"] ])
                break

    unsorted_list = []

    for k,v in ideal.items():
        sublist = []
        idx = k.find("park name")
        idx2 = k.find("distance")
        sublist.append(k[8:idx-2]) # address
        sublist.append(k[idx+10:idx2-2]) # name
        sublist.append(k[idx2+10:]) # distance
        sublist.append(v[0][0][:10]) # date
        sublist.append(v[0][0][11:]) # time
        sublist.append(v[0][1]) # cloud
        unsorted_list.append(sublist)
    
    sorted_list = sorted(unsorted_list, key=lambda x:int(x[int(option)+1]) if str(x[int(option)+1]).isnumeric() else x[int(option)+1])

    total_list = [[] for i in range(6)]
    for info in sorted_list:
        for i in range(len(info)):
            total_list[i].append(info[i])

    header = ["Address","Park name","Distance (mile)","Date", "Time", "Cloudiness (%)"]
    fig = go.Figure(data=[go.Table(header=dict(values=header),
                 cells=dict(values=total_list))
                     ])
    div = fig.to_html(full_html=False)
    
    return render_template('response.html', answer=final_request, info=INFO, ideal=ideal,plot_div=div)


CACHE_FILENAME = "final_project_cache.json"
CACHE_DICT = {}

map_key = secrets_key.MAP_API_KEY
weather_key = secrets_key.WEATHER_API_KEY



def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    if "key" in params:
        del params["key"]
    if "appid" in params:
        del params["appid"]
    print(params)

    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def make_request(baseurl, params, api_type):
    '''Make a request to the Web API using the baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    if api_type == "map":
        params["key"] = map_key
    elif api_type == "weather":
        params["appid"] = weather_key
    response = requests.get(baseurl, params=params)
    return response.json()
    #!!!!!

def make_request_with_cache(baseurl, params, api_type):
    '''Check the cache for a saved result for this baseurl+params
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = make_request(baseurl, params, api_type)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

CACHE_DICT = open_cache()

map_endpoint_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
weather_endpoint_url = 'https://api.openweathermap.org/data/2.5/forecast'
map_find_place_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
distance_url = "https://maps.googleapis.com/maps/api/distancematrix/json"





if __name__ == "__main__":
    app.run(debug=True) 