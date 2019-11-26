#!python
# by courtesy of HuangYi @ 20110424
import sys
import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime
from suds import WebFault

data = sys.argv[1]
c = sys.argv[2]

def DAVIDtermenrich(listF, idType, bgF="/nfs/home/students/chit/Thesis/data/bg_hs.txt", resF='', bgName = 'Background1',listName='List1', category = ''):
    from suds.client import Client
    import os
   
    if len(listF) > 0 and os.path.exists(listF):
        inputListIds = ','.join(open(listF).read().split('\n'))
        print ('List loaded.')     
    else:
        print ('No list loaded.')

        
    flagBg = False
    if len(bgF) > 0 and os.path.exists(bgF):
        inputBgIds = ','.join(open(bgF).read().split('\n'))
        flagBg = True
        print ('Use file background.')
    else:
        print ('Use default background.')
        
    url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    client = Client(url, location = "https://david.ncifcrf.gov/webservice/services/DAVIDWebService")
    client.wsdl.services[0].setlocation('https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/')
    print ('User Authentication:',client.service.authenticate('ge75nij@mytum.de'))

    listType = 0
    print ('Percentage mapped(list):', client.service.addList(inputListIds,idType,listName,listType))
    if flagBg:
        listType = 1
        print ('Percentage mapped(background):', client.service.addList(inputBgIds,idType,bgName,listType))

    print ('Use categories:', client.service.setCategories(category))
    #getTermClusteringReport
    overlap=3
    initialSeed = 3
    finalSeed = 3
    linkage = 0.5
    kappa = 50
    termClusteringReport = client.service.getTermClusterReport(overlap, initialSeed, finalSeed, linkage, kappa)
    
    #parse and print report
    totalRows = len(termClusteringReport)
    print ('Total clusters:',totalRows)
    resF = listF + '.termClusteringReport.txt'
    with open(resF, 'w') as fOut:
        i = 0
        fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\tenrichmentscore\tcluster\n')
        for simpleTermClusterRecord in termClusteringReport:
            i = i+1
            EnrichmentScore = simpleTermClusterRecord.score
            for simpleChartRecord in  simpleTermClusterRecord.simpleChartRecords:
                categoryName = simpleChartRecord.categoryName
                termName = simpleChartRecord.termName
                listHits = simpleChartRecord.listHits
                percent = simpleChartRecord.percent
                ease = simpleChartRecord.ease
                Genes = simpleChartRecord.geneIds
                listTotals = simpleChartRecord.listTotals
                popHits = simpleChartRecord.popHits
                popTotals = simpleChartRecord.popTotals
                foldEnrichment = simpleChartRecord.foldEnrichment
                bonferroni = simpleChartRecord.bonferroni
                benjamini = simpleChartRecord.benjamini
                FDR = simpleChartRecord.afdr
                rowList =[categoryName,termName,str(listHits),str(percent),str(ease),Genes,str(listTotals),str(popHits),str(popTotals),str(foldEnrichment),str(bonferroni),str(benjamini),str(FDR),str(EnrichmentScore),str(i)]
                fOut.write('\t'.join(rowList)+'\n')
    print ('write file:', resF, 'finished!')

if __name__ == '__main__':
    try:
        DAVIDtermenrich(listF = '/nfs/home/students/chit/Thesis/results/{}/clust{}.txt'.format(data,c), idType = 'ENSEMBL_GENE_ID', listName = 'clust{}'.format(c), category = 'abcd,BBID,BIOCARTA,COG_ONTOLOGY,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE,GOTERM_MF_FAT,GOTERM_CC_FAT,GOTERM_BP_FAT')
    except WebFault as detail:
        print(detail)

