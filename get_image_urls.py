
import requests
import os
import yaml
from IPython.display import display, HTML

type_data = 'records_uuid'
with open('{0}.txt'.format(type_data), 'rb') as file:
    data = file.readlines()
    list_uuid = [li.split('\n')[0] for li in data]

urls_list=[]

test_url = 'http://hh.worldmap.harvard.edu/registry/hypermap/layer'

for i in range(len(list_uuid)):
    print "Progress {0} / {1}".format(i+1,len(list_uuid))
    print "Percentage: {0} %".format((i+1)/len(list_uuid)*100.0)

    response = requests.get('{0}/{1}/map/config'.format(test_url, list_uuid[i]))
    try:
        yaml_text = yaml.load(response.content)
        sources = yaml_text['sources']['default_source']
        req = sources['req']
        url_image=('http://hh.worldmap.harvard.edu/registry/hypermap/layer/{0}/map/service?'
                   'LAYERS={1}&FORMAT=image%2Fpng&SRS=EPSG%3A4326'
                   '&EXCEPTIONS=application%2Fvnd.ogc.se_inimage&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&'
                   'REQUEST=GetMap&STYLES=&BBOX={2}&WIDTH=200&HEIGHT=150')
        if 'coverage' in sources:
            coverage = yaml_text['sources']['default_source']['coverage']
            bbox_req = coverage['bbox']
        else:
            bbox_req = '-180,-90,180,90'
        if 'layers'in yaml_text:
            lay_name = yaml_text['layers'][0]['name']
        urls_list.append(url_image.format(list_uuid[i],lay_name,bbox_req))
    except Exception as e:
        pass
with open('urls_image.txt', 'wb') as f:
    for item in urls_list:
         f.write("%s\n" % item)
