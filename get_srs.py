from hypermap.aggregator.models import Layer
from hypermap.aggrefator.models import Service
from collections import Counter 
import csv


uuids=[]
list_srs=[] 

for layer in Layer.objects.all():                      
    uuids.append(str(layer.uuid))                                     
    list_srs.append(sorted (layer.service.srs.values_list('code',flat=True)))


#get all srs into one unique list
ll=[x for sub  in list_srs for  x in sub] 
#count per srs
count=Counter(ll)
with open ('srs_test.csv','wb') as csvfile:
    writer = csv.writer(csvfile,delimiter=' ')
    for w in range (len(uuids)):
        string=" ".join(str(e) for e in list_srs[w])
        writer.writerow([uuids[w], string])
        
