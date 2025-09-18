#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para build do executável
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def cleanup_temp_files():
    """Limpa apenas arquivos temporários, mantém a pasta dist"""
    print("Limpando arquivos temporários...")
    
    # Arquivos temporários para remover (NÃO remover dist!)
    cleanup_items = [
        "build",
        "ProjectLauncher.spec",
        "__pycache__"
    ]
    
    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            print(f"✓ Removido: {item}")
    
    print("✓ Pasta dist/ mantida com o executável")

def move_and_rename_executable():
    """Move o executável para a raiz e renomeia com a data atual"""
    print("Movendo e renomeando executável...")
    
    try:
        # Obter data atual no formato dd/mm/yyyy
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        
        # Nome do arquivo final
        new_name = f"Iniciador de Projetos - {date_str}.exe"
        
        # Caminhos
        source = "dist/ProjectLauncher.exe"
        destination = new_name
        
        # Mover arquivo
        shutil.move(source, destination)
        print(f"✓ Executável movido para: {new_name}")
        
        # Copiar config.json para a raiz se existir
        if os.path.exists("config.json"):
            shutil.copy2("config.json", "config.json")
            print("✓ config.json mantido na raiz")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao mover executável: {e}")
        return False

def cleanup_all_files():
    """Limpa todos os arquivos temporários e a pasta dist"""
    print("Limpando arquivos temporários...")
    
    # Arquivos e pastas para remover
    cleanup_items = [
        "build",
        "dist",
        "ProjectLauncher.spec",
        "__pycache__"
    ]
    
    for item in cleanup_items:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"✓ Removido: {item}")
            except Exception as e:
                print(f"⚠️ Erro ao remover {item}: {e}")
    
    print("✓ Limpeza concluída")

def main():
    print("=== Build Simples do Project Launcher ===\n")
    
    # Verificar se o arquivo principal existe
    if not os.path.exists("project_launcher.py"):
        print("✗ Arquivo project_launcher.py não encontrado!")
        return False
    
    # Instalar PyInstaller se necessário
    print("Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✓ PyInstaller já está disponível")
    except ImportError:
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado com sucesso")
        except Exception as e:
            print(f"✗ Erro ao instalar PyInstaller: {e}")
            return False
    
    # Construir executável
    print("\nConstruindo executável...")
    
    # Comando básico
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=ProjectLauncher",
        "project_launcher.py"
    ]
    
    # Adicionar arquivo de config se existir
    if os.path.exists("config.json"):
        cmd.insert(-1, "--add-data=config.json;.")
    
    # Adicionar ícone se existir
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon=icon.ico")
    
    try:
        print(f"Executando: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("\n✓ Executável criado com sucesso!")
        print("✓ Localização: dist/ProjectLauncher.exe")
        
        # Verificar se foi criado
        if os.path.exists("dist/ProjectLauncher.exe"):
            print("✓ Arquivo executável encontrado!")
            
            # Mover e renomear executável para a raiz
            move_and_rename_executable()
            
            # Limpar arquivos temporários e pasta dist
            cleanup_all_files()
            
            print("\n=== Build Concluído ===")
            print("✓ Executável criado e movido para a raiz")
            print("✓ Pasta dist/ removida")
            print("✓ Arquivos temporários limpos")
            print("\nPara usar:")
            print("1. Execute o arquivo 'Iniciador de Projetos - [data].exe'")
            print("2. Edite config.json conforme necessário")
            
            return True
        else:
            print("✗ Executável não foi criado!")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao criar executável: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPressione Enter para sair...")
    sys.exit(0 if success else 1)
