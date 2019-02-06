import sys
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from subprocess import Popen,PIPE
import re
from collections import Counter
import textwrap
from PyQt4.QtCore import QObject, pyqtSignal

var = 0
f = ""
choiceStr = ""
cs = False
wwo = False

tt = True
tf = True
ts = True
k=""

class Find(QtGui.QMainWindow):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.initUI()
 
    def initUI(self):
 
        self.lb1 = QtGui.QLabel("Search for: ",self)
        self.lb1.setStyleSheet("font-size: 15px; ")
        self.lb1.move(10,10)
 
        self.te = QtGui.QTextEdit(self)
        self.te.move(10,40)
        self.te.resize(250,25)
 
        self.src = QtGui.QPushButton("Find",self)
        self.src.move(270,40)
 
        self.lb2 = QtGui.QLabel("Replace all by: ",self)
        self.lb2.setStyleSheet("font-size: 15px; ")
        self.lb2.move(10,80)
 
        self.rp = QtGui.QTextEdit(self)
        self.rp.move(10,110)
        self.rp.resize(250,25)
 
        self.rpb = QtGui.QPushButton("Replace",self)
        self.rpb.move(270,110)
 
        self.opt1 = QtGui.QCheckBox("Case sensitive",self)
        self.opt1.move(10,160)
        self.opt1.stateChanged.connect(self.CS)
         
        self.opt2 = QtGui.QCheckBox("Whole words only",self)
        self.opt2.move(10,190)
        self.opt2.stateChanged.connect(self.WWO)
 
        self.close = QtGui.QPushButton("Close",self)
        self.close.move(270,220)
        self.close.clicked.connect(self.Close)
         
        self.setGeometry(300,300,360,250)
 
    def CS(self, state):
        global cs
 
        if state == QtCore.Qt.Checked:
            cs = True
        else:
            cs = False
 
    def WWO(self, state):
        global wwo
        print(wwo)
 
        if state == QtCore.Qt.Checked:
            wwo = True
        else:
            wwo = False
 
    def Close(self):
        self.hide()

         
class Main(QtGui.QMainWindow):
 
    def __init__(self):
        QtGui.QMainWindow.__init__(self,None)
        self.initUI()
 
    def initUI(self):    	
 
#------- Toolbar --------------------------------------
 
#-- Upper Toolbar -- 
 
        newAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/delete.png"),"Delete",self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Delete")
        newAction.triggered.connect(self.New)
 
        openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        openAction.setStatusTip("Open")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.Open)
 
        saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        saveAction.setStatusTip("Save")
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.Save)
 
        previewAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/preview.png"),"Page view",self)
        previewAction.setStatusTip("Preview")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.PageView)
 
        findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"),"Find",self)
        findAction.setStatusTip("Find")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.Find)
 
        cutAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/cut.png"),"Cut",self)
        cutAction.setStatusTip("Delete and copy")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.Cut)
 
        copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)
        copyAction.setStatusTip("Copy")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.Copy)
 
        pasteAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/paste.png"),"Paste",self)
        pasteAction.setStatusTip("Paste")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.Paste)
 
        undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)
        undoAction.setStatusTip("Undo last action")
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.Undo)
 
        redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)
        redoAction.setStatusTip("Redo last undone thing")
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.Redo)
 
        printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)
        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(printAction)
        self.toolbar.addAction(previewAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(findAction)
        self.toolbar.addAction(cutAction)
        self.toolbar.addAction(copyAction)
        self.toolbar.addAction(pasteAction)
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.addToolBarBreak()
 
# -- Lower Toolbar -- 
 
        self.fontFamily = QtGui.QFontComboBox(self)
        self.fontFamily.currentFontChanged.connect(self.FontFamily)
        fontSize = QtGui.QComboBox(self)
        fontSize.setEditable(True)
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.FontSize)
        flist = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,
                 54,60,66,72,80,88,96] 
        for i in flist:
            fontSize.addItem(str(i))
        boldAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.Bold)
        italicAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.Italic)
        underlAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/underl.png"),"Underline",self)
        underlAction.triggered.connect(self.Underl)
        alignLeft = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)
        alignCenter = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/Center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)
        alignRight = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)
        alignJustify = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)
        indentAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.Indent)
        dedentAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.Dedent)
        bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"),"Insert Bullet List",self)
        bulletAction.triggered.connect(self.BulletList)
        numberedAction = QtGui.QAction(QtGui.QIcon("icons/ICONNEW/number.png"),"Insert Numbered List",self)
        numberedAction.triggered.connect(self.NumberedList)
        space1 = QtGui.QLabel("  ",self)
        space2 = QtGui.QLabel(" ",self)
        space3 = QtGui.QLabel(" ",self)
        self.formatbar = self.addToolBar("Format")
        self.formatbar.addWidget(self.fontFamily)
        self.formatbar.addWidget(space1)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addWidget(space2)
        self.formatbar.addSeparator()
        self.formatbar.addSeparator()
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addSeparator()
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)
        self.formatbar.addSeparator()
        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)
        self.formatbar.addAction(bulletAction)
        self.formatbar.addAction(numberedAction)
         
