
# Maxwell Fitness Centre
# Program to calculate customer payments

# Function 1: Calculate amount before VAT
def amount_due(facility_code, hours):

    if facility_code == "squa":
        rate = 13.00
    elif facility_code == "swim":
        rate = 12.00
    elif facility_code == "gym":
        rate = 11.00
    elif facility_code == "wei":
        rate = 8.00

    amount = rate * hours

    return amount


# Function 2: Calculate final amount including VAT
def final_amount_due(amount):

    vat = amount * 0.14

    final_amount = amount + vat

    return final_amount


# Function 3: Display customer details and payment
def display(name, final_amount):

    print("\n----- MAXWELL FITNESS CENTRE -----")
    print("Customer name:", name)
    print("Final amount payable: R", format(final_amount, ".2f"), sep="")
    print("----------------------------------")


# Function 4: Process customer payment
def process_payment():

    name = input("Enter customer name: ")

    facility_code = input("Enter facility code (squa/swim/gym/wei): ").lower()

    hours = float(input("Enter number of hours: "))

    amount = amount_due(facility_code, hours)

    final_amount = final_amount_due(amount)

    display(name, final_amount)


# Start the program
process_payment()
