#!/usr/bin/env python3
"""
Copyright 2015 Hippos Technical Systems BV.
Module 'external' within package 'abcraft' relates to the various
command processors (abc2midi etc.) which are executed by abccraft, and to
their assocated widgets and methods.
"""
import logging
logger = logging.getLogger()
import sys, os, re, subprocess, tempfile, locale
from .. import (Shared, dbg_print, QtGui, QtWidgets, head_dir)

encoding = locale.getpreferredencoding()


class StdTab(QtWidgets.QPlainTextEdit):
    """
This once very bare looking class is gradually being embellished with facilities for
error location helpers etc. in due course. It is the class behind the several
tabs (Abcm2svg etc.) within the subprocess output notebook.
    """
    def __init__(self, commander):
        QtWidgets.QPlainTextEdit.__init__(self)
        # self.setFont(commander.font)  # maybe unnecessary - see External.write
        dbg_print(1, self.__class__.__name__+':__init__... commander.reMsg =',
               commander.reMsg)
        self.creMsg = commander.creMsg
        self.rowColOrigin = commander.rowColOrigin
        self.quiet = False
        self.cursorPositionChanged.connect(self.handleCursorMove)

    def handleCursorMove(self):
        # dbg_print(1, self.__class__.__name__+':handleCursorMove... self.quiet =',
        #        self.quiet)
        if self.quiet or self.creMsg is None:
            return
        match = self.creMsg.match(self.textCursor().block().text())
        # dbg_print(1, self.__class__.__name__+':handleCursorMove... match =', match)
        if match is None:
            return
        location = [o1+o2 for (o1, o2) in zip(
                        map(lambda s: int(s), match.groups()),
                       self.rowColOrigin)]

        print ("Autolocating error in ABC", location )
        if location:
            Shared.raft.editBook.moveToRowCol(*location)

    def setPlainText(self, text):
        self.quiet = True
        QtWidgets.QPlainTextEdit.setPlainText(self, text)
        self.quiet = False


class External(object):
    """
'External' is the generic class representing command processors invoked from
within abcraft.
    """
    fmtNameIn  = '%s.in'
    fmtNameOut = '%s.out'
    exec_dir = ''
    exec_file = "base_class_stub_of_exec_file"
    showOut = True
    reMsg = None  # r'$^'  # default = don't match any lines.
    rowColOrigin = (0, -1)
    stdFont = 'Courier New', 10, False, False
    useItalic = False
    tabName = True  # = use class name
    lastStdTab = None

    def __init__(self):
        # Fix up executive directory to be relative to the head directory not the working directory.
        # This behaviour can be circumvened by prefixing path name with './'.
        #
        if self.exec_dir and self.exec_dir[0] not in '/\\.':
            self.exec_dir = os.path.join(head_dir, self.exec_dir)
        self.font = QtGui.QFont(*self.stdFont)
        self.creMsg = (self.reMsg is not None and re.compile(self.reMsg)) or None
        if self.tabName is True:
            self.tabName = self.__class__.__name__
        dbg_print(1, f"??adding tab? name='{self.tabName}'")
        if self.tabName:
            External.lastStdTab = self.stdTab = StdTab(self)
            self.stdTab.setFont(self.font)
            Shared.raft.stdBook.widget.addTab(self.stdTab, self.tabName)
        elif self.tabName is None:
            self.stdTab = External.lastStdTab
        Shared.raft.stdBook.widget.setCurrentWidget(self.stdTab)
        ## phasing out... Shared.raft.editBook.fileSaved.connect(self.process)

    def cmd(self, *pp, stdout=None, stderr=None, **kw):
        answer = ' '.join(((self.exec_dir + self.exec_file),) + pp)
        dbg_print(1, "External commands = ", answer)
        return answer

    def process(self, triggerFileName, **kw):
        dbg_print(1, f"process {triggerFileName}")
        baseName = os.path.splitext(triggerFileName)[0]
        inFileName = (self.fmtNameIn % baseName)
        self.outFileName = self.fmtNameOut % baseName
        outputfile, errorfile = [tempfile.NamedTemporaryFile(
            mode='rb+', suffix='.' + self.__class__.__name__.lower() + '-' + suffix)
                                    for suffix in ('out', 'err')]
        ext_cmd = self.cmd(inFileName, self.outFileName, stdout=outputfile, stderr=errorfile, **kw)
        dbg_print(1, ext_cmd)
        if ext_cmd:
            process = subprocess.Popen(ext_cmd, stdout=outputfile, stderr=errorfile, shell=True)
            process.wait()
        dbg_print(1, f"{self.__class__.__name__}.process 6")
        output, error  = [(file_.seek(0), file_.read().decode(encoding), file_.close())[1]
                          for file_ in  (outputfile, errorfile)]
        dbg_print(1, f"{self.__class__.__name__}.process 7")
        output, error = self.fixup(output, error)
        self.write(out=self.showOut and output or '', err=error, append=False)
        dbg_print(1, f"{self.__class__.__name__}.process 8")
        return output

    def fixup(self, output, error):
        return output, error    # hook function for 're-arranging between output and error.. etc.!

    def write(self, out='', err='', append=True):
        if Shared.bitMaskDebug & 2:
            sys.__stdout__.write(out)
        if Shared.bitMaskDebug & 4:
            sys.__stderr__.write(err)
        if self.stdTab is None:
            dbg_print(1, "self.stdTab is None!")
            return
        if not append:
            self.stdTab.setPlainText('')
        self.stdTab.setFont(self.font)  # to cope with stdout/stderr case.
        tc = self.stdTab.textCursor()
        cf = tc.charFormat()
        for blurb, useItalic in ((out, False),(err, True)):
            if blurb in ('', '\n'): # unjustifiable kludge, perhaps .. but it has the desired effect!
                continue            # compensate for extra new line provided by appendPlainText.
            cf.setFontItalic(useItalic)
            tc.setCharFormat(cf)
            self.stdTab.setTextCursor(tc)
            self.stdTab.appendPlainText(blurb)


class StdOut(External):
    tabName = 'System'

class StdErr(StdOut):
    tabName = None  # = hitch-hike with previously created sibling.

    def write(self, out='', err='', append=True):
        return StdOut.write(self, out=err, err=out, append=append)