#------- Text Edit -----------------------------------
 
        wid = QtGui.QWidget(self)
        self.setCentralWidget(wid)
        self.H_layout = QtGui.QHBoxLayout()
        self.verti = QtGui.QVBoxLayout()
        self.lbl_editor = QLabel("Pengelola Teks")
        self.lbl_kata_salah = QLabel("Daftar Kata Salah")
        self.lbl_rek_kata = QLabel("Rekomendasi Kata")
        self.lbl_rek_kal = QLabel("Rekomendasi kalimat")
        self.list_peringatan = QListWidget()
        self.lbl_peringatan_kal = QLabel("Deteksi Kalimat")
        self.text = QTextEdit()
        self.text.setFixedWidth(1130)
        self.text2 = QListWidget()
        self.te = QLineEdit()
        self.progress = QProgressBar()
        self.kal_rek = QtGui.QListWidget()
        self.tableWidget = QTableWidget()
        self.tabel_rekomendasi_kalimat = QTableWidget()
        self.te2 = QLineEdit()
        self.tombol_kata = QPushButton("CEK KATA")
        self.tombol_kata.clicked.connect(self.spell_chuck)
        self.tombol_kata.setEnabled(False)
        self.text.textChanged.connect(self.disableButton)
        self.tombol_kalimat = QPushButton("CEK KALIMAT")
        self.tombol_kalimat.clicked.connect(self.det_kalimat)
        self.tombol_kalimat.setEnabled(False)
        self.text.textChanged.connect(self.disableButton)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.lbl_editor)
        self.layout.addWidget(self.text)
        self.layout2 = QtGui.QVBoxLayout()
        self.layout2.addWidget(self.lbl_rek_kata)
        self.layout2.addWidget(self.tableWidget)
        self.layout_tombol = QtGui.QHBoxLayout()
        self.layout_tombol.addWidget(self.tombol_kata)
        self.layout_tombol.addWidget(self.tombol_kalimat)
        self.H_layout.addLayout(self.layout)
        self.H_layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout_tombol)
        self.verti.addLayout(self.H_layout)
        self.verti.addWidget(self.lbl_peringatan_kal)
        self.verti.addWidget(self.list_peringatan)
        self.verti.addWidget(self.lbl_rek_kal)
        self.verti.addWidget(self.tabel_rekomendasi_kalimat)
        self.verti.addWidget(self.progress)
        self.progress.hide()
        wid.setLayout(self.verti)

        global sometext
        sometext = self.text.toPlainText()
 
#------- Statusbar ------------------------------------
         
        self.status = self.statusBar()
 
        self.text.cursorPositionChanged.connect(self.CursorPosition)
 
#---------Window settings --------------------------------
         
        self.setGeometry(800,100,100,800)
        self.setWindowTitle("APLIKASI DETEKSI KATA DAN KALIMAT BAHASA INDONESIA")
        self.setWindowIcon(QtGui.QIcon("icons/feather.png"))
        self.show()
 
#------- Menubar --------------------------------------
         
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(newAction)
        file.addAction(openAction)
        file.addAction(saveAction)
        file.addAction(printAction)
        file.addAction(previewAction)
 
        edit.addAction(undoAction)
        edit.addAction(redoAction)
        edit.addAction(cutAction)
        edit.addAction(copyAction)
        edit.addAction(findAction) 
        toggleTool = QtGui.QAction("Toggle Toolbar",self,checkable=True)
        toggleTool.triggered.connect(self.handleToggleTool)
         
        toggleFormat = QtGui.QAction("Toggle Formatbar",self,checkable=True)
        toggleFormat.triggered.connect(self.handleToggleFormat)
         
        toggleStatus = QtGui.QAction("Toggle Statusbar",self,checkable=True)
        toggleStatus.triggered.connect(self.handleToggleStatus)
 
        view.addAction(toggleTool)
        view.addAction(toggleFormat)
        view.addAction(toggleStatus)

    def disableButton(self):
        if len(self.text.toPlainText()) > 0:
            self.tombol_kata.setEnabled(True)
            self.tombol_kalimat.setEnabled(True)

    def handleToggleTool(self):
        global tt
 
        if tt == True:
            self.toolbar.hide()
            tt = False
        else:
            self.toolbar.show()
            tt = True
 
    def handleToggleFormat(self):
        global tf
 
        if tf == True:
            self.formatbar.hide()
            tf = False
        else:
            self.formatbar.show()
            tf = True
 
    def handleToggleStatus(self):
        global ts
 
        if ts == True:
            self.status.hide()
            ts = False
        else:
            self.status.show()
            ts = True
             
