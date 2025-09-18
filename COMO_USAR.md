# 🚀 Project Launcher - Como Usar

## ❌ Problema: Python não encontrado

Se você recebeu o erro "Python não foi encontrado", você tem 3 opções:

---

## 🎯 **OPÇÃO 1: Usar Versão Standalone (Mais Fácil)**

**Não precisa instalar Python!**

1. **Execute o launcher.bat**:
   ```
   launcher.bat
   ```

2. **Configure seus projetos** (primeira vez):
   ```
   configurar_projetos.bat
   ```

3. **Pronto!** Use o launcher.bat sempre que quiser.

---

## 🐍 **OPÇÃO 2: Instalar Python (Recomendado)**

**Para usar a versão completa com interface gráfica:**

1. **Instalação manual**:
   - Acesse: https://www.python.org/downloads/
   - Baixe Python 3.11+
   - **IMPORTANTE**: Marque "Add Python to PATH"
   - Instale

2. **Execute**:
   ```
   python project_launcher.py
   ```

3. **Criar executável**:
   ```
   build.bat
   ```
   ou
   ```
   python build_simple.py
   ```

---

## ⚙️ **OPÇÃO 3: Configuração Manual**

**Se preferir configurar tudo manualmente:**

### 1. Instalar Python
- Download: https://www.python.org/downloads/
- Marcar "Add Python to PATH"

### 2. Instalar dependências
```cmd
pip install pyinstaller
```

### 3. Executar
```cmd
python project_launcher.py
```

### 4. Criar executável
```cmd
build.bat
```
ou
```cmd
python build_simple.py
```

---

## 📁 **Estrutura de Arquivos**

```
project-launcher/
├── project_launcher.py       # ← Versão completa (precisa Python)
├── config.json              # ← Configuração dos projetos
├── build.py                 # ← Script para criar executável (original)
├── build_simple.py          # ← Script simples para criar executável
├── build.bat                # ← Script batch para Windows
└── README.md                # ← Documentação completa
```

---

## 🎮 **Como Funciona**

### Versão Completa (project_launcher.py)
- Interface gráfica bonita
- Configuração via config.json
- Mais opções e funcionalidades
- **Vantagem**: Mais fácil de usar

---

## 🔧 **Configuração de Projetos**

### Para project_launcher.py:
1. Edite o arquivo `config.json`
2. Configure os caminhos e comandos
3. Execute `python project_launcher.py`

---

## ❓ **Problemas Comuns**

### "Python não foi encontrado"
- Instale Python: https://www.python.org/downloads/
- Marque "Add Python to PATH" durante instalação

### "Caminho não encontrado"
- Edite o arquivo `config.json`
- Configure os caminhos corretos

### "Comando não reconhecido"
- Verifique se npm/node estão instalados
- Verifique se pip está instalado

---

## 🎯 **Recomendação**

**Para uso profissional**: Instale Python e use `project_launcher.py`

---

## 📞 **Suporte**

Se tiver problemas:
1. Verifique se os caminhos estão corretos
2. Teste os comandos manualmente no terminal
3. Verifique se as ferramentas (npm, pip) estão instaladas
