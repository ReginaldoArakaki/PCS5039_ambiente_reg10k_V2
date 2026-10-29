# Ambiente de simulação Reg10k — ajuste v2dta

**Versão do documento:** v02 | **Data:** 29/10/2026 | **Situação:** entregue | **Responsável:** Reginaldo Arakaki (EPUSP)
**Linha de pesquisa:** Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP

Ajuste pequeno (guia de convenções, §6): o pedido do responsável vale como aprovação, e o plano sai direto em v02.

## 1. Motivo

Deixar a V0, a V1 e a V2 no **mesmo núcleo (`nucleo-v1.2`)** e com as **mesmas famílias de cenários gerados por planta (G*)**. Só assim os dados das três casas podem ser comparados nos artigos (plano das versões paralelas, §14).

## 2. O que muda

| Item | Antes | Depois |
|---|---|---|
| Núcleo | nucleo-v1.1 | nucleo-v1.2 |
| Cenários gerados por planta | 24 G* | nenhum cenário novo (os 24 G* já existiam) |
| Dados | Rodada de 26/10/2026 | Nova rodada de 29/10/2026 (30 sementes, referência e grupo_exemplo); a rodada anterior fica como registro |

## 3. Regressão

As 58 assinaturas anteriores (decisões e atuações dos cenários que já existiam) são **iguais** com o núcleo novo. Validação dos JSON e catálogo com 30 sementes sem problemas.
