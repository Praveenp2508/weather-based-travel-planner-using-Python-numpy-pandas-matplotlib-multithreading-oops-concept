import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as mtp
import threading

api_key='3f63b27c80e0bcb36be409b77851c54e'
base_url='http://api.openweathermap.org/data/2.5/weather'

class weatherfetcher:

    def __init__(self,cities):
        self.cities=cities
        self.weather_data=[]

    def fetchweather(self,city):

        try:
            params={'q':city,'appid': api_key,'units':'metric'}
            response=requests.get(base_url,params=params)
            data=response.json()

            if response.status_code==200:
                weather={
                    'city':city,
                    'temperature':data['main']['temp'],
                    'condition':data['weather'][0]['main']
                }
                self.weather_data.append(weather)

            else:
                print(f"failed to get data for {city}:{data.get('message','unknown error')}")

        except Exception as e:
                print(f'error fetching data for {city}:{e}')

class travelplanner(weatherfetcher):

    def __init__(self,cities):
        super().__init__(cities)

    def fetch_all_weather(self):
        threads=[]

        for city in self.cities:
            thread=threading.Thread(target=self.fetchweather,args=(city,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def analyze_weather(self):

        if not self.weather_data:
            print('no weather data available..')
            return pd.DataFrame()
        df=pd.DataFrame(self.weather_data)

        avg_temp=np.mean(df['temperature'])
        best_cities=df[df['temperature'] <= avg_temp]

        print(f'average temperture:{avg_temp:.1f}°C')
        print('recommended travel cities:')
        print(best_cities)

        return best_cities

    def plot_weather(self):

        if not self.weather_data:
            print('no weather data to plot')
            return
        df=pd.DataFrame(self.weather_data)

        mtp.Figure(figsize=(8,5))
        mtp.bar(df['city'],df['temperature'],color=['blue','orange','green','red','purple'])
        mtp.axhline(y=np.mean(df['temperature']),color='black',linestyle='--',label='avg temp')

        mtp.xlabel('cities')
        mtp.ylabel('temperature(°C)')
        mtp.title('weather_based travel planner')
        mtp.legend()
        mtp.show()

cities_to_check=['puducherry','kerala','goa','chennai','manali']

planner=travelplanner(cities_to_check)
planner.fetch_all_weather()
recommended_cities=planner.analyze_weather()
planner.plot_weather()
