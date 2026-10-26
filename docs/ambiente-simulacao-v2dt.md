# Ambiente de simulação Reg10k — v2dt: Casa A (4 cômodos)

**Versão do documento:** v02 | **Data:** 26/10/2026 | **Situação:** entregue (publicação da V2 pendente de acesso ao repositório, §12)
**Responsável:** Reginaldo Arakaki (EPUSP)
**Disciplina:** PCS5039 — Engenharia de Software Orientada a IoT (EPUSP)
**Linha de pesquisa:** Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP
**Base:** núcleo `nucleo-v1.0`; V1 (`v1dtb`); plano das versões paralelas v03 (Fase 2c); guia de convenções v04; V1 Business Drivers v02 (H04); V2/V3 v05

| Versão | Data | Mudança |
|---|---|---|
| v01 | 26/10/2026 | Plano para aprovação, com a rodada de dúvidas (§10) |
| v02 | 26/10/2026 | Entregue: as propostas da §10 valeram; resultados na §11 e ajustes (◆) na §12 |

---

## 1. Objetivo

Levar a automação a uma casa de 4 cômodos (Casa A) e, ao mesmo tempo, tornar as versões **comparáveis** para os artigos. Duas entregas, em dois repositórios:

| Entrega | Onde | O que é |
|---|---|---|
| `nucleo-v1.1` | Núcleo | Gerador de cenários por planta (famílias F1–F7 com os mesmos episódios em qualquer planta) e asserções com janela **relativa a um evento** |
| `v2dt` | Repositório `PCS5039_ambiente_reg10k_V2` (novo) | Planta da Casa A, cenários gerados e cenários próprios, parâmetros por cômodo, dados da primeira rodada |

Conceito novo para o aluno: **escala e parâmetros por cômodo**, como previa a trilha (plano do ambiente v02, §2.1, incremento 4). Uma variável por vez (P1): muda só o porte da casa. Os moradores continuam o morador e o Rex; a diversidade de moradores entra na v1dt.1 e na V4.

## 2. A Casa A

Proposta (DQ2-01): a Casa A **estende a planta da V1**. A sala e a cozinha continuam iguais e ganham um quarto e um banheiro. Assim, o que mudar de V1 para V2 vem dos dois cômodos novos, e não de outra geometria.

```
 y=7,5 ┌──────────────── 5,0 ───────────────┬──────── 3,5 ────────┐
       │ Quarto (5 × 3,5)                   │ Banheiro (3,5 × 3,5)│
       │                          PORTA-03  │                     │
       │                          (SA-04)   ▌                     │
 y=4,0 ├────▌PORTA-02 (SA-03)▐──────────────┼─────────────────────┤
       │ Sala (5 × 4)                VAO-01 │ Cozinha (3,5 × 4)   │
       │                             (SA-02)▌                     │
       │                                    │                     │
 y=0   └──▌PORTA-01 (SA-01)▐────────────────┴─────────────────────┘
        x=0                                x=5                  x=8,5
```

| Item | Proposta |
|---|---|
| Cômodos | Sala, cozinha (como na V1), quarto, banheiro |
| Passagens | PORTA-01 (externa, sala), VAO-01 (sala ↔ cozinha), PORTA-02 (sala ↔ quarto, parede horizontal), PORTA-03 (quarto ↔ banheiro, a suíte) |
| Dispositivos | Um SP, um atuador, uma lâmpada e um interruptor por cômodo; um SA por passagem (H04 da V1) |
| Ocupantes | Morador e Rex |
| Parâmetros por cômodo | Banheiro com `t_apagamento` de 5 min (pessoa parada no banho; o PIR não a vê). Os outros cômodos ficam com 60 s |

## 3. Núcleo `nucleo-v1.1`

### 3.1 Janela relativa a um evento

Hoje, uma asserção diz, por exemplo, "cozinha acesa entre 40 e 44 s". Essas janelas absolutas valem só para a semente 42: na rodada de 30 sementes, o M01 falhou na semente 25, porque o morador cruzou o vão aos 44,1 s (plano das versões paralelas, §11.3).

A asserção passa a poder ancorar a janela num evento da verdade:

```json
{"tipo": "luz", "comodo": "cozinha", "valor": "ACESA",
 "apos": {"evento": "CRUZOU_PASSAGEM", "para": "cozinha", "ocorrencia": 1}, "ate_ms": 1000}
```

Leitura: "a cozinha acende até 1 s depois do primeiro cruzamento para a cozinha". O schema `esperado` ganha o campo `apos`, e as asserções com janela absoluta continuam valendo. Os esperados das versões entregues não mudam (regra da skill).

### 3.2 Gerador de cenários por planta

`experimentos/gerador.py` recebe a planta e gera, para cada família, roteiro e esperado com o mesmo episódio em qualquer casa:

