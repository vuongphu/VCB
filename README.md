### Description:
   Class used login vietcombank , check name in bank with account number , get log send and reveice money , send money to account other.
# Example:
Login vietcombank: 
```
user = 'youruser'
password = 'yourpass' 
name='yourholdername'
api2captcha='' 
x = vbc_task(user,password,name,api2captcha) 
if x.main() == True: <br /> 
    x.check_namein('0401000508127') #get name 
    x.detail_exchange('10/08/2016', '10/08/2016') # get history with param 1 is start day and 2 is start end
    x.send_money('50,000', '0401000508252', 'Python') # send money with param 1 is amount , 2 is account number, 3 is meno
