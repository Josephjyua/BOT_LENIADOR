from pyautogui import *
import pyautogui 
import time
from threading import Thread
import cv2
import yaml
import random
import win32api, win32con
import os

class Vector2:
    x = 0
    y = 0   
    def __init__(self,x = 0,y = 0):
        self.x = x
        self.y = y
        
pyautogui.FAILSAFE = False

config = None
with open(f'/Users/josep/OneDrive/Escritorio/BOT/Lenador/config.yml') as f:
    config = yaml.safe_load(f)

directorio = config['directorio']

#hechizo

# Contadores
recolecciones = 0
maxRecolecciones = 100000

# Tiempos
tiempoPuntoAPuntoMax = 4.5
tiempoRecoleccionNogal = 1
tiempoRecoleccionFresno = 12
cdrSacrificada = 0
cdrCombo = 0

# Posiciones
inventarioBancoPosInicialX = 1315
inventarioBancoPosInicialY = 345
posMadera = Vector2(0,0)


# 1 = recolectando
# 2 = combatiendo
estado = 1
turno = 0
turnosDeEspera = 6
def MiTurno():
    logodir = f'{directorio}/image/logoCombate.png'
    logoPos = pyautogui.locateCenterOnScreen(logodir,confidence = 0.6)
    if(logoPos != None):
        return True
    else:
        return False
    
def ComenzarCombate():
    global estado
    dir =f'{directorio}/image/listo.png'
    pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.8)
    if(pos != None):
        estado = 2
        # no entren mas pj
        pyautogui.moveTo(config['iconCandado']['x'],config['iconCandado']['y'])
        pyautogui.click()
        print("estas en combate")
        # Comenzar combate
        pyautogui.moveTo(pos,duration=0.2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        # desactivar espectador 
        pyautogui.moveTo(config['iconDesactivarEspectador']['x'], config['iconDesactivarEspectador']['y'])
        pyautogui.click()
    
def ModoTactico():
        for i in range(config['cantidadImagenesModoTactico']):
            dir =f'{directorio}/image/modoTactico{i+1}.png'
            pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.8)

            if(pos != None):
                return True
            
        return False
        
def EnCombate():
    global estado

    if( ModoTactico() == False):
        estado = 1
        return False
    else:
        estado = 2
        return True
        
