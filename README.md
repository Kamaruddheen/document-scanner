# Document Scanner

To extract text and data from documents like invoices, book pages, tables etc using OpenCV and Tesseract OCR. 

## Overview

The document scanner implements:

- Preprocessing images to improve OCR accuracy
- Contour detection and perspective transforms to isolate ROIs
- Text extraction using PyTesseract 
<!-- - Template matching to identify document types -->

It can handle multiple document types:

- Invoices
- Book pages
- Tables
<!-- - Forms -->
<!-- - Receipts -->

The `dataextractor.py` module contains the core implementation.

## Requirements

The scanner requires:

- OpenCV
- PyTesseract
- NumPy
<!-- - pdf2image (for PDFs) -->

Install requirements using:

```
pip install -r requirements.txt
```

## Examples

The `static/samples/` folder contains example images of different documents.