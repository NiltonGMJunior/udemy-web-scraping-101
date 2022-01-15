from lxml import etree

# Using find and findall methods
# tree = etree.parse("fundamentals/src/web_page.html")
# title_element = tree.find("head/title")
# print(title_element.text)

# paragraph_element = tree.find("body/p")
# print(paragraph_element.text)

# list_items = tree.findall("body/ul/li")
# for li in list_items:
#     a = li.find("a")
#     if a is not None:
#         print(f"{li.text.strip()} {a.text.strip()}")
#     else:
#         print(li.text.strip())

# Using XPath
# tree = etree.parse("fundamentals/src/web_page.html")
# title_element = tree.xpath("//title/text()")[0]
# print(title_element)

# paragraph_element = tree.xpath("//p/text()")[0]
# print(paragraph_element)

# list_items = tree.xpath("//li")
# for li in list_items:
#     text = " ".join(map(str.strip, li.xpath(".//text()")))
#     print(text)

# Using CSS Selectors
tree = etree.parse("fundamentals/src/web_page.html")
html = tree.getroot()
title_element = html.cssselect("title")[0]
print(title_element.text)

paragraph_element = html.cssselect("p")[0]
print(paragraph_element.text)

list_items = html.cssselect("li")
for li in list_items:
    a = li.cssselect("a")
    if a:
        print(f"{li.text.strip()} {a[0].text.strip()}")
    else:
        print(li.text)