def ComboSadida():
    global cdrCombo 
    if(turno >= turnosDeEspera and cdrCombo == 0):
        cdrCombo = 7
        pDir =f'{directorio}/image/personajeIcon.png'
        pPos = pyautogui.locateCenterOnScreen(pDir,confidence = 0.8)
        # Temblor
        pyautogui.moveTo(config['hechizos'][1]['x'],config['hechizos'][1]['y'],duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(pPos,duration=0.2)
        pyautogui.click()
        
        #Viento envenenado
        pyautogui.moveTo(config['hechizos'][2]['x'],config['hechizos'][2]['y'],duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(pPos,duration=0.2)
        pyautogui.click()
        time.sleep(0.3)
        #Desechizar
        pyautogui.moveTo(config['hechizos'][3]['x'],config['hechizos'][3]['y'],duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(pPos,duration=0.2)
        pyautogui.click()
        time.sleep(0.3)
        if(cdrCombo > 0):
            cdrCombo = cdrCombo -1

def Sacrificada():
    global cdrSacrificada
    # Lanzar sacrificada
    if(cdrSacrificada == 0):
        pyautogui.moveTo( config['hechizos'][4]['x'], config['hechizos'][4]['y'],duration=0.2)
        pyautogui.click()
        p1Pos = GetPosCharacter()
        if(p1Pos != None):
            
            pyautogui.moveTo(p1Pos.x + 48 , p1Pos.y -25,duration=0.2)
            pyautogui.click()
            time.sleep(0.3)
            cdrSacrificada = 2
    else:
        cdrSacrificada = cdrSacrificada -1    

def Zarza():
    # Lanzar zarza
    pyautogui.moveTo(config['hechizos'][5]['x'],config['hechizos'][5]['y'],duration=0.2)
    pyautogui.click()
    if(GetPosMadera != None):
        pyautogui.moveTo(GetPosMadera().x,GetPosMadera().y,duration=0.2)
        pyautogui.click()
    time.sleep(0.4)

def FinTurno():
    # fin del turno
    time.sleep(1)
    pyautogui.moveTo(config['finTurnoPos']['x'],config['finTurnoPos']['y'])
    pyautogui.click()

def GetPosMadera():
    v = Vector2()
    global posMadera
    for i in range(config['totalMaderas']):
         
        dir =f'{directorio}/image/m{i+1}.png'
        pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.6)

        if(pos != None):
             posMadera.x = pos.x
             posMadera.y = pos.y
             return pos

    return posMadera       

def GetPosCharacter():
        v = Vector2()
        for i in range(config['cantidadImagenesPersonaje']):
           p1Dir =f'{directorio}/image/s{i+1}.png'
           p1Pos = pyautogui.locateCenterOnScreen(p1Dir,confidence = 0.6)
           if(p1Pos != None):
               img = cv2.imread(f'{directorio}/image/s{i+1}.png')
               
               v.x = p1Pos.x
               v.y = p1Pos.y + (img.shape[1]/2)
               return v
        v.x = 1000
        v.y = 465
        return v   
        
def Move():


    for i in range(1):
           
        time.sleep(0.05)
        p1Pos = GetPosCharacter()

        if(p1Pos.x > GetPosMadera().x and p1Pos.y > GetPosMadera().y ):
            pyautogui.moveTo(p1Pos.x - config['unidadPorCuadro']['x'] * 4, p1Pos.y - config['unidadPorCuadro']['y'] * 4) 
            pyautogui.doubleClick()

        if(p1Pos.x > GetPosMadera().x and p1Pos.y < GetPosMadera().y ):
            pyautogui.moveTo(p1Pos.x - config['unidadPorCuadro']['x']* 4, p1Pos.y + config['unidadPorCuadro']['y']* 4) 
            pyautogui.doubleClick()    

        if(p1Pos.x < GetPosMadera().x and p1Pos.y > GetPosMadera().y ):
            pyautogui.moveTo(p1Pos.x + config['unidadPorCuadro']['x']* 4, p1Pos.y - config['unidadPorCuadro']['y']* 4) 
            pyautogui.doubleClick()    

        if(p1Pos.x < GetPosMadera().x and p1Pos.y < GetPosMadera().y ):
            pyautogui.moveTo(p1Pos.x + config['unidadPorCuadro']['x']* 4, p1Pos.y + config['unidadPorCuadro']['x']* 4) 
            pyautogui.doubleClick()

def PocimaRecuerdo():

    pyautogui.moveTo(config['pocimaRecuerdoPos']['x'],config['pocimaRecuerdoPos']['y'])
    pyautogui.doubleClick()
    time.sleep(1)
    
def AbrirBanco():

    pyautogui.moveTo(config['BanqueroPos']['x'],config['BanqueroPos']['y'])
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(config['hablarBanqueroPos']['x'],config['hablarBanqueroPos']['y']) 
    pyautogui.click()
    time.sleep(1.5)
    pyautogui.moveTo(config['consultarCajaPos']['x'],config['consultarCajaPos']['y'])
    pyautogui.click()
    time.sleep(1.5)
    
def EntrarBanco():

    pyautogui.moveTo(config['entradaBancoPos']['x'],config['entradaBancoPos']['y'])
    time.sleep(0.2)
    pyautogui.doubleClick()
    time.sleep(6)

def IrABonta():
    dir =f'{directorio}/image/pocimaBonta.png'
    pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.6)
    pyautogui.moveTo(pos)
    pyautogui.doubleClick()
    time.sleep(1)

def TomarZaapi():
    dir =f'{directorio}/image/zappi.png'
    pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.6)
    if(pos != None):
        pyautogui.moveTo(pos)
        pyautogui.click()
        pyautogui.moveTo(pos.x + config['dif']['x'], pos.y + config['dif']['y']) 
    else:
        pyautogui.moveTo(config['zappiPos']['x'],config['zappiPos']['y'])
        pyautogui.click()
        pyautogui.moveTo(config['zappiPos']['x'] + config['dif']['x'], config['zappiPos']['y'] + config['dif']['y'] )     
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(config['variosZappiPos']['x'],config['variosZappiPos']['y'])
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(config['bancoZappiPos']['x'],config['bancoZappiPos']['y'],0.2)
    pyautogui.click()
    time.sleep(1)

def VerificarCombateFinalizado():
    global turno
    global estado
    finDir = f'{directorio}/image/finCombate.png'
    finPos = pyautogui.locateCenterOnScreen(finDir,confidence = 0.6)
    if(finPos != None):
        turno = 0
        pyautogui.press('esc')
        estado = 1

def SecuenciaSadidaAtaque():
    ComboSadida()
    Zarza()
    Zarza()
    Sacrificada()

def Cuervo():
    pyautogui.moveTo(config['hechizos'][3]['x'],config['hechizos'][3]['y'],duration=0.2)
    pyautogui.click()
    if(GetPosMadera != None):
        pyautogui.moveTo(GetPosMadera().x,GetPosMadera().y,duration=0.2)
        pyautogui.click()
    time.sleep(0.4)

