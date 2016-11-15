import requests
import os
import yaml
from IPython.display import display, HTML
import csv 

type_data = 'records_uuid'
with open('{0}.txt'.format(type_data), 'rb') as file:
    data = file.readlines()
    list_uuid = [li.split('\n')[0] for li in data]

if not os.path.isdir(type_data):
    os.mkdir(type_data)

#validate from mapproxy
#0 if is a valid mapproxy config - it returns a yaml, 1 if its invalid
valid_config= [0 for i in range (len(list_uuid))]
#0 if it is between -180,-90, 180, 90, 1 if it is outside that range or is None
valid_bbox = [0 for i in range (len(list_uuid))

test_url = 'http://hh.worldmap.harvard.edu/registry/hypermap/layer'

for i in range(len(list_uuid)):
    response = requests.get('{0}/{1}/map/config'.format(test_url, list_uuid[i]))
    
    try:
        yaml_text = yaml.load(response.content)
        wms = yaml_text['services']['wms']
        bbox = wms['bbox'].split(',')
        bbox_x0 = bbox[0]
       	bbox_y0 = bbox[1]
        bbox_x1 = bbox[2]
        bbox_y1 = bbox[3]
        if bbox_x0=='None' or bbox_y0=='None' or bbox_x1=='None' or bbox_y1=='None':
            valid_bbox[i]=1
        else:
        	bbox_x0 = float(bbox_x0)
       		bbox_y0 = float(bbox_y0)
        	bbox_x1 = float(bbox_x1)
        	bbox_y1 = float(bbox_y1)
            if (abs(bbox_x0)>180.0) and (abs(bbox_x1)>180.0) and (abs(bbox_y0)>90) and (abs(bbox_y1)>90):
                valid_bbox[i]=1
        
    except Exception as e:
        #it means it is invalid from mapproxy config
        valid_config[i]=1


with open('new_test_mapproxy.csv', 'wb') as f:
    writer = csv.writer(f,delimiter=' ')
    rows = zip(list_uuid,valid_config,valid_bbox)
    for row in rows:
        writer.writerow(row)
