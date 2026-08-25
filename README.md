# CYBERAPPFIN — Site institucional (projeto Impacta)

Site estático em um único arquivo (`index.html`), sem backend — pronto pra publicar no GitHub Pages.

## Como editar o conteúdo

Abra o `index.html` em qualquer editor de texto/código e procure pelas variáveis no `<script>`:

- **`COMPANY`** — nome da empresa, tagline, texto "sobre" e contato (aparece na home).
- **`TEAMS`** — um bloco por área (network, iam, grc, soc, endpoint). Cada time edita só o seu bloco:
  - `blurb`: frase curta que aparece no card da home.
  - `slides`: conteúdo do modo apresentação daquele time.

Depois de editar, salve o arquivo, suba de novo pro GitHub (commit) e o site atualiza sozinho.

## Editando direto pelo GitHub (sem instalar nada)

Cada time pode clicar no lápis de edição na página do arquivo no GitHub, mudar seu bloco dentro de `TEAMS`, e commitar direto pelo navegador — sem precisar de Git instalado.
