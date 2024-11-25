\
\
![Universidade de Vassouras](img/Universidade_Vassouras_Logo.png)

# Cálculo de Temperatura de uma Sala

## Descrição

Este programa foi desenvolvido pelos alunos **Caio Cezar Jotta Nogueira (202212094)**, **Daniel Monteiro de Carvalho (202212193)**, **Davi Costa Antunes Narcizo (202211007)**, **Gabriel Victor Martins Carvalho (202212175)** e **Yago da Costa Jardim Alves Braga (2022110004)** como parte do trabalho acadêmico da disciplina de **Fenômenos de Transporte**, ministrada pela professora **Ana Carolina Cellular Massone** no curso de **Engenharia de Software** da **Universidade de Vassouras**.

O programa tem como objetivo calcular a temperatura interna de uma sala com base em diversos fatores, incluindo:

- Dimensões da sala.
- Materiais utilizados nas paredes, janelas e portas.
- Fontes térmicas (e.g., pessoas, ar-condicionado, lâmpadas, computadores).
- Temperatura externa.

Além disso, o programa apresenta uma visualização 3D da sala para ilustrar a distribuição espacial.

---

## Funcionalidades

- **Cadastro de materiais**: Inclui materiais com suas respectivas condutividades térmicas.
- **Configuração de aberturas**: Define janelas e portas, incluindo material e dimensões.
- **Fontes térmicas**: Considera diversas fontes de calor e resfriamento, como ar-condicionado, lâmpadas e pessoas.
- **Simulação de temperatura**: Calcula a temperatura interna estimada com base na condutividade térmica, área da sala e fontes de calor ou resfriamento.
- **Visualização 3D**: Gera uma visualização tridimensional da sala configurada.

---

## Como Executar

### Pré-requisitos

- Python 3.9 ou superior.
- Bibliotecas listadas no arquivo `requirements.txt`.

### Instalação

1. Clone o repositório ou baixe os arquivos.
2. Instale as dependências executando:

```bash
pip install -r requirements.txt
```

### Uso

1. Execute o programa:

```bash
python sala.py
```

2. Siga as instruções no terminal para configurar a sala e obter a simulação.

---

## Estrutura do Código

- **`sala.py`**: Contém o código principal com a lógica para cálculo térmico e visualização.
- **`requirements.txt`**: Lista de dependências do projeto.

---

## Exemplo de Saída

- **Temperatura interna estimada**: A simulação retorna a temperatura esperada com base nos dados fornecidos.
- **Visualização 3D**: Uma renderização da sala é exibida usando o `matplotlib`.

---