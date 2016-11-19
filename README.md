# PWGen
PWGen is a simple password generator and formater created for the University of Florida CCDC team.

## Requirements

* Python 2.7
* TeXLive or equivalent for PDF generation

## Usage

Generate 90 words in LaTeX _format_ with the _seed_ 'TEST1234':

```
python gen.py --wordlist diceware.wordlist.asc -n 90 --format latex TEST123 "Test Password List" > test.tex
```

Generate 10 words to STDOUT:

```
python gen.py --wordlist diceware.wordlist.asc -n 10 TEST123 "Test Password List"
```

## Generating a PDF
Emit the .tex file and then use PDFLatex or equivalent to create the PDF.

```
$ pdflatex test
This is pdfTeX, Version 3.14159265-2.6-1.40.16 (TeX Live 2015) (preloaded format=pdflatex)
 restricted \write18 enabled.
entering extended mode
(./test.tex
LaTeX2e <2015/01/01>
Babel <3.9l> and hyphenation patterns for 79 languages loaded.
(/usr/local/texlive/2015/texmf-dist/tex/latex/base/article.cls
Document Class: article 2014/09/29 v1.4h Standard LaTeX document class
(/usr/local/texlive/2015/texmf-dist/tex/latex/base/size11.clo))
(/usr/local/texlive/2015/texmf-dist/tex/latex/geometry/geometry.sty
(/usr/local/texlive/2015/texmf-dist/tex/latex/graphics/keyval.sty)
(/usr/local/texlive/2015/texmf-dist/tex/generic/oberdiek/ifpdf.sty)
(/usr/local/texlive/2015/texmf-dist/tex/generic/oberdiek/ifvtex.sty)
(/usr/local/texlive/2015/texmf-dist/tex/generic/ifxetex/ifxetex.sty))

LaTeX Warning: Unused global option(s):
    [pdftex].

No file test.aux.
*geometry* detected driver: pdftex

Overfull \hbox (23.80237pt too wide) in paragraph at lines 14--125
[][] [] []
[1{/usr/local/texlive/2015/texmf-var/fonts/map/pdftex/updmap/pdftex.map}]
(./test.aux) )
(see the transcript file for additional information)</usr/local/texlive/2015/te
xmf-dist/fonts/type1/public/amsfonts/cm/cmr12.pfb></usr/local/texlive/2015/texm
f-dist/fonts/type1/public/amsfonts/cm/cmr17.pfb></usr/local/texlive/2015/texmf-
dist/fonts/type1/public/amsfonts/cm/cmtt10.pfb></usr/local/texlive/2015/texmf-d
ist/fonts/type1/public/amsfonts/cm/cmtt12.pfb>
Output written on test.pdf (1 page, 44152 bytes).
Transcript written on test.log.

$ ls
test.tex   test.pdf
$ open test.pdf
```

[See the example PDF.](/example/test.pdf?raw=true)
