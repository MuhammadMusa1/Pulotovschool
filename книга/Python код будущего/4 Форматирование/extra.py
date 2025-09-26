item = "apples"
price = 1.49
print(f"The price of {item} is ${price:.2f} per pound.")
print("The price of {} is ${:.2f} per pound.".format(item, price))
print("The price of %s is $%.2f per pound." % (item, price))