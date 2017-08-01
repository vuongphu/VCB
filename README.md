# Example:
Login vietcombank: <br />
user = 'youruser' <br />
password = 'yourpass' <br />
name='yourholdername' <br /> 
api2captcha='' <br />
x = vbc_task(user,password,name,api2captcha) <br />
if x.main() == True: <br /> 
    x.check_namein('0401000508157') #check name <br />
