# 🏢 CYBERAPPFIN

> Site institucional fictício desenvolvido como parte do projeto acadêmico de simulação empresarial — **Faculdade Impacta**.

## 📖 Sobre o projeto

Este repositório contém o site institucional de uma **empresa fictícia**, criada como parte de um trabalho da disciplina de simulação empresarial da Faculdade Impacta. A turma foi dividida em times, cada um responsável por uma área da empresa, e este site reúne a apresentação de todas elas em um único lugar — no lugar de vários arquivos de PowerPoint separados.

O site tem duas partes:

- **Home institucional** — como se fosse a página real da empresa: apresentação, sobre e as áreas.
- **Modo apresentação** — ao clicar em uma área, o site entra em um modo de slides (navegável por seta/clique), ideal para apresentar em sala de aula.

## 🧩 Áreas da empresa

| Área | Responsabilidade |
|---|---|
| 🌐 **Network** | Infraestrutura, topologia de rede e disponibilidade |
| 🔐 **IAM** | Identidades, acessos e controle de permissões |
| 📋 **GRC** | Políticas, gestão de risco e conformidade |
| 🛡️ **SOC** | Monitoramento, detecção e resposta a incidentes |
| 💻 **Endpoint** | Segurança de dispositivos, EDR e gestão de patches |

## 🚀 Como acessar

O site está publicado via **GitHub Pages**:

**🔗 [seu-usuario.github.io/nome-do-repositorio](#)** ← atualize este link depois de publicar

## 🛠️ Tecnologia

Site estático, sem backend — um único arquivo `index.html` com HTML, CSS e JavaScript embutidos. Não depende de instalação, build ou servidor: basta abrir no navegador ou publicar em qualquer serviço de hospedagem estática.

## ✏️ Como editar o conteúdo

Todo o conteúdo do site fica em duas variáveis, no topo do bloco `<script>` dentro do `index.html`:

```js
const COMPANY = { ... }   // nome, tagline, texto "sobre" e contato da empresa
const TEAMS   = { ... }   // um bloco por área — cada time edita só o seu
```

Cada time só precisa mexer no **seu próprio bloco** dentro de `TEAMS`, sem afetar o conteúdo dos outros. Dentro de cada bloco:

- `blurb` → frase curta que aparece no card da área, na home
- `slides` → conteúdo do modo apresentação daquele time (missão, equipe, processos, ferramentas, etc.)

Depois de editar, é só salvar e subir a alteração (commit) — o GitHub Pages atualiza o site sozinho em 1–2 minutos.

## 📤 Como publicar

1. Repositório precisa ser **público** (necessário para GitHub Pages gratuito)
2. `Settings` → `Pages` → Fonte: **Implantar a partir de uma ramificação**
3. Branch: `main` · Pasta: `/ (raiz)` → **Salvar**
4. Aguardar alguns minutos e acessar o link gerado

## 👥 Time responsável por este repositório

_Adicione aqui os nomes dos integrantes do time responsável pela manutenção do site._

---

<p align="center"><sub>Projeto acadêmico — Faculdade Impacta · Simulação Empresarial</sub></p>
