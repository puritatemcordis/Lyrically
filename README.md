# Lyrically

Python scripts that converts music sheets in PDF format into images (JPEG) which is converted into a text file using tesseract OSR. The test set in this repository uses Vietnamese music.

### Getting started
1. Clone app - `git clone https://github.com/puritatemcordis/Lyrically.git`
2. In terminal, run `python lyrically.py [language]` (test set uses: `python lyrically.py vie`)
3. For different test sets, use directory structure:
   * Data set folder
      * Song1 folder
        * music_sheet.pdf
      * Song2 folder
        * music_sheet.pdf
      * ...

### Dependencies
* [tqdm](https://github.com/tqdm/tqdm)
* [pytesseract](https://pypi.org/project/pytesseract/)
* [pdf2image](https://pypi.org/project/pdf2image/)
* [poppler](https://pypi.org/project/python-poppler-qt5/)
