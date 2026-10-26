# Reg10k — versão V2: Casa A: sala, cozinha, quarto e banheiro, com gêmeo digital e espelho

Repositório de versão do ambiente de simulação Reg10k (PCS5039, EPUSP).
Linha de pesquisa: Laboratório de Digital Twin de Arquitetura de Sistemas de Software (EPUSP) e GLIP USP.

O código (motor, hub, plataforma, oráculo, página) fica no **núcleo**, na subpasta `nucleo/`,
fixado numa tag. Esta pasta guarda só o que é da versão:

| Pasta | Conteúdo |
|---|---|
| `ambiente/` | Planta: `casa-a.json` (sala, cozinha, quarto e banheiro; banheiro com T_apagamento de 5 min) |
| `cenarios/` | Roteiros e resultados esperados: 24 cenários gerados por planta (G*, famílias F1–F7) e 5 próprios da Casa A (A01–A05) |
| `alunos/` | Controladores dos alunos (um pacote por grupo) |
| `experimentos/familias.json` | Famílias do protocolo de experimentos e os cenários de cada uma |
| `dados/` | CSV dos experimentos, manifestos e assinaturas de regressão |
| `tools/cenarios_v2dt.py` | Gera os cenários A01–A05; os G* vêm de `python nucleo/reg10k.py gerador --ambiente casa-a --versao v2dt` |
| `docs/` | Plano e entrega da v2dt |
| `site/` | Página gerada |

## Como usar

```
git clone --recurse-submodules <endereço deste repositório>
cd <pasta>
pip install -r nucleo/requirements.txt
python nucleo/reg10k.py catalogo            # catálogo e site/index.html
python nucleo/reg10k.py sim --cenario A01
python nucleo/reg10k.py experimentos --sementes 30
```

Para trocar a versão do núcleo: `cd nucleo && git fetch --tags && git checkout <tag>`, depois
`cd ..`, `git add nucleo` e um commit. Dados de artigo são gerados só com o núcleo numa tag
(o manifesto registra o commit).

Exercício da versão: E13 (parâmetros por cômodo), no roteiro dos alunos do núcleo (`nucleo/docs/roteiro-alunos.md`).

Resultados de simulação, não de medição.

Licenças: código MIT (`LICENSE`); dados e documentos CC BY 4.0 (`LICENSE-dados.md`).
