import sys
import csv
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QApplication, QStackedWidget
from firstLook import BankAccount
from isnumberic import isnumeric
import jdatetime
from PyQt6.QtCore import QTimer
import pandas as pd
import numpy as np

class FirstScreen(QDialog):
    def __init__(self):
        super(FirstScreen, self).__init__()
        uic.loadUi("First_Screen.ui", self)
        self.create_account.clicked.connect(self.goto_CreateAccount)
        self.confirm.clicked.connect(self.goto_Features)
        self.manager_login.clicked.connect(self.goto_manager)####

    def goto_CreateAccount(self):
        create_account = CreateAccount(self)
        widget.addWidget(create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        

    def goto_Features(self):
        create_account = CreateAccount(self)
        features = Features(self, create_account)
        widget.addWidget(features)
        data = self.lineEdit.text()
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                if data == line[5]:
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    self.data = data
                    return
        self.blank_label.setText("شرمنده، همچین شماره حسابی ثبت نشده!")
        widget.removeWidget(features)

    def goto_manager(self):
        manager_login = LoginManager(self)
        widget.addWidget(manager_login)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class CreateAccount(QDialog):
    def __init__(self, first_screen):
        super(CreateAccount, self).__init__()
        uic.loadUi("Create_Account.ui", self)
        self.push1122.clicked.connect(self.goto_homepage)
        self.first_screen = first_screen
        self.confirm_create.clicked.connect(self.goto_final_confirmation)
        self.onlyInt = QIntValidator()
        self.national_input.setValidator(self.onlyInt)
        self.iaom_input.setValidator(self.onlyInt)


    def goto_homepage(self):
        print("Hululululu")#this line will delete
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        self.first_screen.blank_label.setText("")
        self.first_screen.lineEdit.setText("")

    def goto_final_confirmation(self):
        global name
        name = self.name_input.text()
        global family
        family = self.family_input.text()
        global national_code
        national_code = self.national_input.text()
        global iaom
        iaom = self.iaom_input.text()

        if bool(name) == False or bool(family) == False or bool(national_code) == False or bool(iaom) == False:
            self.blank_label_2.setText("خطا : باید تمام فیلد ها را پر کنید")
            self.blank_label_2.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
            return
        
        elif len(name) < 2 or isnumeric(name) == True:
            self.blank_label_2.setText("نام وارد شده معتبر نیست")
            self.blank_label_2.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
            return
        elif len(family) < 2:
            self.blank_label_2.setText("نام خانوادگی وارد شده معتبر نیست")
            self.blank_label_2.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
            return
        elif len(national_code) != 10:
            self.blank_label_2.setText("کد ملی باید عددی ده رقمی باشد")
            self.blank_label_2.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
            return
        elif int(iaom) <= 10:
            self.blank_label_2.setText("مقدار واریزی اولیه نامعتبر است")
            self.blank_label_2.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
            return
        else:
            self.blank_label_2.setText("با موفقیت اکانت شما ساخته شد")
            self.blank_label_2.setStyleSheet("color:#16FF00; font: 700 17pt Vazir;")
            self.bank_account = BankAccount(name, family, national_code, iaom)
            print("GGGGGG")

        info = Info(self, self.first_screen)
        widget.addWidget(info)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)


class Features(QDialog):
    def __init__(self, first_screen, create_account):
        super(Features, self).__init__()
        uic.loadUi("Features.ui", self)
        self.return_features.clicked.connect(self.goto_homepage)
        self.first_screen = first_screen
        self.balance_push.clicked.connect(self.goto_balance)
        self.create_account = create_account
        self.withdraw_push.clicked.connect(self.goto_withdraw)
        self.transfer_push.clicked.connect(self.goto_transform)
        self.turnovers_push.clicked.connect(self.goto_turnovers)
        self.loan_push.clicked.connect(self.goto_loan)

    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        self.first_screen.blank_label.setText("")
        self.first_screen.lineEdit.setText("")

    def goto_balance(self):
        balance = Balance(self.first_screen)
        widget.addWidget(balance)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def goto_withdraw(self):
        withdraw = Withdraw(self.first_screen)
        widget.addWidget(withdraw)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_transform(self):
        transform = Transform(self.first_screen)
        widget.addWidget(transform)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_turnovers(self):
        turnovers = Turnovers(self.first_screen)
        widget.addWidget(turnovers)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_loan(self):
        loan = Loan(self, self.first_screen)
        widget.addWidget(loan)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Info(QDialog):
    def __init__(self, create_account, first_screen):
        super(Info, self).__init__()
        uic.loadUi("Info.ui", self)
        self.name_info.setText(name)
        self.family_info.setText(family)
        self.national_code_info.setText(f"{national_code}")
        self.create_account = create_account
        self.account_number_info.setText(f"{self.create_account.bank_account.accountNumber}")
        self.confirm_info.clicked.connect(self.goto_homepage)
        self.first_screen = first_screen
        with open(f"G:\Smartech PRJ_1\\turnovers\{self.create_account.bank_account.accountNumber}.csv", "w", newline = "") as f:
            writer = csv.writer(f)
            for i in range(3):
                writer.writerow(["-", "-"])
        
    
    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        self.first_screen.blank_label.setText("")
        self.first_screen.lineEdit.setText("")


