# DESIGN.md — Cyberappfin: a jornada do pacote

Linguagem visual da apresentação (`jornada.html`) e dos documentos que ela abre
(`drp.html`, `regras-wazuh.html`, `runbook-tecnico.html`). Quem for mexer nas telas
deve seguir estas regras para a apresentação continuar com uma cara só.

## Contexto de uso

- Exibida em **projetor**, tela cheia, normalmente em **1366×768** ou **1920×1080**.
- Fundo escuro. Tudo precisa ser legível do fundo da sala: texto grosso, contraste alto.
- Duas formas de tela: **mapa** (topologia + painel lateral) e **tela cheia** (processo e gestão).

## Cores

| Token | Valor | Uso | Contraste sobre o fundo |
|---|---|---|---|
| `--bg` | `#0B1520` | fundo geral | — |
| `--panel` / bloco | `#13212F` / `#132233` | painel lateral, cartões | — |
| `--text` | `#F4F7FA` | títulos e texto principal | 17,1:1 |
| `--soft` | `#DCE5EE` | corpo do texto | 12,6:1 |
| `--muted` | `#B7C6D5` | rótulos, legendas, dicas | 9,2:1 |
| `--danger` | `#F87171` | alerta, bloqueado, perdido | — |

**Uma cor por time** (usar sempre a mesma, em rótulos, bordas e pacotes):

| Time | Cor |
|---|---|
| Network | `#14B8A6` |
| IAM | `#8B5CF6` |
| SOC | `#F59E0B` |
| Endpoint | `#22C55E` |
| GRC | `#EAB308` |
| Marca / neutro | `#4C8DF6` |

**Severidade** (matriz, BIA, regras do Wazuh): 2 Médio `#FACC15` · 3 Alto `#FB923C` · 4 Crítico `#F87171`.
Nível baixo / informativo: `#94A3B8`.

Regra: **cor nunca sozinha.** Todo estado também tem texto ou símbolo
(✓ OK, PERDIDA, ✗ bloqueado, "3 Alto", ◐ em validação).

## Tipografia

| Papel | Fonte | Peso |
|---|---|---|
| Títulos, números grandes | Sora | 700–800 |
| Corpo e rótulos | DM Sans | 500 (corpo), 700 (destaque) |
| IPs, comandos, código | JetBrains Mono | 600 |

- Corpo com peso **500** (não 400): no projetor, texto fino some sobre o fundo escuro.
- Rótulos pequenos em caixa alta com espaçamento de letras (`letter-spacing: .1em`).

## Botões de link (convenção)

| Cor | Para quê | Exemplo |
|---|---|---|
| Amarelo `#EAB308` | documento do DRP | "Abrir o documento do DRP ↗" |
| Lilás `#C4B5FD` | runbook técnico | "Runbook técnico ↗" |
| Azul claro `#7DD3FC` | ferramenta do ambiente real (Wazuh, Zabbix, Grafana, OpenVAS, Zammad, Firefly) | "Abrir Wazuh ↗ 10.10.50.21" |

Os endereços das ferramentas ficam na constante `AMBIENTE`, no topo do script.
Os links só abrem no computador ligado à rede do laboratório.

## Componentes recorrentes

- **Bloco** (`.bloco`): cartão com faixa colorida de 5 px no topo (cor do time ou da severidade).
- **Passos** (`.passos`): lista numerada; os já feitos ficam só com o rótulo e ✓, o atual mostra o texto.
- **Card de checklist** (`.vk`): número, título, "Por quê", comandos, ✓ Esperado (verde), Se falhar (âmbar).
- **Linha do tempo do ticket** (`.tk-ev`): hora, fase e texto, com borda colorida pela fase.
- **Selo do mapa**: texto curto na segunda linha do servidor (ao lado do IP), nunca sobre o nome.

## Legibilidade (regras da revisão de design)

- Telas cheias crescem sozinhas até 30% quando sobra espaço (`ajustarTela`); telas densas ficam no tamanho base.
- Nas visões gerais do mapa, a câmera enquadra só as colunas que importam e, em telas até 1500 px,
  o painel lateral estreita para 450 px para o mapa ganhar espaço.
- Pacotes animados sobem e descem pelo corredor lateral de cada coluna, sem cruzar textos.
- Elementos fora de foco no mapa ficam com opacidade 0,3 (não somem no projetor).

## Movimento

- Toda animação tem propósito: mostrar o caminho do pacote ou guiar a atenção (câmera).
- `prefers-reduced-motion`: câmera e pacotes sem animação, cenas em loop rodam uma vez e param.
- Tecla **P** pausa as animações; **B** deixa a tela preta; **N** mostra as notas de fala.

## Acessibilidade

- Contraste mínimo de texto 4,5:1 (todo texto atual passa de 9:1).
- Servidores clicáveis do mapa são focáveis pelo teclado e abrem com Enter.
- Leitor de tela: a cada troca, anuncia só "Parada N de 55: título".
