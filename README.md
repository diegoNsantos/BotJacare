# 🤖 Bot de Ponto para Discord

## 📌 Sobre o projeto

Este projeto consiste em um bot desenvolvido em Python para o Discord, com o objetivo de facilitar o controle de ponto e o acompanhamento das horas trabalhadas diretamente em um servidor.

A proposta é permitir que os usuários registrem seus horários de entrada e saída de forma simples, além de consultar o status do ponto e acompanhar um relatório mensal de horas trabalhadas.

O projeto foi desenvolvido com foco na automação de tarefas, organização de registros e aprendizado de programação.

## 🎯 Objetivo

O principal objetivo é criar uma ferramenta prática para o controle de jornada, reduzindo a necessidade de registros manuais e facilitando a consulta das informações.

Com o bot, é possível:

- Registrar o horário de entrada.
- Registrar o horário de saída.
- Calcular o tempo trabalhado em cada período.
- Consultar se existe um ponto em aberto.
- Visualizar o total de horas trabalhadas durante o mês.

## ⚙️ Funcionalidades

| Comando | Descrição |
|---|---|
| `/entrar` | Registra o horário de entrada. |
| `/sair` | Registra a saída e informa o tempo trabalhado. |
| `/status` | Consulta se o usuário possui um ponto em aberto. |
| `/relatorio` | Apresenta o total de horas trabalhadas no mês, permitindo consultar os registros próprios ou de outro membro. |

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem utilizada para desenvolver a lógica do bot.
- **discord.py:** biblioteca responsável pela integração com a API do Discord.
- **SQLite:** banco de dados utilizado para armazenar informações de forma persistente.
- **Git e GitHub:** ferramentas para versionamento e compartilhamento do código.

## 📂 Como o bot funciona?

O funcionamento do bot pode ser dividido em quatro etapas:

1. **Inicialização:** o bot utiliza o token de autenticação para se conectar ao Discord.
2. **Registro de entrada:** quando o usuário executa `/entrar`, o sistema registra o horário de início da jornada.
3. **Registro de saída:** ao executar `/sair`, o bot registra o horário de término e calcula o tempo decorrido.
4. **Consulta de informações:** os comandos `/status` e `/relatorio` permitem consultar os registros e acompanhar as horas trabalhadas.

Os registros são armazenados em um banco de dados SQLite, permitindo que as informações sejam mantidas entre as execuções do bot.

## 💻 Como executar o projeto

### 1. Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.10 ou superior.
- Uma conta no Discord.
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Clone o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd NOME_DO_PROJETO
```

### 3. Instale as dependências

```bash
pip install discord.py
```

### 4. Configure o token

Crie um token para o seu bot no Discord Developer Portal e configure a variável de ambiente `DISCORD_TOKEN`.

No Windows PowerShell, você pode fazer isso temporariamente para a sessão atual:

```powershell
$env:DISCORD_TOKEN="SEU_TOKEN_AQUI"
```

**Importante:** nunca compartilhe seu token ou publique esse segredo no GitHub. Caso ele seja exposto, regenere-o no portal do Discord.

### 5. Execute o bot

Com as configurações realizadas, execute o arquivo principal do projeto:

```bash
python main.py
```

Substitua `main.py` pelo nome do arquivo principal, caso seja diferente.

## 📚 Aprendizados

O desenvolvimento deste projeto permite praticar conceitos importantes de programação, como:

- Programação em Python.
- Integração com APIs.
- Criação e gerenciamento de comandos.
- Manipulação de datas e horários.
- Operações com banco de dados SQLite.
- Tratamento de registros e cálculos de tempo.
- Configuração de variáveis de ambiente.
- Versionamento de código com Git e GitHub.

## 🚀 Melhorias futuras

Algumas funcionalidades que podem ser implementadas futuramente:

- Exportação de relatórios em CSV ou Excel.
- Resumo semanal das horas trabalhadas.
- Sistema de permissões para administradores.
- Histórico detalhado dos registros.
- Interface visual para consulta dos relatórios.

## 👨‍💻 Autor

Desenvolvido como projeto de estudo e prática em desenvolvimento de software, com foco em Python, automação e integração com o Discord.
