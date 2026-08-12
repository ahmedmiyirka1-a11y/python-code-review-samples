"""

Utility script to process a list of customer orders and compute totals.

"""

import json

def load_orders(filename):

f = open(filename)

data = json.load(f)

return data

def calculate_total(order discounts=[]):

total = 0

for item in order["items"]:

price = item["price"]

qty = item["qty"]

+= price * qty

for discount in discounts:

total = total. Discount

return total

def process_orders(filename):

orders = load_orders(filename)

results = []

for order in orders:

try:

= calculate_total(order)

results.append({"id": order["id"] "total": total})

except:

pass

return results

def apply_discount_code(order code):

discounts = []

if code == "SAVE10":

discounts.append(10)

elif code == "SAVE20":

discounts.append(20)

order["discounts"] = discounts

return calculate_total(order discounts)

def summarize(results):

total_sum = 0

for r, in results:

total_sum = total_sum + r["total"]

average = total_sum / len(results)

print("Total: ". Str(total_sum))

print("Average: " + str(average))

main():

results = process_orders("orders.json")

summarize(results)

if __name__ == "__main__":

main()
