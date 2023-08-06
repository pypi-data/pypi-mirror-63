from typing import List, Union
import subprocess
import tempfile
from io import StringIO, BytesIO, BufferedReader
import re
import os
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter,PDFPageAggregator
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

pdf_default_layout = LAParams(boxes_flow=0, line_margin=0.5)

def parse_pdf_text(pdf_file, 
                     password:str = '',
                     page_numbers:List[int] = None,
                     maxpages:int = 0,
                     caching:bool = True,
                     codec:str = 'utf-8', 
                     laparams:LAParams = pdf_default_layout, 
                     check_extractable:bool = False,**kwargs) -> str:
    """Parse and return the text contained in a PDF file.
    This is a modification of the extract_text function that comes
    with pdfminer.highlevel
    
    Args:
    pdf_file (str): Path to the PDF file to be worked on
    password (str, optional): For encrypted PDFs, the password to decrypt.
    page_numbers (List[int], optional): List of zero-indexed page numbers 
        to extract.
    maxpages (int, optional): The maximum number of pages to parse
    caching (bool, optional): If resources should be cached
    codec (str, optional): Text decoding codec.
    laparams (LAParams, optional): An LAParams object from pdfminer.layout.
        If None, uses some default settings that often work well.
    check_extractable (bool, optional): checks flags in pdf, for whether
        pdf should be extractable. Ignore flag and just extract by default.
        
    Returns:
    A string containing all of the text extracted.
    """
    if laparams is None:
        laparams = LAParams()

    with open(pdf_file, "rb") as fp, StringIO() as output_string:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, codec=codec,
                               laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(
                fp,
                page_numbers,
                maxpages=maxpages,
                password=password,
                caching=caching,
                check_extractable=check_extractable,
        ):
            interpreter.process_page(page)

        return output_string.getvalue()

def parse_pdf_bytes(input_io: Union[BytesIO, BufferedReader], 
                     password:str = '',
                     page_numbers:List[int] = None,
                     maxpages:int = 0,
                     caching:bool = True,
                     codec:str = 'utf-8', 
                     laparams:LAParams = pdf_default_layout, 
                     check_extractable:bool = False,**kwargs) -> str:
    """
    Parse PDF directly from bytes IO/Buffered IO.
    Do not require a filepath. Helpful when PDF is already
    in memory and can't be save to a dir.
    e.g. Dash app uploaded files.
    
    Args:
    input_io (BytesIO, BufferedReader): binary IO/stream for PDF to be processed.
    password (str, optional): For encrypted PDFs, the password to decrypt.
    page_numbers (List[int], optional): List of zero-indexed page numbers 
        to extract.
    maxpages (int, optional): The maximum number of pages to parse
    caching (bool, optional): If resources should be cached
    codec (str, optional): Text decoding codec.
    laparams (LAParams, optional): An LAParams object from pdfminer.layout.
        If None, uses some default settings that often work well.
    check_extractable (bool, optional): checks flags in pdf, for whether
        pdf should be extractable. Ignore flag and just extract by default.
        
    Returns:
    A string containing all of the text extracted.
    """
    if laparams is None:
        laparams = LAParams()

    with StringIO() as output_string:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, codec=codec,
                               laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(
            input_io,
            page_numbers,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=check_extractable,
            ):
            interpreter.process_page(page)
        input_io.close()
        return output_string.getvalue()

    
    
    
    

def repair_pdf(pdf_file:str, output_path:str) -> None:
    """Use ghostscript to repair pdf file
    Args:
    pdf_file (str): Path to PDF file to be worked on
    output_path (str): filename & path to which repaired pdf will be saved
    
    Return:
    None, repaired pdf saved at specified output path
    """
    args = ["gs",
            "-o",
            f"{output_path}", 
            "-sDEVICE=pdfwrite", 
            "-dPDFSETTINGS=/prepress", 
            f"{pdf_file}"]
    gs_process = subprocess.Popen(args,stderr=subprocess.PIPE)
    gs_process.wait()
    #out, err = gs_process.communicate()
    #print(out,err)
    
    
def cleanup_paragraph(page_text:str)->str:
    """Use regex to combine paragraphs,
    
    Args:
    page_text (str): 
    
    Return:
    
    """
    page_paragraphs=page_text.split("\n\n")
    combined_paragraphs = [*map(lambda x: re.sub(r"(\s)?\n"," ",re.sub(r"-\n","",x))\
                           ,page_paragraphs)]
    return "\n".join(combined_paragraphs)


def extract_pdf(pdf_file:str, 
                gs_repair:bool=True, 
                output_raw:bool=False,
                **kwargs)->str:
    """extract PDF file using pdfminer 
    Try to extract pdf text using parse_pdf_text.
    If pdf file is broken, try to repair it with gs.
    
    Args:
    pdf_file (str): Path to PDF file to be worked on
    gs_repair (bool, optional): Whether to use ghostscript
        for repairing pdf fonts
    output_raw (bool, optional): whether to output raw
        extractd text, instead of combining paragraphs 
        using regex.
    kwargs: additional keyword arguments will be passed 
        into extract_pdf_text as text extraction options,
        For kwargs that would be used, check extract_pdf_text.
    
    Return:
    String parsed from PDF.
    Paragraphs grouped together, seperated by `\n`
    pages seperated by `<Page_break>`
    """
    def _get_pagelist(file, pages=None):
        with open(file, "rb") as f:
            number_of_pages = len([page for page in PDFPage.get_pages(fp=f,check_extractable=False)])
        if pages is None:
            pagelist = [i for i in range(number_of_pages)]
        else:
            pagelist = [i for i in pages if 0<=i<number_of_pages]
        return pagelist
    
    page_nums = kwargs.get("page_numbers")
    kwargs.pop("page_numbers",None)
    try:
        pagelist = _get_pagelist(pdf_file,page_nums)
        text = [parse_pdf_text(pdf_file, page_numbers =[i], **kwargs) for i in pagelist]
    except:
        if not gs_repair:
            return ("")
        print("Attempting to use ghostscript to repair pdf")
        with tempfile.TemporaryDirectory() as tmpdir:
            repair_filepath = os.path.join(tmpdir,"tmp_repairfile.pdf")
            repair_pdf(pdf_file, repair_filepath)
            pagelist = _get_pagelist(repair_filepath,page_nums)
            text = [parse_pdf_text(repair_filepath, page_numbers =[i], **kwargs) for i in pagelist]
            
    if not output_raw:
        text = [cleanup_paragraph(page_text) for page_text in text]
        
    return "\n\n".join(text)
    
extract = extract_pdf
