# Myprotein biggest discount avaliable

Don't want to constantly check when the highest discounts during "Impact Week" will be available? When using Myprotein athletes' promo codes, there is only a short time window in which the code provides the highest discount. Therefore, if you don't constantly check Instagram, you will probably miss out.

This Python script notifies you when Myprotein offers the biggest discount.

## How it works

1. Input your personal details in `userdata.json` file  
    a. `productUrl` – Here you have to place the URL of the product you are interested in  
    b. `smtp` – Input your SMTP details with port, server, username and password ([set up your SMTP here](https://myaccount.google.com/apppasswords))  
    c. `emailRecipient` – This is the email address on which you want to be notified  
    d. `promoCode` – Use a promo code of a Myprotein athlete based in your country (look them up on Instagram)  
    e. `notifyWhenDiscount` – Set this to the discount percentage you want to be notified for (historically biggest discounts are over 50%)

2. Run with Task Scheduler, crontab, etc.

