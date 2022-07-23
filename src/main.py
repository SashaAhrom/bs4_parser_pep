import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, BOTTOM_NAME, DOWNLOAD, EXPECTED_STATUS,
                       MAIN_DOC_URL, PATERN_VERSIONS_STATUS, PEP_URL, TAG_A,
                       TAG_DD, TAG_DIV, TAG_DL, TAG_H1, TAG_LI, TAG_SECTION,
                       TAG_TABLE, TAG_TD, TAG_TR, TAG_UL,
                       TITLE_LATEST_VERSIONS, TITLE_PEP, TITLE_WHATSNEW,
                       WHATSNEW)
from outputs import control_output, wrong_status
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, WHATSNEW)
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(
        soup,
        TAG_SECTION,
        attrs={'id': 'what-s-new-in-python'}
    )
    div_with_ul = find_tag(
        main_div,
        TAG_DIV,
        attrs={'class': 'toctree-wrapper'}
    )
    sections_by_python = div_with_ul.find_all(
        TAG_LI,
        attrs={'class': 'toctree-l1'}
    )
    results = [TITLE_WHATSNEW]
    for section in tqdm(sections_by_python, desc='whats new'):
        version_a_tag = find_tag(section, TAG_A)
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, TAG_H1)
        dl = find_tag(soup, TAG_DL)
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, TAG_DIV, attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all(TAG_UL)
    for ul in tqdm(ul_tags, desc='All versions'):
        if 'All versions' in ul.text:
            a_tags = ul.find_all(TAG_A)
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [TITLE_LATEST_VERSIONS]
    for a_tag in tqdm(a_tags, desc='finally way'):
        link = a_tag['href']
        text_match = re.search(PATERN_VERSIONS_STATUS, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, DOWNLOAD)
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, features='lxml')
    table_tag = find_tag(soup, TAG_TABLE, {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag,
        TAG_A,
        {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, features='lxml')
    section = find_tag(soup, TAG_SECTION, attrs={'id': 'pep-content'})
    rows = section.find_all(TAG_TR,
                            attrs={'class': re.compile(r'row-(even|odd)')})
    main_page = {}
    for row in tqdm(rows, desc='main page pep'):
        td_one_line = row.find_all(TAG_TD)
        if len(td_one_line) == 4 and td_one_line[1].text != '':
            td_href = find_tag(td_one_line[1], TAG_A)
            href = td_href['href']
            if href not in main_page:
                if len(td_one_line[0].text) == 2:
                    status = td_one_line[0].text[-1]
                else:
                    status = ''
                main_page[href] = status
    count_pep = {}
    wrong_pep = []
    for href, status in tqdm(main_page.items(),
                             desc='collection from personal page'):
        pep_link = urljoin(PEP_URL, href)
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, features='lxml')
        title = find_tag(
            soup,
            TAG_DL,
            attrs={'class': 'rfc2822 field-list simple'}
        )
        page_status = find_tag(
            title,
            string='Status').find_next(TAG_DD).text
        if page_status not in EXPECTED_STATUS.get(status):
            wrong_pep.append((pep_link, page_status, EXPECTED_STATUS[status]))
        if page_status in count_pep:
            count_pep[page_status] += 1
        else:
            count_pep[page_status] = 1
    results = [TITLE_PEP]
    all_sum = 0
    for status, count in count_pep.items():
        results.append((status, count))
        all_sum += count
    results.append((BOTTOM_NAME, all_sum))
    wrong_status(wrong_pep)
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
