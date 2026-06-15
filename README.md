# Bombásticos

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2026.1  
**Professor:** [André Fonseca]  
**Turma:** [T02]

## Integrantes do Grupo

* Erick Marques Oliveira Azevedo (20210047901)
* Felipe Augusto de Lima Duarte (20250025417)
* Gilberto Gabriel Constantino de Freitas (20250029621)
* Jeziel Honorato da Silva Soares (20250040511)

## Descrição do Projeto

O projeto do grupo **Bombásticos** é uma recriação do clássico jogo Bomberman desenvolvida em Python com Pygame, com foco na implementação e comparação de algoritmos de busca em Inteligência Artificial. O projeto permite que o jogador enfrente inimigos controlados por agentes inteligentes que utilizam diferentes estratégias de navegação no mapa para perseguir o jogador.

Os inimigos podem ser configurados para usar quatro motores de busca distintos — **BFS** (Busca em Largura), **DFS** (Busca em Profundidade), **Busca Gulosa** e **A\*** — permitindo observar na prática as diferenças de comportamento, eficiência e trajetória de cada algoritmo em um ambiente de jogo dinâmico. As tecnologias utilizadas são Python 3, Pygame (renderização e lógica do jogo) e NumPy.

## Guia de Instalação e Execução

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado em seu sistema.

### 2. Configuração do Ambiente Virtual

É recomendado criar e usar um ambiente virtual para isolar as dependências do projeto:

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux / macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instalação das Dependências

Com o ambiente virtual ativo, atualize as ferramentas de instalação e instale os pacotes necessários:

```bash
pip install --upgrade pip
pip3 install --upgrade setuptools wheel
pip install -r requirements.txt
```

### 4. Como Executar

Execute o comando abaixo na raiz do projeto para iniciar o jogo:

```bash
python main.py
```

Ao iniciar, será exibido um menu onde você poderá configurar:
- **Tamanho do mapa** (9×9, 11×11, 13×13 ou 15×15)
- **Quantidade de jogadores** (1 a 4)
- **Quantidade de inimigos** (1 a 4)
- **Algoritmo de busca dos inimigos** (BFS, DFS, A\* ou Busca Gulosa)

Após a configuração, selecione os personagens e inicie a partida. Pressione **ESC** durante o jogo para voltar ao menu.

## Estrutura dos Arquivos

```
IA-Bomberman/
├── main.py              # Ponto de entrada; loop principal do jogo e da partida
├── menu.py              # Tela de menu e seleção de personagens (Pygame)
├── config.py            # Constantes globais: dimensões do mapa, IDs de entidades, tamanho de sprites
├── motores_busca.py     # Implementações dos algoritmos de busca: BFS, DFS, Busca Gulosa e A*
├── efeitos.py           # Gerenciamento dos efeitos visuais (explosões, fogo)
├── testes.py            # Scripts de teste dos algoritmos e mecânicas
└── requirements.txt     # Dependências do projeto (pygame, numpy)
```

## Algoritmos Implementados

| Algoritmo | Estratégia | Característica |
|---|---|---|
| **BFS** | Busca em Largura | Garante o caminho mais curto em número de passos |
| **DFS** | Busca em Profundidade | Não garante o caminho ótimo; pode explorar caminhos longos |
| **Busca Gulosa** | Heurística (Distância de Manhattan) | Rápida, mas não garante o caminho ótimo |
| **A\*** | Custo real + Heurística | Ótimo e eficiente; combina custo acumulado com estimativa de distância |

## Resultados e Demonstração

> *Adicione aqui prints do jogo em execução mostrando os diferentes comportamentos dos agentes com cada algoritmo.*

## Referências

* [Documentação do Pygame](https://www.pygame.org/docs/)
* [Documentação do NumPy](https://numpy.org/doc/)
* Russell, S. & Norvig, P. — *Artificial Intelligence: A Modern Approach* (algoritmos de busca)