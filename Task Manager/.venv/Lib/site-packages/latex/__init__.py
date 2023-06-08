import re
import os
from random import randrange
from cStringIO import StringIO
from StringIO import StringIO as n_StringIO
from subprocess import Popen
from shutil import rmtree
from shutil import copyfile
from tempfile import mkdtemp
from tempfile import gettempdir
from os.path import exists

class File():
    """Define a File to be attached to LatexDocument
    """
    filepath = None
    file_object = None
    name = ""

    def __init__(self, fileorpath, name, check=True):
        if isinstance(fileorpath, str) or isinstance(fileorpath, unicode):
            if check and not exists(fileorpath):
                raise OSError("%s does not exist" % fileorpath)
            self.filepath = fileorpath
        elif type(fileorpath) == file:
            self.file_object = fileorpath
        else:
            raise ValueError("Give absolute filepath or StringIO object")
        self.name = name

    def get_file(self):
        """Give file object
        """
        if self.filepath:
            return open(self.filepath, 'rb')
        else:
            return self.file_object


class LatexDocument():
    """Defines a LaTeX document
    """
    document_class = ""
    document_class_opts = []
    # packages = {"packagename" : ["opt1", "opt2=3"]}
    packages = {}
    preamble = ""
    document = ""
    files = []

    class LatexDocumentParseError(Exception):
        pass

    class LatexPdfGenerationError(Exception):
        pass

    def parse(self, latex):
        """Parse LaTeX text
        """
        # DocumentClass & options
        match = re.search(r"\\documentclass\[?(?P<options>[\w,= ]*)\]?{(?P<documentclass>\w*)}", latex)
        if match:
            results = match.groupdict()
            self.document_class = results["documentclass"]
            self.document_class_opts = results["options"].split(",")

        # Packages
        match = re.findall(r"\\usepackage\[?(?P<options>[\w,= ]*)\]?{(?P<pkg>\w*)}", latex)
        if match:
            self.packages = {}
            for opt, package in match:
                self.packages[package] = [x.strip() for x in opt.split(",")]
        #print self.packages

        # Preamble
        preamble = re.sub(r"(?im)^ *\\documentclass\[?[\w,= ]*\]?{\w*}.*\r?\n", "", latex)
        preamble = re.sub(r"(?im)^ *\\usepackage\[?[\w,= ]*\]?{\w*}.*\r?\n", "", preamble)
        preamble = re.sub(r"(?ism)^ *\\begin{document}.*", "", preamble)
        self.preamble = preamble

        # Document
        match = re.search(r"(?ism)\\begin{document}(.*)^ *\\end{document}", latex)
        if match:
            self.document = match.groups()[0]

    def as_latex(self):
        """Print LaTeX Document
        """
        latex = ""
        # DocumentClass & options
        if self.document_class:
            opts = ",".join(self.document_class_opts)
            latex += "\documentclass[%s]{%s}\n" % (opts, self.document_class)

        # Packages
        for package, opts in self.packages.items():
            opts = ", ".join(opts)
            latex += "\usepackage[%s]{%s}\n" % (opts, package)

        # Preamble
        if self.preamble:
            latex += self.preamble

        # Document
        if self.document:
            latex += "\\begin{document}\n"
            latex += self.document
            latex += "\\end{document}\n"
        return latex

    def add_file(self, fileorpath, name):
        """Add file for pdf generation
        """
        self.files.append(File(fileorpath, name))

    def as_pdf(self, debug=False):
        """Render latex document in pdf
        """
        directory = mkdtemp()
        rand = randrange(100000, 999999)
        ltxfile = "%s.tex" % rand
        ltxpath = os.path.join(directory, ltxfile)
        pdffile = "%s.pdf" % rand
        pdfpath = os.path.join(directory, pdffile)
        try:
            f = open(ltxpath, 'wb')
            f.write(self.as_latex())
            f.close()
            # Add files
            for afile in self.files:
                f = open(os.path.join(directory, afile.name), 'wb')
                f.write(afile.get_file().read())
                f.close()

            from subprocess import PIPE
            cmd = ["pdflatex", "-halt-on-error", "-interaction=batchmode", "%s" % ltxfile]
            p = Popen(cmd, stdout=PIPE, cwd=directory)
            p.wait()
            # Double compilation because of table of content and indexes
            p = Popen(cmd, stdout=PIPE, cwd=directory)
            p.wait()
            if not os.path.isfile(pdfpath):
                if debug:
                    raise self.LatexPdfGenerationError(
                        'pdflatex fail. The pdf file is not generated. Check dir %r manualy' % directory)
                else:
                    raise self.LatexPdfGenerationError('pdflatex fail. The pdf file is not generated.')
            f = open(pdfpath, 'r')
            result = StringIO(f.read())
            f.close()
        finally:
            # clean
            if not debug:
                rmtree(directory)

        return result

    def __add__(self, other):
        # DocumentClass & options
        if not self.document_class:
            self.document_class = other.document_class

        # Add opts is risky
        #tmp_opts = self.document_class_opts
        #for opt in other.document_class_opts:
        #    if opt not in self.document_class_opts:
        #        tmp_opts.append(opt)
        # self.document_class_opts = tmp_opts
        if not self.document_class_opts:
            self.document_class_opts = other.document_class_opts

        # Packages
        for pkg, opts in other.packages.items():
            if pkg not in self.packages.keys():
                self.packages[pkg] = opts

        # Preamble
        # self must be in the end of resulting preamble
        # Because self is the "base"
        self.preamble = other.preamble + self.preamble

        # Document
        self.document += other.document
        return self

    def __str__(self):
        return self.as_latex()

    def __unicode__(self):
        return self.as_latex()

    def __init__(self, text=None):
        """Try to parse latex document
        """
        if text:
            self.parse(text)
