from pynput import keyboard as kb
import pyautogui 
import time
import	yaml
import os

ruta = []
print("_________________________________")
print(("IMPORTANTE"))
print("_________________________________")
print("Presiona X para capturar.")
print("Presiona V para terminar.")
time.sleep(1)
nombre = input("Ingresa un nombre para la ruta: ")
def pulsa(tecla):

    if(str(tecla) == "'x'"):
        captura()
    elif(str(tecla) == "'v'"):
        guardar()
	                           
def captura():
    
    x=pyautogui.position().x
    y=pyautogui.position().y
    arr ={'x':x ,'y':y}
    ruta.append(arr)
    print(f"Se ha capturado la posición: {arr}" )

 

def guardar():
    aRutas = r'\rutas'
    p = f'{os.path.dirname(__file__)}{aRutas}'+  str(r'\ ').replace(" ","")+f'{nombre}.yml'
    with open(p,'w') as f:
        yaml.dump(ruta,f, default_flow_style=False)
        print(f"Se ha guardado la ruta: {nombre} con los valores de: {ruta}")
        exit()
        
    
kb.Listener(pulsa).run()    