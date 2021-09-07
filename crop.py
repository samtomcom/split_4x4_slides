from PyPDF2 import PdfFileWriter, PdfFileReaderimport sys
import os

IN_FILE = sys.argv[1]
TMP_FILE = '__TMP_PDF.pdf'
OUT_FILE = IN_FILE.split('.')[0] + '_1x1.pdf'


def iter_page(pdf):
    pages = pdf.getNumPages()
    for i in range(pages):
        yield pdf.getPage(i)

def crop(page, x1, y1, x2, y2):
    page.cropBox.lowerLeft = x1, y1
    page.cropBox.upperRight = x2, y2
    return page

with open(IN_FILE, 'rb') as in_f:
    pdf = PdfFileReader(in_f)
    duplicate_pages = PdfFileWriter()

    # duplicate each page 4 times
    for page in iter_page(pdf):
        duplicate_pages.addPage(page)
        duplicate_pages.addPage(page)
        duplicate_pages.addPage(page)
        duplicate_pages.addPage(page)
            
    with open(TMP_FILE, 'wb') as inter_f:
        duplicate_pages.write(inter_f)
    
with open(TMP_FILE, 'rb') as inter:
    pdf = PdfFileReader(inter)
    final_out = PdfFileWriter()
    
    count = 0
    for page in iter_page(pdf):
        Ax, Ay, Bx, By = page.mediaBox.lowerLeft + page.mediaBox.upperRight
        Cx, Cy = ((Ax+Bx)/2, (Ay+By)/2)
        
        if count % 4 == 0:
            final_out.addPage(crop(page, Ax, Cy, Cx, By))
        elif count % 4 == 1:
            final_out.addPage(crop(page, Cx, Cy, Bx, By))
        elif count % 4 == 2:
            final_out.addPage(crop(page, Ax, Ay, Cx, Cy))
        else:
            final_out.addPage(crop(page, Cx, Ay, Bx, Cy))
        
        count += 1
            
    with open(OUT_FILE, 'wb') as out_f:
        final_out.write(out_f)

os.remove(TMP_FILE)
