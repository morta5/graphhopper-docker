#!/usr/bin/env python3
"""Begrenztes Abhängigkeits-Overlay für den festgelegten GraphHopper-Quellstand."""
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ns = 'http://maven.apache.org/POM/4.0.0'
ET.register_namespace('', ns)
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
pom = Path(sys.argv[1])
tree = ET.parse(pom, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
managed = tree.getroot().find(f'{{{ns}}}dependencyManagement/{{{ns}}}dependencies')
assert managed is not None
found = False
for dep in managed:
    if dep.findtext(f'{{{ns}}}artifactId') == 'dropwizard-dependencies':
        version = dep.find(f'{{{ns}}}version')
        assert version.text == '4.0.16', 'Unerwarteter Quellstand'
        version.text = '5.0.2'
        found = True
assert found, 'Dropwizard-Verwaltung fehlt'
entries = [
    ('com.fasterxml.jackson', 'jackson-bom', '2.21.7', True),
    ('org.eclipse.jetty', 'jetty-bom', '12.1.14', True),
    ('com.google.protobuf', 'protobuf-java', '3.25.9', False),
    ('org.apache.httpcomponents.core5', 'httpcore5', '5.4.3', False),
    ('org.apache.httpcomponents.core5', 'httpcore5-h2', '5.4.3', False),
]
for index, (group, artifact, version, bom) in enumerate(entries):
    dep = ET.Element(f'{{{ns}}}dependency')
    values = {'groupId': group, 'artifactId': artifact, 'version': version}
    if bom:
        values.update(type='pom', scope='import')
    for key, value in values.items():
        ET.SubElement(dep, f'{{{ns}}}{key}').text = value
    managed.insert(index, dep)
ET.indent(tree, space='    ')
tree.write(pom, encoding='utf-8', xml_declaration=True)

# Die drei alten generierten Protobuf-Signaturen verwenden einen ungebundenen
# Platzhalter statt ihres vorhandenen Typparameters. Nur diese Signaturen
# anpassen; Felder, Deskriptoren und Drahtformat bleiben identisch.
vector = pom.parent / 'web-bundle/src/main/java/vector_tile/VectorTile.java'
source = vector.read_text()
pattern = r'(public <Type> Builder clearExtension\(\s+com\.google\.protobuf\.GeneratedMessage\.GeneratedExtension<\s+vector_tile\.VectorTile\.Tile(?:\.Value|\.Layer)?, )\?'
source, count = re.subn(pattern, r'\1Type', source)
assert count == 3, 'Unerwartete generierte Protobuf-Signaturen'
vector.write_text(source)

# Unveränderte Snake-Case-Prüfung über die aktuelle Jackson-Konstante.
config_test = pom.parent / 'web-bundle/src/test/java/com/graphhopper/jackson/GraphHopperConfigModuleTest.java'
source = config_test.read_text()
assert source.count('PropertyNamingStrategy.SNAKE_CASE') == 1
config_test.write_text(source.replace('PropertyNamingStrategy.SNAKE_CASE',
                      'com.fasterxml.jackson.databind.PropertyNamingStrategies.SNAKE_CASE'))