#-------- Toolbar slots -----------------------------------
 
    def New(self):
        self.text.clear()
 
    def Open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        f = open(filename, 'r')
        filedata = f.read()
        self.text.setText(filedata)
        f.close()
 
    def Save(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        f = open(filename, 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()
 
    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()
 
    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())
 
    def PDF(self):
        printer = QtGui.QPrinter()
        printer.setOutputFormat(printer.NativeFormat)
         
        dialog = QtGui.QPrintDialog(printer)
        dialog.setOption(dialog.PrintToFile)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())
         
    def PaintPageView(self, printer):
        self.text.print_(printer)
 
    def Find(self):
        global f
         
        find = Find(self)
        find.show()
 
        def handleFind():
 
            f = find.te.toPlainText()
            print(f)
             
            if cs == True and wwo == False:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively
                 
            elif cs == False and wwo == False:
                flag = QtGui.QTextDocument.FindBackward
                 
            elif cs == False and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords
                 
            elif cs == True and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords
             
            self.text.find(f,flag)
 
        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()
 
            text = self.text.toPlainText()
             
            newText = text.replace(f,r)
 
            self.text.clear()
            self.text.append(newText)
         
        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)

    def deteksi_kalimat(self):
        global k
         
        kal = deteksi_kalimat(self)
        kal.show()
 
        def handleKal():
 
            k = kal.te.toPlainText()
            print(k)
         
 
    def Undo(self):
        self.text.undo()
 
    def Redo(self):
        self.text.redo()
 
    def Cut(self):
        self.text.cut()
 
    def Copy(self):
        self.text.copy()
 
    def Paste(self):
        self.text.paste()
 
    def DateTime(self):
 
        date = Date(self)
        date.show()
 
        date.ok.clicked.connect(self.insertDate)
 
    def insertDate(self):
        global choiceStr
        print(choiceStr)
        self.text.append(choiceStr)
         
    def CursorPosition(self):
        line = self.text.textCursor().blockNumber()
        col = self.text.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)
 
    def FontFamily(self,font):
        font = QtGui.QFont(self.fontFamily.currentFont())
        self.text.setCurrentFont(font)
 
    def FontSize(self, fsize):
        size = (int(fsize))
        self.text.setFontPointSize(size)
 
    def FontColor(self):
        c = QtGui.QColorDialog.getColor()
 
        self.text.setTextColor(c)
         
    def FontBackColor(self):
        c = QtGui.QColorDialog.getColor()
 
        self.text.setTextBackgroundColor(c)
 
    def Bold(self):
        w = self.text.fontWeight()
        if w == 50:
            self.text.setFontWeight(QtGui.QFont.Bold)
        elif w == 75:
            self.text.setFontWeight(QtGui.QFont.Normal)
         
    def Italic(self):
        i = self.text.fontItalic()
         
        if i == False:
            self.text.setFontItalic(True)
        elif i == True:
            self.text.setFontItalic(False)
         
    def Underl(self):
        ul = self.text.fontUnderline()
 
        if ul == False:
            self.text.setFontUnderline(True) 
        elif ul == True:
            self.text.setFontUnderline(False)
             
    def lThrough(self):
        lt = QtGui.QFont.style()
 
        print(lt)
 
    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)
 
    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)
 
    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)
 
    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)
 
    def Indent(self):
        tab = "\t"
        cursor = self.text.textCursor()
 
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
 
        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()
 
        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()
 
        while cursor.position() < end:
            global var
            print(cursor.position(),end)
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)
             
    def Dedent(self):
        tab = "\t"
        cursor = self.text.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()
        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()
 
        while cursor.position() < end:
            global var
             
            cursor.movePosition(cursor.StartOfLine)
            cursor.deleteChar()
            cursor.movePosition(cursor.EndOfLine)
            cursor.movePosition(cursor.Down)
            end -= len(tab)
 
    def BulletList(self):
        print("bullet connects!")
        self.text.insertHtml("<ul><li> ...</li></ul>")
 
    def NumberedList(self):
        print("numbered connects!")
        self.text.insertHtml("<ol><li> ...</li></ol>")

#DETEKSI KATA
#PEMECAHAN KATA *spell_chunk
    def spell_chuck(self):
        self.text2.clear()
        data_masuk = str(self.text.toPlainText())
        teks_masuk = data_masuk.lower()
        STRteks_masuk = teks_masuk.split()
        list_teks = []
        for data_teks in STRteks_masuk:
            kirim = re.split(",|\.",data_teks)
            Jkirim = " ".join(kirim)
            list_teks.append(Jkirim)
        Jlist_teks = " ".join(list_teks)
        print "list_teks : ",list_teks
        self.damerau_suffix(list_teks)

#PEMISAHAN IMBUHAN
    def damerau_suffix(self,kirim):
        wordlist = kirim
        from pyparsing import StringEnd, oneOf, FollowedBy, Optional, ZeroOrMore, SkipTo
        endOfString = StringEnd()
        prefix = oneOf("di")
        suffix = oneOf("nya") + FollowedBy(endOfString)
        word = (ZeroOrMore(prefix)("prefixes") + SkipTo(suffix | endOfString)("root") + Optional(suffix)("suffix"))
        kamus_kd = open('kamus_kata.txt')
        baca_kd = kamus_kd.read()
        pecah = baca_kd.split()
        text_masuk = []
        ds = []
        for wd in wordlist:
            res = word.parseString(wd)
            join_res=' '.join(res)
            if len(res)>1:
                if res[1] in pecah:
                    ds.append(join_res)
                else:
                    ds.append(wd)
            else:
                ds.append(join_res)
        hasil_suffix =  ' '.join(ds)
        text_masuk.append(hasil_suffix)
        str_forwordblue = ' '.join(text_masuk)
        self.word_blue(str_forwordblue)

