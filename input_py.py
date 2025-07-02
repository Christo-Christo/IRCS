GOC = ["KT_L_IDR_PI_", "KT_L_IDR_NI_", "KT_L_IDR_NO_", "KT_L_USD_PI_", 
             "KT_L_USD_NI_", "KT_L_USD_NO_", "AG_L_IDR_PI_", "AG_L_IDR_NI_",
             "AG_L_IDR_NO_", "AG_L_USD_PI_", "AG_L_USD_NI_", "AG_L_USD_NO_",
             "NK_L_IDR_PI_", "NK_L_IDR_NI_", "NK_L_IDR_NO_", "NK_L_USD_PI_",
             "NK_L_USD_NI_", "NK_L_USD_NO_" ]

START_YEAR = 2014
END_YEAR = 2024
USDIDR = 16162


def GOC_year(GOC= GOC, start = START_YEAR, end = END_YEAR):
    '''
    '''
    
    running_year = [str(i) for i in range(start, end + 1)]
    
    GOC_year_lst = []
    for x in range(len(running_year)):
        for y in range(len(GOC)):
            GOC_year_lst.append(GOC[y] + running_year[x])
    
    return GOC_year_lst

def GOC_year_tradonly(GOC= GOC, start = START_YEAR, end = END_YEAR):
    '''
    '''
    
    running_year = [str(i) for i in range(start, end + 1)]
    
    GOC_year_tradonly_lst = []
    for x in range(len(running_year)):
        for y in range(len(GOC)):
            if 'SN' not in GOC[y] or 'SI' not in GOC[y]:
                GOC_year_tradonly_lst.append(GOC[y] + running_year[x])
    
    return GOC_year_tradonly_lst
