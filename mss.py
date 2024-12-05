import csv  # To allow us to manage and handle CSVs.
from prompt_toolkit import prompt  # To allow us to shield passwords from viewing whilst the program runs.
import os  # To provide a method of clearing the display within the console application, improving quality of life.
import time  # To delay menu returns after an erroneous input, so the user can read what the message says.
import datetime  # Used for date and time functionality.
from tabulate import tabulate  # A table data organiser.
import pandas as pd  # An alternative method for CSV handling. Appears briefly as a showcase of use.
import random  # This is used exclusively for the random password generator.
import string  # This is used exclusively for the random password generator.

userFile = open('User.csv', 'r')
userFileReader = list(csv.reader(userFile))  # Generating the list of users to be modified and read.
userModuleFile = open('UserModule.csv', 'r')
userMFReader = list(csv.reader(userModuleFile))  # Generating the list of modules to be modified and read.
moduleFile = open('Module.csv', 'r')
moduleFileReader = list(csv.reader(moduleFile))  # Generating the list of users with modules to be modified and read.
today = datetime.date.today()  # Creates a variable aware of today's date.
dateToday = today.strftime("%d-%m-%Y")  # Formats it to look nicer to the eye.
CONST_TITLESTRING = ("-------------------------------------------------------------------------\n" +
                     "Sheffield Hallam University – Module and Student System | " + str(dateToday) + "\n" +
                     "-------------------------------------------------------------------------\n")
# We will be calling this above string a lot through the system. Best to make it a variable for easy implementation.
username = ""
password = ""
userFirstName = ""
userSurname = ""
userType = ""
loginStatus = ""
loggedIn = False
userExitApplication = bool
i = 0
# These variables will be used within our function below: therefore, to avoid "This variable can be empty" errors,
# the variables are empty declared before operations begin.


def login_menu():  # Originally was its own block of code, but felt it would be more user-friendly to make a function.
    # Means that we can return to the menu after the program is exited.
    global username, password, loggedIn, userFirstName, userSurname, userType, i, userExitApplication
    #  Making all the variables we will need openly accessible. Felt easier than using return.
    loggedIn = False
    loginAttempts = 3  # Must be reset for when the user returns to this menu.
    while not loggedIn:
        os.system('cls')  # Clear screen
        print(CONST_TITLESTRING)
        username = input("Please enter a valid username: ")
        password = prompt("Please enter the associating password: ", is_password=True)  # Hides password input
        for i in range(len(userFileReader)):
            if username == "UserName":
                loginAttempts -= 1
                print("This is an invalid username. Please try again. You have " + str(loginAttempts) + " remaining.")
                time.sleep(1.5)
                break
            if (username == userFileReader[i][0] and password == userFileReader[i][1] and
                    userFileReader[i][5] != "Blocked"):  # Checks if user and password fit, and that account is active
                print("Successfully logged in.\n")
                loggedIn = True  # When loggedIn becomes true, the original while loop can successfully break.
                userExitApplication = False  # User now enables while loop for next section of main code.
                userFirstName = userFileReader[i][2]  # This section below gathers user data to be displayed in-console.
                userSurname = userFileReader[i][3]
                userType = userFileReader[i][4]
                break  # Exits the function to move on.
            elif (username == userFileReader[i][0] and password == userFileReader[i][1]
                  and userFileReader[i][5] == "Blocked"):
                input("\nThe account you are trying to log into has been blocked from accessing the Module and Student "
                      "System. Please contact a Hallam administrator to have this corrected.\nPlease press enter to "
                      "return to login menu.\n")  # If account is blocked, don't allow access.
            if (i + 2) > len(userFileReader):  # 'i' has to have 2 added to it to make it reach over the list length.
                loginAttempts -= 1
                print("\nFailure to login, username or password incorrect. Please try again. You have " + str(
                    loginAttempts) + " attempt(s) remaining.\n")  # Displays the attempt number and warns the user.
                time.sleep(1.5)
                for v in range(len(userFileReader)):  # Does an additional cycle through the file to compare inputs
                    if loginAttempts == 0:
                        if username == userFileReader[v][0]:  # If the username inputted exists in the database...
                            print("Maximum login attempts exceeded. The username associated with your last attempt has "
                                  "been blocked within the system. Please contact a Hallam administrator to resolve "
                                  "this.")
                            userFileReader[v][5] = "Blocked"  # Blocks the user account to prevent future entry.
                            userfile_writeover('User.csv', userFileReader)
                            #  Here I need to refresh the entire system entry with the new update. Come back to this.
                            exit()
                        elif not username == userFileReader[i][0] and ((v + 2) > len(userFileReader)):
                            print("Maximum login attempts exceeded. Your last inputted username does not exist, so no "
                                  "action has been taken. Please restart the program and try again.")
                            exit()  # This section is here in case the user has simply made a spelling mistake and not
                            # entered the right username. The app simply ends.