#DAMERAU LEVENSHTEIN
    def word_blue(self,str_forwordblue):
    	readyDamerau = str_forwordblue.split()
        print readyDamerau
        daftar_word_user = []
        dic={}
        self.data_input=[]
        saran = []
        pjgReadyDam = len(readyDamerau)
        self.progress.show()
        self.progress.setMaximum(pjgReadyDam)
        iterasi = 0
        saran_kosong = []
        list_periksa_kata = []
        saran_3 = []

        for word_user in readyDamerau:
            iterasi +=1
            self.progress.setValue(iterasi)
            L1=len(word_user)
            wordlist=[]
            D=[[0 for x in range(20)] for y in range(20)]
            for i in range(0,20):
                D[i][0]=i
            for j in range(0,20):
                D[0][j]=j
            Dic=open('kamus_kata.txt') #KAMUS KATA
            for line in Dic:
                wordlist.append(line.strip())
            Dic.close()

            suggest=[]
            saran_2 = []
            for x in wordlist:  #memecah kata kamu
                L2=len(x)
                if (L2<=(L1+3)) and (L2>=(L1-3)):
                    for i in range(1,L1+1): #membentuk baris
                        for j in range(1,L2+1): #membentuk kolom
                            if word_user[i-1]==x[j-1]:
                                cost=0
                            else:
                                cost=1
                            D[i][j]= min(D[i-1][j]+1,D[i][j-1]+1,D[i-1][j-1]+cost)

                            if (i>1 and j>1 and word_user[i-2]==x[j-1] and word_user[i-1]==x[j-2]):
                                D[i][j]=min(D[i][j],D[i-2][j-2]+ cost)

                    if D[L1][L2]<=1:    #membuat daftar rekomendasi kata
                        suggest.append(x)
                        
                    elif D[L1][L2]>1 and D[L1][L2]<=2:
                        saran_2.append(x)#rekomendasi utama
                    elif D[L1][L2]>2 and D[L1][L2]<=3:
                        saran_3.append(x)#rekomendasi cadangan

            if word_user in suggest:
                del suggest
                del word_user
                saran_kosong.append("kosong")
                
            #pengecekan rekomendasi
            elif suggest==[]:
                list_saran2 = []
                for sub_saran2 in saran_2 :
                    if len(sub_saran2)>2 :
                        list_saran2.append(sub_saran2)
                str_saran2 = " , ".join(list_saran2)
                if list_saran2 !=[]:
                    split_word_user = word_user.split()
                    dic[word_user]=list_saran2
                    daftar_word_user.append(word_user)
                    saran.append(list_saran2)
                    self.data_input.append(word_user)
                else:
                    daftar_word_user.append(word_user)
                    print saran_2
                    periksa_kata = ' '.join(word_user)
                    list_periksa_kata.append(periksa_kata)
                    dic[word_user]=saran_3
            else:
                daf_kata = ' , '.join(suggest)
                str_suggest = ' '.join(suggest)
                split_word_user = word_user.split()
                dic[word_user]=suggest
                daftar_word_user.append(word_user)
                saran.append(suggest)
                self.data_input.append(word_user)

#PEMBERITAHUAN
        self.tabelku(dic)
        if len(saran_kosong)==pjgReadyDam:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Tidak terdapat kata salah")
            msg.setWindowTitle("Informasi Kata")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        if list_periksa_kata!=[]:
            self.periksa_kata_kembali(list_periksa_kata)
        self.progress.hide()
        str_DWU = ' '.join(daftar_word_user)
        buat_kata_salah = open("kata_salah.txt","w")
        buat_kata_salah.write(str_DWU)
        buat_kata_salah.close()
        self.highlighter = Highlighter(self.text.document())    #COLOR TEXT
    def periksa_kata_kembali(self,list_periksa_kata):
        periksa_kata = ','.join(list_periksa_kata)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Rekomendasi Kata Mungkin Tidak Tepat")
        msg.setDetailedText(periksa_kata)
        msg.setWindowTitle("Informasi Kata")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

#PEMILIHAN KATA REKOMENDASI
    def tabelku(self,dic):
        numberRows    = len(dic)
        numberColumns = 1
        self.tableWidget.setRowCount(numberRows)
        self.tableWidget.setColumnCount(numberColumns)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[QtGui.QWidget].connect(self.on_signalMapper_mapped)
        headers = []
        for rowNumber,key in enumerate(dic.keys()):
            headers.append(key)
            for columnNumber,item in enumerate(dic[key]):
                comboBox = QtGui.QComboBox()
                comboBox.activated.connect(self.signalMapper.map)
                comboBox.addItems(dic[key])
                comboBox.row = rowNumber
                comboBox.column = columnNumber
                self.tableWidget.setCellWidget(rowNumber, columnNumber, comboBox)
                self.signalMapper.setMapping(comboBox, comboBox)
        self.tableWidget.setVerticalHeaderLabels(headers)
        self.tableWidget.horizontalHeader().hide()
        self.headers = headers

    @QtCore.pyqtSlot(QtGui.QWidget)
    def on_signalMapper_mapped(self, comboBox):

        data_masuk = self.text.toPlainText()
        repl = data_masuk.replace(self.headers[comboBox.row],comboBox.currentText())
        self.text.clear()
        self.text.append(repl)
        print repl

