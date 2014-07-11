# Library from https://github.com/nikipore/alfred-python
import alfred
import re
import unicodedata
import xml.dom
import xml.dom.minidom
import time

# XML verbs db
conjFR = xml.dom.minidom.parse('conjugation-fr.xml')
verbsFR = xml.dom.minidom.parse('verbs-fr.xml')

conjList = conjFR.getElementsByTagName('template')
verbList = verbsFR.getElementsByTagName('v')

usrInput = u'{query}'
pronoms =["je","tu","il/elle","nous","vous","ils/elles"]
results = []

# function to get template
def getTemplate( str ):
  for v in verbList :
    i = v.getElementsByTagName('i')[0].firstChild.nodeValue
    t = v.getElementsByTagName('t')[0].firstChild.nodeValue
    if i.encode('utf-8') == str.encode('utf-8') :
      return(t)

#go for template
template = getTemplate(usrInput)
#check template value
if (template != None) :
  templateSplit = template.split(':')
  radical = usrInput.replace(templateSplit[1], "")
  termina = templateSplit[1]

# loop to check conj list
for v in conjList :
  line = v.attributes['name'].value
  if template == line:
    # we are in the verb
    # we need to extract the verb
    # from
    momentoNode = v.getElementsByTagName('indicative')
    # get each conj
    for tiempoNode in momentoNode :
      #for present
      personas = tiempoNode.getElementsByTagName('present')
      for personaNode in personas :
        persona = personaNode.getElementsByTagName('i')
        idx = 0
        # let s add the verbs to an arrat for alfred use
        for i in persona :
          item = alfred.Item({'uid': idx, 'arg': radical + i.firstChild.nodeValue}, radical + i.firstChild.nodeValue, pronoms[idx])
          results.append(item)
          idx += 1

xml = alfred.xml(results)
alfred.write(xml)