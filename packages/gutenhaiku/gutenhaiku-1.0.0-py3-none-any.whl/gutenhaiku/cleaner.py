"""
from:
https://github.com/kiasar/gutenberg_cleaner/blob/master/LICENSE.md

MIT License

Copyright (c) 2019 Peyman Mohseni Kiasari

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
"""

from __future__ import absolute_import, unicode_literals
from builtins import str
import os

TEXT_START_MARKERS = frozenset(
    (
        "*END*THE SMALL PRINT",
        "*** START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
        "This etext was prepared by",
        "E-text prepared by",
        "Produced by",
        "Distributed Proofreading Team",
        "Proofreading Team at http://www.pgdp.net",
        "http://gallica.bnf.fr)",
        "      http://archive.org/details/",
        "http://www.pgdp.net",
        "by The Internet Archive)",
        "by The Internet Archive/Canadian Libraries",
        "by The Internet Archive/American Libraries",
        "public domain material from the Internet Archive",
        "Internet Archive)",
        "Internet Archive/Canadian Libraries",
        "Internet Archive/American Libraries",
        "material from the Google Print project",
        "*END THE SMALL PRINT",
        "***START OF THE PROJECT GUTENBERG",
        "This etext was produced by",
        "*** START OF THE COPYRIGHTED",
        "The Project Gutenberg",
        "http://gutenberg.spiegel.de/ erreichbar.",
        "Project Runeberg publishes",
        "Beginning of this Project Gutenberg",
        "Project Gutenberg Online Distributed",
        "Gutenberg Online Distributed",
        "the Project Gutenberg Online Distributed",
        "Project Gutenberg TEI",
        "This eBook was prepared by",
        "http://gutenberg2000.de erreichbar.",
        "This Etext was prepared by",
        "This Project Gutenberg Etext was prepared by",
        "Gutenberg Distributed Proofreaders",
        "Project Gutenberg Distributed Proofreaders",
        "the Project Gutenberg Online Distributed Proofreading Team",
        "**The Project Gutenberg",
        "*SMALL PRINT!",
        "More information about this book is at the top of this file.",
        "tells you about restrictions in how the file may be used.",
        "l'authorization à les utilizer pour preparer ce texte.",
        "of the etext through OCR.",
        "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
        "We need your donations more than ever!",
        " *** START OF THIS PROJECT GUTENBERG",
        "****     SMALL PRINT!",
        '["Small Print" V.',
        "      (http://www.ibiblio.org/gutenberg/",
        "and the Project Gutenberg Online Distributed Proofreading Team",
        "Mary Meehan, and the Project Gutenberg Online Distributed Proofreading",
        "                this Project Gutenberg edition.",
    )
)

TEXT_END_MARKERS = frozenset(
    (
        "*** END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
        "***END OF THE PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "End of The Project Gutenberg",
        "Ende dieses Project Gutenberg",
        "by Project Gutenberg",
        "End of Project Gutenberg",
        "End of this Project Gutenberg",
        "Ende dieses Projekt Gutenberg",
        "        ***END OF THE PROJECT GUTENBERG",
        "*** END OF THE COPYRIGHTED",
        "End of this is COPYRIGHTED",
        "Ende dieses Etextes ",
        "Ende dieses Project Gutenber",
        "Ende diese Project Gutenberg",
        "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
        "Fin de Project Gutenberg",
        "The Project Gutenberg Etext of ",
        "Ce document fut presente en lecture",
        "Ce document fut présenté en lecture",
        "More information about this book is at the top of this file.",
        "We need your donations more than ever!",
        "END OF PROJECT GUTENBERG",
        " End of the Project Gutenberg",
        " *** END OF THIS PROJECT GUTENBERG",
    )
)

LEGALESE_START_MARKERS = frozenset(("<<THIS ELECTRONIC VERSION OF",))

LEGALESE_END_MARKERS = frozenset(("SERVICE THAT CHARGES FOR DOWNLOAD",))


def strip_headers(text, progress_bar):
    """Remove lines that are part of the Project Gutenberg header or footer.
    Note: The original version of the code can be found at:
    https://github.com/c-w/gutenberg/blob/master/gutenberg/cleanup/strip_headers.py
    Args:
        text (unicode): The body of the text to clean up.
    Returns:
        unicode: The text with any non-text content removed.
    """

    lines = text.splitlines()
    sep = str(os.linesep)

    out = []
    i = 0
    footer_found = False
    ignore_section = False

    with progress_bar(lines) as gen:
        for line in gen:
            reset = False

            if i <= 600:
                # Check if the header ends here
                if any(line.startswith(token) for token in TEXT_START_MARKERS):
                    reset = True

                # If it's the end of the header, delete the output produced so far.
                # May be done several times, if multiple lines occur indicating the
                # end of the header
                if reset:
                    out = []
                    continue

            if i >= 100:
                # Check if the footer begins here
                if any(line.startswith(token) for token in TEXT_END_MARKERS):
                    footer_found = True

                # If it's the beginning of the footer, stop output
                if footer_found:
                    break

            if any(line.startswith(token) for token in LEGALESE_START_MARKERS):
                ignore_section = True
                continue
            elif any(line.startswith(token) for token in LEGALESE_END_MARKERS):
                ignore_section = False
                continue

            if not ignore_section:
                out.append(line.rstrip(sep))
                i += 1

    return sep.join(out)
