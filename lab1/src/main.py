from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("../results/shkola.xml")
        os.remove("../results/tennismag.xml")
        os.remove("../results/tennismag.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('shkola')
    process.crawl('tennismag')
    process.start()


def task2():
    print("Amount of text elements in all pages of shkola.com.ua")
    root = etree.parse("../results/shkola.xml")
    pages = root.xpath("//page")
    for page in pages:
        print(page.xpath("count(fragment[@type='text'])"))


def task3_4():
    print("Products of internet shop tennismag.ua")
    transform = etree.XSLT(etree.parse("tennismag.xsl"))
    result = transform(etree.parse("../results/tennismag.xml"))
    result.write("../results/tennismag.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("../results/tennismag.xhtml"))


if __name__ == '__main__':
    cleanup()
    scrap_data()
    print("Scraping completed")
    while True:
        print("*" * 50)
        print("1. Task 2")
        print("2. Task 3 and 4")
        print("> ", end='', flush=True)
        number = input()
        if number == "1":
            task2()
        elif number == "2":
            task3_4()
        else:
            break
