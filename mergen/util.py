import os

import numpy as np
import sklearn.decomposition

import tdpy


def exec_prca_skit(listvarb, numbcomp=None, verbtype=2):
    '''
    Execute PCA decomposition using sklearn
    '''
    
    objtprca = sklearn.decomposition.PCA(n_components=numbcomp)
    objtprca.fit(listvarb)
    sklearn.decomposition.PCA(n_components=2)
    
    dictprca = dict()

    dictprca['variexpl'] = objtprca.explained_variance_ratio_
    dictprca['valusing'] = objtprca.singular_values_
    dictprca['vecteige'] = objtprca.components_

    if verbtype > 1:
        print('variexpl')
        print(dictprca['variexpl'])
        print('valusing')
        print(dictprca['valusing'])
        print('vecteige')
        print(dictprca['vecteige'])

    return dictprca


def prca(matr):
    '''
    Execute PCA decomposition
    '''
    
    M = (matr - mean(matr.T, 1)).T
    eigl, eigt = linalg.eig(cov(M))
    tranmatr = dot(eigt.T, M).T
    
    return eigl, tranmatr, eigt


def test_prca():
    '''
    Test PCA decomposition
    '''
    
    numbsamp = 10000
    numbpara = 2
    indxpara = np.arange(numbpara)
    meanpara = np.random.randn(numbpara)
    covapara = np.random.rand(numbpara**2).reshape((numbpara, numbpara))
    listvarb = np.random.multivariate_normal(meanpara, covapara, size=numbsamp)
    
    listlablpara = [[r'$\theta_{%d}$' % n, ''] for n in indxpara]
    pathbase = os.environ['MERGEN_DATA_PATH'] + '/'
    pathimag = pathbase + 'imag/'
    strgplot = 'multnomi'
    
    dictprca = exec_prca(listvarb, numbcomp=1)
    listvectplot = [[meanpara[0], meanpara[1], dictprca['vecteige'][0, 0], dictprca['vecteige'][0, 1]]]
    tdpy.plot_grid(pathimag, strgplot, listvarb, listlablpara, listvectplot=listvectplot, boolsqua=True)
    
    dictprca = exec_prca(listvarb)
    listvectplot = [ \
                    [meanpara[0], meanpara[1], dictprca['vecteige'][0, 0], dictprca['vecteige'][0, 1]], \
                    [meanpara[0], meanpara[1], dictprca['vecteige'][1, 0], dictprca['vecteige'][1, 1]], \
                   ]
    tdpy.plot_grid(pathimag, strgplot, listvarb, listlablpara, listvectplot=listvectplot, boolsqua=True)