##########################DETEKSI KALIMAT##############################
#PEMECAHAN TEKS
    def det_kalimat(self):
        self.list_peringatan.clear()
        self.kal_rek.clear()
        self.tabel_rekomendasi_kalimat.clearContents()
        data_masuk =str(self.text.toPlainText())
        teks_kalimat = data_masuk.lower()
        
        self.baris_rekomendasi = 0
        print "baris_rekomendasi",self.baris_rekomendasi
        kalimat = teks_kalimat.split(".")
        print "kalimat = ",kalimat
        for dataProses in kalimat:
            print "dataProses",dataProses
            if not dataProses.strip():continue
            self.suffix(dataProses)

#PEMISAHAN IMBUHAN
    def suffix(self,dataProses):
        wordlist = dataProses.split()
        from pyparsing import StringEnd, oneOf, FollowedBy, Optional, ZeroOrMore, SkipTo
        endOfString = StringEnd()
        prefix = oneOf("di")
        suffix = oneOf("nya") + FollowedBy(endOfString)
        word = (ZeroOrMore(prefix)("prefixes") + SkipTo(suffix | endOfString)("root") + Optional(suffix)("suffix"))
        kamus_kd = open('kamus_kata.txt')
        baca_kd = kamus_kd.read()
        pecah = baca_kd.split()
        self.ds = []
        for wd in wordlist:
            res = word.parseString(wd)
            join_res=' '.join(res)
            if len(res)>1:
                if res[1] in pecah:
                    self.ds.append(join_res)
                else :
                    self.ds.append(wd)
            else:
                self.ds.append(join_res)
        data_kalimat =  ' '.join(self.ds)
        kamus_kd.close()
        self.proses_cyk(data_kalimat)

#COCKE YOUNGER KASAMI
    def proses_cyk(self,data_kalimat):
    
        word = data_kalimat.split()
        word_length = len(word)
        start_symbol_kalimat1 = "G"
#AKSES KELOMPOK KATA
        buka_nomina = open("KELOMPOK_KATA/nomina.txt","r")
        buka_adjektiva = open("KELOMPOK_KATA/adjektiva.txt","r")
        buka_verba = open("KELOMPOK_KATA/verba.txt","r")
        buka_adverbia = open("KELOMPOK_KATA/adverbia.txt","r")
        buka_me_verba = open("KELOMPOK_KATA/transitif_me.txt","r")
        buka_ter_verba = open("KELOMPOK_KATA/intransitif_ter.txt","r")
        buka_ber_verba = open("KELOMPOK_KATA/intransitif_ber.txt","r")
        buka_nomina_pelaku = open("KELOMPOK_KATA/nomina_pelaku.txt","r")
########
        baca_nomina = buka_nomina.read()
        baca_adjektiva = buka_adjektiva.read()
        baca_verba = buka_verba.read()
        baca_adverbia = buka_adverbia.read()
        baca_me_verba = buka_me_verba.read()
        baca_ter_verba = buka_ter_verba.read()
        baca_ber_verba = buka_ber_verba.read()
        baca_nomina_pelaku = buka_nomina_pelaku.read()
        spt_nomina = baca_nomina.split("\n")
        spt_adjectiva = baca_adjektiva.split("\n")
        spt_verba = baca_verba.split("\n")
        spt_adverbia = baca_adverbia.split("\n")
        spt_me_verba = baca_me_verba.split("\n")
        spt_ter_verba = baca_ter_verba.split("\n")
        spt_ber_verba = baca_ber_verba.split("\n")
        spt_nomina_pelaku = baca_nomina_pelaku.split("\n")

