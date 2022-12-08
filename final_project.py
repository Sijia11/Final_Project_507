#FlaskInputApp.py
from flask import Flask, render_template, request
app = Flask(__name__)
import json
import requests
#from requests_oauthlib import OAuth1

import secrets_key
from collections import defaultdict
map_find_place_params = {"fields" : "formatted_address,name,rating,opening_hours,geometry,type", "inputtype" : "textquery" }
text_search_params = {'query': 'dark sky park', "type": "park", "radius": "10000"}
weather_params = {}
global INFO, LOCATION
@app.route('/')
def index():
    
    return render_template('FlaskInputs2.html'),"aa" # just the static HTML
    

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    user_name = request.form["location"]
    fave_color = request.form["colors"]
    map = request.form["map"]
    result_list = []
    result_list.append(map)
    answer = ask_map(mapTree, result_list,0)
    return render_template('response.html', 
        name=user_name, 
        color=fave_color, map=map, answer=answer, info="1", ideal="1")


@app.route('/search_map_form', methods=['POST'])
def handle_the_search():
    global INFO, LOCATION
    if "start" in request.form:
        start_location = request.form["start"]
        map_find_place_params["input"] = start_location
        print(start_location)
        res = make_request_with_cache(map_find_place_url, map_find_place_params, "map")
        print(type(res))
        lat = res["candidates"][0]["geometry"]["location"]["lat"]
        lng = res["candidates"][0]["geometry"]["location"]["lng"]
        text_search_params["location"] = str(lat) + "," + str(lng)
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




    if "park" in request.form:
        park = request.form["park"]
        map_find_place_params["input"] = park
        result = make_request_with_cache(map_find_place_url, map_find_place_params, "map")["candidates"]
        info = []
        location = []
        for i, val in enumerate(result):
            address = val["formatted_address"]
            name = val["name"]
            info += [f"address:{address}, park name:{name}"]
            location.append([val["geometry"]["location"]["lat"],val["geometry"]["location"]["lng"], i])
        INFO = info
        LOCATION = location


    return render_template('response1.html', 
        
        result=info)

@app.route("/handle_weather", methods=["POST"])
def handle_weather():
    cloud = request.form["cloud"]
    result_list = []
    result_list.append(cloud)
    answer = ask_map(weatherTree, result_list,0)
    weather_params = {}
    ideal = defaultdict(list)
    for lat, lng, i in LOCATION:
        weather_params["lat"] = lat
        weather_params["lon"] = lng
        a = make_request_with_cache(weather_endpoint_url, weather_params, "weather")
        print(a)
        result = make_request_with_cache(weather_endpoint_url, weather_params, "weather")["list"]

        
        for val in result:
            if val["dt_txt"][11:13] == "21" and val["clouds"]["all"] < 20:
                ideal[INFO[i]].append([val["dt_txt"], val["clouds"]["all"] ])
                break
    
                




    return render_template('response.html', answer=answer, info=INFO, ideal=ideal)



CACHE_FILENAME = "final_project_cache.json"
CACHE_DICT = {}

map_key = secrets_key.MAP_API_KEY
weather_key = secrets_key.WEATHER_API_KEY

# access_token = secrets.TWITTER_ACCESS_TOKEN
# access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

# oauth = OAuth1(client_key,
#             client_secret=client_secret,
#             resource_owner_key=access_token,
#             resource_owner_secret=access_token_secret)

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




#results = make_request_with_cache(map_endpoint_url, params)
# tweets = results['statuses']
# for t in tweets:
#     print(t['text'])

mapTree = \
    ("Do you want to enter your begining location? or directly search a park?",
        ("Please type your beginning location", None, None),
        ("Please type your search place", None, None))

weatherTree = \
    ("Please select your maximum acceptable cloud percentage",
        ("Your cloud percentage is at most 20%", None, None),
        ("Your cloud percentage is at most 10%", None, None))

def ask_map(tree, answer, i):

    if not tree[1]:
        if type(tree[0]) != str:
            return tree[0]
        return "I will search for you."
    else:
        if answer[i] == "1":
            return ask_map(tree[1], answer, i + 1)
        else:
            return ask_map(tree[2], answer, i + 1)



    #     if not tree[1]:
    #     prompt = f"Is it {tree[0]}? "
    #     if not check_answer(prompt):
    #         object_name = input('Drats! What was it? ')
    #         question = input(f"What's a question that distinguishes between {object_name} and {tree[0]}? ")
    #         answer = check_answer(f"And what's the answer for {object_name}? ")
    #         if answer:
    #             cur_tree = tree
    #             tree = (question, (object_name, None, None), cur_tree)
    #         else:
    #             cur_tree = tree
    #             tree = (question, cur_tree, (object_name, None, None))

    #     else:
    #         print("I got it!")
    #     return tree
    # else:
    #     prompt = f"{tree[0]} "
    #     if check_answer(prompt):
    #         tree = (tree[0], play(tree[1]), tree[2])
    #         return tree

    #     else:
    #         tree = (tree[0], tree[1], play(tree[2]))
    #         return tree


if __name__ == "__main__":
    app.run(debug=True) 