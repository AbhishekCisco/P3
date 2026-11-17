# this code intially has bugs that are now fixe with inline AI assistance


def greet(name):  # one bug was here ( not closed
	print(f"Hello, {name}")
 
 
def add_numbers(): # one bug was here in 9 and 10 int is not used to convert input to integer
	number1 = int(input("Enter a number: "))
	number2 = int(input("Enter another number: "))
	total = number1 + number2
	print(f"The sum of {number1} and {number2} is {total}")
 
 
def is_eligible_for_discount(age):
	"""Return True if the customer gets the senior discount (age 60 or older)."""
	return age >= 60 #  > was fixed to >= for senior discount eligibility
 
 
if __name__ == "__main__":
	greet("Asha")
	add_numbers()
	print(is_eligible_for_discount(60))
