import dominate
from dominate.tags import *
from dominate.util import raw
from dominate.svg import *
from pathlib import Path


HTML_FILE_PATH = Path(__file__).parent.parent / 'FormatConverter' / 'feed.html'


def main():
    doc = dominate.document(title='RSS Reader')

    with doc.head:
        link(rel='stylesheet', href='style.css')
        script(type='text/javascript', src='script.js')

    with doc:
        with div().add(ol()):
            for i in ['home', 'about', 'contact']:
                li(a(i.title(), href='/%s.html' % i))

    with doc:
        div("Dauren1")['id'] = 'header'
        div("Dauren2", data_employee='101011')
        ulist = ol()
        for item in range(4):
            ulist += li('Item #', item)
        ul(li(a(name, href=link), __pretty=False) for name, link in [('Dauren', 'Dauren')])
        div(raw('<a href="#">Example</a>'))
        with svg(height=100, width=100):
            circle(r=40, stroke_width=3, cx=50, cy=50, stroke='black', fill='red')

    with open(HTML_FILE_PATH, 'w') as fw:
        fw.write(doc.render())


if __name__ == '__main__':
    main()
