# Project Launcher

Um executável para gerenciar e executar projetos de desenvolvimento com interface gráfica intuitiva.

## Funcionalidades

- 🚀 **Interface Gráfica Simples**: Seleção fácil de projetos e opções
- ⚙️ **Configuração Flexível**: Sistema de configuração JSON para definir projetos e ações
- 🔄 **Navegação Hierárquica**: Suporte a opções aninhadas (opções dentro de opções)
- 🎯 **Execução de Ações**: Executa comandos, abre editores e muito mais
- 📁 **Integração com Cursor/VS Code**: Abre projetos automaticamente no editor
- 🖥️ **Multi-plataforma**: Funciona no Windows, Linux e macOS

## Como Usar

### 1. Configuração

Edite o arquivo `config.json` para definir seus projetos:

```json
{
    "Nome do Projeto": {
        "path": "C:/caminho/para/projeto",
        "options": {
            "Opção 1": {
                "type": "execute",
                "actions": [
                    {
                        "type": "open_cursor",
                        "path": "subpasta"
                    },
                    {
                        "type": "run_command",
                        "command": "npm start",
                        "path": "subpasta"
                    }
                ]
            },
            "Opção 2": {
                "type": "options",
                "options": {
                    "Sub-opção A": {
                        "type": "execute",
                        "actions": [...]
                    }
                }
            }
        }
    }
}
```

### 2. Tipos de Ações

- **`open_cursor`**: Abre pasta no Cursor/VS Code
- **`open_postman`**: Abre o Postman
- **`open_dbeaver`**: Abre o DBeaver
- **`open_terminal`**: Abre terminal no diretório do projeto
- **`run_command`**: Executa comando no terminal Windows
- **`run_wsl`**: Executa comandos no WSL Ubuntu
- **`wait`**: Aguarda X segundos

### 3. Tipos de Opções

- **`execute`**: Executa uma lista de ações
- **`options`**: Mostra sub-opções (navegação hierárquica)

## Build do Executável

### Método 1: Script Automático

```bash
python build.py
```

### Método 2: Manual

```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed --name=ProjectLauncher project_launcher.py
```

## Estrutura de Arquivos

```
project-launcher/
├── project_launcher.py    # Código principal
├── config.json            # Configuração dos projetos
├── build.py              # Script de build
├── requirements.txt      # Dependências
└── README.md            # Este arquivo
```

## Exemplo de Configuração Completa

```json
{
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
            },
            "Redis CLI": {
                "type": "execute",
                "actions": [
                    {"type": "run_wsl", "commands": ["redis-cli"], "path": "node-apis-super"}
                ]
            },
            "API Testing": {
                "type": "execute",
                "actions": [
                    {"type": "open_cursor", "path": "back-api"},
                    {"type": "run_command", "command": "npm run dev", "path": "back-api"},
                    {"type": "open_postman"}
                ]
            },
            "Database Management": {
                "type": "execute",
                "actions": [
                    {"type": "open_dbeaver"}
                ]
            },
            "Terminal Only": {
                "type": "execute",
                "actions": [
                    {"type": "open_terminal", "path": "back-api"}
                ]
            }
        }
    }
}
```

## Requisitos

- Python 3.7+
- Cursor ou VS Code (para abrir projetos)
- Terminal/Command Prompt

## Licença

MIT License
