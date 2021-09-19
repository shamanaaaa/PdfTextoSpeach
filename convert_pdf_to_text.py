from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1


def total_pages(file):
    file = open(file, 'rb')
    parser = PDFParser(file)
    document = PDFDocument(parser)
    # This will give you the count of pages
    return (resolve1(document.catalog['Pages'])['Count'])


def convert_pdf_to_txt(path, current_page):
    rsrc_mgr = PDFResourceManager()
    ret_str = StringIO()
    'utf-8'
    la_params = LAParams()
    device = TextConverter(rsrc_mgr, ret_str, laparams=la_params)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrc_mgr, device)
    password = ""
    max_pages = 0
    page_count = 0
    caching = True
    page_nos = set()
    for page in PDFPage.get_pages(fp, page_nos, maxpages=max_pages, password=password, caching=caching, check_extractable=True):
        page_count += 1
        if current_page == page_count:
            interpreter.process_page(page)
    fp.close()
    device.close()
    string = ret_str.getvalue()
    ret_str.close()
    return string

