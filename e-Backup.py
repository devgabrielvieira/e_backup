import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import json
import time


class BackupHandler(FileSystemEventHandler):
    def __init__(self, pasta_selecionada, pasta_backup, app):
        self.pasta_selecionada = pasta_selecionada
        self.pasta_backup = pasta_backup
        self.app = app

    def on_created(self, event):
        if not event.is_directory:
            arquivo = event.src_path
            self.perform_backup(arquivo)
            self.app.update_status("Arquivo criado: {}".format(arquivo))

    def on_modified(self, event):
        if not event.is_directory:
            arquivo = event.src_path
            self.perform_backup(arquivo)
            self.app.update_status("Arquivo modificado: {}".format(arquivo))

    def perform_backup(self, arquivo):
        data_atual = datetime.datetime.today()
        ano = data_atual.strftime("%Y")
        mes = data_atual.strftime("%m")
        dia = data_atual.strftime("%d")

        pasta_backup = os.path.join(self.pasta_backup, ano, mes, dia)

        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup, exist_ok=True)

        nome_final_arquivo = os.path.join(pasta_backup, os.path.basename(arquivo))

        while True:
            try:
                shutil.copy2(arquivo, nome_final_arquivo)
                self.app.update_status("Backup realizado: {}".format(nome_final_arquivo))
                break
            except PermissionError:
                time.sleep(0.1)
            except Exception as e:
                self.app.update_status("Erro ao realizar backup: {}".format(str(e)))
                break


class BackupApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("e-Backup | Versão 3.0.0")
        self.largura = 550
        self.altura = 150
        self.largura_tela = self.root.winfo_screenwidth()
        self.altura_tela = self.root.winfo_screenheight()
        self.x = (self.largura_tela / 2) - (self.largura / 2)
        self.y = (self.altura_tela / 2) - (self.altura / 2)
        self.root.geometry('%dx%d+%d+%d' %
                           (self.largura, self.altura, self.x, self.y))

        self.titulo = ttk.Label(
            root, text="Backup e Monitoramento | Farmácia Popular", font=("Helvetica", 16))
        self.titulo.pack(pady=10)

        self.lbl_status = ttk.Label(root, text="", font=("Helvetica", 10))
        self.lbl_status.pack(pady=2)

        self.pasta_selecionada, self.pasta_backup = self.load_configurations()

        self.btn_monitorar = ttk.Button(root, text="Selecionar Pasta | Realizar Backup | Monitoramento",
                                       command=self.start_backup, bootstyle=SUCCESS)
        self.btn_monitorar.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

        self.lbl_slogan = ttk.Label(root, text="Me sigam no Instagram @devgabiviera", font=("Helvetica", 12))
        self.lbl_slogan.pack(pady=5)

        self.start_application()

    def start_application(self):
        if self.pasta_selecionada and self.pasta_backup:
            self.update_status("Iniciando backup geral...")
            self.perform_general_backup(
                self.pasta_selecionada, self.pasta_backup)
            self.update_status("Backup geral concluído.")
            self.start_monitoring(
                self.pasta_selecionada, self.pasta_backup)
            self.update_status(
                "Monitoramento iniciado para a pasta selecionada.")
        else:
            self.update_status(
                "Nenhuma configuração encontrada. Selecione uma pasta para iniciar o backup e monitoramento.")

    def start_backup(self):
        nome_pasta_selecionada = filedialog.askdirectory(
            title="Selecionar Pasta para Backup e Monitoramento")
        if not nome_pasta_selecionada:
            self.update_status("Nenhuma pasta selecionada.")
            return

        nome_pasta_backup = filedialog.askdirectory(
            title="Selecionar Diretório de Backup")
        if not nome_pasta_backup:
            self.update_status("Nenhum diretório de backup selecionado.")
            return

        self.update_status("Realizando backup geral...")
        self.perform_general_backup(nome_pasta_selecionada, nome_pasta_backup)
        self.update_status("Backup geral da pasta selecionada concluído.")

        self.start_monitoring(nome_pasta_selecionada, nome_pasta_backup)
        self.update_status(
            "Monitoramento iniciado para a pasta selecionada.")

        self.save_configurations(nome_pasta_selecionada, nome_pasta_backup)

    def perform_general_backup(self, pasta_selecionada, pasta_backup):
        data_atual = datetime.datetime.today()
        ano = data_atual.strftime("%Y")
        mes = data_atual.strftime("%m")
        dia = data_atual.strftime("%d")

        pasta_backup_geral = os.path.join(pasta_backup, ano, mes, dia)

        if not os.path.exists(pasta_backup_geral):
            os.makedirs(pasta_backup_geral, exist_ok=True)

        for item in os.listdir(pasta_selecionada):
            origem = os.path.join(pasta_selecionada, item)

            if os.path.isdir(origem):
                destino = os.path.join(pasta_backup_geral, item)
                if not os.path.exists(destino):
                    os.makedirs(destino, exist_ok=True)

                shutil.copytree(origem, destino, dirs_exist_ok=True)

            else:
                destino = os.path.join(pasta_backup_geral, item)
                shutil.copy2(origem, destino)

    def start_monitoring(self, pasta_selecionada, pasta_backup):
        self.manipulador_eventos = BackupHandler(
            pasta_selecionada, pasta_backup, self)
        self.observador = Observer()
        self.observador.schedule(
            self.manipulador_eventos, pasta_selecionada, recursive=True)
        self.observador.start()

    def save_configurations(self, pasta_selecionada, pasta_backup):
        config = {"pasta_selecionada": pasta_selecionada,
                  "pasta_backup": pasta_backup}
        while True:
            try:
                with open("config.txt", "w") as arquivo_config:
                    json.dump(config, arquivo_config)
                break
            except PermissionError:
                time.sleep(0.1)

    def load_configurations(self):
        if os.path.exists("config.txt"):
            while True:
                try:
                    with open("config.txt", "r") as arquivo_config:
                        config = json.load(arquivo_config)
                        return config.get("pasta_selecionada", ""), config.get("pasta_backup", "")
                except PermissionError:
                    time.sleep(0.1)
        return "", ""

    def close_application(self):
        self.observador.stop()
        self.observador.join()
        self.root.destroy()

    def update_status(self, mensagem):
        self.lbl_status.config(text=mensagem)


root = ttk.Window(themename="superhero")
app = BackupApplication(root)
root.mainloop()
