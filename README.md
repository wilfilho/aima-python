

# `aima-python` [![Build Status](https://travis-ci.org/aimacode/aima-python.svg?branch=master)](https://travis-ci.org/aimacode/aima-python) [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/aimacode/aima-python)


Python code for the book *[Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu).* You can use this in conjunction with a course on AI, or for study on your own. We're looking for [solid contributors](https://github.com/aimacode/aima-python/blob/master/CONTRIBUTING.md) to help.

# Resolução do Problema da Seleção Ótima de Pedidos em Waves

Esta documentação apresenta a resolução do problema em três partes, utilizando o paradigma de CSP e a implementação do código do AIMA (em Python) como base. O código foi desenvolvido para modelar as restrições do problema, buscar soluções viáveis através de backtracking e, por fim, selecionar a solução ótima considerando a média de itens coletados por corredor (com critério de desempate pelo total de unidades).

---

## Parte 1: Modelagem do Problema como CSP

**Definição e Variáveis**  
O problema consiste em selecionar um subconjunto dos pedidos e dos corredores de forma a maximizar a produtividade da coleta no armazém. Para isso, o problema foi modelado como um CSP com as seguintes características:

- **Variáveis:**  
  - Pedidos: `O0`, `O1`, `O2`, `O3`, `O4`
  - Corredores: `A0`, `A1`, `A2`, `A3`, `A4`
  
- **Domínio:** Cada variável pode assumir o valor 0 (não selecionado) ou 1 (selecionado).

**Restrições**  
Foram definidas duas restrições principais:
1. **Total de Unidades:** Se todos os pedidos forem avaliados, o total de unidades (obtido somando as quantidades de cada pedido selecionado) deve estar entre um limite inferior (LB) e um limite superior (UB).
2. **Disponibilidade:** Quando a atribuição estiver completa, para cada item o total solicitado nos pedidos selecionados não pode exceder o total disponível nos corredores selecionados.

**Função Objetivo**  
A produtividade é mensurada pela média de itens coletados por corredor:
- Objetivo = (Total de Unidades dos Pedidos Selecionados) ÷ (Número de Corredores Selecionados)

Em caso de empate na média, a solução com maior total de unidades é considerada melhor.

---

## Parte 2: Implementação da Solução em Python

A implementação foi realizada com base no código do AIMA para CSP, utilizando uma classe que estende o CSP e redefine os métodos relevantes para incorporar as restrições globais do problema. Os pontos principais da implementação são:

- **Dados e Domínios:**  
  Os dados dos pedidos e dos corredores foram definidos conforme o exemplo. Cada variável (pedido ou corredor) tem o domínio {0, 1}.

- **Função de Restrições:**  
  A função verifica, de forma global, se o total de unidades dos pedidos selecionados está dentro dos limites e se a disponibilidade dos corredores atende à demanda para cada item.

- **Backtracking com Enumeração Completa:**  
  Foi implementada uma função de backtracking personalizada que, ao invés de retornar apenas a primeira solução viável (como faz o backtracking_search padrão do AIMA), enumera todas as soluções possíveis. Em seguida, é aplicada a função objetivo (definida como um par com média e total de unidades) para selecionar a solução ótima.

- **Critério de Seleção:**  
  A solução ótima é aquela que maximiza o par (média, total de unidades), garantindo que, entre soluções com a mesma média, seja escolhida a que tem maior total de unidades.

---

## Parte 3: Testes e Validação

**Exemplo e Resultados Esperados**  
Para o exemplo fornecido, os dados são:

- **Pedidos:**  
  - O0: [3, 0, 1, 0, 0]
  - O1: [0, 1, 0, 1, 0]
  - O2: [0, 0, 1, 0, 2]
  - O3: [1, 0, 2, 1, 1]
  - O4: [0, 1, 0, 0, 0]

- **Corredores:**  
  - A0: [2, 1, 1, 0, 1]
  - A1: [2, 1, 2, 0, 1]
  - A2: [0, 2, 0, 1, 2]
  - A3: [2, 1, 0, 1, 1]
  - A4: [0, 1, 2, 1, 2]

Com LB = 5 e UB = 12, a análise do código identifica como solução ótima a seguinte wave:

- **Pedidos Selecionados:** O0, O1, O2 e O4  
  - Total de unidades:  
    - O0: 4 unidades  
    - O1: 2 unidades  
    - O2: 3 unidades  
    - O4: 1 unidade  
    - **Total = 10 unidades**
  
- **Corredores Selecionados:** A1 e A3  
  - Número de corredores: 2

- **Valor Objetivo:**  
  Média = 10 / 2 = 5

**Validação e Desempenho**  
- O código enumera todas as soluções viáveis (o espaço total é pequeno, pois há 10 variáveis com domínio binário, totalizando 2¹⁰ = 1024 combinações).
- A função objetivo, definida como um par (média, total de unidades), garante que a solução ótima seja escolhida mesmo em caso de empate na média.
- Os testes realizados confirmam que a solução encontrada é a esperada, atendendo aos critérios de modelagem, restrição e desempenho.

---

## Conclusão

A solução apresentada modela o problema de seleção ótima de pedidos em waves como um CSP, implementa as restrições e a função objetivo usando a estrutura do AIMA e valida a solução por meio de testes com o exemplo fornecido.  
**Resultados esperados:**  
- Total de unidades dos pedidos selecionados: **10**  
- Número de corredores selecionados: **2**  
- Valor objetivo (média de itens por corredor): **5**

Esta abordagem demonstra a aplicação prática da teoria de CSP para problemas de otimização em ambientes logísticos, e pode ser expandida para cenários com maior complexidade.
