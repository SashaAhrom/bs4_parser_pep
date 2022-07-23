from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATSNEW = 'whatsnew/'
PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DOWNLOAD = 'download.html'
TAG_SECTION = 'section'
TAG_DIV = 'div'
TAG_LI = 'li'
TAG_A = 'a'
TAG_H1 = 'h1'
TAG_DL = 'dl'
TAG_DD = 'dd'
TAG_UL = 'ul'
TAG_TABLE = 'table'
TAG_TR = 'tr'
TAG_TD = 'td'
TITLE_WHATSNEW = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
TITLE_LATEST_VERSIONS = ('Ссылка на документацию', 'Версия', 'Статус')
TITLE_PEP = ('Статус', 'Количество')
BOTTOM_NAME = 'Total'
PATERN_VERSIONS_STATUS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
FORMAT_CODE = 'utf-8'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
