mess_account_does_not_exist = u"The Employee Number you entered is incorrect"
username = "username"
password = "password"
email = "email"
remember = "remember"
employee_number = "employee_number"
mess_wrong_password = u"Password you entered is incorrect"
mess_active_user = u"User have not actived yet"

# Method of form
POST = 'POST'
GET = 'GET'

#Label
labChargeType = 'Charge type'
labDebitAccount = "Debit account"
labCreditAccount = "Credit account"
labCurrentBalance = "Current balance"
labCreditAccountName = "Credit account name"

# Some link of website
transfer_external = "/externaltranfer/"
transferIn = "/transferIn/"
error = "Error"
mess = '/mess'
reqconfirmInternalCode = '/confirmInternalCode/'
link = '127.0.0.1:8000/activation/'
reqconfirmInternal = '/confirmInternal/'
index = "/"
home = "/home/"
transferSuccess = '/transferSuccess/'

# Change webservice URL here
webservice_url = 'http://127.0.0.1:8001/'
customer_webservice_url = 'http://127.0.0.1:8001/verify/'
ws_sendOTP = 'http://127.0.0.1:8001/OTP/'
changedPass = "/changedPass/"

# Some page of website
ebankingloginPage = "ebankinglogin.html"
registerPage = "register.html"
openAccount = 'openAccount.html'
openAccSuccessPage = 'openAccSuccess.html'

homePage = "home.html"
logoutPage = "logout.html"
failPage = 'fail.html'
successRegPage = 'registerSuccess.html'

transferSelectPage = "transferSelect.html"
transferPage = "transfer.html"
confirm_ex_r1 = "confirm_external_r1.html"
confirm_ex_r2 = "confirm_external_r2.html"

internalTransferPage = "internalTransfer.html"
internalConfirmPage = "confirmInternal.html"
internalConfirmCodePage = "confirmCode.html"

externalTransferPage = "externalTransfer.html"
successPage = 'success.html'
activeUserPage = "activation_user.html"

viewTransHis = "viewTransaction.html"

ajaxPage = "ajax.html"

changePassPage = "changePass.html"
changedPassPage = "changedPass.html"

# Data transfer between others page
formData = "form"
kind_of_transfer = 'kind_of_transfer'

# Session parameter
usernameParam = "usname"
codeError = 'codeError'
user = 'usersession'
username = "username"
fee = 1000
errorAmountOfMoney = "errorAmountOfMoney"
errorAmountOfMoneyMess = "Amount of money of this account is not enough" 
errorTransfer = "errorTransfer"
errorTransferMess = "Sorry, Our service can not complete your require now"

# Send mail
greeting = 'Dear '
subject = 'Anouncement from e-Banking System'
message = '\n \nThank you for registering e-Banking system.' 
messageLink = '\nPlease click this link to activate:  '
emailSender = 'vietcombank.py@gmail.com'
prefix_usern = 'EBP_'
thank = ' \n \nThanks, \nPython Team.'
viewpage = 'viewInfo.html'
viewBalancePage = 'viewBalance.html'

# Register form
phone = "phone_num"
cardNum = "id_card_num"
mess_error_phone = "Your phone number is not valid"
mess_error_cardN = "Your identity card number is not valid"
fullname = "fullname"
birthday = "birthday"
sex = "sex"
nationality = "nationality"
address = "address"
email = "email"
phoneNum = "phone_num"
city = "city"
id_card_num = "id_card_num"
card_date = "card_date"
card_place = "card_place"
district = "district"
titleDistrict = '--Choose city first--'
titleCity = '-- Choose a city --'

# Form internal
kind_of_transfer = 'kind_of_transfer'
ChargeType = 'ChargeType'
amountInvalid = 'Amount of money is invalid.'
amountLitFee = 'Amount of money to transfer must be more than ' + str(fee)
recieveRequire = 'Receiver account is required!'
recieveAccount_Must_Number = 'Receiver account is number! Please check again!'
sender_reciever_same = 'Sender account and Receiver account is same!'
reciever_not_exist = 'Receiver account maybe not exits! Please check again!'
reciever_not_exist_or_wsfail_to_load = 'Receiver account maybe not exits or Web Service is under maintenance '
not_enough_money = "Current account's amount of money is not enough. (If your change type is 'Include' you must pay fee is " + str(fee) + " VND)"
internal = "in"
external = "ex"
Email = "Email"
beneficiaryNameRequire = 'Beneficiary Name is required!'
beneficiaryBankNameRequire = 'Beneficiary Bank Name is required!' 
beneficiaryBankBranchRequire = 'Beneficiary Bank Name Branch is required!' 

# Confirm internal 
subject = 'Anouncement from Vietcombank'
sendCodeError = "sendCodeError"
sendCodeErrorMess = "Server can not send code confirm to you. Please try again!"


# Confirm internal code
code = 'Code'
amount = "Amount"
chargeType = 'ChargeType'
include = "Include"
exclude = "Exclude"
debitAccount = "DebitAccount"
creditAccount = "CreditAccount"
codeError = 'codeError'
codeErrorMess = "Code is invalid!"

beneficiaryName = "BeneficiaryName"
beneficiaryBankName = "BeneficiaryBankName"
beneficiaryBankBranch = "BeneficiaryBankBranch"

content = "Content"
currentBalance = "CurrentBalance"
creditAccountName = "CreditAccountName"
Email = "Email"

# View transfer's transaction
transfer_type = "trans_type"
sender_acc = "acc_id1"
receive_acc = "acc_id2"
transfer_date = "trans_date"
listTran = 'listTran'
# Open account form
accId = 'accID'
random = 'random'

# Gender
Mr = "Mr. "
Ms = "Ms. "
male = "male"
female = "female"

mess_error_balance = 'Balance is a number'
balance = 'balance'
errorpage = 'error.html'
login = '/login/'