| Família | Episódio gerado | Um por |
|---|---|---|
| F1 | Entra pela porta externa, percorre a casa pelo caminho mais curto até cada cômodo, volta e sai | Cômodo |
| F2 | Fica parado 5 min num cômodo | Cômodo |
| F3 | Espia um cômodo por uma passagem interna, sem entrar | Passagem interna |
| F4 | O SP de um cômodo para de responder com o morador dentro | Cômodo |
| F5 | Desconexão de 10 min com circulação entre dois cômodos | Casa |
| F6 | Comando remoto que acende um cômodo vazio | Cômodo |
| F7 | O Rex vai a um cômodo e deita (espelho e erro de percepção) | Cômodo |

Os IDs seguem o guia: prefixo `G`, família e cômodo (`G1-quarto`, `G3-PORTA-02`…). As asserções geradas são todas relativas (§3.1).

### 3.3 Página com 4 cômodos

O núcleo já desenha a planta de 4 cômodos (teste de N cômodos da `nucleo-v1.0`). Falta só compactar a coluna "o que acontece / hub / plataforma", que com 4 cômodos fica longa: uma linha por cômodo, com abas.

## 4. Cenários da V2

| Grupo | Cenários | Origem |
|---|---|---|
| Gerados (F1–F7) | Cerca de 25 (4 cômodos, 3 passagens internas) | Gerador por planta |
| Próprios da Casa A | A01 banho parado (o `t_apagamento` do banheiro evita o escuro); A02 suíte à noite (quarto → banheiro → quarto); A03 travessia longa (rua → sala → quarto → banheiro); A04 dois cômodos acesos e só um ocupado; A05 desconexão com a casa toda ocupada | Escritos à mão, com asserções relativas |

Cada cenário cita RF, CF ou CV (RF-OPR-01, RNF-DES-03, CF05, CF06…), como nas versões anteriores.

## 5. Regras

| ID | Regra | Base |
|---|---|---|
| RN-V2-01 | Cada cômodo tem os seus parâmetros; o `t_apagamento` pode diferir por cômodo dentro dos limites da plataforma (30 s a 30 min) | RF-OPR-01; PS05 (A13); RN-V1-02 |
| RN-V2-02 | Passagem interna entre dois cômodos em qualquer parede segue a RN-V1-01 (o SA vai aos dois cômodos) | RN-V1-01; A14 |

As invariantes não mudam: OR-01 a OR-14 já valem para N cômodos e foram verificadas com 4 cômodos na `nucleo-v1.0`.

## 6. Regressão

| O quê | Garantia |
|---|---|
| Conjunto de regressão do núcleo (46 cenários) | Assinaturas iguais às da `nucleo-v1.0` (92) |
| V0 e V1 | Não mudam: continuam na `nucleo-v1.0` até decidirem subir |
| Esperados existentes | Intocados; a janela relativa é um campo novo e opcional |

## 7. Dentro × fora

| Dentro (v2dt) | Fora | Entra em |
|---|---|---|
| Casa A, parâmetros por cômodo, gerador, janela relativa, dados com 30 sementes | Mais pessoas, visitante, ocupante dormindo (PI-01) | v1dt.1 (V1) e depois V2 |
| | Casa B (7 cômodos), aprendizado do gêmeo | v3dt (V3) |
| | Várias residências na plataforma | V4.0 |
| | Cenários gerados na V0 e na V1 | Ajustes v0dtb e v1dtc (DQ2-05) |

## 8. Diferenças didáticas

- O aluno vê a mesma lógica de controle em 4 cômodos e descobre que um parâmetro único não serve à casa toda: a pessoa parada no banheiro fica no escuro com 60 s (A01).
- **E13 (novo).** Ajustar os parâmetros por cômodo da Casa A e justificar cada valor com os dados das famílias F1 e F2 (desperdício × escuro), usando o CSV dos experimentos. Pesos sugeridos, como nas versões anteriores (uma tabela por versão): análise dos dados 40%, ajuste e nova medição 40%, discussão 20%.

## 9. Critérios de pronto

| ID | Critério |
|---|---|
| CP-V2-01 | Testes do núcleo verdes em 3.12 e 3.9; 92 assinaturas iguais às da `nucleo-v1.0` |
| CP-V2-02 | Gerador: as mesmas famílias geradas para a sala (V0), a residência (V1) e a Casa A (V2) passam nas invariantes com a referência |
| CP-V2-03 | Janela relativa: o M01 escrito com janela relativa passa nas 30 sementes |
| CP-V2-04 | V2: catálogo com 30 sementes sem problemas, página sem erros, assinaturas gravadas, rodada de experimentos com manifesto |

## 10. Rodada de dúvidas