## ATURAN PRODUKSI
        productions = {
        "N":(spt_nomina),
        "V":(spt_adjectiva),
        "A":(spt_verba),
        "B":(spt_adverbia),
        "R":(["ke","di","kepada","oleh","pada","sebagai","secara","seperti","tentang","terhadap","adapun","dalam ","dari","dengan"]),
        "D":(["itu","ini","DJ"]),
        "H2":(["kecuali","lalu","maupun","melainkan","namun","sedangkan","selain","serta","tetapi","atau","dan","ataupun"]),
        "T":(["nya","mu","ku"]),
        "H1":(["yang"]),
        "H":(["dalam","guna","hingga","jika","kalau","karena","ketika","lantaran","maka","meskipun","saat","sebab","sebagaimana","sebelum","sehingga",
            "sejak","sesudah","setelah","supaya","untuk","yaitu","agar","apabila","bagi","bahwa","bila","demi"]),
        "I":(["tidak","belum"]),
        "I1":(["bukan"]),
        "U":(["harus","hendak","perlu","pernah","sedang","sudah","ingin","akan"]),
        "A1":(["adalah","ialah"]),
        "A2":(["merupakan"]),
        "A3":(spt_ter_verba),
        "A4":(spt_me_verba),
        "A5":(spt_ber_verba),
        "N1":(spt_nomina_pelaku),
        "Z":([","]),
        "S":(["A4X","NA","NV","CP","NN","NP","N1N","N1V","N1A","N1P","KS","SK","SP","CP","NG","N1G","SG","GP","CM","KN","KN1","NK","KG","GN","GN1",
            "N1K","GK","NA3","N1A3","SA3","NA4","N1A4","SA4","NA5","N1A5","SA5","CV","CN"]),
        "P":(["IE","A4E","AN","A3C","I1N","IA","IV","IA5","RN","RV","RA","RE","RC","RO","RQ","RK","H1N","H1V","H1A","H1A4","H1A2","H1A3","H1A5",
            "H1E","H1C","H1O","H1Q","H1K","UV","UA","UN","UC","UA5","UA4","UO","UQ","UK","UE","BN","BC","BV","BA","BA4","BA5","BA3","BE","BO",
            "BQ","BK","PL","A3E","PK","PO","PQ","PN","PN1","A1G","A1N","A1N1","A1O","A1Q","A1L","A1K","A2N","A2E","A2N1","A2O","A2Q","A2K","A2G",
            "A2L","A2V1","A3E","A3N","A3N1","A3O","A3Q","A3K","A3G","A3L","A4N","A4N1","A4O","A4Q","A4K","A4G","A4L","A5E","A5N","A5N1","A5O","A5Q",
            "A5K","A5L","IP","H1F","AA4","NF"]),
        "O":(["NT","ND","N1D","N1T","NV","NA","NQ","N1N","N1V","N1A","HN","HN1","OQ","OK","KO","KQ","HK"]),
        "Q":(["CN","NC","BC","BN","CN","BN","NV","H1V","QK","KQ"]),
        "K":(["RJ","RC","RN","BV","HG","BC","BN","HC","IT","BA","RF","HE","NH","IC","BE","GG","MK","HA","HJ","FN","KF"]),
        "G":(["SP","SO","SQ","GQ","SL","NV","NA","NA3","NA5","NE","NP","N1V","N1A","N1A3","N1A5","N1P","SK"]),
        "L":(["OQ"]),
        "M":(["HN","HV","HA"]),
        "C":(["NN","NC","CN","NT","NI1","N1I1","SI1","ND","N1D","N1T","CC","NV","NA","CD"]),
        "E":(["VA","AA","AV","AB","AE","A4N","AN","A4V","A4B","A4E","A4C","A5V"]),
        "F":(["RA","RV","RN","RC","RE"]),
        "Y":(["H2N","H2G","H2C","H2S","H2F","H2K","H2G"]),
        "J":(["BA","BV","BN","BC","BE"]),
        "V1":(["VN","VV","VA","VC"]),
        "X":(["A2N","A2C"])}

        table = []
#PENGECEKAN PRODUKSI
        def check_grammar():       
            sdf = []
            for i in range(0, word_length):
                table.append([])
                for j in range(0, word_length):
                    table[i].append([])

            for i in range(0, word_length):
                for j in productions:   
                    for symbols in productions[j]:
                        if symbols == word[i]: 
                            table[i][i].append(j)
                            continue

            for k in range(1, word_length): 
                for j in range(k, word_length):
                    for l in range(j-k, j):
                        for list_item in find_production(table[j-k][l], table[l+1][j]):
                            if list_item not in table[j-k][j]:
                                table[j-k][j] += list_item

            baris_tabel = 0
            kolom_tabel = 0

            self.manipulasi_deteksi = []
            self.input_rekomendasi = []
            for indx in word :
                str_daftar = ' '.join(table[baris_tabel][kolom_tabel])
                
                baris_tabel +=1
                kolom_tabel +=1

