# [Nome da Empresa] — Site institucional (projeto SOC Impacta)

Site estático em um único arquivo (`index.html`), sem backend — pronto pra publicar no GitHub Pages.

## Como publicar

1. Crie um repositório novo no GitHub (pode ser público).
2. Faça upload deste `index.html` para a raiz do repositório (botão **Add file > Upload files**).
3. Vá em **Settings > Pages**, escolha a branch `main` e a pasta `/ (root)`, salve.
4. Em 1–2 minutos o site fica no ar em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

## Como editar o conteúdo

Abra o `index.html` em qualquer editor de texto/código e procure pelas variáveis no `<script>`:

- **`COMPANY`** — nome da empresa, tagline, texto "sobre" e contato (aparece na home).
- **`TEAMS`** — um bloco por área (network, iam, grc, soc, endpoint). Cada time edita só o seu bloco:
  - `blurb`: frase curta que aparece no card da home.
  - `slides`: conteúdo do modo apresentação daquele time.

Depois de editar, salve o arquivo, suba de novo pro GitHub (commit) e o site atualiza sozinho.

## Editando direto pelo GitHub (sem instalar nada)

Cada time pode clicar no lápis de edição na página do arquivo no GitHub, mudar seu bloco dentro de `TEAMS`, e commitar direto pelo navegador — sem precisar de Git instalado.
