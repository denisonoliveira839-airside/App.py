def gerar_lista_materiais(resultado):

    return {

        "Item":[
            "Disjuntor",
            "Contator",
            "Relé térmico",
            "Cabo potência"
        ],

        "Especificação":[
            str(resultado["disj"])+" A",
            "Contator AC3",
            "Relé térmico",
            str(resultado["cabo"])+" mm²"
        ]

    }
