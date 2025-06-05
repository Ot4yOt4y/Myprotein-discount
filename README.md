# Myprotein biggest discount avaliable

Don't want to constantly check when the highest discounts during "Impact Week" will be available? When using Myprotein athletes' promo codes, there is only a short time window in which the code provides the highest discount. Therefore, if you don't constantly check Instagram, you will probably miss out.

This Python script use case is to notify you when Myprotein offers the biggest discounts available.

## How it works

1. Manually sign in with your Myprotein profile and put the products you want to order in the basket. (The products stay in the basket indefinitely)  
2. Input your personal details in userdata.json file  
	a. loginUrl - Here you have to place your sign-in URL (depending on your country)  
  b. myProteinAccountData - Input your username and password used to sign-in your Myprotein account  
	c. smtp - Here you have to input your smtp details with port, server, username and password (You can setup your smtp [here](https://myaccount.google.com/apppasswords))  
 	d. emailRecipient - This is the email address on which you want to be notified with  
	e. promoCode - Use a promo code of Myprotein athlete based in your country. (Look them up on Instagram)  
	f. notifyWhenDiscount - Set this value to the percentage of discount you want to be notified for (Historically the biggest discounts are 55%)  
4. Run with task scheduler, crontab, etc.  