def module_list():  # While the function is only used once, having operations separate makes code more readable.
    moduleTable = tabulate(moduleFileReader)  # Tabulate was used to make things look nice.
    print(moduleTable)


def password_change():  # As with this function, it is used to improve readability.
    passInput = prompt("Please enter the password currently in use, or input 'cancel' to return to menu: ",
                       is_password=True)
    if passInput == password:
        newPassword = prompt("Please enter the new password to replace the pre-existing password: ",
                             is_password=True)
        if newPassword.lower() == "cancel":  # A user may set their password to a keyword, which would cause errors
            print("You cannot make your password a key word. Please return and try again.\n" +
                  "Program will return to menu in two seconds.")  # This prevents that
            time.sleep(1.5)  # Adds the two-second timer
        else:
            newPasswordConfirmation = prompt("Please re-enter the new password: ", is_password=True)
            if newPassword == newPasswordConfirmation:
                userFileReader[i][1] = newPassword
                input("The new password has been set, and changes have been saved. Press enter to return to menu.\n")
                userfile_writeover("User.csv", userFileReader)
            else:
                print("The new passwords are not matching. Please return and enter the matching passwords.\n" +
                      "Program will return to menu in two seconds.")
                time.sleep(1.5)
    elif passInput.lower() == "cancel":
        menu_return()
    else:
        print("Invalid password entered. Please input the correct matching password. Returning to menu..\n")
        time.sleep(1.5)


def userfile_writeover(editedfile, filereadertype):
    # Will be used after information change or account login blocks. Adjusts based on which file needs to be written to.
    with open(editedfile, 'w', newline='') as fileShift:
        writer = csv.writer(fileShift)
        writer.writerows(filereadertype)  # Simply rewrites the entire file. Easiest method, and callable throughout.
# This was done as a function and not once at the end, simply because I am afraid of the user force-closing the app with
# no second thought. If they do, changes will not be saved. This guarantees changes are made, even if it's slower.


def module_creation():
    userInput = input("Please enter the new module's numerical ID, or type cancel to exit. It cannot be an "
                      "existing ID.\n")
    if userInput.lower() == "cancel":
        menu_return()
    for j in range(len(moduleFileReader)):
        if not userInput.isnumeric():  # Module ID HAS to be numerical.
            print("The module ID has to be in a numerical form. Please try again, with only numbers.\n" +
                  "Program will return to menu in two seconds.")
            time.sleep(1.5)
    for v in range(len(moduleFileReader)):
        if userInput == moduleFileReader[v][0]:  # ID can't already exist.
            print("You cannot make an ID that already exists. Please return and try again.\n" +
                  "Program will return to menu in two seconds.")
            time.sleep(1.5)
        elif (v + 1) == len(moduleFileReader):  # Once it's checked all values, continue.
            newModuleID = userInput
            userInput = input("Please input the new module's full name, or type cancel to exit."
                              " It cannot be an existing module name.\n")
            if userInput.lower() == "cancel":  # Still gives the chance to cancel.
                menu_return()
                break
            for o in range(len(moduleFileReader)):
                if userInput == moduleFileReader[o][1]:
                    print("You cannot set your new module's name to an existing one. "
                          "Please return and try again.\n" +
                          "Program will return to menu in two seconds.")
                    time.sleep(1.5)
                elif (o + 1) == len(moduleFileReader):
                    newModuleContainer = [newModuleID, userInput]
                    moduleFileReader.append(newModuleContainer)
                    input("You have successfully created Module ID " + newModuleID + ", " + userInput +
                          ". Changes have been saved to the module list. Please press enter to return to menu.")
                    userfile_writeover('Module.csv', moduleFileReader)


def module_register():
    userInput = input("Please enter the ID of the module you wish to register for, or input 'cancel' to return: ")
    if userInput.lower() == "cancel":  # Lets the user cancel, as always.
        menu_return()
        return
    dataModule = pd.read_csv('Module.csv')  # Pandas reads the Module file.
    confirmValue = dataModule.loc[dataModule['ModuleID'] == int(userInput)]   # Pandas tries to confirm the existence of
    if not confirmValue.empty:                                                # the user input in the module file.
        for x in range(len(userMFReader)):
            if userMFReader[x][0] == username and userMFReader[x][1] == userInput:
                print("You are already registered for this module. Please return and try again.")
                menu_return()
                return
        newStudentAddition = [username, userInput]
        userMFReader.append(newStudentAddition)
        input("You have successfully been added to the module. Changes have been saved. Please press enter to return "
              "to menu.\n")
        userfile_writeover('UserModule.csv', userMFReader)
    else:
        input("The module ID you have inputted does not exist. Please return and try again.")
        time.sleep(1.5)


