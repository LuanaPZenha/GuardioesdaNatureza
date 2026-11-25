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

## 1. Obter a pasta do projeto

Copie a pasta inteira do projeto para o computador. No estado atual ela se chama `P2` e ainda não tem um link de repositório publicado.

Para jogar a versão em Python, a pasta precisa conter pelo menos:

- `main.py`
- `requirements.txt`
- `gn/`
- `assets/`

`build/`, `dist/` e `GuardioesDaNatureza.spec` são sobras do empacotamento. Não são necessárias para `python main.py`.

## 2. Abrir um terminal na pasta

No Explorador de Arquivos, entre na pasta do projeto. Na barra de endereço, digite `powershell` e pressione Enter.

Confira se o Python responde:

```powershell
python --version
```

O resultado esperado é Python 3.13.x. Se o comando não for encontrado, feche o terminal, reinstale o Python com o PATH marcado e abra o terminal de novo.
