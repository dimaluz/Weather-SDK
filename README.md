<h1>Weather SDK (Python)</h1>

<h2>Introduction</h2>

<p>
    The Weather SDK can be used by other developers to easily access a weather API and retrieve weather data for a given location. Weather SDK can be used only with weather API (<a href="https://openweathermap.org/api"> https://openweathermap.org/api </a>).
    The SDK was written in Python. It provides an interface for querying the weather API and returning the weather data in a standard JSON format. 
</p>
<h4>Example of JSON structure:</h4>

 ```json
{
   "weather": {
       "main": "Clouds",
       "description": "scattered clouds",
   },
   "temperature": {
     "temp": 269.6,
     "feels_like": 267.57,
   },
   "visibility": 10000,
   "wind": {
     "speed": 1.38,
   },
   "datetime": 1675744800,
   "sys": {
     "sunrise": 1675751262,
     "sunset": 1675787560
   },
   "timezone": 3600,
   "name": "Zocca",
 }
 ```
 <p>
    The user provides API key for OpenWeatherAPI on the object initialization: <code>weather = Weather("937kdh937dho39kdbwwhy45")</code>
 </p>
 <p>
    The user should provide an name of city to 'getWeather' method <code>weather.getWeather("Zocca")</code> to get an information about the weather at the current moment. Weather SDK returns information about the first city which was found by searching for the city name. (Weather SDK stores weather information about the requested cities into a buffer and if it is relevant, return the stored value (Weather is considered to be up to date if less than 10 minutes have passed))
 </p>
 <p>
    In order to save memory, Weather SDK stores information in a buffer for no more than 10 cities at a time.
 </p>
 <p>
     Weather SDK has two types of behavior: on-demand and polling mode. In on-demand mode the SDK updates the weather information only on customer requests. In polling mode SDK requests new weather information for all stored locations to have zero-latency response for customer requests. Mode of the SDK should be passed as parameter on initialization. 'on-demand' mode is set up by default.
 </p>
 <p>
    Also Weather SDK provides a scope of methods to allow a user to work with different keys:
 </p>
<div>

``weather()`` - returns data about weather for the city in JSON format which was found by searching for the city name.
```json 
{
    "weather": {
        "main": "Clouds",
        "description": "scattered clouds"
    }
}
```
</div>

<div>

``temperature()`` - returns data about temperature for the current city in JSON format
```json 
{
    "temperature": {
        "temp": 269.6,
        "feels_like": 267.57
    }
}
```
</div>
<div>

``visibility()`` - returns data about visibility for the current city in JSON format 
```json
{ 
    "visibility": 10000 
}
```
</div>
<div>

``wind()`` - returns data about wind for the current city in JSON format 
```json
{
    "wind": {
        "speed": 1.38
    } 
}
```
</div>
<div>

``timezone()`` - returns data about wind for the current city in JSON format
```json
{
    "timezone": 3600
}
```
</div>
<div>

``sys()`` - returns data about sunrise and sunset for the current city in JSON format
```json
{
    "sys": {
        "sunrise": 1675751262,
        "sunset": 1675787560
    }
}
```
</div>
<div>

``name()`` - returns a cityname of the current city in JSON format
```json
{
    "name": "Zocca",
}
```
</div>
<div>

``datetime()`` - returns date and time of the customer request in JSON format
```json
{
    "datetime": 1675744800,
}
```
</div>
<div>

``delete(cityname)`` - removes data of a city from buffer
</div>
<div>

``clean()`` - removes all data from buffer.
</div>
    
</p>

<div>
<h2>Contents</h2>

[Installation](#Installation)

[Usage Example](#UsageExample)

</div>

<h2>
<a name="Installation"></a>Installation
</h2>

`` pip install wsdk ``
<h2>
<a name="UsageExample"></a>Usage example
</h2>

```python
import wsdk

API_KEY = '851605a536adfc540ed0fd50a42847skd'

obj = wsdk.Weather(API_KEY, 'polling')
zocca = obj.getWeather('Zocca')
print(zocca)
```
<p> 
As a result you will get JSON:
</p>

```json
{
    "weather": {
       "main": "Clouds",
       "description": "scattered clouds",
    },
   "temperature": {
        "temp": 269.6,
        "feels_like": 267.57,
    },
    "visibility": 10000,
    "wind": {
        "speed": 1.38,
    },
    "datetime": 1675744800,
    "sys": {
        "sunrise": 1675751262,
        "sunset": 1675787560
    },
    "timezone": 3600,
    "name": "Zocca"
 }
```
<p>
    You can use the methods, which were discribed above, to get data from JSON:
</p>

```python
import wsdk

API_KEY = '851605a536adfc540ed0fd50a42847skd'

obj = wsdk.Weather(API_KEY, 'polling')
zocca = obj.getWeather('Zocca')
temperature = obj.temperature()
print(temperature)
```
<p>The result will be: </p>

```json
{
    "temperature": {
        "temp": 269.6,
        "feels_like": 267.57,
    }
}
```