# word_doc_services application

This app is all the logic for interractions with the Word Document.

It uses the Python-Docx package, and in some cases uses the Oxml to edit a doc where certain functionality
is not supported by the package (noted in code comments).

Docx documentation can be found here: https://python-docx.readthedocs.io/en/latest/ at time of writing.

## Create

All creation methods are in creating_document.py.

This file contains all methods for paragraph and table creation.

The main class, BusinessCaseWordDocumentWrapper, is a wrapper around a Document which allows
us to interract with the document using predefined methods which will handle formatting, colours etc.

While it's not impossible to work directly with the doc as a result of going through the wrapper,
this approach is discouraged and can lead to errors. You should use the methods that exist, or crete new ones,
so the logic is contained here.


## Read

All read methods are contained in parsing_document.py.
Also contains logic for submitting the data to the models.

This file contains all the methods for reading:
    Paragraphs
    Tables

Other items are not currently supported but could include:
    Embedded Documents
    Pictures
    etc.

Items that are not supported are silently ignored.

We also grab the Summary data as a separate section while we're reading the doc.
This is needed for a separate screen.


