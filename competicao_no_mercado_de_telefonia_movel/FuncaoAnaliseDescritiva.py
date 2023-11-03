def analise_descritiva(df):
    #tipo de dado que tenho em cada coluna do dataframe (ou quantidade, ou qualidade)

    # CNPJ (quantidade)
    print(f"CNPJ - ", len(df['CNPJ'].unique()))

    print()
    # Codigo nacional (quantidade)
    print(f"Código Nacional - ", len(df['Código Nacional'].unique()))

    print()
    # Município (quantidade)
    print(f"Município - ", len(df['Município'].unique()))

    print()
    # UF (dados)
    print(f"UF - ", len(df['Município'].unique()))
    print(f"UF - ", df['UF'].unique())

    print()
    # Modalidade de Cobrança (quantidade)
    print(f"Modalidade de Cobrança - ", len(df['Modalidade de Cobrança'].unique()))
    # Modalidade de Cobrança (dados)
    print(f"Modalidade de Cobrança - ", df['Modalidade de Cobrança'].unique())

    print()
    # Tecnologia (quantidade)
    print(f"Tecnologia - ", len(df['Tecnologia'].unique()))
    # Tecnologia (dados)
    print(f"Tecnologia - ", df['Tecnologia'].unique())

    print()
    # Tecnologia Geração (quantidade)
    print(f"Tecnologia Geração - ", len(df['Tecnologia Geração'].unique()))
    # Tecnologia Geração (dados)
    print(f"Tecnologia Geração - ", df['Tecnologia Geração'].unique())

    print()
    # Empresa (quantidade)
    print(f"Empresa - ", len(df['Empresa'].unique()))
    # Empresa (dados)
    print(f"Empresa - ", df['Empresa'].unique())

    print()
    # Porte da Prestadora (quantidade)
    print(f"Porte da Prestadora - ", len(df['Porte da Prestadora'].unique()))
    # Porte da Prestadora (dados)
    print(f"Porte da Prestadora - ", df['Porte da Prestadora'].unique())

    print()
    # Tipo de Pessoa (quantidade)
    print(f"Tipo de Pessoa - ", len(df['Tipo de Pessoa'].unique()))
    # Tipo de Pessoa (dados)
    print(f"Tipo de Pessoa - ", df['Tipo de Pessoa'].unique())

    print()
    # Tipo de Produto (quantidade)
    print(f"Tipo de Produto - ", len(df['Tipo de Produto'].unique()))
    # Tipo de Produto (dados)
    print(f"Tipo de Produto - ", df['Tipo de Produto'].unique())

    print()
    # Código IBGE Município (quantidade)
    print(f"Código IBGE Município - ", len(df['Código IBGE Município'].unique()))

    print()
    # Grupo Econômico (quantidade)
    print(f"Grupo Econômico - ", len(df['Grupo Econômico'].unique()))
    # Grupo Econômico (dados)
    print(f"Grupo Econômico - ", df['Grupo Econômico'].unique())
