from os import path
import sys
from PyQt5.sip import delete
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDial, QDialog, QApplication, QStackedLayout, QStackedWidget, QWidget
from add_note import datahandler
# initialize global flag for remember checks
flag = False

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.createnewaccount.clicked.connect(self.createacc)

    def gotologin(self):
        global flag
        login = LoginScreen()
        if flag:
            self.gotohome()
        else:
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotohome(self):
        mainScreen = MainScreen()
        widget.addWidget(mainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def createacc(self):
        createaccount = CreateAccountScreen()
        widget.addWidget(createaccount)
        widget.setCurrentIndex(widget.currentIndex()+1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.checkBox.stateChanged.connect(self.keeploggedin)
        self.login.clicked.connect(self.loginfunction)
        self.backwelcome.clicked.connect(self.gotowelcome)

    def gotowelcome(self):
        welcomeScreen = WelcomeScreen()
        widget.addWidget(welcomeScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # login screen checker
    def keeploggedin(self):
        global flag
        flag = True

    def loginfunction(self):
        dic = {"Raman":"Raman@0987", "Shaman":"Shaman@0864"}

        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
            # print("Invalid")
        else:
            if user in dic.keys() and dic[user] == password:
                print("Success")
                self.error.setText("")
                mainScreen = MainScreen()
                widget.addWidget(mainScreen)
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif user in dic.keys():
                self.error.setText("Password incorrect")
            else:
                self.error.setText("Username incorrect")

class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi("createnewacc.ui", self)
        self.createnewbutton.clicked.connect(self.createnew)
        self.backwelcome.clicked.connect(self.gotowelcome)
    
    def gotowelcome(self):
        welcomeScreen = WelcomeScreen()
        widget.addWidget(welcomeScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    
    def createnew(self):
        username = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpass = self.confirmpasswordfield.text()

        if (username == 0) or (password == 0) or (confirmpass == 0):
            self.error.setText("Please enter all fields")
        elif password != confirmpass:
            self.error.setText("Passwords do not match!")
        else:
            self.error.setText("Account successfully created. Please go back and login")

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("homescreen.ui", self)
        self.addnote.clicked.connect(self.addNote)
        self.viewallnotes.clicked.connect(self.viewAllNotes)
        self.deletenote.clicked.connect(self.deleteNote)
        self.todayschedule.clicked.connect(self.todaySchedule)
        self.revisionsummary.clicked.connect(self.revisionSummary)
    
    def addNote(self):
        addNoteWindow = AddNote()
        widget.addWidget(addNoteWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

    def viewAllNotes(self):
        showAllNoteWindow = ShowAllNotes()
        widget.addWidget(showAllNoteWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def deleteNote(self):
        deleteNoteWindow = DeleteNote()
        widget.addWidget(deleteNoteWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def todaySchedule(self):
        todaySchedule = TodaySchedule()
        widget.addWidget(todaySchedule)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def revisionSummary(self):
        pass

class AddNote(QDialog):
    def __init__(self) -> None:
        super(AddNote, self).__init__()
        loadUi("addnotes.ui",self)
        self.addnote.clicked.connect(self.addNote)
        self.backhome.clicked.connect(self.gotohome)
        self.logoutbtn.clicked.connect(self.gotologout)
    
    def gotologout(self):
        global flag
        flag = False
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    
    def gotohome(self):
        mainScreen = MainScreen()
        widget.addWidget(mainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)    


    def addNote(self):
        title = self.titlefield.text()
        if self.pathfield.text() == 0:
            path = ''
        else:
            path = self.pathfield.text()
        if self.linkfield.text() == 0:
            link = ''
        else:
            link = self.linkfield.text()
        importance = self.impfield.text()
        obj1 = datahandler()
        try:
            obj1.insert_data(title=title, importance=importance, npath=path, nlink=link)
            self.error.setText("Note added successfully")
        except:
            self.error.setText("Please checked all the details.")

class ShowAllNotes(QDialog):
    def __init__(self):
        super(ShowAllNotes, self).__init__()
        loadUi("allnotes.ui",self)
        self.tableWidget.setColumnWidth(0,60)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(2,70)
        self.tableWidget.setColumnWidth(3,500)
        self.tableWidget.setColumnWidth(4,150)
        self.tableWidget.setColumnWidth(5,400)
        self.tableWidget.setHorizontalHeaderLabels(["Note ID","Title","Importance","Path","Date","Link"])
        self.backhome.clicked.connect(self.gotohome)
        self.showAllNotes()
        self.logoutbtn.clicked.connect(self.gotologout)
    
    def gotologout(self):
        global flag
        flag = False
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotohome(self):
        mainScreen = MainScreen()
        widget.addWidget(mainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def showAllNotes(self):
        obj1 = datahandler()
        result = obj1.show_data()
        tablerow = 0
        self.tableWidget.setRowCount(len(result))
        for row in obj1.show_data():
            self.tableWidget.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
            tablerow += 1

class DeleteNote(QDialog):
    def __init__(self):
        super(DeleteNote, self).__init__()
        loadUi("deletenote.ui",self)
        self.deletenote.clicked.connect(self.deleteNode)
        self.allnotes.clicked.connect(self.gotoallnotes)
        self.backhome.clicked.connect(self.gotohome)
        self.logoutbtn.clicked.connect(self.gotologout)
    
    def gotologout(self):
        global flag
        flag = False
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotohome(self):
        mainScreen = MainScreen()
        widget.addWidget(mainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoallnotes(self):
        showAllNotes = ShowAllNotes()
        widget.addWidget(showAllNotes)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def deleteNode(self):
        noteId = self.noteidfield.text()
        obj1 = datahandler()
        try:
            obj1.delete_data(noteId)
            self.error.setText("Deleted Note")
        except:
            print("Some error occured")

class TodaySchedule(QDialog):
    def __init__(self):
        super(TodaySchedule, self).__init__()
        loadUi("todayschedule.ui", self)
        self.tableWidget.setColumnWidth(0,60)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(2,150)
        self.backhome.clicked.connect(self.gotohome)
        self.allnotes.clicked.connect(self.gotoallnotes)
        self.checkschedule.clicked.connect(self.checkSchedule)
        self.todaySchedule()
        self.logoutbtn.clicked.connect(self.gotologout)
    
    def gotologout(self):
        global flag
        flag = False
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotohome(self):
        mainScreen = MainScreen()
        widget.addWidget(mainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoallnotes(self):
        showAllNotes = ShowAllNotes()
        widget.addWidget(showAllNotes)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def checkSchedule(self):
        input_date = self.dateEdit.date().toPyDate()
        print(input_date)
        obj1 = datahandler()
        required_list = obj1.today_schedule(today=input_date)
        print(required_list)
        tablerow = 0
        self.tableWidget.setRowCount(len(required_list))
        for row in required_list:
            self.tableWidget.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1

    def todaySchedule(self):
        obj1 = datahandler()
        required_list = obj1.today_schedule()
        tablerow = 0
        self.tableWidget.setRowCount(len(required_list))
        for row in required_list:
            self.tableWidget.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1

# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(680)
widget.setFixedWidth(1280)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")