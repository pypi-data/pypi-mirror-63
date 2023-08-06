#!/usr/bin/python
"""
Copyright 2015 Hippos Technical Systems BV.
Module 'external' within package 'abcraft' relates to the various
command processors (abc2midi etc.) which are executed by abccraft, and to
their assocated widgets and methods.
"""
import re, sys, locale, ghostscript
from .. import (Shared, dbg_print)
from ..raft.external import External, encoding


class Ps2PDF(External):
    tabName = True  # = hitch-hike with previously created sibling, abcm2ps.
    fmtNameIn = '%s.ps'
    fmtNameOut = '%s.pdf'
    exec_file = None  # 'ps2pdf'
    reMsg = r'.*'

    def process(self, triggerFileName, **kw):
        return External.process(self, triggerFileName, **kw)

    def cmd(self, inF, outF, stdout=None, stderr=None, **kw):
        if self.exec_file is not None:  # external approach required?
            dbg_print(1, 'doing ps->pdf conversion extenally')
            return External.cmd(self, inF, outF,
                                stdout=stdout, stderr=stderr)
        else:
            dbg_print(1, 'doing ps->pdf conversion intenally')
            args = [arg.encode(encoding) for arg in [
                "ps2pdf",  # actual value doesn't matter
                "-dCompatibilityLevel=1.4 ", "-q",
                "-dNOPAUSE", "-dBATCH", "-dSAFER",
                "-sDEVICE=pdfwrite",
                "-sstdout=%stderr",
                f"-sOutputFile={outF}",
                "-f", inF
            ]]
            ghostscript.Ghostscript(*args, stdout=stdout, stderr=stderr)
            ghostscript.gs.exit(ghostscript.__instance__)
            return None  # no external command needs to be executed.

    def fixup(self, output, error):
        if self.exec_file is None:
            output += f"internal ps->PDF conversion was used\n"
        elif len(output)<4:
            output += f"('{self.exec_file}' doesn't say much if everything goes well!)\n"
        return output, error


class Abcm2ps(External):
    """
class Abcm2ps - in our usage - relates only to the use of abcm2ps to produce
postscript (as opposed to svg) output. This is currently unused (see
'Abcm2svg' below.)
    """
    fmtNameIn  = '%s.abc'
    fmtNameOut = '%s.ps'
    exec_file = 'abcm2ps'
    reMsg = r'.*'

    def __init__(self):
        External.__init__(self)
        self.outFile_CRE = re.compile("Output written on\s+(\S.*)\s\(.*")

    def cmd(self, inF, outF, stdout=None, stderr=None, **kw):
        return External.cmd(self, '-A', '-O', outF, inF)

    def fixup(self, output, error):
        return output, error


class Abcm2svg(Abcm2ps):
    fmtNameOut = '%s_page_.svg'
    reMsg = r'.*\:(\d+)\:(\d+)\:\s\.*'
    # reMsg = r'.*in\s+line\s(\d+)\.(\d+).*'
    rowColOrigin = (0, 0)

    def __init__(self):
        External.__init__(self)
        self.outFile_CRE = re.compile("Output written on\s+(\S.*)\s\(.*")

    def cmd(self, inF, outF, stdout=None, stderr=None, **kw):
        return External.cmd(self, '-k 640 -v -A -O', outF, inF)

    def fixup(self, output, error):
        # just look for the output file names:
        svgList = []
        for either in (output, error):
            for line in either.split('\n'):
                match = self.outFile_CRE.match(line)
                if match:
                    svgList.append(match.group(1))
        dbg_print(1, svgList)
        if svgList:
            Shared.abcRaft.score.useFiles(svgList)
            Shared.raft.displayBook.setCurrentWidget(Shared.abcRaft.score)
        return output, error


class Abc2midi(External):

    fmtNameIn  = '%s.abc'
    fmtNameOut = '%s.midi'
    exec_file = 'abc2midi'
    showOut = False
    reMsg = r'.*in\s+line-char\s(\d+)\-(\d+).*'
    rowColOrigin = (0, 0)
    
    def cmd(self, inF, outF, stdout=None, stderr=None, **kw):
        return External.cmd(self, inF, '-v', '-EA', '-o', outF)

    def fixup(self, output, error):
        return '', output+error

class Abc2abc(External):
    
    fmtNameIn  = '%s.abc'
    fmtNameOut = '%.0stransposed.abc'  # sneakily don't use basename at all!
    exec_file = 'abc2abc'
    showOut = False
    reMsg = r'(%Warning|%Error).*'

    def cmd(self, inF, outF, stdout=None, stderr=None, transpose=None, **kw):
        pp = [inF, '-OCC', '-r']
        if transpose is not None:
            pp += ['-t', str(transpose)]
        return External.cmd(self, *pp, *kw)

    def fixup(self, output, error):
        new_error = ''
        new_output = ''
        for line in output.split('\n'):
            if self.creMsg.match(line):
                new_output = new_output[:-1]
                new_output = new_output[1:]
                new_error += ('line %d: ' % (1+new_output.count('\n')) + line + '\n')
                
            else:
                new_output += (line + '\n')
        self.stdTab.creMsg = re.compile(r'.*line\s+(\d+)\:.*')
        return new_output, new_error