class Balance(QDialog):
    def __init__(self, first_screen):
        super(Balance, self).__init__()
        uic.loadUi("Balance.ui", self)
        self.return_balance.clicked.connect(self.goto_features)
        self.first_screen = first_screen
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                print(line)
                if line[5] == self.first_screen.data:
                    self.balance = line[4]
        self.dollar_label.setText(f"{self.balance}")    
        self.rial_label.setText(f"{int(self.balance) * 50_000}")
        

    def goto_features(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)


class Withdraw(QDialog):
    def __init__(self, first_screen):
        super(Withdraw, self).__init__()
        uic.loadUi("Withdraw.ui", self)
        self.return_withdraw.clicked.connect(self.goto_homepage)
        self.confirm_withdraw.clicked.connect(self.withdrawing)
        self.onlyInt = QIntValidator()
        self.withdraw_input.setValidator(self.onlyInt)
        self.first_screen = first_screen


    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def withdrawing(self):
        data = self.withdraw_input.text()
        acc_number = self.first_screen.data
        counter = 0
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                counter += 1
                if line[5] == acc_number:
                    self.balance = line[4]
                    break
                    

        if int(data) > int(self.balance):
            self.blank_label_withdraw.setText("موجودی حساب کافی نیست")
            self.blank_label_withdraw.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
        else:
            self.balance = int(self.balance) - int(data)
            self.blank_label_withdraw.setText("وجه با موفقیت برداشت شد")
            self.blank_label_withdraw.setStyleSheet("color:#16FF00; font: 700 17pt Vazir;")
            with open(f"G:\Smartech PRJ_1\\turnovers\{acc_number}.csv", "a", newline = "") as f:
                writer = csv.writer(f)
                writer.writerow([f"-{data}", "bardasht"])##
        
        r = csv.reader(open("main.csv"))
        lines = list(r)
        print(counter)##this line will delete
        lines[counter - 1][4] = int(self.balance)
        writer = csv.writer(open("main.csv", 'w', newline = ""))
        writer.writerows(lines)

class Transform(QDialog):
    def __init__(self, first_screen):
        super(Transform, self).__init__()
        uic.loadUi("Transform.ui", self)
        self.first_screen = first_screen
        self.return_transform.clicked.connect(self.goto_homepage)
        self.confirm_transform.clicked.connect(self.transform)
        self.onlyInt = QIntValidator()
        self.begin_transform.setValidator(self.onlyInt)
        self.final_transform.setValidator(self.onlyInt)
        self.value_transform.setValidator(self.onlyInt)
    
    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def goto_comfirmation(self):
        transform_comfirmation = TransformConfirmation(self.first_screen, self)
        widget.addWidget(transform_comfirmation)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def transform(self):
        self.begin = int(self.begin_transform.text())
        self.final = int(self.final_transform.text())
        self.value = int(self.value_transform.text())

        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            self.balance = ""
            counter_begin = 0
            for line in lines:
                counter_begin += 1
                if line[5] == str(self.begin):
                    self.balance = int(line[4])
                    break

            if self.balance == "":
                self.blank_label_transform.setText("شماره کارت مبدا معتبر نیست")
                self.blank_label_transform.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
                return
            
            if str(self.begin) != self.first_screen.data:
                self.blank_label_transform.setText("انتقال از این کارت مجاز نیست")
                self.blank_label_transform.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
                return
            
        with open("main.csv", "r") as f:
            lines = csv.reader(f)   
            counter_final = 0
            self.fbalance = ""
            for line in lines:
                counter_final += 1
                if line[5] == str(self.final):
                    self.fbalance = int(line[4])
                    self.fname = line[0]
                    self.flastname = line[1]
                    break
            
            if self.fbalance == "":
                self.blank_label_transform.setText("شماره کارت مقصد معتبر نیست")
                self.blank_label_transform.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
                return
            

        if self.value > self.balance:
            self.blank_label_transform.setText("موجودی حساب کافی نیست")
            self.blank_label_transform.setStyleSheet("color:rgb(255, 0, 0); font: 700 17pt Vazir;")
        else:
            self.balance = self.balance - self.value
            self.fbalance = self.fbalance + self.value
            self.goto_comfirmation()#UPDATED
            self.begin_transform.setText("")
            self.final_transform.setText("")
            self.value_transform.setText("")
        

        r = csv.reader(open("main.csv"))
        lines = list(r)
        lines[counter_begin - 1][4] = int(self.balance)
        lines[counter_final - 1][4] = int(self.fbalance)
        writer = csv.writer(open("main.csv", 'w', newline = ""))
        writer.writerows(lines)

        # with open(f"G:\Smartech PRJ_1\\turnovers\{self.begin}.csv", "a", newline = "") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([f"-{self.value}"])
        
        # with open(f"G:\Smartech PRJ_1\\turnovers\{self.final}.csv", "a", newline = "") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([f"+{self.value}"])


