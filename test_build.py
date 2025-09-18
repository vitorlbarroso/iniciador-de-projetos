#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se o build funcionou
"""

import os
import sys

def test_build():
    print("=== Teste do Build ===\n")
    
    # Verificar se o executável foi movido para a raiz
    import glob
    exe_files = glob.glob("Iniciador de Projetos - *.exe")
    
    if not exe_files:
        print("✗ Executável não encontrado na raiz!")
        print("  Procurando por: 'Iniciador de Projetos - *.exe'")
        return False
    
    exe_path = exe_files[0]  # Pegar o primeiro arquivo encontrado
    print(f"✓ Executável encontrado: {exe_path}")
    
    # Verificar tamanho do arquivo
    file_size = os.path.getsize(exe_path)
    print(f"✓ Tamanho do arquivo: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    # Verificar se config.json existe na raiz
    if os.path.exists("config.json"):
        print("✓ Configuração encontrada: config.json")
    else:
        print("⚠️ Configuração não encontrada: config.json")
    
    # Verificar se a pasta dist foi removida
    if os.path.exists("dist"):
        print("⚠️ Pasta dist/ ainda existe (deveria ter sido removida)")
    else:
        print("✓ Pasta dist/ foi removida corretamente")
    
    # Listar arquivos executáveis na raiz
    print("\nArquivos executáveis na raiz:")
    try:
        all_files = os.listdir(".")
        exe_files = [f for f in all_files if f.endswith('.exe')]
        for file in exe_files:
            file_path = os.path.join(".", file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"  - {file} ({size:,} bytes)")
    except Exception as e:
        print(f"✗ Erro ao listar arquivos: {e}")
    
    print("\n=== Teste Concluído ===")
    print("✓ Build funcionou corretamente!")
    print("\nPara usar:")
    print(f"1. Execute o arquivo: {exe_path}")
    print("2. Edite config.json conforme necessário")
    
    return True

if __name__ == "__main__":
    success = test_build()
    input("\nPressione Enter para sair...")
    sys.exit(0 if success else 1)
