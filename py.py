"""
##if-else
age=int(input("Enter your age: "))
if(age>=18):
    print("Eligible to vote")
else:
    print("Not Eligible to vote")
   
##ladder if
age=int(input("Enter your age: "))
if(age>0 and age<18):
    print("Child / Teenager")
elif(age>=18 and age<=60):
    print("Adult Citizen")
else:
    print("Senior Citizen")
##nested if
Amount=int(input("Enter the amount"))
if(Amount<=1000):
    if(Amount%100==0):
       print("Amount is withdraw successfull")
    else:
        print("Enter the multiples of 100")
else:
        print("Amout cannot be withdraw")

##for loop
start=int(input("Enter the start number"))
end=int(input("enter the end number"))
for start in range(start,end+1):
    print(start)

    """
##match case
vowels=input("enter a letter: ")
match vowels:
    case 'a':
        print(vowels,"Is vowels")
    case 'e':
        print(vowels,"Is vowels")
    case 'i':
        print(vowels,"Is vowels")
    case 'o':
        print(vowels,"Is vowels")
    case 'u':
        print(vowels,"Is vowels")
    case _:
        print("invalid input")

        
month=int(input("Enter the number to get marathi month"))
match month:
    case 1:
        print("Chairta")
    case 2:
        print("Vaishakh")
    case 3:
        print("Jyeshtha")
    case 4:
        print("Ashadha")
    case 5:
        print("Shravan")
    case 6:
        print("Bhadrapad")
    case 7:
        print("Ashwin")
    case 8:
        print("kartik")
    case 9:
        print("Margashirsha")
    case 10:
        print("Pausha")
    case 11:
        print("Magha")
    case 12:
        print("Phalguna")
    case _:
        print("Invalid input")