class TransformConfirmation(QDialog):
    def __init__(self, fisrt_screen, transform):
        super(TransformConfirmation, self).__init__()
        uic.loadUi("Transform_Confirmatino.ui", self)
        self.first_screen = fisrt_screen
        self.transform = transform
        self.back_tr.clicked.connect(self.goto_homepage)
        self.amount.setText(f"{self.transform.value}")
        self.fname.setText(self.transform.fname)
        self.lname.setText(self.transform.flastname)
        now = jdatetime.datetime.now()
        self.date_real = now.strftime("%Y-%m-%d")
        self.time_real = now.strftime("%H:%M:%S")
        self.date.setText(self.date_real)
        self.date33.setText(self.time_real)
        self.confirm_tr.clicked.connect(self.goto_final)


    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def goto_final(self):
        transform_final = TransformFinal(self.transform)
        widget.addWidget(transform_final)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self.transform)
        widget.removeWidget(self)

class TransformFinal(QDialog):
    def __init__(self, transform):
        super(TransformFinal, self).__init__()
        uic.loadUi("Transform_Final.ui", self)
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)
        self.log_label.setText("درحال انتقال وجه...")
        self.return_features_2.setVisible(False)
        self.return_features_2.clicked.connect(self.goto_homepage)
        self.transform = transform

    def update_progress(self):
        current_value = self.progressBar.value()
        new_value = current_value + 1
        if new_value <= self.progressBar.maximum():
            self.progressBar.setValue(new_value)

        else:
            self.log_label.setText("پرداخت با موفقیت انجام شد")
            self.return_features_2.setVisible(True)
            with open(f"G:\Smartech PRJ_1\\turnovers\{self.transform.begin}.csv", "a", newline = "") as f:
                writer = csv.writer(f)
                writer.writerow([f"-{self.transform.value}", "enteghal"])##
        
            with open(f"G:\Smartech PRJ_1\\turnovers\{self.transform.final}.csv", "a", newline = "") as f:
                writer = csv.writer(f)
                writer.writerow([f"+{self.transform.value}", "varizi"])##
                self.timer.stop()

    
    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)



class Turnovers(QDialog):
    def __init__(self, first_screen):
        super(Turnovers, self).__init__()
        uic.loadUi("turnovers.ui", self)
        self.return_turnovers.clicked.connect(self.goto_homepage)
        self.first_screen = first_screen
        data = self.first_screen.data
        with open(f"G:\Smartech PRJ_1\\turnovers\{data}.csv", "r") as f:
            lines = list(csv.reader(f))
            first = lines[-1][0]
            second = lines[-2][0]
            third = lines[-3][0]
            first_log = lines[-1][1]
            second_log = lines[-2][1]
            third_log = lines[-3][1]

        self.label_first.setText(first)
        self.label_second.setText(second)
        self.label_third.setText(third)
        if first_log == "enteghal":
            self.first_log.setText("انتقال وجه")
        elif first_log == "varizi":
            self.first_log.setText("وجه واریزی")
        elif first_log == "bardasht":
            self.first_log.setText("برداشت وجه")
        elif first_log == "vam":
            self.first_log.setText("وام دریافتی")
        
        if second_log == "enteghal":
            self.second_log.setText("انتقال وجه")
        elif second_log == "varizi":
            self.second_log.setText("وجه واریزی")
        elif second_log == "bardasht":
            self.second_log.setText("برداشت وجه")
        elif second_log == "vam":
            self.second_log.setText("وام دریافتی")
        

        if third_log == "enteghal":
            self.third_log.setText("انتقال وجه")
        elif third_log == "varizi":
            self.third_log.setText("وجه واریزی")
        elif third_log == "bardasht":
            self.third_log.setText("برداشت وجه")
        elif third_log == "vam":
            self.third_log.setText("وام دریافتی")

    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)



