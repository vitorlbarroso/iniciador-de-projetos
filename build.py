#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para build do executável
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar PyInstaller: {e}")
        return False
    return True

def build_executable():
    """Constrói o executável"""
    print("Construindo executável...")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console (GUI)
        "--name=ProjectLauncher",  # Nome do executável
        "--add-data=config.json;.",  # Incluir arquivo de config
        "--icon=icon.ico",  # Ícone (se existir)
        "project_launcher.py"
    ]
    
    # Remover parâmetro de ícone se não existir
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao criar executável: {e}")
        return False

def cleanup():
    """Limpa arquivos temporários"""
    print("Limpando arquivos temporários...")
    
    # Diretórios e arquivos para remover
    cleanup_items = [
        "build",
        "dist",
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

def main():
    """Função principal"""
    print("=== Build do Project Launcher ===\n")
    
    # Verificar se o arquivo principal existe
    if not os.path.exists("project_launcher.py"):
        print("✗ Arquivo project_launcher.py não encontrado!")
        return False
    
    # Instalar dependências
    if not install_requirements():
        return False
    
    # Construir executável
    if not build_executable():
        return False
    
    # Limpar arquivos temporários
    cleanup()
    
    print("\n=== Build Concluído ===")
    print("✓ Executável criado em: dist/ProjectLauncher.exe")
    print("✓ Arquivo de configuração: config.json")
    print("\nPara usar:")
    print("1. Copie o ProjectLauncher.exe para onde desejar")
    print("2. Copie o config.json para o mesmo diretório")
    print("3. Edite o config.json com seus projetos")
    print("4. Execute o ProjectLauncher.exe")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
