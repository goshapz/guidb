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
        self._create_shedule_tab2()

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
        self.tabs.addTab(self.shedule_tab, "odd week")

        self.monday_gbox = QGroupBox("")
        self.tuesday_gbox = QGroupBox("")
        self.wednesday_gbox = QGroupBox("")
        self.thursday_gbox = QGroupBox("")
        self.friday_gbox = QGroupBox("")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shboxt = QHBoxLayout()
        self.shboxw = QHBoxLayout()
        self.shboxth = QHBoxLayout()
        self.shboxf = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shboxt)
        self.svbox.addLayout(self.shboxw)
        self.svbox.addLayout(self.shboxth)
        self.svbox.addLayout(self.shboxf)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shboxt.addWidget(self.tuesday_gbox)
        self.shboxw.addWidget(self.wednesday_gbox)
        self.shboxth.addWidget(self.thursday_gbox)
        self.shboxf.addWidget(self.friday_gbox)

        self._create_monday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_shedule_tab2(self):
        self.shedule_tab0 = QWidget()
        self.tabs.addTab(self.shedule_tab0, "even week")

        self.monday_gbox0 = QGroupBox("")
        self.tuesday_gbox0 = QGroupBox("")
        self.wednesday_gbox0 = QGroupBox("")
        self.thursday_gbox0 = QGroupBox("")
        self.friday_gbox0 = QGroupBox("")

        self.svbox0 = QVBoxLayout()
        self.shbox01 = QHBoxLayout()
        self.shbox0t = QHBoxLayout()
        self.shbox0w = QHBoxLayout()
        self.shbox0th = QHBoxLayout()
        self.shbox0f = QHBoxLayout()
        self.shbox02 = QHBoxLayout()

        self.svbox0.addLayout(self.shbox01)
        self.svbox0.addLayout(self.shbox0t)
        self.svbox0.addLayout(self.shbox0w)
        self.svbox0.addLayout(self.shbox0th)
        self.svbox0.addLayout(self.shbox0f)
        self.svbox0.addLayout(self.shbox02)

        self.shbox01.addWidget(self.monday_gbox0)
        self.shbox0t.addWidget(self.tuesday_gbox0)
        self.shbox0w.addWidget(self.wednesday_gbox0)
        self.shbox0th.addWidget(self.thursday_gbox0)
        self.shbox0f.addWidget(self.friday_gbox0)

        self._create_monday_table0()

        self.update_shedule_button0 = QPushButton("Update")
        self.shbox02.addWidget(self.update_shedule_button0)
        self.update_shedule_button0.clicked.connect(self._update_shedule0)

        self.shedule_tab0.setLayout(self.svbox0)

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

        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["id", "Subject", "", ""])

        self._update_subject_table()

        self.mvbox11 = QVBoxLayout()
        self.mvbox11.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox11)

    def _update_subject_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM subjects order by id;")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")
            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, joinButton)
            self.subject_table.setCellWidget(i, 3, joinButton2)
            joinButton.clicked.connect(lambda ch, num=i: self._change_subject_from_table(num))
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_subject_from_table(num))
        joinButton = QPushButton("New")
        self.subject_table.setCellWidget(len(records), 3, joinButton)
        joinButton.clicked.connect(lambda ch: self.insert_subject())
        self.subject_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.subject_table.setItem(len(records), 2,
                                   QTableWidgetItem('-'))
        self.subject_table.resizeRowsToContents()

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.tuesday_table = QTableWidget()
        self.wednesday_table = QTableWidget()
        self.thursday_table = QTableWidget()
        self.friday_table = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(8)
        self.monday_table.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.tuesday_table.setColumnCount(8)
        self.tuesday_table.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.wednesday_table.setColumnCount(8)
        self.wednesday_table.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.thursday_table.setColumnCount(8)
        self.thursday_table.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.friday_table.setColumnCount(8)
        self.friday_table.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _create_monday_table0(self):
        self.monday_table0 = QTableWidget()
        self.tuesday_table0 = QTableWidget()
        self.wednesday_table0 = QTableWidget()
        self.thursday_table0 = QTableWidget()
        self.friday_table0 = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table0.setColumnCount(8)
        self.monday_table0.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.tuesday_table0.setColumnCount(8)
        self.tuesday_table0.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.wednesday_table0.setColumnCount(8)
        self.wednesday_table0.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.thursday_table0.setColumnCount(8)
        self.thursday_table0.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self.friday_table0.setColumnCount(8)
        self.friday_table0.setHorizontalHeaderLabels(["id", "day", "week", "Subject", "Room", "Time", "", ""])

        self._update_monday_table0()

        self.mvbox0 = QVBoxLayout()
        self.mvbox0.addWidget(self.monday_table0)
        self.monday_gbox0.setLayout(self.mvbox0)

        self.mvbox0 = QVBoxLayout()
        self.mvbox0.addWidget(self.tuesday_table0)
        self.tuesday_gbox0.setLayout(self.mvbox0)

        self.mvbox0 = QVBoxLayout()
        self.mvbox0.addWidget(self.wednesday_table0)
        self.wednesday_gbox0.setLayout(self.mvbox0)

        self.mvbox0 = QVBoxLayout()
        self.mvbox0.addWidget(self.thursday_table0)
        self.thursday_gbox0.setLayout(self.mvbox0)

        self.mvbox0 = QVBoxLayout()
        self.mvbox0.addWidget(self.friday_table0)
        self.friday_gbox0.setLayout(self.mvbox0)

    def _create_teacher_table(self):
        self.conn.rollback()
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["id", "teacher", "Subject", "", ""])

        self._update_teacher_table()

        self.mvbox3 = QVBoxLayout()
        self.mvbox3.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox3)

    def _update_monday_table0(self):
        self.conn.rollback()
        self.monday_table0.setRowCount(0)
        self.tuesday_table0.setRowCount(0)
        self.wednesday_table0.setRowCount(0)
        self.thursday_table0.setRowCount(0)
        self.friday_table0.setRowCount(0)
        self.cursor.execute(
            "SELECT * FROM timetable where day = 'monday' and week = 'even' or day = 'write here' order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table0.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.monday_table0.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.monday_table0.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.monday_table0.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.monday_table0.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.monday_table0.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.monday_table0.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.monday_table0.setCellWidget(i, 6, joinButton)
            self.monday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablee(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablee(num))
        self.monday_table0.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 1,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 2,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 3,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 4,
                                   QTableWidgetItem('-'))
        joinButton1: Union[QPushButton, QPushButton] = QPushButton("New")
        self.monday_table0.setCellWidget(len(records), 6, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=len(records): self.insert_day())

        self.cursor.execute("SELECT * FROM timetable where day = 'tuesday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.tuesday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.tuesday_table0.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))
            self.tuesday_table0.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))
            self.tuesday_table0.setItem(i, 2,
                                        QTableWidgetItem(str(r[5])))
            self.tuesday_table0.setItem(i, 3,
                                        QTableWidgetItem(str(r[2])))
            self.tuesday_table0.setItem(i, 4,
                                        QTableWidgetItem(str(r[3])))
            self.tuesday_table0.setItem(i, 5,
                                        QTableWidgetItem(str(r[4])))
            self.tuesday_table0.setCellWidget(i, 6, joinButton)
            self.tuesday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablete(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablete(num))
        joinButton3 = QPushButton("New")
        self.tuesday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.tuesday_table0.resizeRowsToContents()
        self.monday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'wednesday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.wednesday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.wednesday_table0.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.wednesday_table0.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
            self.wednesday_table0.setItem(i, 2,
                                          QTableWidgetItem(str(r[5])))
            self.wednesday_table0.setItem(i, 3,
                                          QTableWidgetItem(str(r[2])))
            self.wednesday_table0.setItem(i, 4,
                                          QTableWidgetItem(str(r[3])))
            self.wednesday_table0.setItem(i, 5,
                                          QTableWidgetItem(str(r[4])))
            self.wednesday_table0.setCellWidget(i, 6, joinButton)
            self.wednesday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablewe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablewe(num))
        joinButton3 = QPushButton("New")
        self.wednesday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.wednesday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'thursday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.thursday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.thursday_table0.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.thursday_table0.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.thursday_table0.setItem(i, 2,
                                         QTableWidgetItem(str(r[5])))
            self.thursday_table0.setItem(i, 3,
                                         QTableWidgetItem(str(r[2])))
            self.thursday_table0.setItem(i, 4,
                                         QTableWidgetItem(str(r[3])))
            self.thursday_table0.setItem(i, 5,
                                         QTableWidgetItem(str(r[4])))
            self.thursday_table0.setCellWidget(i, 6, joinButton)
            self.thursday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablethe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablethe(num))
        joinButton3 = QPushButton("New")
        self.thursday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.thursday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'friday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.friday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.friday_table0.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.friday_table0.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.friday_table0.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.friday_table0.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.friday_table0.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.friday_table0.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.friday_table0.setCellWidget(i, 6, joinButton)
            self.friday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablefe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablefe(num))
        joinButton3 = QPushButton("New")
        self.friday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.friday_table0.resizeRowsToContents()

    def _update_monday_table(self):
        self.conn.rollback()
        self.monday_table.setRowCount(0)
        self.tuesday_table.setRowCount(0)
        self.wednesday_table.setRowCount(0)
        self.thursday_table.setRowCount(0)
        self.friday_table.setRowCount(0)
        self.cursor.execute(
            "SELECT * FROM timetable where day = 'monday' and week = 'odd' or day = 'write here' order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[5])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 5,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 6, joinButton)
            self.monday_table.setCellWidget(i, 7, joinButton2)
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
        self.monday_table.setItem(len(records), 4,
                                  QTableWidgetItem('-'))
        joinButton1: Union[QPushButton, QPushButton] = QPushButton("New")
        self.monday_table.setCellWidget(len(records), 6, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=len(records): self.insert_day())

        self.cursor.execute("SELECT * FROM timetable where day = 'tuesday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.tuesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.tuesday_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.tuesday_table.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.tuesday_table.setCellWidget(i, 6, joinButton)
            self.tuesday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tableto(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tableto(num))
        joinButton3 = QPushButton("New")
        self.tuesday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.tuesday_table.resizeRowsToContents()
        self.monday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'wednesday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.wednesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.wednesday_table.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2,
                                         QTableWidgetItem(str(r[5])))
            self.wednesday_table.setItem(i, 3,
                                         QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 4,
                                         QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 5,
                                         QTableWidgetItem(str(r[4])))
            self.wednesday_table.setCellWidget(i, 6, joinButton)
            self.wednesday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablewo(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablewo(num))
        joinButton3 = QPushButton("New")
        self.wednesday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.wednesday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'thursday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.thursday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.thursday_table.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2,
                                        QTableWidgetItem(str(r[5])))
            self.thursday_table.setItem(i, 3,
                                        QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 4,
                                        QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 5,
                                        QTableWidgetItem(str(r[4])))
            self.thursday_table.setCellWidget(i, 6, joinButton)
            self.thursday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tabletho(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tabletho(num))
        joinButton3 = QPushButton("New")
        self.thursday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.thursday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'friday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.friday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.friday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[5])))
            self.friday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 5,
                                      QTableWidgetItem(str(r[4])))
            self.friday_table.setCellWidget(i, 6, joinButton)
            self.friday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablefo(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablefo(num))
        joinButton3 = QPushButton("New")
        self.friday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.friday_table.resizeRowsToContents()

    def insert_day(self):
        self.conn.rollback()
        self.cursor.execute(
            "INSERT INTO timetable (day, subject, room, time, week) values('write here',"
            " 'maths','write here', 'write here', 'write here');", )
        self.conn.commit()
        self._update_monday_table()
        self._update_monday_table0()

    def _update_teacher_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM teacher order by id;")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            self.teacher_table.setCellWidget(i, 4, joinButton2)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_teacher_from_table(num))

        joinButton1 = QPushButton("New")
        self.teacher_table.setCellWidget(len(records), 3, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=len(records) + 1: self.insert_teacher())
        self.teacher_table.resizeRowsToContents()

    def _change_subject_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row[0], rowNum)
        print(int(int(rowNum) + 1))
        try:
            self.cursor.execute("Update subjects set subject ='{}' where id = '{}'".format(row[1], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tableto(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablewo(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tabletho(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablefo(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablee(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.monday_table0.columnCount()):
            try:
                row.append(self.monday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablete(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.tuesday_table0.columnCount()):
            try:
                row.append(self.tuesday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablewe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.wednesday_table0.columnCount()):
            try:
                row.append(self.wednesday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablethe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.thursday_table0.columnCount()):
            try:
                row.append(self.thursday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _change_day_from_tablefe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.friday_table0.columnCount()):
            try:
                row.append(self.friday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute(
                "update timetable set day='{}', week = '{}', subject='{}', room='{}', time='{}'  WHERE id='{}'".format(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Something wrong!")

    def _delete_day_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tableto(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablewo(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tabletho(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablefo(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablee(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.monday_table0.columnCount()):
            try:
                row.append(self.monday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablete(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.tuesday_table0_table.columnCount()):
            try:
                row.append(self.thursday_table0.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablewe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.wednesday_table0_table.columnCount()):
            try:
                row.append(self.wednesday_table0day_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablethe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.thursday_table0monday_table.columnCount()):
            try:
                row.append(self.thursday_table0_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_day_from_tablefe(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.friday_table0_table.columnCount()):
            try:
                row.append(self.friday_table0_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM timetable WHERE id = '{}'".format(row[0], ))
        self.conn.commit()

    def _delete_teacher_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM teacher WHERE id='{}'".format(row[0], ))
        self.conn.commit()
        self._update_teacher()

    def _delete_subject_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum + 5)
        self.cursor.execute("DELETE FROM subjects WHERE id='{}'".format(row[0], ))
        self.conn.commit()
        self._update_subject()

    def _change_teacher_from_table(self, rowNum):
        self.conn.rollback()
        row = list()
        for column in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, column).text())
            except:
                row.append(None)
        print(row, rowNum)

        try:
            self.cursor.execute("update teacher set teacher = '{}', subject ='{}' WHERE id ='{}';".format(row[1],
                                                                                                          row[2],
                                                                                                          row[0], ))
            self.conn.commit()
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", "Something wrong!")

    def _update_shedule(self):
        self.conn.rollback()
        self.monday_table.setRowCount(0)
        self.tuesday_table.setRowCount(0)
        self.wednesday_table.setRowCount(0)
        self.thursday_table.setRowCount(0)
        self.friday_table.setRowCount(0)
        self._update_monday_table()
        self.cursor.execute(
            "SELECT * FROM timetable where day = 'monday' and week = 'odd' or day = 'write here' order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[5])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 5,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 6, joinButton)
            self.monday_table.setCellWidget(i, 7, joinButton2)
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
        self.monday_table.setItem(len(records), 4,
                                  QTableWidgetItem('-'))
        joinButton1: Union[QPushButton, QPushButton] = QPushButton("New")
        self.monday_table.setCellWidget(len(records), 6, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=len(records): self.insert_day())

        self.cursor.execute("SELECT * FROM timetable where day = 'tuesday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.tuesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.tuesday_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.tuesday_table.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.tuesday_table.setCellWidget(i, 6, joinButton)
            self.tuesday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
        joinButton3 = QPushButton("New")
        self.tuesday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.tuesday_table.resizeRowsToContents()
        self.monday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'wednesday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.wednesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.wednesday_table.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2,
                                         QTableWidgetItem(str(r[5])))
            self.wednesday_table.setItem(i, 3,
                                         QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 4,
                                         QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 5,
                                         QTableWidgetItem(str(r[4])))
            self.wednesday_table.setCellWidget(i, 6, joinButton)
            self.wednesday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablewo(num))
        joinButton3 = QPushButton("New")
        self.wednesday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.wednesday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'thursday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.thursday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.thursday_table.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2,
                                        QTableWidgetItem(str(r[5])))
            self.thursday_table.setItem(i, 3,
                                        QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 4,
                                        QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 5,
                                        QTableWidgetItem(str(r[4])))
            self.thursday_table.setCellWidget(i, 6, joinButton)
            self.thursday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tabletho(num))
        joinButton3 = QPushButton("New")
        self.thursday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.thursday_table.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'friday' and week = 'odd' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.friday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.friday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[5])))
            self.friday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 5,
                                      QTableWidgetItem(str(r[4])))
            self.friday_table.setCellWidget(i, 6, joinButton)
            self.friday_table.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablefo(num))
        joinButton3 = QPushButton("New")
        self.friday_table.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.friday_table.resizeRowsToContents()

    def _update_shedule0(self):

        self.conn.rollback()
        self.monday_table0.setRowCount(0)
        self.tuesday_table0.setRowCount(0)
        self.wednesday_table0.setRowCount(0)
        self.thursday_table0.setRowCount(0)
        self.friday_table0.setRowCount(0)
        self.cursor.execute(
            "SELECT * FROM timetable where day = 'monday' and week = 'even' or day = 'write here' order by id;")
        records = list(self.cursor.fetchall())

        self.monday_table0.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.monday_table0.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.monday_table0.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.monday_table0.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.monday_table0.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.monday_table0.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.monday_table0.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.monday_table0.setCellWidget(i, 6, joinButton)
            self.monday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablee(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablee(num))
        self.monday_table0.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 1,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 2,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 3,
                                   QTableWidgetItem('-'))
        self.monday_table0.setItem(len(records), 4,
                                   QTableWidgetItem('-'))
        joinButton1: Union[QPushButton, QPushButton] = QPushButton("New")
        self.monday_table0.setCellWidget(len(records), 6, joinButton1)
        joinButton1.clicked.connect(lambda ch, num=len(records): self.insert_day())

        self.cursor.execute("SELECT * FROM timetable where day = 'tuesday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.tuesday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.tuesday_table0.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))
            self.tuesday_table0.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))
            self.tuesday_table0.setItem(i, 2,
                                        QTableWidgetItem(str(r[5])))
            self.tuesday_table0.setItem(i, 3,
                                        QTableWidgetItem(str(r[2])))
            self.tuesday_table0.setItem(i, 4,
                                        QTableWidgetItem(str(r[3])))
            self.tuesday_table0.setItem(i, 5,
                                        QTableWidgetItem(str(r[4])))
            self.tuesday_table0.setCellWidget(i, 6, joinButton)
            self.tuesday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablete(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablete(num))
        joinButton3 = QPushButton("New")
        self.tuesday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.tuesday_table0.resizeRowsToContents()
        self.monday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'wednesday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.wednesday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.wednesday_table0.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.wednesday_table0.setItem(i, 1,
                                          QTableWidgetItem(str(r[1])))
            self.wednesday_table0.setItem(i, 2,
                                          QTableWidgetItem(str(r[5])))
            self.wednesday_table0.setItem(i, 3,
                                          QTableWidgetItem(str(r[2])))
            self.wednesday_table0.setItem(i, 4,
                                          QTableWidgetItem(str(r[3])))
            self.wednesday_table0.setItem(i, 5,
                                          QTableWidgetItem(str(r[4])))
            self.wednesday_table0.setCellWidget(i, 6, joinButton)
            self.wednesday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablewe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablewe(num))
        joinButton3 = QPushButton("New")
        self.wednesday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.wednesday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'thursday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.thursday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.thursday_table0.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.thursday_table0.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.thursday_table0.setItem(i, 2,
                                         QTableWidgetItem(str(r[5])))
            self.thursday_table0.setItem(i, 3,
                                         QTableWidgetItem(str(r[2])))
            self.thursday_table0.setItem(i, 4,
                                         QTableWidgetItem(str(r[3])))
            self.thursday_table0.setItem(i, 5,
                                         QTableWidgetItem(str(r[4])))
            self.thursday_table0.setCellWidget(i, 6, joinButton)
            self.thursday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablethe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablethe(num))
        joinButton3 = QPushButton("New")
        self.thursday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.thursday_table0.resizeRowsToContents()

        self.cursor.execute("SELECT * FROM timetable where day = 'friday' and week = 'even' "
                            "or day = 'write here' "
                            "order by id;")
        records = list(self.cursor.fetchall())
        self.friday_table0.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.friday_table0.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.friday_table0.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.friday_table0.setItem(i, 2,
                                       QTableWidgetItem(str(r[5])))
            self.friday_table0.setItem(i, 3,
                                       QTableWidgetItem(str(r[2])))
            self.friday_table0.setItem(i, 4,
                                       QTableWidgetItem(str(r[3])))
            self.friday_table0.setItem(i, 5,
                                       QTableWidgetItem(str(r[4])))
            self.friday_table0.setCellWidget(i, 6, joinButton)
            self.friday_table0.setCellWidget(i, 7, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tablefe(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_tablefe(num))
        joinButton3 = QPushButton("New")
        self.friday_table0.setCellWidget(len(records), 6, joinButton3)
        joinButton3.clicked.connect(lambda ch: self.insert_day())
        self.friday_table0.resizeRowsToContents()

    def _update_subject(self):
        self.conn.rollback()
        self.subject_table.setRowCount(0)
        self._update_subject_table()
        self.cursor.execute("SELECT * FROM subjects order by id;")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton2 = QPushButton("Delete")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, joinButton)
            self.subject_table.setCellWidget(i, 3, joinButton2)
            joinButton2.clicked.connect(lambda ch, num=i: self._delete_subject_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_subject_from_table(num))
        self.subject_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.subject_table.setItem(len(records), 3,
                                   QTableWidgetItem('-'))
        self.subject_table.resizeRowsToContents()

    def _update_teacher(self):
        self.conn.rollback()
        self._update_teacher_table()
        self.teacher_table.setRowCount(0)
        self.cursor.execute("SELECT * FROM teacher order by id;")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Set")
            joinButton1 = QPushButton('Delete')
            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            self.teacher_table.setCellWidget(i, 4, joinButton1)
            joinButton1.clicked.connect(lambda ch, num=i: self._delete_teacher_from_table(num))
            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
        joinButton1 = QPushButton("New")
        self.teacher_table.setCellWidget(len(records), 3, joinButton1)
        self.teacher_table.setItem(len(records), 0,
                                   QTableWidgetItem('-'))
        self.teacher_table.setItem(len(records), 1,
                                   QTableWidgetItem('-'))
        self.teacher_table.setItem(len(records), 3,
                                   QTableWidgetItem('-'))
        joinButton1.clicked.connect(lambda ch: self.insert_teacher())
        self.teacher_table.resizeRowsToContents()

    def insert_teacher(self):
        self.conn.rollback()
        self.cursor.execute("INSERT INTO teacher (teacher, subject) VALUES ('write here', 'maths');")
        self.conn.commit()
        self._update_teacher()

    def insert_subject(self):
        self.conn.rollback()
        self.cursor.execute("INSERT INTO subjects (subject) VALUES ('write here');")
        self.conn.commit()
        self._update_subject()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