##MERUBAH LABEL KE KELOMPOK KATA

                if str_daftar == 'N':
                    self.input_rekomendasi.append("N")
                    self.list_peringatan.addItem( "Nomina" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Nomina) ")
                if str_daftar == 'A':
                    self.input_rekomendasi.append("A")
                    self.list_peringatan.addItem( "Verba" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Verba) ")
                if str_daftar == 'V':
                    self.input_rekomendasi.append("V")
                    self.list_peringatan.addItem( "Adjektiva" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Adjektiva) ")
                if str_daftar == 'B':
                    self.input_rekomendasi.append("B")
                    self.list_peringatan.addItem( "Adverbia" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Adverbia) ")
                if str_daftar == 'R':
                    self.input_rekomendasi.append("R")
                    self.list_peringatan.addItem( "Preposisi" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Preposisi) ")
                if str_daftar == 'D':
                    self.input_rekomendasi.append("D")
                    self.list_peringatan.addItem( "Demonstrativa" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Demonstrativa) ")
                if str_daftar == 'H':
                    self.input_rekomendasi.append("H")
                    self.list_peringatan.addItem( "Konjungsi Subordinatif" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Konjungsi Subordinatif) ")
                if str_daftar == 'I':
                    self.input_rekomendasi.append("I")
                    self.list_peringatan.addItem( "Negasi" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Negasi) ")
                if str_daftar == 'U':
                    self.input_rekomendasi.append("U")
                    self.list_peringatan.addItem( "Modalitas" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Modalitas) ")
                if str_daftar == 'A3':
                    self.input_rekomendasi.append("A3")
                    self.list_peringatan.addItem( "Adjektiva/Verba Prefik" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Adjektiva/Verba Prefik) ")
                if str_daftar == 'A4':
                    self.input_rekomendasi.append("A4")
                    self.list_peringatan.addItem( "Prefik-Verba Transitif" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Prefik-Verba Transitif) ")
                if str_daftar == 'A5':
                    self.input_rekomendasi.append("A5")
                    self.list_peringatan.addItem( "Prefik-Verba Intransitif" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Prefik-Verba Intransitif) ")
                if str_daftar == 'T':
                    self.input_rekomendasi.append("T")
                    self.list_peringatan.addItem( "Sufik-Nomina" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Sufik-Nomina) ")
                if str_daftar == 'N1':
                    self.input_rekomendasi.append("N1")
                    self.list_peringatan.addItem( "Prefik-Nomina" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Prefik-Nomina) ")
                if str_daftar == 'I1':
                    self.input_rekomendasi.append("I1")
                    self.list_peringatan.addItem( "Negasi Nomina" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Negasi Nomina) ")
                if str_daftar == 'H1':
                    self.input_rekomendasi.append("H1")
                    self.list_peringatan.addItem( "Konjungsi Penjelas" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Konjungsi Penjelas) ")
                if str_daftar == 'A2':
                    self.input_rekomendasi.append("A2")
                    self.list_peringatan.addItem( "Verba Penggambaran" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Verba Penggambaran) ")
                if str_daftar == 'H2':
                    self.input_rekomendasi.append("H2")
                    self.list_peringatan.addItem( "Konjungsi Koordinatif" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Konjungsi Koordinatif) ")
                if str_daftar == 'A1':
                    self.input_rekomendasi.append("A1")
                    self.list_peringatan.addItem( "Verba Deskripsi" + " => " + str(indx))
                    self.manipulasi_deteksi.append(" (Verba Deskripsi) ")
                if str_daftar == '':
                    self.list_peringatan.addItem("Kata tidak terdapat dalam kamus" + " => " + str(indx))
                    self.manipulasi_deteksi.append("Kata tidak terdapat dalam kamus")

            print "input_rekomendasi: ",self.input_rekomendasi 
            print_table()

            if start_symbol_kalimat1 in table[0][word_length - 1]: return 1

            else: return 0

        def find_production(list1, list2):

            new_list = []
            if not list1 or not list2:
                return new_list

            for x in list1:
                for y in list2:
                    for i in productions:
                        for j in range(0, len(productions[i])):
                            if (x+y) == productions[i][j] and i not in new_list:
                                new_list.append(i)
            return new_list

        def print_table():

            for i in range(0, word_length):
                for j in range(0, word_length):
                    print(table[i][j]),
                print ('\n'),
            print ('\n'),

#MENENTUKAN KALIMAT
        if (check_grammar()):
            print "Your word \"" + str(word) + "\" KALIMAT BENAR!"
            self.list_peringatan.addItem(str("\nStruktur Kalimat BENAR!\n====================\n"))
            rekomen = ''.join(self.input_rekomendasi)
        else:
            print "Sorry, your word \"" + str(word) + "\" KALIMAT SALAH!"
            self.list_peringatan.addItem(str("\nStruktur Kalimat TIDAK terdapat dalam tatabahasa!\n==========================================\n"))
            rekomen = ''.join(self.input_rekomendasi)
            Word = ' '.join(word)
            self.split_kalimat = re.split('\W+',Word)
            self.rekomendasi_Tag(Word)
            print "input_rekomendasi = ",self.input_rekomendasi


#REKOMENDASI KALIMAT
    def rekomendasi_Tag(self,Word):
        print "selfinput= ",self.input_rekomendasi
        kamus = open("kamus_kalimat.txt") #MEMBUKA KAMUS KALIMAT
        bacaKamus = kamus.read()
        stripKamus = bacaKamus.strip()
        target = self.input_rekomendasi
        sptKamus = stripKamus.split('\n')
        a = []
        for kt2 in sptKamus:
            spt2 =kt2.split()
            lenkalimat2= len(spt2)
            lenkalimat1 = len(target)
            d = {}
            for i in range(-1, lenkalimat1 + 1):
                d[(i, -1)] = i + 1
            for j in range(-1, lenkalimat2 + 1):
                d[(-1, j)] = j + 1
            for i in range(lenkalimat1):
                for j in range(lenkalimat2):

                    if target[i] == spt2[j]:
                        cost = 0
                    else:
                        cost = 1
                    d[(i, j)] = min(d[i - 1, j] + 1,
                    d[i, j - 1] + 1, 
                    d[i - 1, j - 1] + cost) 
                    if i and j and target[i] == spt2[j - 1] and target[i - 1] == spt2[j]:
                        d[i, j] = min(d[i, j], d[i - 2, j - 2] + cost)
            g = d[(lenkalimat1-1,lenkalimat2-1)]
            t = g,target,spt2
            a.append(t)
        fg=min(a)
        MLK=("%s => %s"%(fg[1],fg[2]))
        print "rekomendasi tag= ",MLK
        print "rekomendasi tag= ",fg
        minimal1 = fg[2]
        print "REKOMENDASI KALIMAT=",minimal1
        self.manipulasi_rekomendasi(minimal1,Word)
    def manipulasi_rekomendasi(self,dataRekom,Word):
        list_rekomendasi = []

