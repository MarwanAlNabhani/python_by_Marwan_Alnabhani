def convertToInt():
    try:
        userInput = input("Please enter a number: ")

        number = int(userInput)
        print("The conversion is successful.")
        return number
        
    except ValueError:
        print("Invalid Number.")
        return None   


result = convertToInt()  
if result is not None:
    print(f"The converted number is: {result}")  