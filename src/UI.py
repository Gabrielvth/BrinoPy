#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPlainTextEdit)

import Menu
import DestaqueSintaxe

"""
Br.ino Qt UI

Interface base da IDE Br.ino
em PyQt5 (python 2.7)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica
    Geral GNU, conforme publicado pela Free Software Foundation,
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer
    versao posterior.

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA; sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

website: brino.cc
author: Mateus Berardo
email: mateus.berardo@brino.cc
contributor: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""


class Centro(QWidget):

    def __init__(self):
        super(Centro, self).__init__()
        self.layout = 0

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setRowStretch(0, 7.5)
        layout.setRowStretch(1, 2.5)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        menu = Menu.Menu()
        layout.addWidget(menu, 0, 0, 1, 0)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget(self)
        container.setStyleSheet("background:#252525")
        editor = QPlainTextEdit(container)
        highlight = DestaqueSintaxe.PythonHighlighter(editor.document())
        layout.addWidget(container, 0, 1, 9, 9)

        container_log = QWidget(self)
        log = QPlainTextEdit(container_log)
        log.setStyleSheet("background:#000000")
        log.setDisabled(True)
        layout.addWidget(container_log, 1, 1, 1, 8)



        self.show()
