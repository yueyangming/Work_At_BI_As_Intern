import lxml


import xml.etree.ElementTree as ETree
filename = 'Simple_xml.xml'

f = open(filename, 'rt')

tree = ETree.parse(f)
root = tree.getroot()
print('root.tag =', root.tag)
# print('root.attrib =', root.attrib)

for child in root:      # 仅可以解析出root的儿子，不能解析出root的子孙
    print(child.tag, '\n')
    for each_child in child:
        print(each_child.tag)
        print(each_child.text)

    # print(child.attrib) # attrib is a dict

# for element in root.iter('environment'):
#     print(element.attrib)