# Anatomia — Design Language (referência)

> Extraído de um quadro de vídeo ("Mechanical Key Switch", vista explodida). Valores de cor
> medidos; tamanhos e espaçamentos estimados (fonte de baixa resolução, 459×533 px).
> Referência separada do `DESIGN.md` da apresentação (`jornada.html`).

## Visual Theme
**Técnico, silencioso, preciso — prancha de engenharia.**
Ilustração isométrica explodida sobre papel claro com grade, como uma figura de manual
técnico ou patente. A cor é eliminada para que forma, linha e rótulo carreguem tudo;
o único contraste forte é o item que o usuário está examinando.

## Color Palette
### Neutrals (primitivos — saturação 0)
| Token | Valor | Papel |
|---|---|---|
| gray-0 | #FFFFFF | face superior das peças |
| gray-50 | #F8F8F8 | papel / fundo da prancha |
| gray-100 | #F2F2F2 | face lateral clara das peças |
| gray-150 | #EDEDED | pontos da grade (estimado) |
| gray-200 | #E4E4E4 | face lateral escura das peças (estimado) |
| gray-300 | #D0D0D0 | linhas de chamada, borda do cartão |
| gray-500 | #969696 | contorno das peças, rótulos inativos |
| gray-700 | #696969 | rótulos, título |
| gray-950 | #1E1E1E | tinta: rótulo ativo, eixo tracejado |

### Semantic
| Role | Light | Dark (proposta, não observada) |
|---|---|---|
| canvas | gray-50 | #0E0E0E |
| part/top · part/left · part/right | gray-0 · gray-100 · gray-200 | #1C1C1C · #161616 · #111111 |
| stroke/part | gray-500 | #5A5A5A |
| stroke/leader | gray-300 | #2E2E2E |
| text/label | gray-500 | #7A7A7A |
| text/title | gray-700 | #B0B0B0 |
| state/active-bg · state/active-fg | gray-950 · gray-0 | #F2F2F2 · #0E0E0E |

Sem cores de marca nem semânticas (sucesso/erro). Se o projeto precisar de cor, entra
**uma** cor de destaque, só no estado ativo.

## Typography
**Família:** monoespaçada única — original não identificável; substituta: JetBrains Mono
(já usada no projeto, Google Fonts).
**Escala:** ad-hoc, pequena; tudo em caixa alta, `letter-spacing: .12em`.

| Token | Tamanho (est.) | Papel | Line height |
|---|---|---|---|
| label | 11px | rótulos de peça | 1 |
| title | 12px | título da prancha | 1 |
| fig | 9px, vertical | código da figura (FIG_003) | 1 |
| label-active | 11px, peso 600 | rótulo invertido | 1 |

## Components
| Componente | Hierarquia | Função | Variantes |
|---|---|---|---|
| Grid background | Primitivo | textura de papel milimetrado | — |
| Leader label | Primitivo | nome da peça + linha até ela | esquerda / direita |
| Assembly axis | Primitivo | eixo tracejado que liga as peças | — |
| Isometric part | Componente | peça em 3 tons, contorno fino | qualquer forma |
| Active label | Componente | rótulo invertido (fundo tinta, texto branco) | hover / foco / fixado |
| Plate header | Componente | título + código da figura | — |
| Exploded stack | Padrão | peças ao longo do eixo, espaçamento uniforme | montado / explodido |
| Hover-to-identify | Padrão | apontar a peça destaca o rótulo | — |
| Figure card | Template | prancha completa em cartão | — |

## Layout
**Grade:** coluna central para a ilustração; coluna fixa de rótulos à esquerda e à direita.
**Base unit:** 8px (proposta).
**Espaçamento:** xs=4, sm=8, md=16, lg=32, xl=64. Gap entre peças no eixo: uniforme (~lg–xl).
**Cartão:** raio ~16px, borda 1px gray-300, margens internas generosas.

## Depth
| Nível | Valor | Uso |
|---|---|---|
| 0 | nenhum | peças: volume só por 3 tons de face, sem sombra projetada |
| 1 | borda 1px gray-300 + sombra muito suave | cartão da prancha |

Camadas: grade < linhas de chamada < peças < rótulo ativo.

## Do's and Don'ts
### Do
- Usar só a escala de cinzas; o contraste forte é reservado ao item ativo.
- Desenhar peças em isométrico com exatamente 3 tons de face e contorno fino.
- Ligar todo rótulo à peça com linha horizontal fina; alinhar rótulos em coluna.
- Manter espaçamento uniforme entre as peças ao longo do eixo.
- Rótulos em monoespaçada, caixa alta, espaçamento de letras amplo.

### Don't
- Não usar sombra projetada, gradiente ou brilho nas peças.
- Não colorir rótulos ou peças por categoria (quebra o silêncio visual).
- Não cruzar linhas de chamada entre si nem sobre outra peça.
- Não destacar mais de um item por vez.
- Não usar texto corrido dentro da prancha; descrição vai fora dela.

## Responsive
Não observado. Definir: no celular, rótulos passam para uma lista abaixo da figura
(numerada, ligada à peça por número) em vez de linhas de chamada laterais.

## Agent Prompt Guide
- Monocromático: saturação zero; só o estado ativo usa contraste máximo (gray-950 / branco).
- Peças isométricas com 3 tons de face, contorno 1px, sem sombra.
- Todo rótulo tem linha de chamada horizontal até a peça; colunas de rótulos fixas.
- Uma família monoespaçada, caixa alta, letter-spacing .12em.
- Interação "apontar para identificar": hover/foco inverte o rótulo; acessível por teclado.
