# 🏢 CYBERAPPFIN

> Empresa fictícia desenvolvida como projeto acadêmico de simulação empresarial e Defesa Cibernética — **Faculdade Impacta**.

A turma foi dividida em times, cada um responsável por uma área da empresa (Network, IAM, SOC, Endpoint e GRC). Este repositório reúne a apresentação de todas elas — e mostra como ela evoluiu ao longo do semestre.

---

## 🏁 Apresentação final — Anatomia da Cyberappfin

**👉 [Abrir a Apresentação final](https://gil0f.github.io/CYBERAPPFIN/anatomia.html)** · [ver o arquivo no GitHub](https://github.com/GIL0F/CYBERAPPFIN/blob/main/anatomia.html)

Uma página só, de rolagem, com tudo o que o projeto construiu:

| Capítulo | O que mostra |
|---|---|
| **Anatomia** | As 7 camadas do ambiente em vista explodida (SD-WAN → UniFi → Cisco 2960 → VLANs → servidores → Wazuh → Zammad) e um pacote atravessando cada uma |
| **Organização** | Os cinco times e o plano de subida do ambiente |
| **Topologia** | O mapa da rede com o fluxo dos pacotes, passo a passo: perímetro, VLANs, AD, SOC, agentes, OpenVAS, DMZ e as regras de firewall |
| **Detecção** | As 30 regras customizadas do Wazuh, regras de correlação, CyberFin IA e as demonstrações ao vivo |
| **Dashboards** | Os 11 dashboards do Grafana do SOC, com zoom em cada área, gráficos se desenhando e números animados |
| **Incidente** | Simulação de phishing no mapa e o tratamento completo: severidade, CSIRT, escalonamento, Zammad e o ticket do início ao fim |
| **Continuidade** | Backup, BIA (impacto e mitigação), ordem de recuperação, o DR no mapa e o checklist pós-restauração |
| **GRC** | Políticas e conformidade |

Um menu fixo no topo leva a qualquer capítulo. Os documentos completos abrem em outra aba:

- 📄 [Plano de Recuperação de Desastres (DRP)](https://gil0f.github.io/CYBERAPPFIN/drp.html)
- 🛡️ [Catálogo de regras do Wazuh](https://gil0f.github.io/CYBERAPPFIN/regras-wazuh.html)
- 🔧 [Runbook técnico](https://gil0f.github.io/CYBERAPPFIN/runbook-tecnico.html)

---

## 🗺️ Evolução do projeto

Cada etapa continua publicada, para mostrar o caminho até a versão final.

| # | Versão | Quando | Abrir | Arquivo |
|---|---|---|---|---|
| 1 | **Site institucional** — home da empresa + modo slides por área | ago/2026 | [abrir](https://gil0f.github.io/CYBERAPPFIN/index.html) | [`index.html`](index.html) |
| 2 | **Protótipo V2** — prédio 3D, um andar por time, status em % | set/2026 | [abrir](https://gil0f.github.io/CYBERAPPFIN/prototipo-v2.html) | [`prototipo-v2.html`](prototipo-v2.html) |
| 3 | **Relatórios do OpenVAS** — scan, matriz de risco e guia | set/2026 | [scan](https://gil0f.github.io/CYBERAPPFIN/openvas-scan.html) · [matriz](https://gil0f.github.io/CYBERAPPFIN/openvas-risk-matrix.html) · [guia](https://gil0f.github.io/CYBERAPPFIN/openvas-guia.html) | [`openvas-*.html`](openvas-scan.html) |
| 4 | **A jornada do pacote** — apresentação em slides para projetor (55 telas) | out/2026 | [abrir](https://gil0f.github.io/CYBERAPPFIN/jornada.html) | [`jornada.html`](jornada.html) |
| 5 | **Dashboards do Grafana** — apresentação guiada dos painéis do SOC | nov/2026 | [abrir](https://gil0f.github.io/CYBERAPPFIN/dashboards/) | [`dashboards/`](dashboards/index.html) |
| 6 | **🏁 Apresentação final** — Anatomia da Cyberappfin, tudo numa página | nov/2026 | [abrir](https://gil0f.github.io/CYBERAPPFIN/anatomia.html) | [`anatomia.html`](anatomia.html) |

> **Na sala:** a versão em slides (`jornada.html`) é a feita para o projetor — setas navegam, **N** mostra as notas, **F** tela cheia, **B** tela preta, **P** pausa as animações.

---

## 🧩 Áreas da empresa

| Área | Responsabilidade |
|---|---|
| 🌐 **Network** | Infraestrutura, topologia de rede e disponibilidade |
| 🔐 **IAM** | Identidades, acessos e controle de permissões |
| 📋 **GRC** | Políticas, gestão de risco e conformidade |
| 🛡️ **SOC** | Monitoramento, detecção e resposta a incidentes |
| 💻 **Endpoint** | Segurança de dispositivos e hardening |

---

## 🛠️ Tecnologia

Site estático, sem backend: cada página é um arquivo HTML com CSS e JavaScript embutidos. Não depende de instalação, build ou servidor — basta abrir no navegador ou publicar em qualquer hospedagem estática.

| Arquivo | O que é |
|---|---|
| `anatomia.html` | Apresentação final (gerada pelo script abaixo) |
| `jornada.html` | Apresentação em slides — **fonte do conteúdo** da apresentação final |
| `drp.html`, `regras-wazuh.html`, `runbook-tecnico.html` | Documentos de apoio |
| `DESIGN.md` | Linguagem visual dos slides |
| `referencias/DESIGN-anatomia.md` | Linguagem visual da apresentação final ("Engenharia crua") |
| `ferramentas/` | Script que monta a apresentação final |

### ✏️ Como atualizar a apresentação final

O conteúdo (textos, IPs, regras, telas) vem da `jornada.html`. Depois de editar a jornada, gere a página única de novo:

```bash
python3 ferramentas/montar-pagina-unica.py
```

Assim os slides e a apresentação final nunca ficam diferentes.

---

## 📤 Como publicar

O site está no **GitHub Pages**, a partir da branch `main`, pasta raiz. Depois de um commit no `main`, o Pages atualiza sozinho em 1–2 minutos.

---

<p align="center"><sub>Projeto acadêmico — Faculdade Impacta · Simulação Empresarial · Defesa Cibernética</sub></p>
