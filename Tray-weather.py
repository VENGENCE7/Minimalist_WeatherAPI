
import tkinter as tk
import requests
import time

from pystray import MenuItem as item
import pystray
from PIL import Image

import os
import sys

# import win10toast for WINDOWS
#from win10toast import ToastNotifier

canvas = tk.Tk()

# create an object to ToastNotifier class   FOR WINDOWS
#toast = ToastNotifier()

canvas.tk.call('wm', 'iconphoto', canvas._w, tk.PhotoImage(file='/home/vengence/Apps/Weather/Weather-Light-Tray/weather.png'))
canvas.geometry("700x700")
canvas.title("Weather App")
f1 = ("poppins", 18, "bold")
f2 = ("Poplar Std", 35, "bold")
f3 = ("Tekton Pro Ext",15)

textField = tk.Entry(canvas, justify='center', width = 20, font = f2)
textField.pack(pady = 20)
textField.focus()


label1 = tk.Label(canvas, font=f2)
label1.pack()
label2 = tk.Label(canvas, font=f1)
label2.pack()

N = tk.IntVar()
NC = tk.Checkbutton(canvas, font=f3,text = 'Move to tray',bd=4,variable=N,onvalue=1, offvalue=0)
NC.pack(side='bottom')

# Define a function for quit the window
def quit_window(icon):
   icon.stop()
   canvas.destroy()
   sys.exit()

# Define a function to show the window again
def show_window(icon):
   icon.stop()
   canvas.after(0,canvas.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
    if N.get()==1:
        canvas.withdraw()
        image=Image.open("/home/vengence/Apps/Weather/Weather-Light-Tray/weather.png")
        menu=(item('Quit', quit_window), item('Show', show_window),item('Notify Now',notify))
        icon=pystray.Icon("weather", image, "My System Tray Icon", menu)
        icon.run()
    else:
        sys.exit()
        
#notification from tray
def notify():
    getWeather(canvas)         

   

def getWeather(canvas):
   global city
   city = textField.get()
   api = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=9a9a8abe63e24aa5d92dcc87697b76b4"
   
   json_data = requests.get(api).json()
   condition = json_data['weather'][0]['main']
   temp = int(json_data['main']['temp'] - 273.15)
   min_temp = int(json_data['main']['temp_min'] - 273.15)
   max_temp = int(json_data['main']['temp_max'] - 273.15)
   pressure = json_data['main']['pressure']
   humidity = json_data['main']['humidity']
   wind = json_data['wind']['speed']
   sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
   sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))
      
   final_info = condition + "\n" + str(temp) + "°C" 
   final_data = "\n"+ "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" +"\n" + "Pressure: " + str(pressure) + "\n" +"Humidity: " + str(humidity) + "\n" +"Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
   label1.config(text = final_info)
   label2.config(text = final_data)

   city.upper()   
   notif=city+" Condition:"+condition+"'  'Temp:"+str(temp)+"°C"
   os.system("notify-send -t 10 -i '/home/vengence/Apps/Weather/Weather-Light-Tray/weather.png' "+notif) 
   
     #FOR WINDOWS NOTIFICATION
     '''notif=" Condition:"+condition+"  Temp:"+str(temp)+"°C"
   toast.show_toast(city, notif, duration = 5,
   icon_path ="E:\Weather\Weather-Dark-Tray\weather.ico",threaded=True) '''
   

      
textField.bind('<Return>', getWeather)

canvas.protocol("WM_DELETE_WINDOW",hide_window)

canvas.mainloop()

