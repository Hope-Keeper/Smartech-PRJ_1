import random
import csv
#IAOM --> Initial Amount Of Money

class BankAccount:
    def __init__(self, firstName, lastName, nationalCode, iaom):
        self.firstName = firstName
        self.lastName = lastName
        self.nationalCode = nationalCode
        self.iaom = iaom
        self.accountNumber = random.randint(11111111, 99999999)
        self.balance = iaom

        with open("main.csv", "a", newline = "") as f:
            writer = csv.writer(f)
            writer.writerow([self.firstName, self.lastName, self.nationalCode, self.iaom, self.balance,self.accountNumber])


if __name__ == "__main__":
    ins1 = BankAccount("Arash", "Tahamtan", 1742544148, 1000)