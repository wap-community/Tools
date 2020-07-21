from CarrierLookup import numberSearch
from EmailScan import haveibeenPwned
from IPTrace import getIP

# pip install pyfiglet
import pyfiglet
banner = pyfiglet.figlet_format("OSINTRecon")
print(banner)

MainFunctions={
    1: numberSearch,
    2: haveibeenPwned,
    3: getIP
}


def Menu():
    Selection = 1
    while True:
        print('Menu:')
        print("1. Carrier Lookup")
        print("2. Email Breach")
        print("3. IP Trace")
        print("4. Exit")
        print('')
        Selection = int(input(">> "))
        print('')
        if Selection == 1:
            MainFunctions[Selection]()
        elif Selection == 2:
            MainFunctions[Selection]()
        elif Selection == 3:
            MainFunctions[Selection]()
        elif Selection == 4:
            exit()
        else:
            print("Please choose an Appropriate option")


if __name__ == "__main__":
    Menu()
