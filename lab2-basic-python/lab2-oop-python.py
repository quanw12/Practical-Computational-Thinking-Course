from math import pi
from abc import ABC, abstractmethod
from datetime import datetime
import json

# 1
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    def get_info(self):
        return f"{self.make} {self.model} {self.year}"

car = Car("V", "Honda", 1999)
print(car.get_info())

# 2
class BankAccount:
    def __init__(self, account_number, owner, balance = 0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ Đã nạp {amount} vào tài khoản.")
        else:
            print("❌ Số tiền nạp phải lớn hơn 0!")
    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Số tiền rút phải lớn hơn 0!")
        elif amount > self.balance:
            print("❌ Số dư không đủ để rút!")
        else:
            self.balance -= amount
            print(f"💸 Đã rút {amount} từ tài khoản.")
    def get_balance(self):
        print (f"Số dư hiện tại: {self.balance}")

user = BankAccount(234,"QUan")
user.deposit(50000)
user.withdraw(20000)
user.get_balance()

# 3
class Student:
    def __init__(self,name, _grade = 0):
        self.__grade = _grade
        self.name = name
    def set_grade(self, grade):
        if 0 <= grade <= 100:
            self.__grade = grade
        else :
            raise ValueError(f"Số điểm của học sinh này không hợp lệ")
    def get_grade(self):
        return self.__grade
    def show_info(self):
        print(f"Học sinh: {self.name}, Điểm: {self.__grade}")
try:
    s1 = Student("An")
    s1.set_grade(95)
    s1.show_info()

    s2 = Student("Bình")
    s2.set_grade(105)   # Sẽ gây lỗi
    s2.show_info()

except ValueError as e:
    print(e)

# 4
class Vehicle:
    def __init__(self, max_speed, mileage):
        self.max_speed = max_speed
        self.mileage = mileage
    def show_info(self):
        print(f"Tốc độ tối đa của xe này: {self.max_speed}")
        print(f"Số dặm của chiếc xe này: {self.mileage}")
class Bus(Vehicle):
    def __init__(self, max_speed, mileage, passengers):
        super().__init__(max_speed, mileage)
        self.passengers = passengers
    def show_info(self):
        super().show_info()
        print(f"Số hành khách: {self.passengers}")
# 5
class Robot:
    # Thuộc tính lớp - đếm số robot còn hoạt động
    active_count = 0

    def __init__(self, name):
        self.name = name
        Robot.active_count += 1
    def remove(self):
        if (Robot.active_count > 0):
            Robot.active_count -= 1
        else:
            print(f"Không còn robot nào đang hoạt động!")
    
    @classmethod
    def number_active(cls):
        print(f"Hiện đang có {cls.active_count} robot đang hoạt động")
r1 = Robot("Alpha")
r2 = Robot("Beta")

Robot.number_active()   # Gọi qua lớp

r1.remove()
Robot.number_active()

r2.remove()
Robot.number_active()
# 6
class Shape:
    def area(self):
        # Đây là phương thức "ảo" (abstract) — lớp con sẽ override lại
        raise NotImplementedError("Lớp con phải định nghĩa lại phương thức area()!")
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * (self.radius ** 2)
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
shapes = [
    Circle(3),
    Rectangle(4, 5),
    Circle(2),
    Rectangle(2, 6)
]
total_area = 0
for shape in shapes:
    print(f"Diện tích: {shape.area():.2f}")
    total_area += shape.area()

print(f"\n🧮 Tổng diện tích tất cả các hình: {total_area:.2f}")
# 7
class Person:
    def __init__(self, name, age):
        self.name = name 
        self.age = age
    def __str__(self):
        return f"{self.name} is {self.age} years old."
p1 = Person("An", 21)
p2 = Person("Bình", 25)
p3 = Person("Chi", 19)

print(p1)
print(p2)
print(p3)

# 8
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Chỉ có thể cộng với Vecto khác")
    def __str__(self):
        return f"({self.x},{self.y})"
v1 = Vector2D(2, 3)
v2 = Vector2D(5, 7)
v3 = Vector2D(-1, 4)
sum_vector = v1 + v2
print("\nv1 + v2 =", sum_vector)
total = sum_vector + v3
print("Tổng v1 + v2 + v3 =", total)

# 9
class Salary:
    def __init__(self, pay, bonus):
        self.pay = pay
        self.bonus = bonus
class Employee:
    def __init__(self, name, salary_obj):
        self.name = name
        self.salary_obj = salary_obj
    def total_compensation(self):
        return self.salary_obj.pay + self.salary_obj.bonus
salary1 = Salary(5000, 1000)
emp1 = Employee("Alice", salary1)

salary2 = Salary(7000, 2000)
emp2 = Employee("Bob", salary2)

print(f"{emp1.name} tổng thu nhập: {emp1.total_compensation()} USD/tháng")
print(f"{emp2.name} tổng thu nhập: {emp2.total_compensation()} USD/tháng")

# 10
class Logger:
    def log(self,message):
        print("[LOG]: {self.message}")
class FileWriter:
    def __init__(self, filename):
        self.filename = filename
    def write(self, text):
        with open(self.filename, "a" ,encoding= "utf-8") as f:
            f.write(text +"\n")
class LogFileWriter(Logger, FileWriter):
    def __init__(self, filename):
        FileWriter.__init__(self, filename)
    def log(self, message):
        self.write(f"[Log]: {message}")
logger = LogFileWriter("log.txt")
logger.log("Chương trình bắt đầu chạy.")
logger.log("Ghi dữ liệu thành công.")
logger.log("Chương trình kết thúc.")
# 11
class DatabaseConnection:
    __instance = None
    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("Chỉ được tạo 1 instance duy nhất")
        else:
            DatabaseConnection.__instance = self

    @staticmethod
    def get_instance(self):
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
        return DatabaseConnection.__instance

# 12
class AbstractAnimal(ABC):
    @abstractmethod
    def speak(self):
        pass
class Dog(AbstractAnimal):
    def speak(self):
        return "Gau gau"
dog = Dog()
print(dog.speak())

# 13
class Employee:
    def __init__(self, name, salary):
        self.name = name 
        self.salary = salary
    def show_information(self):
        return f"Tên: {self.name}, Lương: {self.salary} VND"
class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department
    def show_information(self):
        return f"{super().show_information()}, Phòng ban: {self.department}"
class Executive(Manager):
    def __init__(self, name, salary, department, stock_options):
        super().__init__(name, salary, department)
        self.stock_options = stock_options
    def show_information(self):
        return f"{super().show_information()}, Cổ phiếu thưởng: {self.stock_options}"
emp = Employee("An", 15000000)
mgr = Manager("Bình", 25000000, "Phát triển phần mềm")
exe = Executive("Chi", 40000000, "Chiến lược kinh doanh", "500 cổ phiếu")

print(emp.show_information())
print(mgr.show_information())
print(exe.show_information())

# 14
class JsonSerializableMixin:
    def to_json(self):
        # chuyen doi tuong sang dang json
        return json.dumps(self.__dict__, ensure_ascii = False, indent = 2)
class Product(JsonSerializableMixin):
    def __init__(self, name, price):
        self.name = name
        self.price = price
p1 = Product("Laptop", 25000000)
p2 = Product("Chuột không dây", 350000)

print("JSON Product 1:")
print(p1.to_json())

print("\nJSON Product 2:")
print(p2.to_json())

# 15
class Circle:
    def __init__(self, radius):
        self._radius = radius # thuộc tính được đóng gói 
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        if (value < 0):
            raise ValueError("R phải lớn hơn 0")
        self._radius = value
    def area(self):
        return pi * (self._radius ** 2)
    
c = Circle(5)
print("Bán kính:", c.radius)
print("Diện tích:", c.area())

# Thay đổi bán kính hợp lệ
c.radius = 10
print("\nSau khi thay đổi bán kính:")
print("Bán kính:", c.radius)
print("Diện tích:", c.area())

# Thử đặt giá trị không hợp lệ
try:
    c.radius = -3
except ValueError as e:
    print("\n❌ Lỗi:", e)

# 16
class Book:
    def __init__(self, title, author, status = "available"):
        self.title = title
        self.author = author
        self.status = status # available or borrowed
class Library:
    def __init__(self):
        self.books = []
    def add_book(self,book):
        self.books.append(book)
        print("Đã thêm sách")
    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.status == "available":
                    book.status = "borrowed"
                    print("Đã cho mượn")
                    return
                else:
                    print("Hiện tại sách này đã cho mượn")
                    return 
        print("Không tìm thấy sách này")
    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.status == "borrowed":
                    book.status = "available"
                    print("Bạn đã trả sách thành công")
                    return
                else:
                    print("Sách này chưa được mượn")
                    return 
        print("Không tìm thấy sách này")
    def list_available(self):
        for book in self.books:
            if book.status == "available":
                print(f" - {book.title} ({book.author})")
            print()
library = Library()

library.add_book(Book("Harry Potter", "J.K. Rowling"))
library.add_book(Book("Sherlock Holmes", "Arthur Conan Doyle"))
library.add_book(Book("Doraemon", "Fujiko F. Fujio"))

library.list_available()

library.borrow_book("Harry Potter")
library.borrow_book("Harry Potter") 
library.list_available()

library.return_book("Harry Potter")
library.list_available()

# 17
class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
    def __str__(self):
        return f"{self.name} - {self.price}₫ (Còn {self.stock} sản phẩm)"
class Order:
    def __init__(self):
        self.items = [] # ds các product, quantity
        self.discount = 0
    def add_product(self,product, quantity):
        if quantity < 0 :
            print("Số lượng không hợp lệ")
            return 
        if product.stock >= quantity:
            self.items.append((product, quantity))
            product.stock -= quantity
        else:
            print("Không đủ hàng")
    def apply_discount(self,percent):
        if 0 <= percent <= 100:
            self.discount = percent
            print("Đã áp dụng mã giảm giá")
        else:
            print("Phần trăm giảm giá không hợp lệ")
    def get_total(self):
        subtotal = sum(product.price * qty for product, qty in self.items)
        total = subtotal * (1 - self.discount) / 100
        return total
    def print_invoice(self):
        """In hóa đơn chi tiết"""
        print("\n🧾 --- HÓA ĐƠN MUA HÀNG ---")
        for product, qty in self.items:
            print(f"{product.name:20} x{qty:<3} = {product.price * qty:,.0f}₫")
        print(f"\nGiảm giá: {self.discount}%")
        print(f"Tổng cộng: {self.get_total():,.0f}₫")
        print("---------------------------\n")

p1 = Product("Laptop", 25000000, 5)
p2 = Product("Chuột", 300000, 10)
p3 = Product("Bàn phím", 800000, 4)

order = Order()
order.add_product(p1, 1)
order.add_product(p2, 2)
order.add_product(p3, 1)

order.apply_discount(10)

order.print_invoice()

# 18
class Movie:
    def __init__(self,title, director, rental_price):
        self.title = title
        self.director = director
        self.rental_price = rental_price
        self.is_rented = False # Trạng thái đã thuê hay chưa
class Rental:
    def __init__(self):
        self.movies = []
        self.total_income = 0.0 # tổng doanh thu

    def add_movie(self, movie):
        self.movies.append(movie)
        print("Đã thêm phim mới")

    def rent_movie(self,title):
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                if not movie.is_rented:
                    movie.is_rented = True
                    self.total_income += movie.rental_price
                    print("Đã mượn phim này")
                    return
                else:
                    print("Phim này đã được mượn")
                    return
        print("Không tìm thấy phim này")
    def return_movie(self,title):
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                if movie.is_rented:
                    movie.is_rented = False
                    print(f"Bạn đã trả phim: {movie.title}")
                    return
                else:
                    print(f"Phim '{movie.title}' chưa được thuê.")
                    return
        print(f"Không tìm thấy phim '{title}'.")
    def get_rented_movies(self):
        rented = [m.title for m in self.movies if m.is_rented]
        print("\nCác phim đang được thuê:")
        if rented:
            for name in rented:
                print(" -", name)
        else:
            print("Không có phim nào đang được thuê.")
        print()
    def get_total_income(self):
        return self.total_income
rental_store = Rental()

rental_store.add_movie(Movie("Inception", "Christopher Nolan", 30000))
rental_store.add_movie(Movie("Interstellar", "Christopher Nolan", 35000))
rental_store.add_movie(Movie("Avatar", "James Cameron", 40000))

rental_store.rent_movie("Inception")
rental_store.rent_movie("Avatar")

rental_store.get_rented_movies()

rental_store.return_movie("Inception")

print(f"Tổng doanh thu: {rental_store.get_total_income():,.0f}₫")

# 19
class Task:
    def __init__(self,description, priority = "Medium"):
        self.description = description
        self.priority = priority
        self.status = "Pending"
    def __str__(self):
        return f"[{self.status}] {self.description} (Priority: {self.priority})"
class TaskManager:
    def __init__(self):
        self.tasks = []
    def add_task(self, description, priority="Medium"):
        task = Task(description, priority)
        self.tasks.append(task)
        print(f"Thêm task: {description}, Priority: {priority}")
    def mark_completed(self,description):
        for task in self.tasks:
            if task.description.lower() == description.lower():
                if task.status == "Pending":
                    task.status = "Done"
                    print("Đã hoàn thành task này")
                    return 
                else:
                    print("Task này đã được đánh dấu hoàn thành rồi")
        print("Không tìm thấy task có description như vậy")
    def change_priority(self, description, new_priority):
        for task in self.tasks:
            if task.description.lower() == description.lower():
                task.priority = new_priority
                print("Đã thay đổi sự ưu tiên")
                return 
        print("Không tìm thấy task có description như vậy")
    def list_tasks(self):
        if not self.tasks:
            print("Danh sách trống")
            return
        print("\n Danh sách ")  
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")   
        print()

manager = TaskManager()

manager.add_task("Viết báo cáo đồ án", "High")
manager.add_task("Dọn dẹp thư mục code", "Low")
manager.add_task("Họp nhóm review tiến độ", "Medium")

manager.list_tasks()

manager.mark_completed("Dọn dẹp thư mục code")

manager.change_priority("Họp nhóm review tiến độ", "High")

manager.list_tasks()

#20
class Transaction:
    def __init__(self, t_type, amount):
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.type = t_type  # 'deposit' hoặc 'withdrawal'
        self.amount = amount

    def __str__(self):
        sign = "+" if self.type == "deposit" else "-"
        return f"[{self.date}] {self.type.title():<10} {sign}{self.amount:,.2f} VND"

class Account:
    def __init__(self, owner, pin, balance=0):
        self.owner = owner
        self.__pin = pin
        self.balance = balance
        self.transactions = []

    def check_pin(self, pin):
        return self.__pin == pin

    def deposit(self, amount):
        if amount <= 0:
            print("Số tiền nạp không hợp lệ.")
            return
        self.balance += amount
        self.transactions.append(Transaction("deposit", amount))
        print(f"Nạp {amount:,.0f} VND thành công. Số dư hiện tại: {self.balance:,.0f} VND")

    def withdraw(self, amount):
        if amount <= 0:
            print("Số tiền rút không hợp lệ.")
            return
        if amount > self.balance:
            print("Số dư không đủ để rút.")
            return
        self.balance -= amount
        self.transactions.append(Transaction("withdrawal", amount))
        print(f"Rút {amount:,.0f} VND thành công. Số dư còn lại: {self.balance:,.0f} VND")

    def get_statement(self):
        print(f"\nSao kê giao dịch của {self.owner}:")
        if not self.transactions:
            print("Không có giao dịch nào.")
            return
        for t in self.transactions:
            print(" -", t)
        print(f"Tổng số dư: {self.balance:,.0f} VND\n")


# --- Lớp ATM ---
class ATM:
    def __init__(self):
        self.current_account = None
        self.is_authenticated = False

    def insert_card(self, account):
        self.current_account = account
        self.is_authenticated = False
        print(f"Thẻ của {account.owner} đã được đưa vào ATM.")

    def enter_pin(self, pin):
        if self.current_account is None:
            print("Chưa có thẻ nào được đưa vào.")
            return
        if self.current_account.check_pin(pin):
            self.is_authenticated = True
            print("Mã PIN hợp lệ. Bạn có thể bắt đầu giao dịch.")
        else:
            print("Sai mã PIN.")

    def withdraw(self, amount):
        if not self.is_authenticated:
            print("Vui lòng nhập đúng mã PIN trước khi rút tiền.")
            return
        self.current_account.withdraw(amount)

    def deposit(self, amount):
        if not self.is_authenticated:
            print("Vui lòng nhập đúng mã PIN trước khi nạp tiền.")
            return
        self.current_account.deposit(amount)

    def print_statement(self):
        if not self.is_authenticated:
            print("Cần xác thực PIN trước khi xem sao kê.")
            return
        self.current_account.get_statement()

    def eject_card(self):
        if self.current_account:
            print(f"Trả thẻ cho {self.current_account.owner}.")
            self.current_account = None
            self.is_authenticated = False
        else:
            print("Không có thẻ nào trong máy.")


# --- Mô phỏng quá trình sử dụng ---
if __name__ == "__main__":
    acc1 = Account("Nguyễn Kiều Anh Quân", pin="1234", balance=5_000_000)
    atm = ATM()

    atm.insert_card(acc1)
    atm.enter_pin("1234")

    atm.deposit(2_000_000)
    atm.withdraw(1_500_000)
    atm.withdraw(10_000_000)  # Rút quá số dư
    atm.print_statement()
    atm.eject_card()
