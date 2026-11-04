*# 🐍 Python Reverse Shell — Estudos de Cibersegurança

Projeto desenvolvido em Python com o objetivo de estudar conceitos de comunicação via sockets TCP, arquitetura cliente-servidor e funcionamento de conexões reversas (*Reverse Shell*).

## 🎯 Objetivo

Compreender como funciona uma conexão reversa, na qual uma aplicação cliente inicia uma conexão com um servidor, permitindo estudar conceitos importantes de redes e segurança da informação.

## 🛠️ Tecnologias utilizadas

- **Python**
- `socket` — Comunicação através de sockets TCP.
- `subprocess` — Estudo da execução de processos no sistema operacional.
- `os` — Manipulação de diretórios.
- `time` — Controle de intervalos de execução.
- `PyInstaller` — Empacotamento de aplicações Python em executáveis.
- `python-dotenv` — Gerenciamento de variáveis de ambiente.

## ⚙️ Conceitos estudados

- Comunicação TCP/IP.
- Arquitetura cliente-servidor.
- Reverse Shell.
- Comunicação entre processos.
- Execução de comandos no sistema operacional.
- Tratamento de exceções.
- Variáveis de ambiente.
- Criação de executáveis com PyInstaller.

## 📡 Funcionamento

O projeto explora o conceito de conexão reversa:

1. O cliente inicia uma conexão TCP com um servidor previamente configurado.
2. O servidor recebe a conexão.
3. O cliente permanece aguardando mensagens.
4. O encerramento da conexão é controlado por uma mensagem específica.

O código também explora a utilização de processos externos e a manipulação de diretórios.

## 📦 Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Instale as dependências:

```bash
pip install pyinstaller
```

## 🔧 Configuração

As configurações de rede do projeto estão definidas diretamente no código-fonte.

Para manter o ambiente de laboratório organizado, utilize configurações específicas da sua máquina de testes e evite publicar informações privadas no GitHub.

## 🏗️ Geração do executável

Após finalizar as configurações e revisar o código, utilize o PyInstaller:

```bash
pyinstaller -F --clean -w trojan.py
```

O arquivo executável será gerado no diretório:

```text
dist/
```

**Observação:** sempre que houver alterações no código-fonte, será necessário gerar novamente o executável para incorporar as mudanças.

## 📚 Aprendizados

Este projeto foi desenvolvido para aprofundar meus conhecimentos em Python, comunicação de rede e fundamentos de cibersegurança, explorando na prática conceitos relacionados a conexões TCP, arquitetura cliente-servidor e execução de processos.

## ⚠️ Aviso de segurança

Este projeto possui finalidade exclusivamente educacional, sendo destinado ao estudo de redes de computadores e segurança da informação.

Técnicas de Reverse Shell podem ser utilizadas em ataques cibernéticos. Qualquer experimentação deve ocorrer exclusivamente em ambientes isolados, em máquinas próprias ou com autorização explícita.

**Não utilize este projeto em sistemas de terceiros sem autorização.****
