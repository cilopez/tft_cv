import zipfile
XLSname = "./tft.xlsx"

EmbeddedFiles = zipfile.ZipFile(XLSname).namelist()
ImageFiles = [F for F in EmbeddedFiles if F.count('.png') or F.count('.jpeg') ]

for Image in ImageFiles:
    zipfile.ZipFile(XLSname).extract(Image)