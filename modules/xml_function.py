import xml.etree.ElementTree as ET
from re import sub

def xml_params(response):
	params = []
	root = ET.fromstring(response.content)
	for child in root.iter('*'):
		child = str(child.tag)
		child = sub('{.+}', '', child)
		params.append(child)
	params = list(set(params))
	return params