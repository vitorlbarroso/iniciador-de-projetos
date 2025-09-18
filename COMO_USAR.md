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

1. **Instalação automática**:
   ```
   instalar_python.bat
   ```

2. **Ou instalação manual**:
   - Acesse: https://www.python.org/downloads/
   - Baixe Python 3.11+
   - **IMPORTANTE**: Marque "Add Python to PATH"
   - Instale

3. **Execute**:
   ```
   python project_launcher.py
   ```

4. **Criar executável**:
   ```
   python build.py
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
python build.py
```

---

## 📁 **Estrutura de Arquivos**

```
project-launcher/
├── launcher.bat              # ← Versão standalone (sem Python)
├── configurar_projetos.bat   # ← Configurador de caminhos
├── instalar_python.bat       # ← Instalador automático do Python
├── project_launcher.py       # ← Versão completa (precisa Python)
├── config.json              # ← Configuração dos projetos
├── build.py                 # ← Script para criar executável
└── README.md                # ← Documentação completa
```

---

## 🎮 **Como Funciona**

### Versão Standalone (launcher.bat)
- Menu de texto no terminal
- Configuração via configurar_projetos.bat
- Abre projetos e executa comandos
- **Vantagem**: Não precisa instalar nada

### Versão Completa (project_launcher.py)
- Interface gráfica bonita
- Configuração via config.json
- Mais opções e funcionalidades
- **Vantagem**: Mais fácil de usar

---

## 🔧 **Configuração de Projetos**

### Para launcher.bat:
1. Execute `configurar_projetos.bat`
2. Digite os caminhos dos seus projetos
3. Pronto!

### Para project_launcher.py:
1. Edite o arquivo `config.json`
2. Configure os caminhos e comandos
3. Execute `python project_launcher.py`

---

## ❓ **Problemas Comuns**

### "Python não foi encontrado"
- Use `launcher.bat` (versão standalone)
- Ou instale Python com `instalar_python.bat`

### "Caminho não encontrado"
- Execute `configurar_projetos.bat`
- Configure os caminhos corretos

### "Comando não reconhecido"
- Verifique se npm/node estão instalados
- Verifique se pip está instalado

---

## 🎯 **Recomendação**

**Para começar rapidamente**: Use `launcher.bat`

**Para uso profissional**: Instale Python e use `project_launcher.py`

---

## 📞 **Suporte**

Se tiver problemas:
1. Verifique se os caminhos estão corretos
2. Teste os comandos manualmente no terminal
3. Verifique se as ferramentas (npm, pip) estão instaladas
