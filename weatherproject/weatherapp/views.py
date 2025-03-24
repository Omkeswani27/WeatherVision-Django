from django.shortcuts import render
from django.contrib import messages
import datetime
import requests  # Import the requests module

def home(request):
    city = request.POST.get('city', 'Indore')

    # OpenWeatherMap API Key (Replace with your actual key)
    WEATHER_API_KEY = ""
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

    # Google Custom Search API Key (Replace with your actual key)
    GOOGLE_API_KEY = ""
    SEARCH_ENGINE_ID = ""
    
    query = f"{city} 1920x1080"
    start = 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Default values in case of an error
    description = "clear sky"
    icon = "01d"
    temp = 25
    image_url = "https://via.placeholder.com/1920x1080"  # Default fallback image
    exception_occurred = False
    day = datetime.date.today()

    try:
        # Fetch weather data
        weather_data = requests.get(url).json()
        
        if "weather" in weather_data and "main" in weather_data:
            description = weather_data["weather"][0]["description"]
            icon = weather_data["weather"][0]["icon"]
            temp = weather_data["main"]["temp"]
        else:
            raise KeyError  # If API does not return expected data, trigger exception
        
        # Fetch city image
        image_response = requests.get(city_url).json()
        search_items = image_response.get("items", [])

        if search_items and len(search_items) > 1:
            image_url = search_items[1].get("link", image_url)  # Use a valid image URL or default
    
    except KeyError:
        exception_occurred = True
        messages.error(request, "Weather data is not available for the entered city.")
    
    except requests.exceptions.RequestException as e:
        exception_occurred = True
        messages.error(request, f"An error occurred while fetching data: {str(e)}")

    return render(request, 'weatherapp/index.html', {
        "description": description,
        "icon": icon,
        "temp": temp,
        "day": day,
        "city": city,
        "exception_occurred": exception_occurred,
        "image_url": image_url
    })
