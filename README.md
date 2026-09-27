# PEDE — Radar de Risco de Defasagem

Aplicação Streamlit para estimar a probabilidade de um aluno entrar em situação de defasagem no próximo ciclo.

## Modelo

- Algoritmo: Regressão Logística
- Target: `Defasagem < 0` no ciclo seguinte
- Features: IAN, IDA, IEG, IAA, IPS, IPV e Pedra
- Treinamento do artefato de produção: transições 2022→2023 e 2023→2024
- Faixas: Baixo <30%, Médio 30–70%, Alto >70%

A avaliação temporal do modelo deve ser consultada no notebook do projeto. O artefato usado pela aplicação é treinado com os dois ciclos rotulados disponíveis depois dessa avaliação.