def module_withdrawal():
    removingModule = input("Please enter the ID of the module you would like to withdraw from: ")
    for mod in range(len(userMFReader)):  # For every value in the UserModule file...
        if username == userMFReader[mod][0] and removingModule == userMFReader[mod][1]:
            userConfirm = input("\nAre you sure you would like to withdraw from this module? Doing so without proper"
                                "permission can cause issues for yourself and your lecturers.\nType 'cancel' if you "
                                "wish to change your mind (if not, press enter): ")
            if userConfirm.lower() != "cancel":
                del userMFReader[mod]
                input("You have successfully withdrawn from the module. Your changes will be saved. Please press "
                      "enter to return to menu.")
                userfile_writeover('UserModule.csv', userMFReader)
                break  # Breaks out of the loop. If this isn't done, it will output the error line.
            else:
                menu_return()
                break
        elif (len(userMFReader)) < (mod + 2):  # The user will be returned to menu to allow them to check their info.
            input("The module you have input either does not exist, or you are not registered to it. "
                  "Please double check your registered modules, and try again.\n")


def user_module_view():
    userMList = []
    moduleNameList = []
    for tot in range(len(userMFReader)):  # For every value in the UserModule.csv file...
        if username == userMFReader[tot][0]:  # If the username is equal to the username value in UserModule...
            userMList.append(userMFReader[tot][1])  # Add the corresponding module ID to a list.
    for k in range(len(moduleFileReader)):  # For every value in Module.csv...
        for m in range(len(userMList)):  # For every value collected in the userMList...
            if userMList[m] == moduleFileReader[k][0]:  # If the collected ID matches an existing module...
                moduleNameList.append([userMList[m], moduleFileReader[k][1]])  # Add the module details to second list.
    print("Your registered modules are as thus:")
    for k in range(len(moduleNameList)):  # For every value in the module list gathered...
        print("Module " + moduleNameList[k][0] + ", " + moduleNameList[k][1])  # Outputs the first and second list.
    input("------------------------------------\n" +
          "Please press enter to return to menu.\n")


def student_record_update():
    studentUNSelection = input("Please enter the username of the student who's records you want to alter, or "
                               "enter 'cancel' to exit: ")
    if studentUNSelection.lower() == "cancel":
        menu_return()
        return
    userData = pd.read_csv('User.csv')
    confirmValue = userData.loc[userData['UserName'] == studentUNSelection]
    for x in range(len(userFileReader)):
        if studentUNSelection == userFileReader[x][0] and userFileReader[x][4] == "Lecturer":
            print("You cannot edit the information of another lecturer. Please return and try again.")
            menu_return()
            return
    if not confirmValue.empty:
        newUsername = input("Student identified.\nPlease enter the new username for the student "
                            "(data may be re-inputted): ")
        newPassword = input("Would you like to reset the student's password to a default value? Yes or No: ")
        newFirstname = input("Please enter the student's new first name (original data may be re-inputted): ")
        newSurname = input("Please enter the student's new surname (original data may be re-inputted): ")
        if not newUsername.isalpha() or not newFirstname.isalpha() or not newSurname.isalpha():
            print("The username, first name and surname can only contain letters. Please return and try again with"
                  " accepted values.")
            menu_return()
            return
        if newUsername.lower() == "cancel" or newFirstname.lower() == "cancel" or newSurname.lower() == "cancel":
            print("No changes have been saved.")
            menu_return()
            return
        for x in range(len(userFileReader)):
            if studentUNSelection == userFileReader[x][0]:
                userFileReader[x][0] = newUsername
                userFileReader[x][2] = newFirstname
                userFileReader[x][3] = newSurname
                if newPassword.lower() == "yes":
                    #  Potential random password generator.
                    new_password_gen(x)
                userfile_writeover('User.csv', userFileReader)
                input("Student information has successfully been updated, and changes have been saved. The new password"
                      " is: '" + userFileReader[x][1] + "'. Ensure that you deliver this information to the student."
                      " Please press enter to return to menu.")
                break
    else:
        print("The student username you have entered does not exist. Please return and try again.")
        menu_return()
        return


def new_password_gen(studentPosi):
    algoPass = ""
    characterList = string.ascii_lowercase + string.digits + "!?@#"
    for b in range(7):
        algoPass = algoPass + random.choice(characterList)
    userFileReader[studentPosi][1] = algoPass


def menu_return():
    print("Returning to menu...\n")
    time.sleep(1.5)


