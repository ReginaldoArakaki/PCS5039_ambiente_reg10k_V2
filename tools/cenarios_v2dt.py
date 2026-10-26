"""Cenários próprios da Casa A (v2dt): A01–A05, com asserções de janela relativa.

Uso, na raiz do repositório da V2:  python tools/cenarios_v2dt.py
Os cenários das famílias F1–F7 (G*) vêm do gerador do núcleo:
    python nucleo/reg10k.py gerador --ambiente casa-a --versao v2dt
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRA = {"evento": "CRUZOU_PORTA", "sentido": "ENTRADA"}
SAI = {"evento": "CRUZOU_PORTA", "sentido": "SAIDA"}
INV = {"id": "INV", "nivel": "REQUISITO", "dado": "qualquer controlador", "quando": "o cenário termina",
       "entao": {"tipo": "invariantes"}}
BASE = {"versao": "v2dt", "ambiente": "casa-a", "modo": "IDEAL",
        "estado_inicial": {"ocupantes_na_sala": [], "luz": "APAGADA"}, "falhas": []}


def a(t, quem, acao, **kw):
    return {"t_ms": t, "ocupante": quem, "acao": acao, **kw}


def r(id_, n, dado, quando, entao):
    return {"id": id_, "nivel": n, "dado": dado, "quando": quando, "entao": entao}


CENARIOS = [
    ({**BASE, "id": "A01", "titulo": "Banho parado", "tipo": "FALSO_NEGATIVO", "duracao_ms": 600_000,
      "descricao": "O morador vai ao banheiro (sala → quarto → banheiro) e fica parado no banho por 4 min; depois sai da casa.",
      "comportamento_ideal": "A luz do banheiro fica acesa durante o banho.",
      "comportamento_referencia": "Com T_apagamento de 5 min no banheiro (RN-V2-01), a luz não apaga durante os 4 min parado; com 60 s, apagaria.",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-V2-01", "RN-I0-03"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(10_000, "morador", "MUDAR_COMODO", para="quarto"),
                a(22_000, "morador", "MUDAR_COMODO", para="banheiro"), a(34_000, "morador", "ANDAR", ate=[7.2, 6.4]),
                a(40_000, "morador", "PARADO"), a(280_000, "morador", "ANDAR_ALEATORIO", duracao_ms=20_000),
                a(302_000, "morador", "MUDAR_COMODO", para="quarto"), a(314_000, "morador", "MUDAR_COMODO", para="sala"),
                a(326_000, "morador", "ANDAR", ate=[0.95, 1.0]), a(334_000, "morador", "SAIR")]},
     [r("A1", "REQUISITO", "morador parado no banho", "4 min sem movimento",
        {"tipo": "luz_constante", "comodo": "banheiro", "valor": "ACESA", "apos": ENTRA, "entre_ms": [1_000, 240_000]}),
      r("A2", "REQUISITO", "banheiro com T_apagamento de 5 min", "o morador deixa o banheiro",
        {"tipo": "metrica", "comodo": "banheiro", "nome": "desperdicio_por_saida_s_max", "max": 330}),
      r("A3", "CARACTERIZACAO", "parâmetro por cômodo", "o cenário termina",
        {"tipo": "metrica", "comodo": "banheiro", "nome": "escuro_com_ocupante_s", "max": 1})]),

    ({**BASE, "id": "A02", "titulo": "Suíte: deitado no quarto, ida ao banheiro e volta", "tipo": "FALSO_NEGATIVO",
      "duracao_ms": 480_000,
      "descricao": "O morador deita no quarto, vai ao banheiro por 1 min e volta a deitar.",
      "comportamento_ideal": "O banheiro acende ao entrar; o quarto não apaga com o morador deitado.",
      "comportamento_referencia": "O banheiro acende pelo SA da PORTA-03; o quarto, com 60 s, apaga com o morador deitado (limitação conhecida, como o FN01).",
      "requisitos": ["RF-OPR-01", "CF05"], "regras": ["RN-V2-01", "RN-V2-02", "RN-I0-03"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(10_000, "morador", "MUDAR_COMODO", para="quarto"),
                a(22_000, "morador", "ANDAR", ate=[2.5, 6.6]), a(30_000, "morador", "PARADO"),
                a(150_000, "morador", "MUDAR_COMODO", para="banheiro"),
                a(162_000, "morador", "ANDAR_ALEATORIO", duracao_ms=50_000),
                a(215_000, "morador", "MUDAR_COMODO", para="quarto"), a(227_000, "morador", "ANDAR", ate=[2.5, 6.6]),
                a(235_000, "morador", "PARADO")]},
     [r("A1", "REQUISITO", "banheiro escuro", "o morador entra pela porta da suíte",
        {"tipo": "luz", "comodo": "banheiro", "valor": "ACESA", "apos": ENTRA, "ate_ms": 1_000}),
      r("A2", "REQUISITO", "quarto escuro", "o morador volta do banheiro",
        {"tipo": "luz", "comodo": "quarto", "valor": "ACESA", "apos": {**ENTRA, "ocorrencia": 2}, "ate_ms": 1_000}),
      r("A3", "CARACTERIZACAO", "morador deitado no quarto", "60 s sem movimento",
        {"tipo": "metrica", "comodo": "quarto", "nome": "apagamentos_indevidos", "min": 1})]),

    ({**BASE, "id": "A03", "titulo": "Travessia longa: da rua ao banheiro sem parar", "tipo": "NORMAL",
      "duracao_ms": 600_000,
      "descricao": "O morador entra e vai direto ao banheiro, passando pela sala e pelo quarto; fica 1 min e volta para a rua.",
      "comportamento_ideal": "Cada cômodo acende ao ser atravessado e apaga depois.",
      "comportamento_referencia": "Acende em até 1 s a cada passagem; cada cômodo apaga T_apagamento depois da última evidência.",
      "requisitos": ["RF-OPR-01", "RNF-DES-03"], "regras": ["RN-I0-02", "RN-V2-01", "RN-V2-02"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(9_000, "morador", "MUDAR_COMODO", para="quarto"),
                a(21_000, "morador", "MUDAR_COMODO", para="banheiro"),
                a(33_000, "morador", "ANDAR_ALEATORIO", duracao_ms=60_000),
                a(95_000, "morador", "MUDAR_COMODO", para="quarto"), a(107_000, "morador", "MUDAR_COMODO", para="sala"),
                a(119_000, "morador", "ANDAR", ate=[0.95, 1.0]), a(127_000, "morador", "SAIR")]},
     [r(f"A{i}", "REQUISITO", f"{c} escuro", "o morador entra",
        {"tipo": "luz", "comodo": c, "valor": "ACESA", "apos": ENTRA, "ate_ms": 1_000})
      for i, c in enumerate(["sala", "quarto", "banheiro"], 1)]
     + [r("A4", "REQUISITO", "entrada em cômodo escuro", "a lâmpada acende",
          {"tipo": "metrica", "nome": "atraso_percebido_ms_max", "max": 1_000}),
        r("A5", "REQUISITO", "casa vazia", "5 min e meio depois da saída",
          {"tipo": "luz", "comodo": "banheiro", "valor": "APAGADA", "em_ms": 127_000 + 335_000})]),

    ({**BASE, "id": "A04", "titulo": "Dois cômodos acesos e só um ocupado", "tipo": "FALSO_POSITIVO",
      "duracao_ms": 300_000,
      "descricao": "O morador anda na sala e espia o quarto pela PORTA-02 sem entrar; continua na sala.",
      "comportamento_ideal": "O quarto não acende.",
      "comportamento_referencia": "O SA da PORTA-02 vai aos dois cômodos (RN-V1-01): o quarto acende e apaga T_apagamento depois.",
      "requisitos": ["RN09", "RF-OPR-01"], "regras": ["RN-V1-01", "RN-V2-02"],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(10_000, "morador", "ANDAR", ate=[1.45, 3.6]),
                a(20_000, "morador", "ESPIAR", comodo="quarto"), a(25_000, "morador", "ANDAR_ALEATORIO", duracao_ms=250_000)]},
     [r("A1", "REQUISITO", "morador sempre na sala", "o cenário corre",
        {"tipo": "luz_constante", "comodo": "sala", "valor": "ACESA", "entre_ms": [6_000, 270_000]}),
      r("A2", "REQUISITO", "quarto acendido sem ninguém", "passa T_apagamento",
        {"tipo": "luz", "comodo": "quarto", "valor": "APAGADA", "apos": {"evento": "ESPIOU"}, "em_ms": 75_000}),
      r("A3", "CARACTERIZACAO", "quarto vazio", "o SA da PORTA-02 dispara",
        {"tipo": "metrica", "comodo": "quarto", "nome": "desperdicio_s", "min": 55})]),

    ({**BASE, "id": "A05", "titulo": "Desconexão com a casa ocupada em dois cômodos", "tipo": "GEMEO_DIGITAL",
      "duracao_ms": 600_000,
      "descricao": "O morador fica no quarto e o Rex na cozinha quando o canal cai por 5 min.",
      "comportamento_ideal": "A automação local segue; o gêmeo de cada cômodo se declara desatualizado e reconcilia ao voltar.",
      "comportamento_referencia": "Fila persistente; um estado por cômodo; reconciliação em até 5 s.",
      "requisitos": ["RF-SYN-03", "RF-SYN-04", "RNF-CON-01", "CF06"], "regras": ["RN-DT-03", "RN-DT-04", "RN-V1-04"],
      "falhas": [{"t_ms": 60_000, "tipo": "CANAL_DESCONECTA", "duracao_ms": 300_000}],
      "acoes": [a(5_000, "morador", "ENTRAR"), a(8_000, "rex", "ENTRAR"),
                a(10_000, "morador", "MUDAR_COMODO", para="quarto"), a(12_000, "rex", "MUDAR_COMODO", para="cozinha"),
                a(24_000, "morador", "ANDAR_ALEATORIO", duracao_ms=576_000),
                a(26_000, "rex", "ANDAR_ALEATORIO", duracao_ms=574_000)]},
     [r("A1", "REQUISITO", "canal caído", "logo depois da queda",
        {"tipo": "gemeo", "comodo": "quarto", "em_ms": 61_000, "atualidade": "DESATUALIZADO", "conexao": "DESCONECTADO"}),
      r("A2", "REQUISITO", "canal volta", "o hub reconcilia",
        {"tipo": "metrica", "nome": "reconciliacao_ms_max", "max": 5_000}),
      r("A3", "REQUISITO", "fila persistente", "o cenário termina",
        {"tipo": "metrica", "nome": "eventos_nao_entregues", "igual": 0}),
      r("A4", "REQUISITO", "morador e Rex andando", "o canal está fora",
        {"tipo": "luz_constante", "comodo": "quarto", "valor": "ACESA", "entre_ms": [30_000, 500_000]})]),
]


def main() -> int:
    for rot, asserc in CENARIOS:
        for sub, doc in (("roteiros", rot), ("esperado", {"cenario": rot["id"], "modo": "IDEAL", "semente_referencia": 42,
                                                          "requisitos": rot["requisitos"], "assercoes": asserc + [INV]})):
            p = RAIZ / "cenarios" / sub / f"{rot['id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fp = RAIZ / "experimentos" / "familias.json"
    fam = json.loads(fp.read_text(encoding="utf-8"))
    for f, ids in {"F1": ["A03"], "F2": ["A01", "A02"], "F3": ["A04"], "F5": ["A05"]}.items():
        fam["familias"][f] = sorted(set(fam["familias"].get(f, [])) | set(ids))
    fp.write_text(json.dumps(fam, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(CENARIOS)} cenários próprios gravados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
