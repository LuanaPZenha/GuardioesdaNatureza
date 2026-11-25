# Guardiões da Natureza

Plataforma 2D de um jogador. Kai atravessa seis regiões danificadas, derrota o chefe de cada uma e restaura o santuário. O Vale Industrial só abre depois das outras cinco vitórias.

Este arquivo é o passo a passo da seção 12 do GDD. Ele parte de um Windows sem o projeto instalado.

## O que a máquina precisa

- Windows 10 ou 11.
- Python 3.13, com a opção **Add python.exe to PATH** marcada na instalação.
- Rede, só na instalação das bibliotecas. O jogo em si não usa internet.
- Teclado. O mouse serve para os botões dos menus.

Não é preciso placa de vídeo dedicada. A janela do jogo é 960×540 e o alvo é 60 quadros por segundo.

Bibliotecas, instaladas pelo passo 3:

- `pygame` 2.5 ou mais recente. A versão testada foi a 2.6.1.
- `numpy` 2.0 ou mais recente. Entra no recorte das imagens e na música.
