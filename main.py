from typing import Union

import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                            QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="GUI",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("GUI")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_teacher_tab()
        self._create_subject_tab()
        self._create_shedule_tab()

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teacher")

        self.teacher_gbox = QGroupBox("")

        self.svbox3 = QVBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()

        self.svbox3.addLayout(self.shbox4)
        self.svbox3.addLayout(self.shbox5)

        self.shbox4.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.update_teacher_button = QPushButton("Update")
        self.shbox5.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_teacher)

        self.teacher_tab.setLayout(self.svbox3)

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Timetable")

        self.monday_gbox = QGroupBox("")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)

        self._create_monday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.subject_gbox = QGroupBox("")

        self.svbox11 = QVBoxLayout()
        self.shbox12 = QHBoxLayout()
        self.shbox13 = QHBoxLayout()

        self.svbox11.addLayout(self.shbox12)
        self.svbox11.addLayout(self.shbox13)

        self.shbox12.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.update_subject_button = QPushButton("Update")
        self.shbox13.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_subject)

        self.subject_tab.setLayout(self.svbox11)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Subject", "", ""])

        self._update_subject_table()

        self.mvbox11 = QVBoxLayout()
        self.mvbox11.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox11)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subjects order by id;")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")
            self.subject_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, joinButton2)
            joinButton.clicked.connect(lambda ch, num=i: self._change_subject_from_table(num))
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_subject_from_table(num))
        joinButton = QPushButton("New")
        self.subject_table.setCellWidget(len(records), 1, joinButton)
        joinButton.clicked.connect(lambda ch: self.insert_subject())
        self.subject_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.subject_table.setItem(i, 3,
                                   QTableWidgetItem('-'))
        self.subject_table.resizeRowsToContents()

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(["day", "Subject", "Room", "Time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(["teacher", "Subject", "", ""])

        self._update_teacher_table()

        self.mvbox3 = QVBoxLayout()
        self.mvbox3.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox3)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 4, joinButton)
            self.monday_table.setCellWidget(i, 5, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
        joinButton = QPushButton("New")
        self.monday_table.setCellWidget(len(records), 4, joinButton)
        joinButton.clicked.connect(lambda ch: self.insert_day())
        self.monday_table.resizeRowsToContents()

    def insert_day(self):
        self.cursor.execute("INSERT INTO timetable (day, subject, room, time) values('write here', 'maths','write here', 'write here');",)
        self.conn.commit()
        self._update_shedule()

    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher order by id;")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 2, joinButton)
            self.teacher_table.setCellWidget(i, 3, joinButton2)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_teacher_from_table(num))

        joinButton1 = QPushButton("New")
        self.teacher_table.setCellWidget(len(records), 2, joinButton1)
        joinButton.clicked.connect(lambda ch, num=len(records) + 1: self._change_teacher_from_table(num))
        self.teacher_table.resizeRowsToContents()

    def _change_subject_from_table(self, rowNum):
        row = list()
        for column in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row[0], rowNum)
        print(int(int(rowNum)+1))
        try:
            self.cursor.execute("Update subjects set subject ='{}' where subject = 'write here'".format(row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_table(self, rowNum):
        row = list()
        for column in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute("update timetable set day='{}', subject='{}', room='{}', time='{}'  WHERE day='write here'".format(row[0], row[1],
                                                                     row[2], row[3]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _delete_day_from_table(self, rowNum):
        row = list()
        for column in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum+5)
        self.cursor.execute("DELETE FROM timetable WHERE day='{}' and subject='{}'"
                                "and room='{}' and time='{}'".format(row[0], row[1],
                                                                               row[2], row[3]))
        self.conn.commit()

    def _delete_teacher_from_table(self, rowNum):
        row = list()
        for column in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum+5)
        self.cursor.execute("DELETE FROM teacher WHERE teacher='{}' and subject='{}'".format(row[0], row[1],))
        self.conn.commit()
        self._update_teacher()

    def _delete_subject_from_table(self, rowNum):
        row = list()
        for column in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum+5)
        self.cursor.execute("DELETE FROM subjects WHERE subject='{}'".format(row[0],))
        self.conn.commit()
        self._update_subject()

    def _change_teacher_from_table(self, rowNum):
        row = list()
        for column in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute("update teacher set teacher = "
                                "%s, subject = %s where teacher = 'write here'", (row[0], row[1],))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _update_shedule(self):
        self._update_monday_table()
        self.cursor.execute("SELECT * FROM timetable order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton1: Union[QPushButton, QPushButton] = QPushButton("New")
            joinButton2 = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 4, joinButton)
            self.monday_table.setCellWidget(i, 5, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
        self.monday_table.setItem(len(records), 0,
                                  QTableWidgetItem('-'))
        self.monday_table.setItem(len(records), 1,
                                  QTableWidgetItem('-'))
        self.monday_table.setItem(len(records), 2,
                                  QTableWidgetItem('-'))
        self.monday_table.setItem(len(records), 3,
                                  QTableWidgetItem('-'))
        self.monday_table.setItem(len(records), 5,
                                  QTableWidgetItem('-'))
        self.monday_table.setCellWidget(len(records), 4, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
        self.monday_table.resizeRowsToContents()

    def _update_subject(self):
        self._update_subject_table()
        self.cursor.execute("SELECT * FROM subjects order by id;")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.subject_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_subject_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_subject_from_table(num))
        self.subject_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.subject_table.setItem(i, 3,
                                   QTableWidgetItem('-'))
        self.subject_table.resizeRowsToContents()

    def _update_teacher(self):
        self._update_teacher_table()
        self.cursor.execute("SELECT * FROM teacher order by id;")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")

            self.teacher_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 2, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
        joinButton1 = QPushButton("New")
        self.teacher_table.setCellWidget(len(records), 2, joinButton1)
        self.teacher_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.teacher_table.setItem(len(records), 1,
                                   QTableWidgetItem('-'))
        self.teacher_table.setItem(len(records), 3,
                                   QTableWidgetItem('-'))
        joinButton1.clicked.connect(lambda ch: self.insert_teacher())
        self.teacher_table.resizeRowsToContents()

    def insert_teacher(self):
        self.cursor.execute("INSERT INTO teacher (teacher, subject) VALUES ('write here', 'maths');")
        self.conn.commit()
        self._update_teacher()

    def insert_subject(self):
        self.cursor.execute("INSERT INTO subjects (subject) VALUES ('write here');")
        self.conn.commit()
        self._update_subject()



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
