# Final_Project_507 - Spectacular Parks Flask App
## About the Project
Finding a suitable location for stargazing can be very difficult especially for beginners. We need to consider not only the location but also the weather. Currently 
there are no such applications which integrate both location and weather 
recommendation for stargazing. This project is about designing a website that provide 
recommendation for suitable stargazing location based on weather and location 
preferences provided by users.   
 
The project will combine a Google Map API and OpenWeather API to find the best 
location where clouds are less and suitable for stargazing. Users will submit preference for distance, cloud percentage, etc by a 
html form.   
 
The data will be presented by table using Plotly which will ranked by the attribute chosen by 
users. 

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Required Python packages
* pip
  ```sh
  pip install flask requests
  ```

### Installation

1. Get a free map API Key at [https://developers.google.com/maps/documentation/javascript/get-api-key](https://developers.google.com/maps/documentation/javascript/get-api-key)
2. Get a free weather API key at [https://openweathermap.org/](https://openweathermap.org/)
3. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install Python packages
   ```sh
   pip install
   ```
4. Enter your API in `secrets_key.py`
   ```py
   MAP_API_KEY = 'ENTER YOUR API KEY'
   WEATHER_API_KEY = 'ENTER YOUR API KEY'
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

* Run the `final_project.py` file.

* Head over to [http://127.0.0.1:5000/](http://127.0.0.1:5000/), and you should see the application.

* Fill in your preferences and hit the submit button.

* You will see the results showing in a table.


<p align="right">(<a href="#readme-top">back to top</a>)</p>
