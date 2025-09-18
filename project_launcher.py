#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher de Projetos - Executável para gerenciar e executar projetos
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import subprocess
import sys
from pathlib import Path
import threading
import time

class ProjectLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Launcher de Projetos")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configurações
        self.config_file = "config.json"
        self.projects = {}
        self.current_project = None
        self.current_options = []
        self.option_stack = []  # Para navegação entre opções
        
        # Carregar configurações
        self.load_config()
        
        # Criar interface
        self.create_interface()
        
    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.projects = json.load(f)
            else:
                self.create_default_config()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")
            self.create_default_config()
    
    def create_default_config(self):
        """Cria arquivo de configuração padrão"""
        default_config = {
            "Super Pagamentos": {
                "path": "C:/projetos/super-pagamentos",
                "options": {
                    "Front Dashboard": {
                        "type": "execute",
                        "actions": [
                            {"type": "open_cursor", "path": "front-dashboard"},
                            {"type": "run_command", "command": "npm install", "path": "front-dashboard"},
                            {"type": "run_command", "command": "npm start", "path": "front-dashboard"}
                        ]
                    },
                    "Back Dashboard": {
                        "type": "execute",
                        "actions": [
                            {"type": "open_cursor", "path": "back-dashboard"},
                            {"type": "run_command", "command": "npm install", "path": "back-dashboard"},
                            {"type": "run_command", "command": "npm run dev", "path": "back-dashboard"}
                        ]
                    },
                    "Back API": {
                        "type": "execute",
                        "actions": [
                            {"type": "open_cursor", "path": "back-api"},
                            {"type": "run_command", "command": "pip install -r requirements.txt", "path": "back-api"},
                            {"type": "run_command", "command": "python app.py", "path": "back-api"}
                        ]
                    },
                    "Todos": {
                        "type": "execute",
                        "actions": [
                            {"type": "open_cursor", "path": "front-dashboard"},
                            {"type": "open_cursor", "path": "back-dashboard"},
                            {"type": "open_cursor", "path": "back-api"},
                            {"type": "run_command", "command": "npm install", "path": "front-dashboard"},
                            {"type": "run_command", "command": "npm install", "path": "back-dashboard"},
                            {"type": "run_command", "command": "pip install -r requirements.txt", "path": "back-api"}
                        ]
                    }
                }
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        
        self.projects = default_config
    
    def create_interface(self):
        """Cria a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Launcher de Projetos", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Seleção de projeto
        ttk.Label(main_frame, text="Selecione o projeto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(main_frame, textvariable=self.project_var, 
                                         state="readonly", width=40)
        self.project_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_selected)
        
        # Frame para opções
        self.options_frame = ttk.LabelFrame(main_frame, text="Opções do Projeto", padding="10")
        self.options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                               pady=20)
        self.options_frame.columnconfigure(0, weight=1)
        
        # Lista de opções
        self.options_listbox = tk.Listbox(self.options_frame, height=8)
        self.options_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.options_listbox.bind('<Double-1>', self.on_option_selected)
        
        # Scrollbar para lista
        scrollbar = ttk.Scrollbar(self.options_frame, orient="vertical", command=self.options_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.options_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.back_button = ttk.Button(button_frame, text="← Voltar", 
                                    command=self.go_back, state="disabled")
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        self.execute_button = ttk.Button(button_frame, text="Executar", 
                                       command=self.execute_option, state="disabled")
        self.execute_button.pack(side=tk.LEFT, padx=5)
        
        self.config_button = ttk.Button(button_frame, text="Configurar", 
                                      command=self.open_config)
        self.config_button.pack(side=tk.LEFT, padx=5)
        
        # Barra de progresso (inicialmente oculta)
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        # Não adicionar ao grid inicialmente - será mostrada apenas durante execução
        
        # Status
        self.status_var = tk.StringVar(value="Pronto")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Atualizar lista de projetos
        self.update_project_list()
    
    def update_project_list(self):
        """Atualiza a lista de projetos no combobox"""
        projects = list(self.projects.keys())
        self.project_combo['values'] = projects
        if projects:
            self.project_combo.set(projects[0])
            self.on_project_selected()
    
    def on_project_selected(self, event=None):
        """Callback quando um projeto é selecionado"""
        project_name = self.project_var.get()
        if project_name in self.projects:
            self.current_project = project_name
            self.option_stack = []
            self.show_options(self.projects[project_name]["options"])
    
    def show_options(self, options):
        """Mostra as opções disponíveis"""
        self.current_options = options
        self.options_listbox.delete(0, tk.END)
        
        for option_name, option_data in options.items():
            option_type = option_data.get("type", "execute")
            icon = "📁" if option_type == "options" else "▶️"
            self.options_listbox.insert(tk.END, f"{icon} {option_name}")
        
        self.execute_button.config(state="disabled")
        self.back_button.config(state="disabled" if not self.option_stack else "normal")
    
    def on_option_selected(self, event):
        """Callback quando uma opção é selecionada"""
        selection = self.options_listbox.curselection()
        if selection:
            index = selection[0]
            option_name = list(self.current_options.keys())[index]
            option_data = self.current_options[option_name]
            
            if option_data.get("type") == "options":
                # Navegar para sub-opções
                self.option_stack.append((self.current_options, option_name))
                self.show_options(option_data["options"])
            else:
                # Marcar para execução
                self.execute_button.config(state="normal")
    
    def go_back(self):
        """Volta para o nível anterior de opções"""
        if self.option_stack:
            self.current_options, _ = self.option_stack.pop()
            self.show_options(self.current_options)
    
    def execute_option(self):
        """Executa a opção selecionada"""
        selection = self.options_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma opção para executar")
            return
        
        index = selection[0]
        option_name = list(self.current_options.keys())[index]
        option_data = self.current_options[option_name]
        
        if option_data.get("type") == "execute":
            self.run_actions(option_data["actions"])
        else:
            messagebox.showinfo("Info", "Esta opção não pode ser executada diretamente")
    
    def run_actions(self, actions):
        """Executa uma lista de ações"""
        def run_in_thread():
            # Mostrar barra de progresso
            self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
            self.progress['maximum'] = len(actions)
            self.progress['value'] = 0
            self.status_var.set("Executando ações...")
            
            try:
                project_path = self.projects[self.current_project]["path"]
                
                for i, action in enumerate(actions):
                    action_type = action.get("type")
                    
                    # Atualizar status com ação atual
                    if action_type == "open_cursor":
                        self.status_var.set(f"Abrindo projeto: {action.get('path', '')}")
                        self.open_cursor(project_path, action.get("path", ""))
                    elif action_type == "open_postman":
                        self.status_var.set("Abrindo Postman...")
                        self.open_postman()
                    elif action_type == "open_dbeaver":
                        self.status_var.set("Abrindo DBeaver...")
                        self.open_dbeaver()
                    elif action_type == "open_terminal":
                        self.status_var.set(f"Abrindo terminal em: {action.get('path', '')}")
                        self.open_terminal(project_path, action.get("path", ""))
                    elif action_type == "run_command":
                        self.status_var.set(f"Executando: {action.get('command', '')}")
                        self.run_command(project_path, action.get("path", ""), action.get("command", ""))
                    elif action_type == "run_wsl":
                        self.status_var.set(f"Executando no WSL: {action.get('commands', '')}")
                        self.run_wsl_command(project_path, action.get("path", ""), action.get("commands", ""))
                    elif action_type == "wait":
                        self.status_var.set(f"Aguardando {action.get('seconds', 1)} segundos...")
                        time.sleep(action.get("seconds", 1))
                    
                    # Atualizar progresso
                    self.progress['value'] = i + 1
                    self.root.update_idletasks()
                    
                    # Pequena pausa entre ações
                    time.sleep(0.5)
                
                self.status_var.set("Ações executadas com sucesso!")
                messagebox.showinfo("Sucesso", "Todas as ações foram executadas com sucesso!")
                
            except Exception as e:
                self.status_var.set(f"Erro: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao executar ações: {str(e)}")
            finally:
                # Ocultar barra de progresso
                self.progress.grid_remove()
                self.progress['value'] = 0
        
        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
    
    def open_cursor(self, project_path, sub_path=""):
        """Abre o projeto no Cursor"""
        full_path = os.path.join(project_path, sub_path) if sub_path else project_path
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Caminho não encontrado: {full_path}")
        
        try:
            # Tentar abrir com Cursor
            subprocess.Popen(["cursor", full_path], shell=True)
            self.status_var.set(f"Abrindo {full_path} no Cursor...")
        except Exception as e:
            # Fallback para VS Code se Cursor não estiver disponível
            try:
                subprocess.Popen(["code", full_path], shell=True)
                self.status_var.set(f"Abrindo {full_path} no VS Code...")
            except:
                raise Exception(f"Não foi possível abrir o editor. Caminho: {full_path}")
    
    def open_postman(self):
        """Abre o Postman"""
        self.status_var.set("Abrindo Postman...")
        
        try:
            if sys.platform == "win32":
                # Tentar diferentes formas de abrir o Postman no Windows
                postman_paths = [
                    r"C:\Users\%USERNAME%\AppData\Local\Postman\Postman.exe",
                    r"C:\Program Files\Postman\Postman.exe",
                    r"C:\Program Files (x86)\Postman\Postman.exe",
                    "Postman.exe"  # Se estiver no PATH
                ]
                
                for path in postman_paths:
                    try:
                        expanded_path = os.path.expandvars(path)
                        if os.path.exists(expanded_path) or path == "Postman.exe":
                            subprocess.Popen([expanded_path], shell=True)
                            self.status_var.set("Postman aberto com sucesso!")
                            return
                    except:
                        continue
                
                # Se não encontrou, tentar abrir pelo nome
                subprocess.Popen(["start", "postman:"], shell=True)
                self.status_var.set("Tentando abrir Postman...")
                
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "Postman"])
                self.status_var.set("Postman aberto com sucesso!")
            else:  # Linux
                subprocess.Popen(["postman"])
                self.status_var.set("Postman aberto com sucesso!")
                
        except Exception as e:
            raise Exception(f"Não foi possível abrir o Postman: {str(e)}")
    
    def open_dbeaver(self):
        """Abre o DBeaver"""
        self.status_var.set("Abrindo DBeaver...")
        
        try:
            if sys.platform == "win32":
                # Tentar diferentes formas de abrir o DBeaver no Windows
                dbeaver_paths = [
                    r"C:\Users\%USERNAME%\AppData\Local\DBeaver\dbeaver.exe",
                    r"C:\Program Files\DBeaver\dbeaver.exe",
                    r"C:\Program Files (x86)\DBeaver\dbeaver.exe",
                    r"C:\Users\%USERNAME%\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\dbeaver.exe",
                    "dbeaver.exe"  # Se estiver no PATH
                ]
                
                for path in dbeaver_paths:
                    try:
                        expanded_path = os.path.expandvars(path)
                        if os.path.exists(expanded_path) or path == "dbeaver.exe":
                            subprocess.Popen([expanded_path], shell=True)
                            self.status_var.set("DBeaver aberto com sucesso!")
                            return
                    except:
                        continue
                
                # Se não encontrou, tentar abrir pelo nome
                subprocess.Popen(["start", "dbeaver:"], shell=True)
                self.status_var.set("Tentando abrir DBeaver...")
                
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "DBeaver"])
                self.status_var.set("DBeaver aberto com sucesso!")
            else:  # Linux
                subprocess.Popen(["dbeaver"])
                self.status_var.set("DBeaver aberto com sucesso!")
                
        except Exception as e:
            raise Exception(f"Não foi possível abrir o DBeaver: {str(e)}")
    
    def open_terminal(self, project_path, sub_path=""):
        """Abre um terminal no diretório do projeto"""
        full_path = os.path.join(project_path, sub_path) if sub_path else project_path
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Caminho não encontrado: {full_path}")
        
        self.status_var.set(f"Abrindo terminal em: {full_path}")
        
        # Abrir terminal no diretório
        if sys.platform == "win32":
            cmd = f'start cmd /k "cd /d "{full_path}""'
        elif sys.platform == "darwin":  # macOS
            cmd = f'osascript -e "tell application \\"Terminal\\" to do script \\"cd \\"{full_path}\\"\\""'
        else:  # Linux
            cmd = f'gnome-terminal -- bash -c "cd \\"{full_path}\\"; exec bash"'
        
        subprocess.Popen(cmd, shell=True)
    
    def run_command(self, project_path, sub_path, command):
        """Executa um comando no terminal"""
        full_path = os.path.join(project_path, sub_path) if sub_path else project_path
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Caminho não encontrado: {full_path}")
        
        self.status_var.set(f"Executando: {command} em {full_path}")
        
        # Executar comando em nova janela do terminal
        if sys.platform == "win32":
            cmd = f'start cmd /k "cd /d "{full_path}" && {command}"'
        else:
            cmd = f'gnome-terminal -- bash -c "cd "{full_path}" && {command}; exec bash"'
        
        subprocess.Popen(cmd, shell=True)
    
    def run_wsl_command(self, project_path, sub_path, wsl_commands):
        """Executa comandos no WSL Ubuntu"""
        full_path = os.path.join(project_path, sub_path) if sub_path else project_path
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Caminho não encontrado: {full_path}")
        
        # Preparar comandos para WSL
        if isinstance(wsl_commands, list):
            # Se for lista de comandos, juntar com && para executar sequencialmente
            wsl_command_string = " && ".join(wsl_commands)
        else:
            wsl_command_string = wsl_commands
        
        self.status_var.set(f"Executando no WSL: {wsl_command_string}")
        
        # Executar no WSL Ubuntu
        if sys.platform == "win32":
            # Abrir WSL Ubuntu e executar comandos
            cmd = f'start cmd /k "cd /d "{full_path}" && wsl -d Ubuntu -e bash -c "{wsl_command_string}; exec bash""'
        else:
            # Para Linux, usar bash normal
            cmd = f'gnome-terminal -- bash -c "cd "{full_path}" && {wsl_command_string}; exec bash"'
        
        subprocess.Popen(cmd, shell=True)
    
    def open_config(self):
        """Abre o arquivo de configuração no editor padrão"""
        try:
            if sys.platform == "win32":
                os.startfile(self.config_file)
            else:
                subprocess.Popen(["xdg-open", self.config_file])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo de configuração: {str(e)}")
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProjectLauncher()
    app.run()
