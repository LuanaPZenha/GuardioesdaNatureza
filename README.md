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

## 3. Instalar as bibliotecas

Ainda na pasta do projeto:

```powershell
python -m pip install -r requirements.txt
```

Esse comando instala o Pygame e o NumPy. Espere ele terminar sem mensagem de erro.

## 4. Abrir o jogo

```powershell
python main.py
```

A primeira tela é o título.

- **Jogar** entra no santuário.
- **Controles** lista as teclas.
- **Créditos** mostra o contexto da aventura.
- **Novo jogo** só aparece quando já existe progresso. Apaga cristais, habilidades e regiões restauradas.
- **Sair** fecha o programa.

Na primeira visita ao santuário, Lumi explica os portais, a loja e a cura. O botão **Entendi** fecha esse painel e não o mostra de novo.

## 5. Como jogar

No santuário, aproxime-se de um portal e pressione **E**. O Vale Industrial fica selado até as outras cinco regiões serem restauradas. A loja também abre com **E**, no balcão do santuário.

Dentro da região, Kai começa à esquerda. O chefe espera na arena do fim. Quando Kai passa da trava, a arena fecha e a música muda. A vida do chefe em 0 restaura a região. A vida de Kai em 0 encerra a tentativa: os cristais já guardados continuam no save.

Controles durante a partida:

| Tecla | Ação |
|---|---|
| A D ou setas esquerda e direita | Andar |
| Espaço, W ou seta para cima | Pular. O mesmo botão no ar faz o segundo pulo |
| J | Ataque |
| Seta para baixo + J, no ar | Esporos, depois do pântano |
| Shift | Dash, depois das marés |
| K | Tiro, depois do Coração do Planeta |
| Q | Poção, dentro da região |
| E | Loja, portal ou baú |
| Esc | Pausa |
| Setas ou W S, e Enter | Mover e confirmar nos menus |
| Clique | Apertar o botão sob o cursor |

As habilidades novas só passam a existir depois da primeira vitória da região que as entrega. Setas e Enter também funcionam no título e nos painéis.
