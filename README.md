# PlantExpert

Sistema especialista para diagnóstico inicial de problemas em plantas domésticas e de pequeno cultivo.

Trabalho de **Análise Orientada a Objetos** — Universidade Veiga de Almeida (UVA)
Alunos: Lucas Gonçalves Carvalho Machado (matrícula 1250119031)
        Roberto Teixeira Mocho Junior (matrícula 1250112526)

## Sobre o projeto

O PlantExpert usa uma base de conhecimento formada por fatos e regras de produção no formato SE/ENTÃO, com um mecanismo de inferência por encadeamento para frente (forward chaining), para relacionar sintomas e condições de cultivo a possíveis diagnósticos e recomendações.

O resultado apresentado é uma **hipótese orientativa**, não uma confirmação científica de doença, e não substitui avaliação profissional.

## Estrutura do repositório

```
plant-expert/
├── plant_expert.py          # implementação do motor de inferência (Python)
├── prototype/
│   └── index.html           # protótipo navegável das telas (HTML/CSS/JS)
├── PlantExpert_Trabalho_ABNT.pdf   # documento completo do trabalho
└── README.md
```

## Base de conhecimento (regras)

| ID  | Condições (SE) | Conclusão (ENTÃO) |
|-----|-----------------|--------------------|
| R01 | folhas amareladas + solo muito úmido + rega frequente | Possível excesso de água |
| R02 | folhas secas + solo seco + rega não frequente | Possível falta de água |
| R03 | folhas amareladas + pouca luz | Possível deficiência de luminosidade |
| R04 | manchas + umidade alta | Possível problema fúngico |
| R05 | pequenos insetos + folhas danificadas | Possível presença de pragas |

## Como executar o programa em Python

Requer Python 3.7 ou superior.

```bash
python plant_expert.py
```

O programa apresenta um menu no terminal para iniciar um diagnóstico (responder sim/não a perguntas sobre sintomas e condições de cultivo), consultar o histórico de diagnósticos da sessão, ou sair.

## Como visualizar o protótipo de telas

Abra o arquivo `prototype/index.html` diretamente no navegador (duplo clique) ou publique a pasta `prototype/` no GitHub Pages para gerar um link navegável.

## Referências

- RUSSELL, Stuart; NORVIG, Peter. *Artificial Intelligence: A Modern Approach*. 4. ed. Pearson, 2020.
- SOMMERVILLE, Ian. *Engenharia de Software*. 10. ed. Pearson, 2019.
- ELMASRI, Ramez; NAVATHE, Shamkant B. *Sistemas de Banco de Dados*. 7. ed. Pearson, 2018.
- PYTHON SOFTWARE FOUNDATION. *Python Documentation*. Disponível em: https://docs.python.org/3/.