login_menu()  # Carries out the login menu function. Below section only initiates when a boolean is disabled.
while not userExitApplication:
    os.system('cls')  # This command is frequently used to clear the user interface. Permission of use given by lecturer
    print(CONST_TITLESTRING +
          "Welcome, " + userFirstName + " " + userSurname + ".\n" +
          "User Type: " + userType + "\n" +
          "------------------------------------")
    print("Please select an option by inputting the relevant number (and only the number) to the section:\n" +
          "1. View User Profile\n" +
          "2. View All Modules\n" +
          "3. Change Password")  # These sections are universal for lecturer and student.
    if userType == "Student":  # If the user is a student, these sections are added.
        print("4. View My Personal Modules\n" +
              "5. Register A Module\n" +
              "6. Withdraw From A Module\n" +
              "7. Exit Application")
    elif userType == "Lecturer":  # If the user is a lecturer, these sections are added.
        print("4. Create A Module\n" +
              "5. Update Student Records\n" +
              "6. Exit Application")
    menuSelection = input("------------------------------------\n")
    if menuSelection == "1" or menuSelection.lower() == "one":
        os.system('cls')
        input(CONST_TITLESTRING +
              "View User Profile\n" +
              "------------------------------------\n" +
              "Username - " + username + "\n" +
              "First Name - " + userFirstName + "\n" +
              "Surname - " + userSurname + "\n" +
              "User Type - " + userType + "\n" +
              "Any incorrect information should be reported to Hallam administration for assistance and correction.\n" +
              "------------------------------------\n" +
              "Please press enter to return to menu.\n")
    elif menuSelection == "2" or menuSelection.lower() == "two":
        os.system('cls')
        print(CONST_TITLESTRING +
              "View All Existing Modules\n" +
              "------------------------------------\n" +
              "All existing modules with their corresponding IDs:")
        module_list()
        input("------------------------------------\n" +
              "Please press enter to return to menu.\n")
    elif menuSelection == "3" or menuSelection.lower() == "three":
        os.system('cls')
        print(CONST_TITLESTRING +
              "Change My Password\n" +
              "------------------------------------")
        password_change()  # Refers to function to change password.
    elif (menuSelection == "4" or menuSelection.lower() == "four") and userType == "Student":
        os.system('cls')
        print(CONST_TITLESTRING +
              "View My Personal Modules\n" +
              "------------------------------------")
        user_module_view()  # Refers to function to view their own modules.
    elif (menuSelection == "4" or menuSelection.lower() == "four") and userType == "Lecturer":
        os.system('cls')
        print(CONST_TITLESTRING +
              "Create a Module\n" +
              "------------------------------------")
        module_creation()  # Refers to function to make a module.
    elif (menuSelection == "5" or menuSelection.lower() == "five") and userType == "Student":
        os.system('cls')
        print(CONST_TITLESTRING +
              "Register a Module\n" +
              "------------------------------------\n")  # Add (APPEND)
        module_register()  # Refers to function to join a module.
    elif (menuSelection == "5" or menuSelection.lower() == "five") and userType == "Lecturer":
        os.system('cls')
        print(CONST_TITLESTRING +
              "Update Student Records\n" +
              "------------------------------------")  # Remove and Replace (TUPLE AND SET + APPEND)
        student_record_update()  # Refers to function to update student info.
    elif (menuSelection == "6" or menuSelection.lower() == "six") and userType == "Student":
        os.system('cls')
        print(CONST_TITLESTRING +
              "Withdraw from a Module\n" +
              "------------------------------------\n")  # Remove (REFER TO TUPLE AND SET POWERPOINT)
        module_withdrawal()  # Refers to function to withdraw from a module.
    elif (menuSelection == "6" or menuSelection.lower() == "six" and userType == "Lecturer") or (
            menuSelection == "7" or menuSelection.lower() == "seven" and userType == "Student"):
        os.system('cls')
        print(CONST_TITLESTRING +
              "Exit Application\n" +
              "------------------------------------\n" +
              "Are you sure you would like to exit? If not, please type “Cancel”. Else, press enter to exit.")
        menuSelection = input("------------------------------------\n")
        if menuSelection.lower() == "cancel":  # Only triggers if user input is cancel, in any case format.
            print("Exit Application canceled. You will now be returned to the menu.\n")
        else:
            print("Thank you for using the Module and Student System. We hope your experience was enjoyable.\n" +
                  "You will now be returned to the login menu.\n")
            time.sleep(1.5)
            userExitApplication = True  # Sets the looping value to true, breaking the menu loop
            login_menu()  # Returns to the original login menu function, repeating the cycle.
    else:
        print("Your input was not an available menu option. Please input a correct number.\n")
        time.sleep(1.5)
