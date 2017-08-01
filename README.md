# Example:
Login vietcombank:
user = 'youruser'
password = 'yourpass'
name='yourholdername'
api2captcha=''
x = vbc_task(user,password,name,api2captcha)
if x.main() == True:
    x.check_namein('0401000508157') #check name
