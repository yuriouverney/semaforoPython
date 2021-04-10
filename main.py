import time
import threading
import PySimpleGUI as sg
from tkinter import *

FECHADO = 'FECHADO'
AMARELO = 'AMARELO'
ABERTO = 'ABERTO'
ligado = 0

class Semaforo:
    def __init__(self, desligar_event, tempo_fechado=2, tempo_amarelo=1, tempo_aberto=2):
        self.tempo_fechado = tempo_fechado
        self.tempo_amarelo = tempo_amarelo
        self.tempo_aberto = tempo_aberto
        self.ligado = False
        self.estado = ABERTO
        self.desligar_event = desligar_event

    def deve_desligar(self):
        return self.desligar_event.isSet()

    def ligar(self):
        self.ligado = True
        while not self.deve_desligar():
            self.abrir()
            self.amarelar()
            self.fechar()
        self.desligar()

    def abrir(self):
        if self.deve_desligar() and status_semaforo == "Desligado":
            return
        self.estado = ABERTO

        # muda imagem semaforo
        progress_bar.UpdateBar(1)
        img = PhotoImage(file="semaforo_verde.png")
        canv.create_image(1, 1, anchor=NW, image=img)
        #####################
        cor_semaforo = f"Verde {str(self.tempo_aberto)}"
        window.Element(_COR_).Update(cor_semaforo)
        time.sleep(self.tempo_aberto)

    def amarelar(self):
        if self.deve_desligar():
            return

        self.estado = AMARELO

        # muda imagem semaforo
        img = PhotoImage(file="semaforo_amarelo.png")
        canv.create_image(1, 1, anchor=NW, image=img)
        #####################
        status_semaforo = "Ligado"
        progress_bar.UpdateBar(2)
        cor_semaforo = f"Amarelo {str(self.tempo_amarelo)}"
        window.Element(_COR_).Update(cor_semaforo)
        time.sleep(self.tempo_amarelo)

    def fechar(self):
        if self.deve_desligar():
            return

        self.estado = FECHADO

        # muda imagem semaforo
        img = PhotoImage(file="semaforo_vermelho.png")
        canv.create_image(1, 1, anchor=NW, image=img)
        #####################
        status_semaforo = "Ligado"
        progress_bar.UpdateBar(3)
        cor_semaforo = f"Vermelho {str(self.tempo_fechado)}"
        window.Element(_COR_).Update(cor_semaforo)
        time.sleep(self.tempo_fechado)

    def desligar(self):
        self.ligado = False
        window['Iniciar Semaforo'].update(disabled=False)
        # muda imagem semaforo
        img = PhotoImage(file="semaforo_desligado.png")
        canv.create_image(1, 1, anchor=NW, image=img)
        #####################
        cor_semaforo = "Desligado"
        window.Element(_COR_).Update(cor_semaforo)
        status_semaforo = "Desligado"
        window.Element(_STATUS_).Update(status_semaforo)
        progress_bar.UpdateBar(0)

def iniciar_semaforo(desligar_event):
    semaforo = Semaforo(desligar_event)
    semaforo.ligar()

if __name__ == '__main__':
    # Janela do semaforo (Tkinter)
    root = Tk()
    root.title("Semáforo Visual")

    canv = Canvas(root, width=252, height=476, bg='white')
    canv.grid(row=1, column=1)

    img = PhotoImage(file="semaforo_desligado.png")
    canv.create_image(1, 1, anchor=NW, image=img)


    # janela da parte (pySimpleGUI) que mostra o status em label
    _STATUS_ = "Atualizar _STATUS_"
    _COR_ = "Atualizar _COR_"

    layout = [
        [sg.Text("semáforo desligado", key=_STATUS_)],
        [sg.Text("Desligado               ", key=_COR_)],
        [sg.Button("Iniciar Semaforo")],
        [sg.Button("Desligar Semaforo")],
        [sg.ProgressBar(3, orientation='h', size=(13, 20), key='progressbar')],
        [sg.Button("Fechar")]]

    # Create the window
    window = sg.Window("Semaforo", layout)
    progress_bar = window.FindElement('progressbar')

    desligar_event = threading.Event()
    # Create an event loop
    while True:
        event, values = window.Read()
        # End program if user closes window or
        # presses the OK button
        if event == "Fechar" or event == sg.WIN_CLOSED:
            break

        if event == "Desligar Semaforo":
            if ligado == 1:
                window['Iniciar Semaforo'].update(disabled=True)
            desligar_event.set()
            desligar_event = threading.Event()
            ligado = 0

        if event == "Iniciar Semaforo":
            status_semaforo = "Ligado"
            window.Element(_STATUS_).Update(status_semaforo)

            semaforo_ligado = True
            ligado += 1
            if semaforo_ligado and ligado == 1:
                th1 = threading.Thread(target=iniciar_semaforo, args=[desligar_event], daemon=True)
                th1.start()
            else:
                print("Semáforo já está ativo!")

    window.close()