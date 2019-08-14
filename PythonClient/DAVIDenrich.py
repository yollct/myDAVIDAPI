#! python
import sys

data = sys.argv[1]
c = sys.argv[2]

def DAVIDenrich(listF, idType, bgF='', resF='', bgName = "/home/chit/Desktop/Thesis/data/bg_hs.txt",listName='List1', category = '', thd=0.1, ct=2):
    from suds.client import Client
    import os
   
    if len(listF) > 0 and os.path.exists(listF):
        inputListIds = ','.join(open(listF).read().split('\n'))
        print ('List loaded.' )       
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
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print ('Total chart records:',chartRow)
    
    if len(resF) == 0 or not os.path.exists(resF):
        if flagBg:
            resF = listF + '.withBG.chartReport'
        else:
            resF = listF + '.chartReport'
    with open(resF, 'w') as fOut:
        fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
        for row in chartReport:
            rowDict = dict(row)
            categoryName = str(rowDict['categoryName'])
            termName = str(rowDict['termName'])
            listHits = str(rowDict['listHits'])
            percent = str(rowDict['percent'])
            ease = str(rowDict['ease'])
            Genes = str(rowDict['geneIds'])
            listTotals = str(rowDict['listTotals'])
            popHits = str(rowDict['popHits'])
            popTotals = str(rowDict['popTotals'])
            foldEnrichment = str(rowDict['foldEnrichment'])
            bonferroni = str(rowDict['bonferroni'])
            benjamini = str(rowDict['benjamini'])
            FDR = str(rowDict['afdr'])
            rowList = [categoryName,termName,listHits,percent,ease,Genes,listTotals,popHits,popTotals,foldEnrichment,bonferroni,benjamini,FDR]
            fOut.write('\t'.join(rowList)+'\n')
        print ('write file:', resF, 'finished!')


if __name__ == '__main__':
	DAVIDenrich(listF = '/home/chit/Desktop/Thesis/results/{}/clust{}.txt'.format(data,c), idType = 'ENSEMBL_GENE_ID', listName = 'clust{}'.format(c), category = 'abcd,BBID,BIOCARTA,COG_ONTOLOGY,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE,GOTERM_MF_FAT,GOTERM_CC_FAT,GOTERM_BP_FAT')

