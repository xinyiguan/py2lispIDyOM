from dataclasses import dataclass


class Apple:
    def __init__(self,age:int,price = 15):
        self.age = age
        self.price = price

@dataclass
class Apple:
    age: int
    price = 15


def func():
    apple = Apple(age=8)
    print(apple.age)


if __name__ == '__main__':
    func()