#MERUBAH LABEL KE KELOMPOK KATA
        for sub_x in dataRekom:
            if sub_x=='N' :
                ganti_x = sub_x.replace('N',' (Nomina) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='V':
                ganti_x = sub_x.replace('V',' (Adjektiva) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A':
                ganti_x = sub_x.replace('A',' (Verba) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='B':
                ganti_x = sub_x.replace('B',' (Adverbia) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='R':
                ganti_x = sub_x.replace('R',' (Preposisi) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='D':
                ganti_x = sub_x.replace('D',' (Demonstrativa) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='H':
                ganti_x = sub_x.replace('H',' (Konjungsi Subordinatif) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='I':
                ganti_x = sub_x.replace('I',' (Negasi) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='U':
                ganti_x = sub_x.replace('U',' (Modalitas) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A3':
                ganti_x = sub_x.replace('A3',' (Adjektiva/Verba Prefik) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A4':
                ganti_x = sub_x.replace('A4',' (Prefik-Verba Transitif) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A5':
                ganti_x = sub_x.replace('A5',' (Prefik-Verba Intransitif) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='T':
                ganti_x = sub_x.replace('T',' (Sufik-Nomina) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='N1':
                ganti_x = sub_x.replace('N1',' (Prefik-Nomina) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='I1':
                ganti_x = sub_x.replace('I1',' (Negasi Nomina) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='H1':
                ganti_x = sub_x.replace('H1',' (Konjungsi Penjelas) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A2':
                ganti_x = sub_x.replace('A2',' (Verba penggambaran) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='H2':
                ganti_x = sub_x.replace('H2',' (Konjungsi Koordinatif) ')
                list_rekomendasi.append(ganti_x)
            if sub_x=='A1':
                ganti_x = sub_x.replace('A1',' (Verba Deskripsi) ')
                list_rekomendasi.append(ganti_x)
        print "\n"
        a = self.split_kalimat
        b =self.manipulasi_deteksi
        c = list_rekomendasi
        print "a=",a
        print "b=",b
        print "c=",c
        for iterasi,item in enumerate(a):
            if b[iterasi] in c:
                if iterasi<=len(b):
                    e= c.index(b[iterasi])
                    c[e]=a[iterasi]
            else:
                pass
        joinRekomen = ' '.join(c)
        print "\n"
        
        self.tabel_rekomendasi_kalimat.setRowCount(7)
        self.tabel_rekomendasi_kalimat.setColumnCount(2)
        self.tabel_rekomendasi_kalimat.setMinimumWidth(400)
        self.layout2.addStretch()
        self.tabel_rekomendasi_kalimat.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        tabel_data_rekomendasi = QTableWidgetItem(joinRekomen)
        tabel_data_kalsal = QTableWidgetItem(Word)
        self.tabel_rekomendasi_kalimat.setItem(self.baris_rekomendasi,0,tabel_data_kalsal)
        self.tabel_rekomendasi_kalimat.setItem(self.baris_rekomendasi,1,tabel_data_rekomendasi)
        self.tabel_rekomendasi_kalimat.resizeRowsToContents()
        self.tabel_rekomendasi_kalimat.verticalHeader().setDefaultSectionSize(self.tabel_rekomendasi_kalimat.rowHeight(0))
        self.tabel_rekomendasi_kalimat.horizontalHeader().setStretchLastSection(True)
        self.tabel_rekomendasi_kalimat.sizeHint()
        self.tabel_rekomendasi_kalimat.horizontalHeader().hide()
        self.baris_rekomendasi+=1
        c = list_rekomendasi
##################### WARNA #######################
class Highlighter(QSyntaxHighlighter):
    def __init__(self,parent=None):
        super(Highlighter, self).__init__(parent)
        brush   = QBrush(Qt.red, Qt.SolidPattern)
        keyword = QTextCharFormat()
        keyword.setForeground(brush)
        keyword.setFontWeight(QFont.Bold)
        open_listKeywords = open("kata_salah.txt")
        baca_listKeywords = open_listKeywords.read()
        listKeywords = baca_listKeywords.split()
        self.highlightingRules = [  highlightRule(QRegExp("\\b" + key + "\\b"), keyword)
                                    for key in listKeywords
                                    ]
    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index      = expression.indexIn(text)
            while index >= 0:
              length = expression.matchedLength()
              self.setFormat(index, length, rule.format)
              index = text.indexOf(expression, index + length)
        self.setCurrentBlockState(0)  
class highlightRule(object):
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format  = format
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
