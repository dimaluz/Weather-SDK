import requests
import time
import json

# Exceptions
class InvalidAPIKey(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class CityNotFound(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class BadRequest(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class Unauthorized(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class NotFound(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class TooManyRequests(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;

class UnexpectedError(Exception):
    def __init__(self, error):
        self.error = error;

    def __repr__(self):
        return self.error;



# This class saves a json object of response from server
class Response:
    def __init__(self, jsonObj):
        self.obj = jsonObj;

    def getWeather(self):
        obj = json.loads(self.obj);
        return obj['weather'];
    def getMain(self):
        obj = json.loads(self.obj);
        return obj['weather']['main'];
    def getDescription(self):
        obj = json.loads(self.obj);
        return obj['weather']['description'];
    
    def getTemperature(self):
        obj = json.loads(self.obj);
        return obj['temperature'];
    def getTemp(self):
        obj = json.loads(self.obj);
        return obj['temperature']['temp'];
    def getFeelsLike(self):
        obj = json.loads(self.obj);
        return obj['temperature']['feels_like'];

    def getVisibility(self):
        obj = json.loads(self.obj);
        return obj['visibility'];

    def getWind(self):
        obj = json.loads(self.obj);
        return obj['wind'];
    def getWindSpeed(self):
        obj = json.loads(self.obj);
        return obj['wind']['speed'];

    def getDatetime(self):
        obj = json.loads(self.obj);
        return obj['datetime'];

    def getSys(self):
        obj = json.loads(self.obj);
        return obj['sys'];
    def getSunrise(self):
        obj = json.loads(self.obj);
        return obj['sys']['sunrise'];
    def getSunset(self):
        obj = json.loads(self.obj);
        return obj['sys']['sunset'];

    def getTimezone(self):
        obj = json.loads(self.obj);
        return obj['timezone'];

    def getName(self):
        obj = json.loads(self.obj);
        return obj['name'];

    def __repr__(self):
        return self.obj;




class Weather:
    def __init__(self, api_key='', method='on-demand'):
        self.api_key = api_key;
        self.baseURL = 'https://api.openweathermap.org/data/2.5/weather?';
        self.weatherRequests = {};
        self.method = method;
        self.qtyOfCities = 10;
        self.cityname = '';

    # This method makes a request to API for a city name
    def getWeather(self, cityname):
        self.cityname = cityname;
        if len(self.weatherRequests) >= self.qtyOfCities:
            keys = list(self.weatherRequests.keys());
            key = keys.pop();
            del self.weatherRequests[key];
        if self.method == 'on-demand':
            response = self.on_demand();
        else:
            response = self.polling();
        return response;

    # This method is used by default to fetch data from API
    # This method updates data of the city by demand
    def on_demand(self):
        currentTime = time.time();
        if self.cityname in self.weatherRequests.keys():
            if currentTime - self.weatherRequests[self.cityname]['timeRequest'] <= 600:
                return self.weatherRequests[self.cityname]['response'];
        else:
            try:
                self.makeRequest(self.cityname);
                return self.weatherRequests[self.cityname]['response'];
            except InvalidAPIKey as e:
                return e;
            except CityNotFound as e:
                return e;
            except BadRequest as e:
                return e;
            except Unauthorized as e:
                return e;
            except NotFound as e:
                return e;
            except TooManyRequests as e:
                return e;
            except UnexpectedError as e:
                return e;
    
    # This method updates all list of cities in buffer
    def polling(self):
        currentTime = time.time();
        needMakeRequest = False;
        keys = list(self.weatherRequests.keys()); 
        if keys:
            for city in keys:
                if currentTime - self.weatherRequests[city]['timeRequest'] >= 600:
                    needMakeRequest = True;
                    break;
        
        if needMakeRequest:
            try:
                for city in keys:
                    self.makeRequest(city);
            except InvalidAPIKey as e:
                return e;
            except CityNotFound as e:
                return e;
            except BadRequest as e:
                return e;
            except Unauthorized as e:
                return e;
            except NotFound as e:
                return e;
            except TooManyRequests as e:
                return e;
            except UnexpectedError as e:
                return e;
        
        if self.cityname in self.weatherRequests.keys():
            return self.weatherRequests[self.cityname]['response'];
        else:
            try:
                self.makeRequest(self.cityname);
                return self.weatherRequests[self.cityname]['response'];
            except InvalidAPIKey as e:
                return e;
            except CityNotFound as e:
                return e;
            except BadRequest as e:
                return e;
            except Unauthorized as e:
                return e;
            except NotFound as e:
                return e;
            except TooManyRequests as e:
                return e;
            except UnexpectedError as e:
                return e;
    
    # This method is used by app to fetch data from API
    def makeRequest(self, cityname):
            currentTime = time.time();
            url = self.baseURL + 'q=' + str(cityname) + '&appid=' + self.api_key;
            response = requests.get(url).json();
            if response['cod'] == 401 and "Invalid API key" in response['message']:
                raise InvalidAPIKey(response);
            if response['cod'] == 404 and 'city not found' in response['message']:
                raise CityNotFound(response);
            if response['cod'] == 400:
                raise BadRequest(response);
            if response['cod'] == 401:
                raise Unauthorized(response);
            if response['cod'] == 404:
                raise NotFound(response);
            if response['cod'] == 429:
                raise TooManyRequests(response);
            if response['cod'] == 500:
                raise UnexpectedError(response);
            response = Weather.parse(response);
            response = Response(response);
            self.weatherRequests[cityname] = {'response':response, 'timeRequest':currentTime};

    # This method delete all cities from the buffer
    def clean(self):
        self.weatherRequests.clear();
    
    # This method delete a specific city from the buffer
    def delete(self, cityname):
        if cityname in self.weatherRequests.keys():
            del self.weatherRequests[cityname];
            self.cityname = '';
        else:
            print('There is no this city in buffer');
        
    # This class method is used by object to parse JSON 
    def parse(response):
        jsonObj = {
            'weather':{
                'main':response['weather'][0]['main'],
                'description':response['weather'][0]['description'],
            },
            'temperature':{
                'temp':response['main']['temp'],
                'feels_like':response['main']['feels_like'],
            },
            'visibility':response['visibility'],
            'wind':{
                'speed':response['wind']['speed'],
            },
            'datetime':response['dt'],
            'sys':{
                'sunrise':response['sys']['sunrise'],
                'sunset':response['sys']['sunset'],
            },
            'timezone':response['timezone'],
            'name':response['name'],
        }
        jsonObj = json.dumps(jsonObj);
        return jsonObj;

    # This method returns weather of the current city
    def weather(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'weather': obj.getWeather(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No weather found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;

    # This method returns a temperature of the current city
    def temperature(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'temperature': obj.getTemperature(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No temperature found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;

    # This method returns the data about visibility in the current city
    def visibility(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'visibility': obj.getVisibility(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No visibility found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
    
    # This method returns data about wind speed in the current city
    def wind(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'wind': obj.getWind(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No wind found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;

    # This method returns a timazone of the current city
    def timezone(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'timezone': obj.getTimezone(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No timezone found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
    
    # This method returns data about sunset and sunrise in the current city
    def sys(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'sys': obj.getSys(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No sys found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;

    # This method returns a name of the current city
    def name(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'name': obj.getName(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No city found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;

    # This method returns date and time of request
    def datetime(self):
        if self.cityname in self.weatherRequests.keys():
            obj = self.weatherRequests[self.cityname]['response'];
            jsonObj = {
                'datetime': obj.getDatetime(),
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
        else:
            jsonObj = {
                'error': "No datetime found",
            }
            jsonObj = json.dumps(jsonObj);
            return jsonObj;
    



