import json
import final_project
import random
cache_file = open("final_project_cache.json", 'r')
cache_contents = cache_file.read()
cache_dict = json.loads(cache_contents)
print(len(cache_dict))
cache_file.close()
req = []
def preload_find_place_api():
    for i in range(1400,1500):
        final_project.map_find_place_params["input"] = f"{i} Mcintyre"
        final_project.make_request_with_cache(final_project.map_find_place_url,final_project.map_find_place_params,"map")
#preload_find_place_api()
def preload_text_search_api():
    for i in range(100):
        lat = random.randint(30,40)
        lng = random.randint(-100,-80)
        final_project.text_search_params["location"] = str(lat) + "," + str(lng)
        final_project.make_request_with_cache(final_project.map_endpoint_url, final_project.text_search_params, "map")
#preload_text_search_api()
def preload_distance_api():
    for i in range(100):
        lat1 = random.randint(30,40)
        lng1 = random.randint(-100,-80)
        lat2 = random.randint(30,40)
        lng2 = random.randint(-100,-80)
        final_project.distance_params["origins"] = str(lat1) + "," + str(lng1)
        final_project.distance_params["destinations"] = str(lat2) + "," + str(lng2)
        final_project.make_request_with_cache(final_project.distance_url, final_project.distance_params, "map")
#preload_distance_api()
def preload_weather_api():
    for i in range(60):
        weather_params = {}
        weather_params["lat"] = random.randint(30,40)
        weather_params["lon"] = random.randint(-100,-80)

        final_project.make_request_with_cache(final_project.weather_endpoint_url, weather_params, "weather")
#preload_weather_api()

