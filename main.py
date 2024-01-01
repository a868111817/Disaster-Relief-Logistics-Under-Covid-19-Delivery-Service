#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

import sp_model 
from util import to_range, DATA_PATH, FIG_PATH, OptimizationMethod
from sp_model import SET, PARAMETER

if __name__ == "__main__":
    # %%
    d = dict()
    w = 0.1
    eps = [7,8]
    m, obj1, obj2 = sp_model.solve(1, OptimizationMethod.WEIGHTED_SUM)
    obj1_star = obj1.getValue() 
    m, obj1, obj2 = sp_model.solve(0, OptimizationMethod.WEIGHTED_SUM)
    obj2_star = obj2.getValue()
    objstars = [obj1_star, obj2_star]



    # for w in np.arange(0.01, 0.2, 0.01):
    spm, o1, o2 = sp_model.solve(w,
                OptimizationMethod.LP_METRIC,
                single_objval = objstars, eps = eps)
    alpha, beta = [], [] 
    for j in to_range(SET['J']):
        alpha_j = spm.getVarByName(f'alpha[{j}]').x
        beta_j = spm.getVarByName(f'beta[{j}]').x
        alpha.append(alpha_j)
        beta.append(beta_j)
        d[str(w)] = {'#RDC': sum(alpha), '#CS': sum(beta)}
    # ============================ 
    # soldict = {} 
    # for rdc_num in to_range(SET['J']):
    #     eps = [rdc_num, 15 - rdc_num - 1] 
    #     model = sp_model.solve(w,
    # In[2]:


    for j in to_range(SET['J']):
    for c in to_range(SET['C']):
        for s in to_range(SET['S']): 
            delta = spm.getVarByName('delta[0,0,0]').x
            if delta != 0 :
                print(f'j={j}, c={c}, s={s}, delta={delta}')


    # In[3]:


    # get supplier names 
    import pandas as pd 
    PATH_PREFIX = 'MoDRL_'
    df_supplier = pd.read_csv(DATA_PATH 
    + f'/{PATH_PREFIX}supplier.csv')
    suppliers = df_supplier['Suppliers'].values 

    df_distance = pd.read_csv(DATA_PATH + f'/{PATH_PREFIX}distance.csv')
    AA = df_distance.columns.values
    J = AA
    print(suppliers)
    print(AA)
    Commodities = ['Water', 'Food', 'Shelter']


    # ### $\alpha_j, \beta_j$ Build RDC/CS or not 

    # In[5]:


    from sp_model import SET, PARAMETER
    alpha, beta = [], [] 
    for j in to_range(SET['J']):
        alpha_j = spm.getVarByName(f'alpha[{j}]').x
        beta_j = spm.getVarByName(f'beta[{j}]').x
        # alpha_i: build RDC or not 
        # beta_i: build CS or not
        alpha.append(alpha_j)
        beta.append(beta_j)
        # print(AA[i], alpha_i, beta_i)
    build_df = pd.DataFrame({'RDC': alpha, 'CS': beta}, index=AA)
    build_df = build_df.transpose() 
    build_df


    # In[6]:


    print(f'RDC #: {sum(alpha)}')
    print(f'CS #: {sum(beta)}')


    # In[7]:


    i, j, k, k_prime, s, c = [len(idx) for idx in SET.values()]
    import numpy as np 
    Q = np.zeros((i, j, c))
    X = np.zeros((i, j, c, s))
    Y = np.zeros((j, k, c, s))


    # ### $Q_{ijc}, X_{ijcs}$ transported commodities to RDC/CS

    # In[8]:


    ## in preparedness phase 
    ## get Q_ijc: Sup to RDC/CS
    for i in to_range(SET['I']):
        for j in to_range(SET['J']):
            for c in to_range(SET['C']):
                Q[i, j, c] = spm.getVarByName(f'Q[{i},{j},{c}]').x
                if Q[i, j, c] > 0: 
                    print(f'Supplier {suppliers[i]} => {J[j]} {Commodities[c]} : {Q[i, j, c]}') 


    # In[ ]:


    ## response phase 
    #  get X_ijcs: Sup to RDC/CS in response phase 
    print('======= RDC =======')
    for i in to_range(SET['I']):
        for j in to_range(SET['J']):
            for c in to_range(SET['C']):
                s_vec = np.zeros(len(SET['S']))
                for s in to_range(SET['S']):
                    X[i, j, c, s] = spm.getVarByName(f'X[{i},{j},{c},{s}]').x
                    s_vec[s] = X[i, j, c, s] 
                if np.sum(s_vec) != 0 and alpha[j]: 
                    print(f'{suppliers[i]} => {AA[j]}', Commodities[c], s_vec)


    # In[9]:


    import os 
    from copy import deepcopy
    from util import RESULT_PATH

    def PrecisionTuple(x):
        return '(' + ', '.join(('%.1f' % f) for f in x) + ')'


    Xfilename = os.path.join(RESULT_PATH, 'X_ijcs.csv')

    print(f'======= CS =======')
    rowdict = {} 
    for i in to_range(SET['I']):
        for c in to_range(SET['C']):
            row = np.zeros((len(SET['J']))).tolist()
            for j in to_range(SET['J']):
                s_vec = np.zeros(len(SET['S']))
                for s in to_range(SET['S']):
                    X[i, j, c, s] = spm.getVarByName(f'X[{i},{j},{c},{s}]').x
                    s_vec[s] = X[i, j, c, s] 
                # if np.sum(s_vec) != 0 and beta[j]:
                #     print(f'{suppliers[i]} => {AA[j]}', Commodities[c], s_vec)
                if np.sum(s_vec) != 0:
                    row[j] = PrecisionTuple(s_vec) 
                else: row[j] = '-'
            rowname = f'{suppliers[i]}_{Commodities[c]}'
            rowdict[rowname] = deepcopy(row)

    rowdict = {k: v for k, v in sorted(rowdict.items(), key=lambda item: item[0])}
    Xijcs = pd.DataFrame.from_dict(rowdict, orient = 'index', columns=AA)
    Xijcs = Xijcs.round(2)
    Xijcs 
    Xijcs.to_csv(Xfilename)


    # ### $Y_{jkcs}$ transported commodities to AA

    # In[10]:


    def isNotZero(x):
        return abs(x) > 1e-6

    import os 
    from copy import deepcopy
    from util import RESULT_PATH

    Yfilename = os.path.join(RESULT_PATH, 'Y_jkcs.csv')
    rowdict = {} 
    for j in to_range(SET['J']):
        if not (alpha[j] or beta[j]):
            continue 
    
        for c in to_range(SET['C']):
            
            row = np.zeros((len(SET['K']))).tolist()
            for k in to_range(SET['K']):
                
                s_vec = np.zeros(len(SET['S']))
                for s in to_range(SET['S']):
                    Y[j, k, c, s] = spm.getVarByName(f'Y[{j},{k},{c},{s}]').x
                    s_vec[s] = Y[j, k, c, s] 
                # if np.sum(s_vec) != 0: 
                    # print(f'{suppliers[i]} => {AA[j]}', Commodities[c], s_vec)
                if np.sum(s_vec) != 0: 
                    print(f'{suppliers[i]} => {AA[j]}', Commodities[c], s_vec)
                    row[k] = PrecisionTuple(s_vec) 
                else: 
                    row[k] = '-'
            rowname = f'{J[j]}_{Commodities[c]}'
            rowdict[rowname] = deepcopy(row)

    rowdict = {k: v for k, v in sorted(rowdict.items(), key=lambda item: item[0])}
    Yjkcs = pd.DataFrame.from_dict(rowdict, orient = 'index', columns=AA)
    Yjkcs.to_csv(Yfilename)


    # ### $I_{kcs}$: the inventory held at AA k for commod c under s 
    # ### $b_{kcs}$: the shortage held at AA k for commod c under s  

    # In[11]:


    k, c, s = len(SET['K']), len(SET['C']), len(SET['S'])
    I = np.zeros((k, c, s))
    b = np.zeros((k, c, s))


    rows_i = {} 
    rows_b = {}
    for c in to_range(SET['C']): 
        row_i = []
        row_b = []

        for k in to_range(SET['K']):
            s_vec_i = np.zeros(len(SET['S'])) 
            s_vec_b = np.zeros(len(SET['S'])) 
            for s in to_range(SET['S']):
                I[k, c, s] = spm.getVarByName(f'I[{k},{c},{s}]').x
                b[k, c, s] = spm.getVarByName(f'b[{k},{c},{s}]').x

                s_vec_i[s] = I[k, c, s] 
                s_vec_b[s] = b[k, c, s]
            if np.sum(s_vec_i) == 0: 
                row_i.append('-')
            else:  
                row_i.append(PrecisionTuple(s_vec_i))
            if np.sum(s_vec_b) == 0:
                row_b.append('-')
            else:
                row_b.append(PrecisionTuple(s_vec_b))

        rowname = f'{Commodities[c]}'
        rows_i[rowname] = deepcopy(row_i) 
        rows_b[rowname] = deepcopy(row_b)

    b_kcs = pd.DataFrame.from_dict(rows_b, orient = 'index', columns=AA)
    Bfilename = os.path.join(RESULT_PATH, 'b_kcs.csv')
    b_kcs.to_csv(Bfilename)
    i_kcs = pd.DataFrame.from_dict(rows_i, orient = 'index', columns=AA)
    Ifilename = os.path.join(RESULT_PATH, 'I_kcs.csv')
    i_kcs.to_csv(Ifilename)




