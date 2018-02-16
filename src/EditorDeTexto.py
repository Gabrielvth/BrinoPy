from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QWidget
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QColor, QTextFormat, QPainter

"""
Br.ino Qt editor de texto

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
    mas SEM QUALQUER GARANTIA sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

    Codigo fonte retirado de:
    https: http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
    **  Copyright (C) 2016 The Qt Company Ltd.
    **
    **  "Redistribution and use in source and binary forms, with or without
    ** modification, are permitted provided that the following conditions are
    ** met:
    **   * Redistributions of source code must retain the above copyright
    **     notice, this list of conditions and the following disclaimer.
    **   * Redistributions in binary form must reproduce the above copyright
    **     notice, this list of conditions and the following disclaimer in
    **     the documentation and/or other materials provided with the
    **     distribution.
    **   * Neither the name of The Qt Company Ltd nor the names of its
    **     contributors may be used to endorse or promote products derived
    **     from this software without specific prior written permission.
    **
    **
    ** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    ** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    ** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    ** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    ** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    ** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    ** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
    ** DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    ** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    ** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    ** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""


class CodeEditor(QPlainTextEdit):
    instancia = 0

    def __init__(self, parent):
        super(CodeEditor, self).__init__(parent)
        self.contador_de_linhas = ContadorDeLinhas(self)
        self.largura_contador = 38
        self.blockCountChanged.connect(self.atualizar_largura_contador)
        self.updateRequest.connect(self.atualizar_area_contador)
        self.cursorPositionChanged.connect(self.marcar_linha_atual)
        self.atualizar_largura_contador(0)
        self.marcar_linha_atual()
        global instancia
        instancia = self

    def atualizar_largura_contador(self, largura):
        self.setViewportMargins(self.largura_contador, 0, 0, 0)

    def atualizar_area_contador(self, rect, dy):
        if dy != 0:
            self.contador_de_linhas.scroll(0, dy)
        else:
            self.contador_de_linhas.update(0, rect.y(), self.contador_de_linhas.width(), rect.height())

            if rect.contains(self.viewport().rect()):
                self.atualizar_largura_contador(0)

    def marcar_linha_atual(self):
        extraSelections = list()
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            cor_linha = QColor("#505050")
            selection.format.setBackground(cor_linha)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def resizeEvent(self, QResizeEvent):
        cr = self.contentsRect()
        self.contador_de_linhas.setGeometry(QRect(cr.left(), cr.top(), self.largura_contador, cr.height()))

    def lineNumberAreaPaintEvent(self, QPaintEvent):
        painter = QPainter(self.contador_de_linhas)
        painter.fillRect(QPaintEvent.rect(), QColor("#252525"))

        bloco = self.firstVisibleBlock()
        numero_bloco = bloco.blockNumber()
        top = int(self.blockBoundingGeometry(bloco).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(bloco).height())
        painter.fillRect(self.contador_de_linhas.width() - 2, top, 1, 9999, QColor("#505050"))

        while bloco.isValid() and top <= QPaintEvent.rect().bottom():
            if bloco.isVisible() and bottom >= QPaintEvent.rect().top():
                number = str(numero_bloco + 1)
                painter.setPen(QColor("#505050"))
                painter.drawText(0, top, self.contador_de_linhas.width() - 2, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            bloco = bloco.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(bloco).height())
            numero_bloco += 1


def set_texto(texto):
    global instancia
    instancia.setPlainText(texto)


def get_texto():
    global instancia
    return instancia.toPlainText()


class ContadorDeLinhas(QWidget):

    def __init__(self, editor):
        super(ContadorDeLinhas, self).__init__(editor)
        self.editor_de_codigo = editor
        self.setStyleSheet("border:1px solid red;")

    def sizeHint(self):
        return QSize(self.editor_de_codigo.largura_contador, 0)

    def paintEvent(self, event):
        self.editor_de_codigo.lineNumberAreaPaintEvent(event)
