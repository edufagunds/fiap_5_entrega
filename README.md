# 🎓 PEDE — Radar de Risco de Defasagem (Datathon Passos Mágicos)

Este projeto foi desenvolvido como solução para o **Datathon PEDE**, combinando engenharia de dados, modelagem preditiva com Machine Learning e uma interface interativa em Streamlit para apoiar a priorização de intervenções pedagógicas.

O principal objetivo da aplicação é estimar a probabilidade de um aluno entrar ou permanecer em situação de defasagem escolar no ciclo seguinte, servindo como uma ferramenta de alerta antecipado para a coordenação pedagógica.

---

## 📈 Resultados do Diagnóstico Analítico

A modelagem e a análise exploratória foram baseadas no histórico de transições anuais (2022→2023 e 2023→2024), trazendo os seguintes insights:
* **Evolução da Defasagem:** Houve uma redução consistente nos três ciclos examinados. A proporção de alunos com alguma defasagem caiu de 69,9% (2022) para 46,2% (2024).
* **Heterogeneidade de Desempenho:** Embora o Indicador de Autoavaliação (IAA) e o Índice de Adequação de Nível (IAN) apresentem melhoras, os indicadores acadêmicos purificados (IDA e IEG) recuaram em 2024, exigindo atenção focada.
* **Métrica do Modelo:** O modelo de classificação baseado em Regressão Logística atingiu uma **AUC de aproximadamente 0,71** na validação temporal, provando-se robusto para triagem em lote.

---

## 🛠️ Arquitetura Técnica & Stack

O projeto foi segmentado de forma inteligente para rodar de maneira leve em servidores de nuvem de baixa memória RAM:

* **Análise e Modelagem:** Desenvolvida via Jupyter Notebook para extração de coeficientes e validação temporal.
* **Pipeline de Treinamento (`train_model.py`):** Processa e harmoniza os dados brutos e salva um artefato de produção encapsulado.
* **Interface Visual (`app.py`):** Aplicação interativa construida com a biblioteca Streamlit.
* **Modelo Preditivo:** Regressão Logística com pesos de classe balanceados, utilizando os indicadores `IAN`, `IDA`, `IEG`, `IAA`, `IPS`, `IPV` e `Pedra`.

### Tecnologias Utilizadas
* Python 3.11 / 3.12
* Streamlit
* Scikit-Learn
* Pandas & NumPy
* Joblib (para serialização do modelo)

## ☁️ Deploy no Streamlit

A aplicação está configurada para deploy automático na infraestrutura do Streamlit Cloud. 

### Faixas de Alerta Definidas
* **🟢 Baixo Risco (< 30%):** Acompanhamento pedagógico regular.
* **🟡 Risco Intermediário (30% – 70%):** Investigar componentes acadêmicos específicos de perto.
* **🔴 Alto Risco (> 70%):** Priorizar avaliação psicopedagógica urgente e intervenção ativa.
