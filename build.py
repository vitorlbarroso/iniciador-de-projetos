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
        # Verificar se PyInstaller já está instalado
        try:
            subprocess.check_call([sys.executable, "-c", "import pyinstaller"], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✓ PyInstaller já está instalado")
            return True
        except subprocess.CalledProcessError:
            pass
        
        # Instalar PyInstaller
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return False

def build_executable():
    """Constrói o executável"""
    print("Construindo executável...")
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console (GUI)
        "--name=ProjectLauncher",  # Nome do executável
        "--add-data=config.json;.",  # Incluir arquivo de config
        "project_launcher.py"
    ]
    
    # Adicionar ícone se existir
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon=icon.ico")
    
    try:
        print(f"Executando: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("✓ Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao criar executável: {e}")
        print("Tentando método alternativo...")
        return build_executable_alternative()
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return False

def build_executable_alternative():
    """Método alternativo para construir executável"""
    print("Tentando método alternativo...")
    
    try:
        # Comando mais simples
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=ProjectLauncher",
            "project_launcher.py"
        ]
        
        print(f"Executando: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("✓ Executável criado com sucesso (método alternativo)!")
        return True
    except Exception as e:
        print(f"✗ Erro no método alternativo: {e}")
        return False

def cleanup():
    """Limpa arquivos temporários"""
    print("Limpando arquivos temporários...")
    
    # Diretórios e arquivos para remover (NÃO remover dist!)
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
    
    # Verificar se o executável foi criado
    if os.path.exists("dist/ProjectLauncher.exe"):
        print("✓ Executável mantido em: dist/ProjectLauncher.exe")
    else:
        print("⚠️ Executável não encontrado em dist/")

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