| ID | Pergunta | Opções | Proposta |
|---|---|---|---|
| **DQ2-01** (bloqueante) | Planta da Casa A | (a) V1 + quarto + banheiro, em suíte; (b) casa nova com corredor (5º espaço); (c) outra planta sua | **(a)**: preserva a sala e a cozinha da V1 e isola o efeito dos cômodos novos |
| **DQ2-02** (bloqueante) | Nome do repositório | `PCS5039_ambiente_reg10k_V2` | Esse; você o cria vazio, como a V0 e a V1 |
| DQ2-03 | `t_apagamento` do banheiro | 60 s, 5 min, 15 min | 5 min: o A01 mostra o escuro com 60 s e o desperdício com 15 min |
| DQ2-04 | Ordem dentro da Fase 2 | V2 antes de v1dt.1 e V4.0, ou o contrário | V2 primeiro: o gerador e a janela relativa servem a todas as versões |
| DQ2-05 | Cenários gerados na V0 e na V1 | Agora, com a V2; ou depois, em ajustes próprios | Depois (v0dtb, v1dtc), para mexer numa versão por vez |
| DQ2-06 | Exercício E13 | Obrigatório, com tabela de pesos própria; opcional | Obrigatório: análise 40%, ajuste e medição 40%, discussão 20% |

Sem objeção, as propostas valem.

**Duração de referência:** núcleo `nucleo-v1.1`, 1 dia; v2dt, 1 a 2 dias.

## 11. Resultados

### 11.1 Critérios de pronto

| ID | Resultado |
|---|---|
| CP-V2-01 | ✔ 251 testes em 3.12 e 3.9; 92 assinaturas iguais às da `nucleo-v1.0` |
| CP-V2-02 | ✔ Famílias geradas para a sala (6 cenários), a residência da V1 (12) e uma casa de 4 cômodos (24): a referência passa em todas as asserções e invariantes, nas sementes 1 a 15 e 42 |
| CP-V2-03 | ✔ O M01 com janela relativa passa nas 30 sementes; com a janela absoluta, continua falhando na semente 25 (teste no núcleo) |
| CP-V2-04 | ✔ V2: 29 cenários, 58 execuções; catálogo com 30 sementes sem problemas; página sem erros no navegador; 58 assinaturas gravadas; 1.740 execuções de experimentos com manifesto |

### 11.2 Primeira rodada de dados da Casa A

30 sementes, referência e `grupo_exemplo`, núcleo no commit da `nucleo-v1.1`. Simulação, não medição.

| Família | Medida (média) | Referência | grupo_exemplo |
|---|---|---|---|
| F1 | Requisitos atendidos | 100% | 34,7% |
| F1 | Atraso percebido máx. (ms) | 400 | 1.271 |
| F2 | Escuro com ocupante (s) | 162 | 164 |
| F3 | Desperdício (s) | 168 | 79 |
| F7 | Espelho fiel (%) | 66,1 | 66,0 |

- **Achado da v1dt ampliado.** O `grupo_exemplo` espera o PIR confirmar antes de acender. Com três passagens internas, isso o faz reprovar a maioria dos percursos (34,7% na F1, contra 100% da referência), mas reduz o falso positivo à metade (F3). O E12 continua sendo o exercício certo, agora numa casa onde o custo de cada estratégia é maior.
- **Parâmetro por cômodo.** O banheiro com 5 min mantém a luz no banho parado (A01, sem escuro), e o quarto com 60 s apaga com o morador deitado (A02: 247 s de escuro). É a matéria do E13.
- **Comparação entre versões:** só vale entre famílias com cenários equivalentes. Os G* existem por enquanto só na V2; a V0 e a V1 os recebem nos ajustes v0dtb e v1dtc (DQ2-05). Até lá, os números da V2 não devem ser comparados com os da V0 e da V1.

## 12. Ajustes feitos na construção (◆)

| Item | Motivo |
|---|---|
| ◆ Correção no oráculo: o desperdício por saída termina quando alguém volta ao cômodo antes do apagamento | O gerador revelou o defeito: no G01-cozinha, sair da sala e voltar antes do apagamento contava como uma saída de 122,8 s, quando a espera real foi de 61,5 s. No conjunto de regressão, só o M10 muda (125,7 → 66,1 s), e nenhuma asserção muda de resultado. A V0 e a V1 continuam na `nucleo-v1.0` com a métrica antiga até subirem de núcleo |
| ◆ Padrão dos IDs de regra generalizado (`RN-V<n>-nn`) | O schema só aceitava RN-I0, RN-DT e RN-V1 |
| ◆ A05: caminhadas estendidas até o fim do cenário | Na primeira versão, a caminhada acabava aos 524 s e as luzes apagavam com os dois parados, um artefato do roteiro, não do controlador |
| ◆ Coluna de estados como tabela, com seletor de cômodo para o detalhe | Com 4 cômodos, três cartões empilhados ficavam longos demais |
| ◆ Publicação da V2 pendente | O repositório `PCS5039_ambiente_reg10k_V2` não está acessível a esta sessão; a V2 está pronta localmente, com dois commits, e sobe assim que o acesso existir |
