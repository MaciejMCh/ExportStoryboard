
import sys
import os, os.path
import xml.etree.ElementTree

def upperfirst(x):
    return x[0].upper() + x[1:]

def camelCase(st):
    if len(st.split(" ")) == 1:
        return upperfirst(st)
    output = ''.join(x for x in st.title() if x.isalpha())
    result = output[0].lower() + output[1:]
    return upperfirst(result)

storyboardsDirPath = sys.argv[1]
outputFilePath = sys.argv[2]

result = "// https://github.com/MaciejMCh/ExportStoryboard\n\n"
result += "import UIKit\n\n"
for storyboard in [i for i in os.listdir(storyboardsDirPath) if i.endswith('.storyboard')]:
    root = xml.etree.ElementTree.parse(storyboardsDirPath + "/" + storyboard).getroot()
    for viewController in root.iterfind('.//viewController'):
        attributes = viewController.attrib
        customClass = attributes.get("customClass")
        if customClass:
            connections = viewController.find('connections')
            if connections is not None:
                if len(connections.findall('segue')) > 0:
                    result += "extension " + customClass + " {\n"
                    result += "\tenum Segue {\n"

                    for segue in connections.findall('segue'):
                        segueIdentifier = segue.get('identifier')
                        result += "\t\tcase " + camelCase(segueIdentifier) + "\n"

                    result += "\n\t\tfunc identifier() -> String {\n"
                    result += "\t\t\tswitch(self) {\n"
                    for segue in connections.findall('segue'):
                        segueIdentifier = segue.get('identifier')
                        result += "\t\t\tcase ." + camelCase(segueIdentifier) + ": return \"" + segueIdentifier + "\"\n"
                    result += "\t\t\t}\n"
                    result += "\t\t}\n"
                    result += "\t}\n"
                    result += "\tfunc navigate(segue: Segue) {\n"
                    result += "\t\tperformSegueWithIdentifier(segue.identifier(), sender: self)\n"
                    result += "\t}\n"
                    result += "}\n\n"

f = open(outputFilePath, 'w+')
f.write(result)
