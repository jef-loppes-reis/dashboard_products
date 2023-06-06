# Dashboard Products

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

![GitHub Org's stars](https://img.shields.io/github/stars/jef-loppes-reis?style=social)

## Índice

* [Dashboard-Products](#Título-e-Imagem-de-capa)
* [Descrição do Projeto](#descrição-do-projeto)
* [Status do Projeto](#status-do-Projeto)
* [Funcionalidades e Demonstração da Aplicação](#funcionalidades-e-demonstração-da-aplicação)
* [Acesso ao Projeto](#acesso-ao-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Pessoas Desenvolvedoras do Projeto](#pessoas-desenvolvedoras)

## Descrição do projeto
O Dashboard products tem o principal objetivo em mostrar as situacoes de todos os produtos de um Dataset, apresentando as situacoes de estoque atual, pedidos de compras, fotos e outros fatores.

```mermaid
graph LR;

A[Consulta Banco de Dados]-->B[(Banco de Dados)]

B-->C[DataSet Compra]
B-->D[DataSet Nota de Compra]
B-->E[DataSet DataChegou]
B-->F[DataSet Produtos]
B-->G[DataSet MercadoLivre]

C-->H[Merge e Tratamento de Dados]
D-->H[Merge e Tratamento de Dados]
E-->H[Merge e Tratamento de Dados]
F-->H[Merge e Tratamento de Dados]
G-->H[Merge e Tratamento de Dados]

H-->I[DataFrame final Dashboard]

```

![Exemplo do Projeto](./docs/Ex_Projeto.JPG)

## :hammer: Funcionalidades do projeto

- `Funcionalidade 1`: QTD de SKUs distintos com pedido de compra ou em estoque no grupo.
- `Funcionalidade 2`: QTD SKUs com pedido de compra ou em estoque no grupo, que tem fotos Vs. que não tem fotos.
- `Funcionalidade 3`: QTD SKUs com pedido de compra ou em estoque no grupo que tem fotos, e estão cadastrados Vs. que não estão cadastrados.
- `Funcionalidade 4`: Tabela com SKUs em estoque ou com pedido de compra, que não tem fotos, acompanhado de sua marca.
- `Funcionalidade 5`: Tabela com SKUs em estoque ou com pedido de compra, que tem fotos e não estão cadastrados.

## 📁 Acesso ao projeto
Você pode acessar os arquivos do projeto clicando [aqui](https://github.com/E-commerce-Pecista/sales_operations).

## ✔️ Técnicas e tecnologias utilizadas

- ``Python 3.11.3``
- ``Pandas 2.0.2``

## Autores

| [<img src="https://avatars.githubusercontent.com/u/88293401?v=4" width=115><br><sub>Jeferson Lopes Reis</sub>](https://github.com/jef-loppes-reis) | [<img src="https://avatars.githubusercontent.com/u/62766923?v=4" width=115><br><sub>Lucas Pereira Pires</sub>](https://github.com/l-pires) |
| :---: | :---: |
