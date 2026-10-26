"""Check the generated site without third-party Python dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path('_site')
BASE = '/LJT-Homepage'
HOST = 'spanellisnikolaos564-max.github.io'
EXPECTED = {'index.html', 'publications/index.html'}
TITLES = (
    'SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond',
    'On the Perception Bottleneck of VLMs for Chart Understanding',
    'On the Universal Truthfulness Hyperplane Inside LLMs',
    'In-Context Sharpness as Alerts: An Inner Representation Perspective for Hallucination Mitigation',
    'C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models',
    'Composing Parameter-Efficient Modules with Arithmetic Operations',
)
CONTACTS = {
    'mailto:jliugi@connect.ust.hk',
    'https://github.com/Vicent0205',
    'https://scholar.google.com/citations?hl=en&user=tbK9jl4AAAAJ&view_op=list_works&sortby=pubdate',
    'https://x.com/junteng88716710',
}


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.text = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ('href', 'src'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if attrs.get('id'):
            self.ids.add(attrs['id'])

    def handle_data(self, data):
        self.text.append(data)


actual = {str(path.relative_to(ROOT)) for path in ROOT.rglob('*.html')}
assert actual == EXPECTED, f'Unexpected page output: {actual ^ EXPECTED}'
docs = {path: Document((ROOT / path).read_text()) for path in EXPECTED}
for path, doc in docs.items():
    text = ' '.join(' '.join(doc.text).split())
    for title in TITLES:
        assert title in text, f'Missing publication on {path}: {title}'
    assert CONTACTS <= set(doc.links), f'Missing contact link on {path}'
    for placeholder in ('Your Name', 'Your Sidebar Name', 'Red Brick University',
                        'none@example.org', 'Paper Title Number', 'John Doe'):
        assert placeholder not in text, f'Template placeholder on {path}'
    for link in doc.links:
        parsed = urlsplit(link)
        if parsed.scheme not in ('', 'http', 'https'):
            continue
        if parsed.netloc and parsed.netloc != HOST:
            continue
        if not parsed.path:
            target = path
        else:
            assert parsed.path == BASE or parsed.path.startswith(BASE + '/'), (
                f'Project baseurl missing on {path}: {link}'
            )
            target = unquote(parsed.path[len(BASE):]).lstrip('/')
            target_path = ROOT / target
            if target_path.is_dir():
                target_path /= 'index.html'
            assert target_path.is_file(), f'Broken internal link on {path}: {link}'
            target = str(target_path.relative_to(ROOT))
        if parsed.fragment and target in docs:
            assert unquote(parsed.fragment) in docs[target].ids, f'Broken anchor: {link}'

home = ' '.join(' '.join(docs['index.html'].text).split())
for detail in ('Junteng Liu', 'Junxian He', 'HKUST NLP Group',
               'Shanghai Jiao Tong University', 'June 2024',
               'Ph.D. in Computer Science', 'B.Eng.',
               'MINIMAX', 'Tencent WXG', 'Shanghai AI Lab',
               'Zifei Shan', 'Yu Cheng', 'Zhiyuan Honor Scholarship',
               'LLM Reasoning and Reinforcement Learning',
               'Hallucination in Vision-Language Models',
               'LLM truthfulness and Interpretability'):
    assert detail in home, f'Missing About detail: {detail}'
print('PASS: exactly two pages; all six publications on both; memory details and links verified.')
