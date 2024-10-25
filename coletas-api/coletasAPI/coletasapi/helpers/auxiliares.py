def add_partes_do_processo(schema, nome, papel, advogado):
    """Adiciona partes do processo ao JSON"""
    if advogado != False:
        schema["partes_do_processo"].append({
            "nome": nome,
            "papel": papel,
            "advogado(as)": advogado
        })
    else:
        #Quando uma parte não tiver advogado
        schema["partes_do_processo"].append({
            "nome": nome,
            "papel": papel
        })

    return schema

def add_lista_das_movimentacoes(schema, data, movimento):
    """Adiciona movimentação ao JSON"""
    schema["lista_das_movimentacoes"].append({
        "data": data,
        "movimento": movimento
    })

    return schema

def validaTribunais(jtr):
    """Só deve aceitar JTR do TJAL e TJCE"""
    if jtr != "806" and jtr!="802":
        return False
    else:
        return True

def validaNumeroDeProcesso(numero_processo):
    """Valida se o número do processo está de acordo com o padrão CNJ"""
    #De acordo com o padrão CNJ: N6 N5 N4 N3 N2 N1 N0 A3 A2 A1 A0 J2 T1 R0 O3 O2 O1 O0 D1D0 módulo 97 tem que ser igual a 1 para o numero do processo ser válido
    
    #Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
    partes = numero_processo.split(".")
    
    n = partes[0].split("-")[0]
    d = partes[0].split("-")[1]
    a = partes[1]
    j = partes[2]
    tr = partes[3]
    o = partes[4]

    tribunal = {"02": "TJAL", "06": "TJCE"}

    if validaTribunais(j+tr):
        numero = n + a + j + tr + o + d
        resto = int(numero) % 97
        if resto == 1:
            return (True, tribunal[tr])
        else:
            return (False, False)
    else:
        return (False, False)
    

def valida_tempo_cache(processo, max_cache, tempo_consulta):
    """Verifica se o processo está dentro do tempo máximo de cache informado"""
    tempo_coleta = processo["tempo_coleta"]

    if tempo_coleta >= tempo_consulta - max_cache:
        return True
    else:
        return False