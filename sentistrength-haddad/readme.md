* Como usei o sentistrenth:
	- Instalei a versão 0.0.5 com o comando:
		pip install sentistrength==0.0.5
	- Utilizei o dicionário contendo as palavras em pt-br normalizado colocando os seus arquivos dentro do diretorio SentiStrength_Data.

* Apliquei o sentistrength na coleta realizada no twitter para o Haddad (final de 2017 até o final de 2019)

* pré-processei(removendo stop-words, urls, datas, numeros, e.t.c.) os textos contidos no atributo "full_text" e criei um novo atributo dentro desse json chamado "pre_processed_full_text". Como por exemplo:
	
	"pre_processed_full_text": [
            "agricultura",
            "brasileira",
            "mais",
            "consome",
            "agrotóxicos",
            "mundo",
            "vamos",
            "mudar",
            "trazer",
            "saúde",
            "mesa",
            "brasileiro",
            "conheça",
            "propostas",
            "plano",
            "governo",
            "vote",
            "haddadpresidente"
        ]

* Apliquei o algoritmo de analise de sentimentos em cada um dos atributos "pre_processed_full_text" json. Criei um novo atributo em cada um deles chamado score_binary e score_scale. Como abaixo:
        "score_binary": [
            [
                1,
                -1
            ]
        ],
        "score_scale": [
            0.0
        ]

	ou

	"score_binary": [
            [
                1,
                -2
            ]
        ],
        "score_scale": [
            -0.25
        ]


* Foram usados varios algoritmos(scripts-sentistrength-haddad) para gerar conhecimentos (resultados-sentistrength-haddad) a partir desses atributos score_binary e score_scale
