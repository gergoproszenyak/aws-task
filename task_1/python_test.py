#!/usr/bin/env python3


def count_vowels(string):
    vowel = ['a', 'e', 'i', 'o', 'u']
    string = string.lower()
    count = 0
    for letter in string:
        if letter in vowel:
            count += 1
    return count


print (count_vowels('Celebration'))
print (count_vowels('Palm'))
print (count_vowels('Prediction'))


class Calculator():
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def add(self):
        return self.a + self.b
    def subtract(self):
        return self.a - self.b
    def multiply(self):
        return self.a * self.b
    def divide(self):
        return self.a / self.b


calculator = Calculator(10,5)


print (calculator.add())
print (calculator.subtract())
print (calculator.multiply())
print (calculator.divide())


def will_hit(trajectory, coordinates):
    trajectory = trajectory[4:].replace('x','*x')
    x, y = coordinates
    return y == eval(trajectory)


print (will_hit("y = 2x - 5", (0, 0)))
print (will_hit("y = -4x + 6", (1, 2)))
print (will_hit("y = 2x + 6", (3, 2)))