from person import Person
from student import Student

def main():
    # Create an object of the Person class
    person1 = Person("Alice", 30)

    # Use the object
    person1.greet()

    print()
    student1 = Student("Bob", 30, 'S12345')
    student1.greet()
    student1.study()

if __name__ == "__main__":
    main()