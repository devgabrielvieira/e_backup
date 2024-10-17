# e-Backup | Versão 3.0.0

O **e-Backup** é uma aplicação em Python desenvolvida para realizar backup automático e monitoramento de arquivos em tempo real, utilizando o Watchdog para detectar modificações em arquivos e pastas. A aplicação também fornece uma interface gráfica construída com Tkinter e ttkbootstrap.

## Funcionalidades

- Backup automático de arquivos modificados ou criados.
- Monitoramento contínuo de uma pasta selecionada pelo usuário.
- Interface gráfica simples e intuitiva.
- Backup completo ao iniciar o sistema.
- Estrutura de backup organizada por ano, mês e dia.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação.
- **Tkinter**: Interface gráfica para a aplicação.
- **ttkbootstrap**: Biblioteca para estilização de widgets do Tkinter.
- **Watchdog**: Biblioteca para monitoramento de arquivos em tempo real.
- **Shutil**: Biblioteca para operações de cópia e remoção de arquivos.
- **JSON**: Armazenamento de configurações.

## Requisitos

- Python 3.x
- Bibliotecas Python: 
  - `ttkbootstrap`
  - `watchdog`

## Instalação

1. Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/seu-usuario/e-backup.git
cd e-backup

2. Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

3. Instale as dependências necessárias:

pip install -r requirements.txt

## Execução

Após a instalação das dependências, você pode executar o programa com o seguinte comando:

python e-backup.py

A interface gráfica será exibida, permitindo que você selecione a pasta para backup e monitoramento.

## Configurações

O e-Backup salva automaticamente as configurações da pasta selecionada para backup e o diretório de destino. Essas configurações são armazenadas no arquivo config.txt no diretório raiz do projeto. Quando a aplicação é iniciada novamente, ela carrega essas configurações e continua o backup e monitoramento da pasta previamente selecionada.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias, correções de bugs ou novas funcionalidades.

## Licença

Este projeto é licenciado sob a MIT License.
