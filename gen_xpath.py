import bs4
from bs4 import BeautifulSoup
import re
from parsel import Selector
import time
from loguru import logger


class Xpath:
    def __init__(self, selector, soup, string):
        self.known_attribute_list = ['id', 'class', 'name', 'placeholder', 'value', 'title', 'type']
        self.selector = selector
        self.soup = soup
        self.string = string

    def gen_components(self, components, parent, child, key=None, value=None) -> list:
        """
        倒序查询tag的父级标签
        @param components: list of tag
        @param parent:
        @param child:
        @param key: attr
        @param value: attr's value
        @return:
        """
        xpath_str = f'{child.name}[@{key}="{value}"]' if key and value else child.name
        siblings = parent.find_all(child.name, {key: value}, recursive=False)
        components.insert(0, xpath_str if 1 == len(siblings) else '%s[%d]' % (
            xpath_str, next(i for i, s in enumerate(siblings, 1) if s is child)
        ))
        return components

    def condition(self, tag) -> bs4.Tag:
        """
        返回包含查询字符串的标签
        @param tag: 文档中每一个tag
        @return: 符合条件的tag
        """
        s = ''.join(list(tag.stripped_strings))
        s = re.sub(r'[\s|\n]', '', s)
        if self.string.findall(s):
            return tag

    def get_xpath(self, element, is_single_tag: bool) -> dict:
        """

        @param element: 包含所需字符串的标签
        @param is_single_tag: 查询字符串是否在同一个标签中
        @return:
        """
        full_xpath = ''
        components = []
        child = element if element.name else element.parent
        shortest_xpath, longest_xpath = '', ''
        result = {}
        for parent in child.parents:
            key, value = '', ''
            for k, v in child.attrs.items():
                if k in self.known_attribute_list:
                    if isinstance(v, list):
                        v = ' '.join(v)
                    key, value = k, v
                    break
            components = self.gen_components(components, parent, child, key, value)
            components_str = '/'.join(components)
            xpath = f'//{components_str}/text()'
            if key and value:
                if is_single_tag:
                    try:
                        res = self.selector.xpath(xpath).getall()
                        if len(res) == 1:
                            full_xpath = f'//{components_str}/text()'
                    except Exception as e:
                        logger.error(e)
                else:
                    full_xpath = f'//{components_str}/*/text()'
                if not shortest_xpath:
                    shortest_xpath = xpath
                    result['shortest_xpath'] = full_xpath
            child = parent
        if not result.get('shortest_xpath', ''):
            result['shortest_xpath'] = ''
        result['longest_xpath'] = '/%s' % '/'.join(components)
        return result

    def filter_tag(self, tags) -> list:
        """
        过滤出最小标签
        :param tags:过滤之前的 tags
        :return:过滤后的 tags
        """
        tags = list(reversed(tags))
        filter_tags = []
        temp = []
        for index, elem in enumerate(tags, start=1):
            temp.append(elem)
            if index == len(tags):
                filter_tags.append(temp[0])
                temp.clear()
                break
            if elem.parent is tags[index]:
                continue
            else:
                filter_tags.append(temp[0])
                temp.clear()
        return filter_tags

    def run(self):
        tags = self.soup.find_all(self.condition)
        tags = self.filter_tag(tags)
        logger.info(f'在网页中找到{len(tags)}处该字符串')
        result = []
        for index, elem in enumerate(tags, start=1):
            is_single_tag = True if len(elem.contents) == 1 else False
            logger.info(f'尝试获取第{index}处的xpath')
            res = self.get_xpath(elem, is_single_tag)
            result.append(res)
        return result


class Test:
    def __init__(self, strings: str, html: str):
        self.selector = Selector(html)
        self.strings = re.compile(re.escape(re.sub(r'[\s|\n]', '', strings)))
        self.soup = BeautifulSoup(html, 'lxml')

    def start(self):
        xpath = Xpath(self.selector, self.soup, self.strings)
        result = xpath.run()
        re.purge()
        return result


if __name__ == '__main__':
    with open('test/htmls/wangyi.html', 'r', encoding='utf-8') as f:
        html = f.read()
    strings = r'''联播+｜'''
    # strings = '联播+｜推动我国数字经济健康发展 习近平作出最新部署'
    start_time = time.time()
    t = Test(strings, html)
    t.start()
    logger.info(f'用时：{time.time() - start_time}')
