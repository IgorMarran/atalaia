# ATALAIA

Plataforma de monitoramento inteligente e inspeção autônoma para a segurança física de instalações nucleares. Projeto desenvolvido para o desafio proposto pela **Amazul**, na disciplina **Software Engineering** (Prof. Leandro Ramos da Silva).

## Sprint 1 – Documento de Visão

O documento está em [`Documento_de_Visao_Sprint1_ATALAIA.pdf`](Documento_de_Visao_Sprint1_ATALAIA.pdf). Ele reúne:

- contexto do problema e situações anômalas;
- objetivos e metas;
- stakeholders, matriz de poder × interesse e personas;
- solução proposta, arquitetura e tecnologias;
- escopo (dentro e fora), premissas, restrições e riscos;
- protótipo conceitual de baixa fidelidade (tela principal, detalhe da ocorrência e fluxo de uso).

## Integrantes

| Nome | RM | Papel na Sprint 1 |
|---|---|---|
| Igor Mota Marran | 567823 | Elaboração do Documento de Visão (responsável principal) |
| Kaue Souza Rodrigues | 567716 | Contexto do problema e pesquisa |
| Dante Daher Garçon | 567727 | Análise de stakeholders |
| Pedro Henrique Camacho de Alencar | 568071 | Definição da solução e arquitetura |
| Gabriel Kenishi Furuzawa | 568245 | Definição do escopo |
| Murylo Silva Amaral | 568241 | Protótipo conceitual |

## Como gerar o PDF

```bash
pip install -r requirements.txt
python gerar_pdf.py Documento_de_Visao_Sprint1_ATALAIA.pdf
```

O script usa a fonte Arial de `C:/Windows/Fonts`.
