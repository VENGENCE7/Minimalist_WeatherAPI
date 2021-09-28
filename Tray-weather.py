
import tkinter as tk
import requests
import time

from pystray import MenuItem as item
import pystray
from PIL import Image

import sys

# import win10toast 
from win10toast import ToastNotifier
'''for LINUX 
import os'''

canvas = tk.Tk()
     

canvas.tk.call('wm', 'iconphoto', canvas._w, tk.PhotoImage(file='weather.png'))
canvas.geometry("500x500")
canvas['bg']="#D1F2EB"
canvas.title("Weather App")
f1 = ("poppins", 18, "bold")
f2 = ("Poplar Std", 35, "bold")
f3 = ("Tekton Pro Ext",15)

textField = tk.Entry(canvas, justify='center',bg='#85C1E9', width = 20, font = f2)
textField.pack(pady = 20)
textField.focus()


label1 = tk.Label(canvas,bg='#D1F2EB', font=f2)
label1.pack()
label2 = tk.Label(canvas,bg='#D1F2EB', font=f1)
label2.pack()

N = tk.IntVar()
NC = tk.Checkbutton(canvas, font=f3,text = 'Move to tray',bd=4,bg='#28B463',variable=N,onvalue=1, offvalue=0)
NC.pack(side='bottom')

# create an object to ToastNotifier class
toast = ToastNotifier()

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
        image=Image.open("weather.png")
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

   notif=" Condition:"+condition+"  Temp:"+str(temp)+"°C"
   toast.show_toast(city, notif, duration = 3,
   icon_path ="weather.ico",threaded=True)
   '''for LINUX:
   img=str(os.getcwd())
   img=img+"/weather.png"
   os.system("notify-send -t 10 -i '"+img+"' "+notif) '''
   


      
textField.bind('<Return>', getWeather)

canvas.protocol("WM_DELETE_WINDOW",hide_window)

canvas.mainloop()

