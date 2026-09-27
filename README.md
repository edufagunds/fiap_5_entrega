# PEDE — Radar de Risco de Defasagem

Aplicação Streamlit para estimar a probabilidade de um aluno entrar em situação de defasagem no próximo ciclo.

## Modelo

- Algoritmo: Regressão Logística
- Target: `Defasagem < 0` no ciclo seguinte
- Features: IAN, IDA, IEG, IAA, IPS, IPV e Pedra
- Treinamento do artefato de produção: transições 2022→2023 e 2023→2024
- Faixas: Baixo <30%, Médio 30–70%, Alto >70%

A avaliação temporal do modelo deve ser consultada no notebook do projeto. O artefato usado pela aplicação é treinado com os dois ciclos rotulados disponíveis depois dessa avaliação.

## Executar localmente

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Deploy no Streamlit Community Cloud

1. Crie um repositório no GitHub.
2. Suba os arquivos deste diretório para o repositório.
3. Acesse https://share.streamlit.io e conecte sua conta GitHub.
4. Clique em **Create app**.
5. Selecione o repositório, a branch e `app.py` como arquivo de entrada.
6. Clique em **Deploy**.

O `requirements.txt` deve ficar na raiz do repositório ou junto do arquivo de entrada. O Community Cloud instala as dependências declaradas nesse arquivo.
