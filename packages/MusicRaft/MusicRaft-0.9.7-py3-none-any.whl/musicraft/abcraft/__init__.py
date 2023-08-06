#!/usr/bin/python
"""
Copyright 2015 Hippos Technical Systems BV.

@author: larry
"""
import os
from .. import (Shared, QtWidgets, Printer, dbg_print, version)
from .score import Score
from .syntax import AbcHighlighter

from .external import (Abc2midi, Abcm2svg, Abcm2ps, Ps2PDF, Abc2abc)

from .midiplayer import MidiPlayer


class AbcRaft(object):

    def __init__(self):
        Shared.abcRaft = self
        self.score = Score()
        self.abc2abc = Abc2abc()
        self.abc2midi = Abc2midi()
        self.abcm2ps = Abcm2ps()
        self.ps2PDF = Ps2PDF()
        self.abcm2svg = Abcm2svg()

        Shared.raft.setWindowTitle(f"Musicraft version {version}")
        Shared.raft.displayBook.addTab(self.score, "Score")
        #Share.raft.displayBook.setFixedWidth(800)

        self.midiPlayer = MidiPlayer()
        Shared.raft.menuBar().show()

    def checkLoadedFile(self, editor, filename):
        dbg_print(1, 'checkLoadedFile', filename)
        if os.path.splitext(filename)[1] in ('.abc', '.ABC'):
            dbg_print(1, "we expect ABC syntax in " + filename)
            editor.highlighter = syntax.AbcHighlighter(editor.document(), editor)
