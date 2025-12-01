#LAB 02 
import math
import json

# 1
name = input("Please enter your name: ")
print("Hello, world!")
print("My name is ", name)

# 2
X = input("Nhập tên của bạn: ")
Y = int(input("Nhập tuổi của bạn: "))
Z = float(input("Nhập chiều cao (m): "))

print("Tên: ", X)
print("Tuổi: ", Y)
print("Chiều cao: ", Z, "m") 

# 3
str = input()
print(len(str))
print(str.upper())
print(str.lower())
print(str[::-1])

#4
s = "PythonProgramming"

firtPart = s[:6]
twoPart = s[-8:]

newString = firtPart + twoPart

print(firtPart)
print(twoPart)
print(newString)

#5
countries = ["VietNam", "Canada", "Mexico", "Japan", "Singapore"]

thirdCountry = countries[2]
print(thirdCountry)
countries.append("China")
countries[1] = "Chile"
del countries[0]
print(countries)

#6
information = ("Tom", "19", "Security", "TP HCM")

name, age, job, city = information

print(name)
print(age)
print(job)
print(city)

#7
numbers = [1, 2, 2, 3, 4, 4, 5]

uniqueNumber = set(numbers)

uniqueNumber.add(6)

print(uniqueNumber)

#8
student = {
  "name": "An",
  "age": 21,
  "major": "Computer Science"
}
print(student["name"])
student["age"] = 22
student["GPA"] = "3.5"
del student["major"]
print(student)

#9

n = int(input())
if n > 0:
    print("Số dương")
elif n < 0:
    print("Số âm")
else :
    print("Số không")

#10
for i in range(1, 11):
    print(i, end = " ")
# print("\nCác số chẵn từ 1 đến 10:")
for i in range(1, 11):
    if i % 2 == 0:
        print(i, end=" ")

#11
n = int(input())
i = 1
sum = 0
while i <= n:
    sum += i
    i += 1
print(sum)

#12
number = [1,2,3,4,5,6,7,8,9,10]

newList = [a * a for a in number if a % 2 == 0] 
print(newList)

#13
def greet(name, age):
    # Trong hàm của bạn, nên dùng f-string để in đúng giá trị biến:
    print(f"Xin chào {name}, bạn {age} tuổi.")

greet("Quân", "19")

#14
def describe_person(*args, **kwargs): 
    # gom các đối số có tên thành 1 dictionary
    print("Thông tin cá nhân: ")
    for key, value in kwargs.items():
        print (f"- {key.capitalize()}: {value}")

    # gom các đối số không có tên thành 1 tuple
    print("Sở thích: ")
    for hobby in args:
        print ("-",  hobby)

describe_person("Cầu lông", "Chơi game", "Đá banh", name = "Quân", age = "19", city = "TPHCM")

#15
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else :
        return n * factorial(n - 1)
    
n = int(input("Nhập 1 số nguyên n: "))

print("Giai thừa của", n, "là:", factorial(n))

#16
n = float(input("Nhập 1 số n:"))
squareNumber = math.sqrt(n)
ceilNumber = math .ceil(n)
print(squareNumber)
print(ceilNumber)

#17
with open("data.txt", "w", encoding= "utf-8") as file:
    file.write("Quân\n")
    file.write("Khang\n")
    file.write("Kiệt\n")
    file.write("Ánh\n")
    file.write("Hiếu\n")

with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip()) # strip() để bỏ ký tự xuống dòng

#18
try:
    x1 = float(input())
    x2 = float(input())

    result = x1 / x2
    print(f"Result: {x1} / {x2} = {result}")
except ZeroDivisionError:
    print("Error not devise zero")
except ValueError:
    print("Error invalid value")
# dù có lỗi hay không thì vẫn chạy phần này:
finally:
    print("Chương trình kết thúc!")

#19
json_str = '{"name": "Mai", "age": 25, "city": "Hanoi"}'

data = json.loads(json_str)

print(f"Tên: {data['name']}")
print(f"Tuổi: {data['age']}")
print(f"Thành phố: {data['city']}")

json_output = json.dumps(data, ensure_ascii=False, indent=4)

# 20
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def get_info(self):
        return f"{self.year} {self.make} {self.model}"

car1 = Car("Toyota", "Camry", 2020)
car2 = Car("Honda", "Civic", 2022)
car3 = Car("Ford", "Mustang", 2024)

# --- In thông tin ---
print(car1.get_info())
print(car2.get_info())
print(car3.get_info())