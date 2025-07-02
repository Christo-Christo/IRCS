import pandas as pd
import csv
import input_py
import time

start_time = time.time()

fp = csv.DictReader(open("D:/17. IRCS/Control 3/DV_AZTRAD_Stat.csv", 'r'))
fp_pd = pd.DataFrame(fp)
goc_year = input_py.GOC_year()
USDIDR = input_py.USDIDR


def pol_num(goc_year= goc_year, fp_pd= fp_pd):
    '''
    '''
    grand_total_sum = 0
    
    for goc in goc_year:
        fp_pd_goc = fp_pd[[goc in i for i in fp_pd['goc']]]

        for i in fp_pd_goc['pol_num']:
            grand_total_sum += int(i)
    
    return grand_total_sum


def sum_ass (goc_year= goc_year, fp_pd= fp_pd, USDIDR= USDIDR):
    '''
    '''
    
    grand_total_sum = 0.0
    
    for goc in goc_year:
        if 'USD' in goc:
            fp_pd_goc = fp_pd[[goc in i for i in fp_pd['goc']]]
            
            for i in fp_pd_goc['sum_assd']:
                grand_total_sum += float(i) * USDIDR
        else:
            fp_pd_goc = fp_pd[[goc in i for i in fp_pd['goc']]]
            
            for i in fp_pd_goc['sum_assd']:
                grand_total_sum += float(i)
    
    return grand_total_sum

        
end_time = time.time()

# print(f'ELAPSED: {round((end_time - start_time) * 1000,2)} ms')
# print(f"Sum of DV # of pol = {pol_num()}")
# print(f"Sum of DV sum assured = {int(round(sum_ass(),0))}")
# print(fp_pd)




