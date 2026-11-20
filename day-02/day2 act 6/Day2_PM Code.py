import random


def generate_minutes():
  """Generate and return a random integer between 30 and 180, inclusive."""
  return random.randint(30, 180)


def calc_amount(machine_type, minutes):
  """Calculate the rental amount before VAT based on machine type and minutes used."""
  machine_type = machine_type.upper()

  if machine_type == "A":
    initial_cost = 50.00
    hourly_rate = 30.00
  elif machine_type == "B":
    initial_cost = 62.50
    hourly_rate = 36.25
  elif machine_type == "C":
    initial_cost = 74.87
    hourly_rate = 40.50
  else:
    initial_cost = 0.00
    hourly_rate = 0.00

  hours_used = minutes / 60
  amount_before_vat = initial_cost + (hourly_rate * hours_used)
  return amount_before_vat


def calc_total_amount(amount):
  """Calculate 14% VAT and the total amount payable."""
  vat_rate = 0.14
  vat_amount = amount * vat_rate
  total_payable = amount + vat_amount
  return vat_amount, total_payable


def display_summary(payments):
  """Calculate and display the daily summary statistics from the payments list."""
  num_customers = len(payments)
  combined_amount = sum(payments)
  average_payment = combined_amount / num_customers
  highest_payment = max(payments)
  lowest_payment = min(payments)

  print("\n========================================")
  print("         WISHYWASHY DAILY SUMMARY       ")
  print("========================================")
  print(f"Customers processed : {num_customers}")
  print(f"Combined payable    : R{combined_amount:.2f}")
  print(f"Average payment     : R{average_payment:.2f}")
  print(f"Highest payment     : R{highest_payment:.2f}")
  print(f"Lowest payment      : R{lowest_payment:.2f}")
  print("========================================")


def process_payments():
  """Main workflow to process customer rentals and print invoices."""
  num_customers = int(input("Enter the number of customers to process: "))
  payments = []

  for i in range(num_customers):
    print(f"\n--- Customer {i + 1} ---")
    customer_name = input("Enter customer's name: ")
    machine_type = input("Enter machine type (A, B, or C): ").strip().upper()

    minutes = generate_minutes()
    amount_before_vat = calc_amount(machine_type, minutes)
    vat_amount, total_payable = calc_total_amount(amount_before_vat)

    payments.append(total_payable)

    print("\n--- CUSTOMER INVOICE ---")
    print(f"Customer Name     : {customer_name}")
    print(f"Machine Type      : {machine_type}")
    print(f"Usage Time        : {minutes} minutes")
    print(f"Amount before VAT : R{amount_before_vat:.2f}")
    print(f"VAT (14%)         : R{vat_amount:.2f}")
    print(f"Total Payable     : R{total_payable:.2f}")
    print("------------------------")

  display_summary(payments)


# Start the program
process_payments()
