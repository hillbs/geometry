 # -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" NINJA-IDE Interactive Geometry Plotter "
__version__ = ' 0.2 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 25/06/2013 '
__prj__ = ' geometry '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from sip import setapi

from PyQt4.QtGui import (QIcon, QLabel, QDockWidget,
                         QFileDialog, QToolBar, QAction)
from webbrowser import open_new_tab

try:
    from PyKDE4.kdecore import KPluginLoader, KUrl
    from PyKDE4.kparts import *
except ImportError:
    pass

from ninja_ide.core import plugin


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


###############################################################################


class Main(plugin.Plugin):
    " dock Class "
    def initialize(self):
        " Init Class dock "
        self.dock = QDockWidget()
        self.dock.setFeatures(QDockWidget.DockWidgetFloatable |
                              QDockWidget.DockWidgetMovable)
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.boton = QAction(QIcon.fromTheme("list-add"), 'Open', self)
        self.saver = QAction(QIcon.fromTheme("document-save"), 'Save', self)
        self.apiss = QAction(QIcon.fromTheme("help"), 'Python API Help', self)
        QToolBar(self.dock).addActions((self.boton, self.saver, self.apiss))
        try:
            self.factory = KPluginLoader("kigpart").factory()
            self.part = self.factory.create(self)
            self.part.setReadWrite(True)
            self.boton.triggered.connect(lambda: self.part.openUrl(KUrl(str(
                QFileDialog.getOpenFileName(self.dock, ' Open Geometry Plot ',
                path.expanduser("~"),
                ';;'.join(['(*.{})'.format(e) for e in ['fig', 'kig', 'kigz',
                                                        'seg', 'fgeo']]))))))
            self.saver.triggered.connect(lambda: self.part.saveAs(KUrl(str(
                QFileDialog.getSaveFileName(self.dock, ' Save Geometry Plot ',
                path.expanduser("~"),
                ';;'.join(['(*.{})'.format(e) for e in ['kig', 'kigz', 'fig']])
            )))))
            self.apiss.triggered.connect(lambda: open_new_tab(
                'http://edu.kde.org/kig/manual/scripting-api/classObject.html'))
            self.dock.setWidget(self.part.widget())
        except:
            self.dock.setWidget(QLabel(""" <center> <h3>ಠ_ಠ<br>
            ERROR: Please, install KIG and PyKDE ! </h3><br>
            <br><i> (Sorry, cant embed non-Qt Apps). </i><center>"""))
        self.misc = self.locator.get_service('misc')
        self.misc.add_widget(self.dock,
                            QIcon.fromTheme("accessories-calculator"), __doc__)


###############################################################################


if __name__ == "__main__":
    print(__doc__)
