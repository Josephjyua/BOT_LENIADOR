from pynput import keyboard as kb
import pyautogui 
import time
import	yaml

ruta = []
nombre = input("Ingresa un nombre para la ruta")
def pulsa(tecla):

    if(str(tecla) == "'x'"):
        captura()
    elif(str(tecla) == "'v'"):
        guardar()
	   

 
            

                    
def captura():
    x=pyautogui.position().x
    y=pyautogui.position().y
    arr ={'x':x ,'y':y}

    data = {'Coordenada':arr}
    
    ruta.append(data)
 

def guardar():
    with open(f'/Users/josep/OneDrive/Escritorio/BOT/Lenador/rutas/{nombre}.yml','w') as f:
        yaml.dump(ruta,f, default_flow_style=False)
        print(ruta)
    
kb.Listener(pulsa).run()    