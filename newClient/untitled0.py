#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime

errors = 0

setup_logging()

logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    
print ('url=%s' % url)

#
# create a service client using the wsdl.
#
client = Client(url, location = "https://david.ncifcrf.gov/webservice/services/DAVIDWebService")
client.wsdl.services[0].setlocation('https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/')
#
# print the service (introspection)
#
#print client

#authenticate user email 
client.service.authenticate('ge75nij@mytum.de')

#add a list 

inputIds = ','.join(open('/home/chit/Desktop/Thesis/results/27.05/clust31.txt').read().split('\n'))


idType = 'ENSEMBL_GENE_ID'
listName = 'make_up'
listType = 0
print (client.service.addList(inputIds, idType, listName, listType))

#print client.service.getDefaultCategoryNames()
# setCategories
#categorySting = str(client.service.setCategories('BBID,BIOCARTA,COG_ONTOLOGY,GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE'))

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
resF = 'list1.termClusteringReport.txt'
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
            rowList = [categoryName,termName,str(listHits),str(percent),str(ease),Genes,str(listTotals),str(popHits),str(popTotals),str(foldEnrichment),str(bonferroni),str(benjamini),str(FDR),str(EnrichmentScore),str(i)]
            fOut.write('\t'.join(rowList)+'\n')
print ('write file:', resF, 'finished!')

