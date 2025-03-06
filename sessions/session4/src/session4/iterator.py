class EvenIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0
    def __iter__(self):
        return self
    def __next__(self):
        while self.index < len(self.numbers):
            num = self.numbers[self.index] # attr num with item from list with current index
            self.index += 1 # index count
            if num % 2 == 0:
                return num
        raise StopIteration

def fibonacci(n):
    a, b = 0, 1 
    for _ in range(n):
        yield a 
        a, b = b, a + b

numbers = EvenIterator([11,22,30,40,32,33,34,36])
#iter(numbers)

for num in numbers:
    print(num)

for num in fibonacci(10):
    print("Fibo Number: ",num)




