import os, fnmatch

import numpy as np

import matplotlib.pyplot as plt

import miletos
import ephesos
import tdpy
from tdpy import summgene


# global object
gdat = tdpy.gdatstrt()

## time stamp
gdat.strgtimestmp = tdpy.retr_strgtimestmp()

print('Anomalous transit search pipeline started at %s.' % gdat.strgtimestmp)

# get the Composite Planetary Systems table from the NASA Exoplanet Archive
gdat.dictexartarg = ephesos.retr_dictexar()

# list of names of planetary systems with transiting planets
listnamesyst = gdat.dictexartarg['namesyst']
indx = np.where(gdat.dictexartarg['booltran'])[0]
listnamesyst = listnamesyst[indx]
listnamesyst = np.unique(listnamesyst)
numbsyst = len(listnamesyst)
print('%d systems will be processed...' % numbsyst)

# define paths
gdat.pathbase = os.environ['MERGEN_DATA_PATH'] + '/seti/'
gdat.pathdata = gdat.pathbase + 'data/'
gdat.pathimag = gdat.pathbase + 'imag/'
gdat.pathdatafracineg = gdat.pathdata + 'fracineg/'

# make folders
for attr, valu in gdat.__dict__.items():
    if attr.startswith('path'):
        os.system('mkdir -p %s' % valu)

# settings
## seed
np.random.seed(0)

## plotting
gdat.typefileplot = 'pdf'

# input dictionary to miletos
dictmileinpt = dict()
#dictmileinpt['verbtype'] = 0
dictmileinpt['pathbasetarg'] = gdat.pathbase
#### Boolean flag to use PDC data
dictmileinpt['listtypeanls'] = []
dictmileinpt['typedataspoc'] = 'PDC'
dictmileinpt['boolplottser'] = False
dictmileinpt['boolplotprio'] = False
dictmileinpt['boolplotprop'] = False
dictmileinpt['boollspe'] = False
#### SDE threshold for the pipeline to search for periodic boxes
dictmileinpt['dictsrchpboxoutp'] = {'thrssdee': 0.}
#dictmileinpt['verbtype'] = 0
#dictmileinpt['boolsrchsingpuls'] = True

dictexar = ephesos.retr_dictexar()
listtici = np.empty_like(listnamesyst, dtype=int)
for k, name in enumerate(listnamesyst):
    indx = np.where(dictexar['namesyst'] == name)[0][0]
    tici = dictexar['tici'][indx]
    listtici[k] = tici

liststrgsyst = np.empty_like(listnamesyst)
for k, namesyst in enumerate(listnamesyst):
    liststrgsyst[k] = ''.join(namesyst.split(' '))

for k, name in enumerate(listnamesyst):
    path = gdat.pathdatafracineg + 'fracineg_%s_0000.csv' % liststrgsyst[k]
    
    if not os.path.exists(path):
        # call miletos to analyze data
        print('Calling miletos.init() to analyze and model the data for the target...')
        dictmileoutp = miletos.init( \
                                  ticitarg=listtici[k], \
                                  strgexar=listnamesyst[k], \
                                  labltarg=listnamesyst[k], \
                                  epocprio=np.random.rand(5), \
                                  boolplot=False, \
                                  typeprioplan='exar', \
                                  **dictmileinpt, \
                                 )
        
        if not 'numbcomp' in dictmileoutp:
            continue
        for j in range(dictmileoutp['numbcomp']):
            path = gdat.pathdatafracineg + 'fracineg_%s_%04d.csv' % (liststrgsyst[k], j)
            print('Writing to %s...' % path)
            fracineg = dictmileoutp['fracineg%04d' % j]
            np.savetxt(path, fracineg)
    
    else:
        for j in range(dictexar['numbplantranstar'][k]):
            path = gdat.pathdatafracineg + 'fracineg_%s_%04d.csv' % (liststrgsyst[k], j)
            if os.path.exists(path):
                print('Reading from %s...' % path)
                fracineg = np.loadtxt(path)
                listfracineg.append(fracineg)

# read files
listfracineg = []
listnamefile = fnmatch.filter(os.listdir(gdat.pathdatafracineg), 'fracineg_*.csv')
for namefile in listnamefile:
    path = gdat.pathdatafracineg + namefile
    print('Reading from %s...' % path)
    fracineg = np.loadtxt(path)
    listfracineg.append(fracineg)

fracineg = [[] for k in range(2)]
for k in range(2):
    fracineg[k] = [temp[k] for temp in listfracineg]
    fracineg[k] = np.array(fracineg[k])
    fracineg[k] = fracineg[k][np.where(fracineg[k] > 0)]
    fracineg[k] -= 1.
    fracineg[k] *= 1e3
    fracineg[k] -= np.mean(fracineg[k])
fracineg[0] += 2.
fracineg[1] += 4.

# plot the histograms of ingress and egress anomalies
for limt in [5, 100]:
    figr, axis = plt.subplots(figsize=(6, 4))
    bins = np.linspace(-limt, limt, 100)
    axis.hist(fracineg[0], color='r', alpha=0.3, bins=bins, label='Ingress')
    axis.hist(fracineg[1], color='b', alpha=0.3, bins=bins, label='Egress')
    axis.set_yscale('log')
    axis.set_ylabel('N')
    axis.set_xlabel(r'$\Delta f$ [ppt]')
    axis.legend()
    path = gdat.pathimag + 'fracineg%04d.pdf' % limt
    print('Writing to %s...' % path)
    plt.savefig(path)
    plt.close()