class Manager(QDialog):
    def __init__(self, first_screen):
        super(Manager, self).__init__()
        uic.loadUi("Manager.ui", self)
        self.first_screen = first_screen
        self.return_manager.clicked.connect(self.goto_homepage)####
        self.df = pd.read_csv("loan.csv")
        number_of_rows = self.df.shape[0]
        print(number_of_rows)
        self.name1 = "-"
        self.lastname1 = "-"
        self.acc_number1 = "-"
        self.amount1 = "-"
        self.name2 = "-"
        self.lastname2 = "-"
        self.acc_number2 = "-"
        self.amount2 = "-"
        self.name3 = "-"
        self.lastname3 = "-"
        self.acc_number3 = "-"
        self.amount3 = "-"

        if number_of_rows == 1:
            self.name1 = self.df["firstname"][0]
            self.lastname1 = self.df["lastname"][0]
            self.acc_number1 = self.df["account_number"][0]
            self.amount1 = self.df["wanted_amount"][0]
            if self.df["eligible"][0] == True:
                self.log1.setText("این کاربر واجد شرایط است")
            else:
                self.log1.setText("این کاربر واجد شرایط نیست")

            self.ok2.setVisible(False)
            self.nokay2.setVisible(False)
            self.ok3.setVisible(False)
            self.nokay3.setVisible(False)
            self.log2.setVisible(False)
            self.log3.setVisible(False)
        elif number_of_rows == 2:
            self.name1 = self.df["firstname"][0]
            self.lastname1 = self.df["lastname"][0]
            self.acc_number1 = self.df["account_number"][0]
            self.amount1 = self.df["wanted_amount"][0]
            self.name2 = self.df["firstname"][1]
            self.lastname2 = self.df["lastname"][1]
            self.acc_number2 = self.df["account_number"][1]
            self.amount2 = self.df["wanted_amount"][1]
            if self.df["eligible"][0] == True:
                self.log1.setText("این کاربر واجد شرایط است")
            else:
                self.log1.setText("این کاربر واجد شرایط نیست")
            
            if self.df["eligible"][1] == True:
                self.log2.setText("این کاربر واجد شرایط است")
            else:
                self.log2.setText("این کاربر واجد شرایط نیست")

            self.ok3.setVisible(False)
            self.nokay3.setVisible(False)
            self.log3.setVisible(False)

        elif number_of_rows == 3:
            self.name1 = self.df["firstname"][0]
            self.lastname1 = self.df["lastname"][0]
            self.acc_number1 = self.df["account_number"][0]
            self.amount1 = self.df["wanted_amount"][0]
            self.name2 = self.df["firstname"][1]
            self.lastname2 = self.df["lastname"][1]
            self.acc_number2 = self.df["account_number"][1]
            self.amount2 = self.df["wanted_amount"][1]
            self.name3 = self.df["firstname"][2]
            self.lastname3 = self.df["lastname"][2]
            self.acc_number3 = self.df["account_number"][2]
            self.amount3 = self.df["wanted_amount"][2]
            if self.df["eligible"][0] == True:
                self.log1.setText("این کاربر واجد شرایط است")
            else:
                self.log1.setText("این کاربر واجد شرایط نیست")
            
            if self.df["eligible"][1] == True:
                self.log2.setText("این کاربر واجد شرایط است")
            else:
                self.log2.setText("این کاربر واجد شرایط نیست")

            if self.df["eligible"][2] == True:
                self.log3.setText("این کاربر واجد شرایط است")
            else:
                self.log3.setText("این کاربر واجد شرایط نیست")

        elif number_of_rows == 0:
            self.ok1.setVisible(False)
            self.nokay1.setVisible(False)
            self.log1.setVisible(False)
            self.ok2.setVisible(False)
            self.nokay2.setVisible(False)
            self.log2.setVisible(False)
            self.ok3.setVisible(False)
            self.nokay3.setVisible(False)
            self.log3.setVisible(False)

        
        self.fullname1.setText(f"{self.name1} {self.lastname1}")
        self.acc_number11.setText(f"{self.acc_number1}")
        self.amount11.setText(f"{self.amount1}")
        
        self.fullname2.setText(f"{self.name2} {self.lastname2}")
        self.acc_number22.setText(f"{self.acc_number2}")
        self.amount22.setText(f"{self.amount2}")  

        self.fullname3.setText(f"{self.name3} {self.lastname3}")
        self.acc_number33.setText(f"{self.acc_number3}")
        self.amount33.setText(f"{self.amount3}") 

        self.ok1.clicked.connect(self.goto_pay1)
        self.nokay1.clicked.connect(self.goto_reject1)
        self.ok2.clicked.connect(self.goto_pay2)
        self.nokay2.clicked.connect(self.goto_reject2)
        self.ok3.clicked.connect(self.goto_pay3)
        self.nokay3.clicked.connect(self.goto_reject3)

    def goto_pay1(self):
        counter = 0
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            print(type(np.int64(self.acc_number1).item()))
            for line in lines:
                if line[5] == str(np.int64(self.acc_number1).item()):
                    break                
                counter += 1
        
        with open("main.csv", "r") as f:
            lines = list(csv.reader(f))
        print(lines[counter][4])
        lines[counter][4] = int(lines[counter][4]) + np.int64(self.amount1).item() 

        writer = csv.writer(open("main.csv", 'w', newline = ""))
        writer.writerows(lines)
        #begin log for turnovers
        with open(f"G:\Smartech PRJ_1\\turnovers\{np.int64(self.acc_number1).item()}.csv", "a", newline = "") as f:
            writer = csv.writer(f)
            writer.writerow([f"+{self.amount1}", "vam"])
        #end log for turnovers
        self.goto_reject1()

    def goto_pay2(self):
        counter = 0
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            print(type(np.int64(self.acc_number2).item()))
            for line in lines:
                if line[5] == str(np.int64(self.acc_number2).item()):
                    break                
                counter += 1
        
        with open("main.csv", "r") as f:
            lines = list(csv.reader(f))

        print(lines[counter][4])
        lines[counter][4] = int(lines[counter][4]) + np.int64(self.amount2).item() 
        writer = csv.writer(open("main.csv", 'w', newline = ""))
        writer.writerows(lines)
        #begin log for turnovers
        with open(f"G:\Smartech PRJ_1\\turnovers\{np.int64(self.acc_number2).item()}.csv", "a", newline = "") as f:
            writer = csv.writer(f)
            writer.writerow([f"+{self.amount2}", "vam"])
        #end log for turnovers
        
        self.goto_reject2()

    def goto_pay3(self):
        counter = 0
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            print(type(np.int64(self.acc_number3).item()))
            for line in lines:
                if line[5] == str(np.int64(self.acc_number3).item()):
                    break                
                counter += 1
        
        with open("main.csv", "r") as f:
            lines = list(csv.reader(f))

        print(lines[counter][4])
        lines[counter][4] = int(lines[counter][4]) + np.int64(self.amount3).item() 
        writer = csv.writer(open("main.csv", 'w', newline = ""))
        writer.writerows(lines)
        #begin log for turnovers
        with open(f"G:\Smartech PRJ_1\\turnovers\{np.int64(self.acc_number3).item()}.csv", "a", newline = "") as f:
            writer = csv.writer(f)
            writer.writerow([f"+{self.amount3}", "vam"])
        #end log for turnovers
        
        self.goto_reject3()


    def goto_reject1(self):
        with open("loan.csv", "r") as f:
            lines = list(csv.reader(f))
        
        del lines[1]

        writer = csv.writer(open("loan.csv", "w", newline = ""))
        writer.writerows(lines)
        self.ok1.setVisible(False)
        self.nokay1.setVisible(False)
        self.log1.setVisible(False)
        self.blank1.setText("انجام شد")

    def goto_reject2(self):
        counter = 0
        with open("loan.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[5] == str(np.int64(self.acc_number2).item()):
                    break                
                counter += 1

        with open("loan.csv", "r") as f:
            lines = list(csv.reader(f))
        
        del lines[counter]

        writer = csv.writer(open("loan.csv", "w", newline = ""))
        writer.writerows(lines)
        
        self.ok2.setVisible(False)
        self.nokay2.setVisible(False)
        self.log2.setVisible(False)
        self.blank2.setText("انجام شد")

    def goto_reject3(self):
        counter = 0
        with open("loan.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[5] == str(np.int64(self.acc_number3).item()):
                    break              
                counter += 1

        with open("loan.csv", "r") as f:
            lines = list(csv.reader(f))
        
        del lines[counter]

        writer = csv.writer(open("loan.csv", "w", newline = ""))
        writer.writerows(lines)
        
        self.ok3.setVisible(False)
        self.nokay3.setVisible(False)
        self.log3.setVisible(False)
        self.blank3.setText("انجام شد")

    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        

class Loan(QDialog):
    def __init__(self, features, first_screen):
        super(Loan, self).__init__()
        uic.loadUi("Loan.ui", self)
        self.features = features
        self.first_screen = first_screen
        self.return_loan.clicked.connect(self.goto_features)
        self.confirm_loan_push.clicked.connect(self.confirm_loan)

    def goto_features(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def confirm_loan(self):
        self.name = self.name_loan.text()
        self.lastname = self.lname_loan.text()
        self.national_number = self.acc_number_loan.text()
        self.wanted_amout = self.amount_loan.text()
        
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            
            self.balance = "" #understanding
            
            for line in lines:
                if line[2] == str(self.national_number):
                    self.balance = int(line[4])
                    self.account_number = int(line[5])
                    break
        
        with open("main.csv", "r") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[5] == self.first_screen.data:
                    name_should  = line[0]
                    lname_should = line[1]
                    national_code_should = int(line[2])
                    break 

            if self.balance == "":
                self.blank_label_loan.setText("چنین فردی در بانک حساب ندارد")
                return
            
            if ((self.name != name_should) or (self.lastname != lname_should) or (int(self.national_number) != national_code_should)):
                self.blank_label_loan.setText("دسترسی به این حساب را ندارید")
                return


            if self.balance >= (int(self.wanted_amout) * (30 / 100)):
                self.eligible = True
            else:
                self.eligible = False

        with open("loan.csv", "r") as f:
            lines = csv.reader(f)
            counter = 0
            for line in lines:
                counter += 1
            
        if counter >= 4:
            self.blank_label_loan.setText("در حال حاضر امکان دریافت وام وجود ندارد")
        else:
            with open("loan.csv", "r") as f:
                lines = csv.reader(f)
                for line in lines:
                    if line[2] == self.national_number:
                        self.blank_label_loan.setText("شما یک درخواست بررسی نشده دارید")
                        return
            with open("loan.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([self.name, self.lastname, self.national_number, self.balance,self.wanted_amout ,self.account_number, self.eligible])####
                loan_final = LoanFinal(self, self.first_screen)
                widget.addWidget(loan_final)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                widget.removeWidget(self)

class LoanFinal(QDialog):
    def __init__(self, transform, fisrt_screen):
        super(LoanFinal, self).__init__()
        uic.loadUi("Loan_Final.ui", self)
        self.return_features_loan.clicked.connect(self.goto_homepage)
        self.transform = transform
        self.first_screen = fisrt_screen

    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)


class LoginManager(QDialog):
    def __init__(self, first_screen):
        super(LoginManager, self).__init__()
        uic.loadUi("Login_Manager.ui", self)
        self.return_manage11.clicked.connect(self.goto_homepage)
        self.confirm_manage.clicked.connect(self.goto_manage)
        self.onlyInt = QIntValidator()
        self.user_id_manager.setValidator(self.onlyInt)
        self.first_screen = first_screen

    def goto_homepage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        self.first_screen.blank_label.setText("")

    def goto_manage(self):
        self.user_id = self.user_id_manager.text()
        self.password = self.password_manager.text()

        if self.user_id == "5224647":
            if self.password == "Modir01":
                manager = Manager(self.first_screen)
                widget.addWidget(manager)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                widget.removeWidget(self)
            else:
                self.label_2.setText("خطا: رمز عبور اشتباه است")
        else:
            self.label_2.setText("خطا: شماره پرسنلی اشتباه است")


# main
app = QApplication(sys.argv)
firstWindow = FirstScreen()
widget = QStackedWidget()
widget.addWidget(firstWindow)
widget.setFixedSize(1200, 800)
widget.setWindowTitle("Cyber-Bank")
widget.setWindowIcon(QIcon("66455.png"))
widget.show()
sys.exit(app.exec())