def InvoCombo():
    pyautogui.moveTo( config['hechizos'][1]['x'], config['hechizos'][1]['y'],duration=0.2)
    pyautogui.click()
    p1Pos = GetPosCharacter()
    if(p1Pos != None):
        
        pyautogui.moveTo(p1Pos.x + config['unidadPorCuadro']['x'] , p1Pos.y -config['unidadPorCuadro']['y'],duration=0.2)
        pyautogui.click()
        time.sleep(0.3)

        pyautogui.moveTo( config['hechizos'][2]['x'], config['hechizos'][2]['y'],duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(p1Pos.x + config['unidadPorCuadro']['x'] , p1Pos.y -config['unidadPorCuadro']['y'],duration=0.2)
        pyautogui.click()
        time.sleep(0.3)

def SecuenciaAtaqueOsamodas():
    InvoCombo()
    Cuervo()
    Cuervo()
    pass
    

def Combate():
    global turno
    global estado
    while(True):
        if(EnCombate()):

            print("En combate")
            ComenzarCombate()
              
            if(MiTurno()):
                
                turno = turno + 1
                estado = 2             
                if(config['movimiento']):
                    Move()
                if (config['clase'] == 'Sadida'):
                    SecuenciaSadidaAtaque()
                
                if (config['clase'] == 'Osamodas'):
                    SecuenciaAtaqueOsamodas()
                    
                FinTurno()

        VerificarCombateFinalizado()

def DepositarRecursos():
    pyautogui.moveTo(config['iconRecursoBancoPos']['x'],config['iconRecursoBancoPos']['y'])
    pyautogui.click()
    time.sleep(1)
    with pyautogui.hold("ctrl"):
        for y in range(7):
            for x in range(5):
              pyautogui.moveTo(config['iconRecursoBancoPos']['x']+(config['factor']['x'] * x) ,config['iconRecursoBancoPos']['y']+(config['factor']['y'] * y),0.2)  
              pyautogui.click()
              time.sleep(0.13)

        pyautogui.moveTo(config['inventarioBancoPosInicial']['x'],config['inventarioBancoPosInicial']['y'],0.2) 
        pyautogui.doubleClick() 
        time.sleep(1)    
    pyautogui.press('esc')
    time.sleep(1)

def IrAlBanco():
    IrABonta()
    TomarZaapi()
    EntrarBanco()
    AbrirBanco()
    DepositarRecursos()
    global recolecciones
    recolecciones = 0

def CheckMadera(m):
            print(m)
            for i in range(config['cantidadMaderasPorVerificar']):

                dir =f'{directorio}/image/{m}{i+1}.png'
                pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.7)

                if(pos != None):
                    return pos
            return None   
     
def Recolectar(m):
    
    global recolecciones
    global estado
    while(True):
        if(estado == 1):
            pos = CheckMadera(m)
            if(pos == None):
                print(f'{m} no encontrado')
                break
        
            recolecciones = recolecciones + 1
            pyautogui.moveTo(pos)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.moveTo(pos.x + config['dif']['x'],pos.y + config['dif']['y'])
            pyautogui.click()
            time.sleep(2)
        
        while(estado == 2):
            time.sleep(1)


def MoveTo(a,b):
    pyautogui.moveTo(a,b)
    time.sleep(0.3)
    pyautogui.doubleClick()
    time.sleep(tiempoPuntoAPuntoMax)
    time.sleep(3.5)

def Ruta(ruta):
    
        for i in ruta:
            while(EnCombate()):
                print("Esperando que termine combate para recolectar")
                time.sleep(5)
            
            MoveTo(i.x,i.y)  
            for i in config['maderas'].keys():
                if(config['maderas'][i]):
                    Recolectar(i)

def LvlUp():
    while(True):

        dir =f'{directorio}/image/lvlup.png'
        pos = pyautogui.locateCenterOnScreen(dir,confidence = 0.8)
        if(pos != None):
            pyautogui.moveTo(961,464)
            time.sleep(0.2)
            pyautogui.click()
            print("Lvl Up")
            LvlUp()
        
        time.sleep(1)

def ReadYML(yml):
    r = []
    with open(f'{directorio}/rutas/{yml}.yml') as f:
        data = yaml.safe_load(f)

    for i in data:
        r.append(Vector2(i['x'],i['y']))
    
    return r      

   
if __name__ == '__main__':

    ruta = ReadYML(config['rutaRecoleccion'])
 
          
    hilo1 = Thread(target=LvlUp)
    hilo2 = Thread(target=Combate)
    hilo1.start()
    hilo2.start()

    while(True): 
  
      for i in range(config['vueltas']):
            
        Ruta(ruta)
        PocimaRecuerdo()

      IrAlBanco()
      PocimaRecuerdo()
        

       
      
      

        


