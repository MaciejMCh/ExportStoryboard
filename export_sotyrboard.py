import sys
import os, os.path
import xml.etree.ElementTree



def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]

storyboardsDirPath = sys.argv[1]
outputFilePath = sys.argv[2]

result = "import UIKit\n\n"
for storyboard in [i for i in os.listdir(storyboardsDirPath) if i.endswith('.storyboard')]:
    root = xml.etree.ElementTree.parse(storyboardsDirPath + "/" + storyboard).getroot()
    for viewController in root.iterfind('.//viewController'):
        attributes = viewController.attrib
        customClass = attributes.get("customClass")
        if customClass:
            result += "extension " + customClass + " {\n"
            result += "\tenum Segue {\n"

            connections = viewController.find('connections')
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