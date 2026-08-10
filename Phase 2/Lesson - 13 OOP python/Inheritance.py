"""
Comprehensive Inheritance Example in Python OOP
This code demonstrates various inheritance concepts including:
- Single Inheritance
- Multiple Inheritance
- Multi-level Inheritance
- Method Overriding
- super() function
- Abstract Base Classes
- Method Resolution Order (MRO)
"""

from abc import ABC, abstractmethod
from datetime import datetime
import json


# ============================================================
# BASE CLASS (Parent Class)
# ============================================================

class Person:
    """Base class representing a person"""

    # Class variable (shared across all instances)
    species = "Homo sapiens"

    def __init__(self, name, age, email):
        """Constructor method"""
        self.name = name
        self.age = age
        self.email = email
        self._id = self._generate_id()  # Protected attribute

    def _generate_id(self):
        """Private method to generate unique ID"""
        return f"P{datetime.now().timestamp()}{hash(self.name) % 1000}"

    def introduce(self):
        """Method to introduce the person"""
        return f"Hello, I'm {self.name}, I'm {self.age} years old."

    def get_contact_info(self):
        """Method to get contact information"""
        return f"Email: {self.email}"

    def celebrate_birthday(self):
        """Method to celebrate birthday"""
        self.age += 1
        return f"Happy Birthday {self.name}! Now {self.age} years old."

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Person('{self.name}', {self.age}, '{self.email}')"


# ============================================================
# SINGLE INHERITANCE
# ============================================================

class Student(Person):
    """Student class inheriting from Person"""

    def __init__(self, name, age, email, student_id, major, gpa=0.0):
        """Constructor with additional student attributes"""
        # Call parent constructor using super()
        super().__init__(name, age, email)
        self.student_id = student_id
        self.major = major
        self.gpa = gpa
        self.courses = []

    def enroll_course(self, course_name):
        """Method to enroll in a course"""
        self.courses.append(course_name)
        return f"{self.name} enrolled in {course_name}"

    def update_gpa(self, new_gpa):
        """Method to update GPA"""
        if 0.0 <= new_gpa <= 4.0:
            self.gpa = new_gpa
            return f"GPA updated to {self.gpa}"
        else:
            raise ValueError("GPA must be between 0.0 and 4.0")

    # Method Overriding - overriding the introduce method
    def introduce(self):
        """Overridden introduction method"""
        parent_intro = super().introduce()
        return f"{parent_intro} I'm a student majoring in {self.major} with GPA: {self.gpa}"

    # Method Overriding - additional functionality
    def get_contact_info(self):
        """Overridden method with additional info"""
        parent_info = super().get_contact_info()
        return f"{parent_info} | Student ID: {self.student_id}"

    def __str__(self):
        return f"Student(name={self.name}, major={self.major}, gpa={self.gpa})"


# ============================================================
# MULTI-LEVEL INHERITANCE
# ============================================================

class GraduateStudent(Student):
    """GraduateStudent class inheriting from Student"""

    def __init__(self, name, age, email, student_id, major, gpa,
                 research_area, advisor):
        super().__init__(name, age, email, student_id, major, gpa)
        self.research_area = research_area
        self.advisor = advisor
        self.publications = []

    def publish_paper(self, title):
        """Method to publish research paper"""
        self.publications.append(title)
        return f"New publication: {title}"

    def defend_thesis(self):
        """Method to defend thesis"""
        return f"{self.name} is defending their thesis on {self.research_area}"

    # Further overriding
    def introduce(self):
        parent_intro = super().introduce()
        return f"{parent_intro} I'm a graduate student researching {self.research_area}"


# ============================================================
# MULTIPLE INHERITANCE
# ============================================================

class Employee:
    """Another parent class for multiple inheritance"""

    def __init__(self, employee_id, department, salary):
        self.employee_id = employee_id
        self.department = department
        self.salary = salary

    def work(self):
        return f"Employee {self.employee_id} is working in {self.department}"

    def get_salary(self):
        return f"Salary: ${self.salary}"

    def __str__(self):
        return f"Employee(id={self.employee_id}, dept={self.department})"


class TeachingAssistant(Student, Employee):
    """TeachingAssistant inherits from both Student and Employee"""

    def __init__(self, name, age, email, student_id, major, gpa,
                 employee_id, department, salary, courses_assigned):
        # Initialize both parent classes
        Student.__init__(self, name, age, email, student_id, major, gpa)
        Employee.__init__(self, employee_id, department, salary)
        self.courses_assigned = courses_assigned

    def teach_lab(self, lab_course):
        """Method specific to TeachingAssistant"""
        return f"{self.name} is teaching lab for {lab_course}"

    def grade_papers(self, assignment_name):
        """Method specific to TeachingAssistant"""
        return f"{self.name} is grading {assignment_name} papers"

    # Override method from both parents
    def work(self):
        # Call parent methods to show combined functionality
        student_work = f"Studying {self.major} with GPA: {self.gpa}"
        employee_work = Employee.work(self)
        return f"TA duties: {employee_work} and {student_work}"

    def introduce(self):
        # Choose which parent's method to use
        student_intro = Student.introduce(self)
        return f"{student_intro} I'm also a Teaching Assistant in {self.department}"


# ============================================================
# ABSTRACT BASE CLASS (ABC)
# ============================================================

class Shape(ABC):
    """Abstract base class for shapes"""

    @abstractmethod
    def area(self):
        """Abstract method to calculate area"""
        pass

    @abstractmethod
    def perimeter(self):
        """Abstract method to calculate perimeter"""
        pass

    def describe(self):
        """Concrete method available to all subclasses"""
        return f"This is a {self.__class__.__name__}"


class Rectangle(Shape):
    """Concrete implementation of Shape"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Circle(Shape):
    """Concrete implementation of Shape"""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

    def __str__(self):
        return f"Circle(radius={self.radius})"


# ============================================================
# HIERARCHY WITH MIXINS
# ============================================================

class SerializableMixin:
    """Mixin class to add serialization capability"""

    def to_json(self):
        """Convert object to JSON format"""
        return json.dumps(self.__dict__, default=str)

    def from_json(self, json_str):
        """Load object from JSON"""
        data = json.loads(json_str)
        for key, value in data.items():
            setattr(self, key, value)
        return self


class LoggableMixin:
    """Mixin class to add logging capability"""

    def log(self, message):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {self.__class__.__name__}: {message}"


class AdvancedStudent(Student, SerializableMixin, LoggableMixin):
    """Student with additional capabilities from mixins"""

    def __init__(self, name, age, email, student_id, major, gpa):
        super().__init__(name, age, email, student_id, major, gpa)
        self.created_at = datetime.now()

    def study(self):
        self.log(f"studying {self.major}")
        return f"{self.name} is studying {self.major}"


# ============================================================
# DEMONSTRATION AND USAGE
# ============================================================

def demonstrate_inheritance():
    """Demonstrate all inheritance concepts"""

    print("=" * 60)
    print("INHERITANCE DEMONSTRATION")
    print("=" * 60)

    # 1. Single Inheritance
    print("\n1. SINGLE INHERITANCE")
    print("-" * 40)
    person = Person("John Doe", 30, "john@email.com")
    student = Student("Alice Smith", 22, "alice@university.edu",
                      "S12345", "Computer Science", 3.8)

    print(f"Person: {person.introduce()}")
    print(f"Student: {student.introduce()}")
    print(f"Student contact: {student.get_contact_info()}")
    print(f"Enroll: {student.enroll_course('Data Structures')}")
    print(f"Update GPA: {student.update_gpa(3.9)}")

    # 2. Multi-level Inheritance
    print("\n2. MULTI-LEVEL INHERITANCE")
    print("-" * 40)
    grad = GraduateStudent("Bob Johnson", 26, "bob@research.edu",
                           "G67890", "Physics", 3.7,
                           "Quantum Computing", "Dr. Smith")
    print(f"Graduate: {grad.introduce()}")
    print(f"Publications: {grad.publish_paper('Quantum Entanglement')}")
    print(f"Thesis: {grad.defend_thesis()}")

    # 3. Multiple Inheritance
    print("\n3. MULTIPLE INHERITANCE")
    print("-" * 40)
    ta = TeachingAssistant("Carol White", 24, "carol@university.edu",
                           "TA1234", "Mathematics", 3.9,
                           "EMP5678", "Mathematics Dept", 45000,
                           ["Calculus I", "Calculus II"])
    print(f"TA Introduction: {ta.introduce()}")
    print(f"TA Work: {ta.work()}")
    print(f"TA Salary: {ta.get_salary()}")
    print(f"TA Teaching: {ta.teach_lab('Linear Algebra')}")
    print(f"TA Grading: {ta.grade_papers('Midterm Exam')}")

    # Check Method Resolution Order
    print(f"\nMRO for TeachingAssistant: {[cls.__name__ for cls in TeachingAssistant.__mro__]}")

    # 4. Abstract Base Classes
    print("\n4. ABSTRACT BASE CLASSES")
    print("-" * 40)
    rect = Rectangle(5, 3)
    circle = Circle(4)

    print(f"Rectangle area: {rect.area()}, perimeter: {rect.perimeter()}")
    print(f"Circle area: {circle.area():.2f}, perimeter: {circle.perimeter():.2f}")
    print(f"Shape description: {rect.describe()}")

    # 5. Mixins
    print("\n5. MIXINS (Multiple Inheritance for Capabilities)")
    print("-" * 40)
    adv_student = AdvancedStudent("David Brown", 23, "david@university.edu",
                                  "A9999", "Engineering", 3.6)
    print(f"Advanced Student: {adv_student.introduce()}")
    print(f"Logging: {adv_student.study()}")

    # Serialization
    json_data = adv_student.to_json()
    print(f"Serialized JSON: {json_data[:100]}...")  # Truncated for display

    # 6. Polymorphism
    print("\n6. POLYMORPHISM DEMONSTRATION")
    print("-" * 40)

    # Creating a list of different objects
    people = [
        Person("Eve Wilson", 35, "eve@company.com"),
        Student("Frank Miller", 21, "frank@university.edu", "S7890", "Biology", 3.5),
        GraduateStudent("Grace Lee", 28, "grace@research.edu", "G4567", "Chemistry", 3.8, "Biochemistry", "Dr. Chen"),
        TeachingAssistant("Henry Zhao", 25, "henry@university.edu", "TA5678", "Computer Science", 3.7, "EMP1234",
                          "CS Dept", 48000, ["Programming 101"])
    ]

    # All objects respond to introduce() but with different behaviors
    for person in people:
        print(f"Polymorphic introduction: {person.introduce()}")

    # 7. isinstance() and issubclass() checks
    print("\n7. TYPE CHECKING")
    print("-" * 40)
    print(f"Is Student a subclass of Person? {issubclass(Student, Person)}")
    print(f"Is GraduateStudent a subclass of Student? {issubclass(GraduateStudent, Student)}")
    print(f"Is TA instance of Student? {isinstance(ta, Student)}")
    print(f"Is TA instance of Employee? {isinstance(ta, Employee)}")
    print(f"Is TA instance of Person? {isinstance(ta, Person)}")


# ============================================================
# ADDITIONAL UTILITY FUNCTIONS
# ============================================================

def demonstrate_method_overriding():
    """Show detailed method overriding behavior"""
    print("\n" + "=" * 60)
    print("METHOD OVERRIDING DETAILS")
    print("=" * 60)

    # Create objects
    person = Person("Test Person", 30, "test@email.com")
    student = Student("Test Student", 22, "test@university.edu", "S999", "Physics", 3.5)

    # Compare methods
    print("\nPerson's introduce():")
    print(f"  {person.introduce()}")
    print("\nStudent's introduce() (overridden):")
    print(f"  {student.introduce()}")
    print("\nStudent's introduce() with super() call:")
    print(f"  {student.introduce()}")

    # Access parent method explicitly
    print("\nCalling parent method from student:")
    print(f"  {super(Student, student).introduce()}")

    # Demonstrate __str__ and __repr__
    print("\nString representations:")
    print(f"  str(person): {str(person)}")
    print(f"  repr(person): {repr(person)}")
    print(f"  str(student): {str(student)}")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run main demonstration
    demonstrate_inheritance()
    demonstrate_method_overriding()

    # Additional demonstration: Composition vs Inheritance
    print("\n" + "=" * 60)
    print("INHERITANCE TREE VISUALIZATION")
    print("=" * 60)
    print("""
    Inheritance Hierarchy:

    Person
      └── Student
            ├── GraduateStudent
            └── TeachingAssistant (also inherits from Employee)
                    └── Employee

    Shape (Abstract)
      ├── Rectangle
      └── Circle

    Mixins:
      SerializableMixin, LoggableMixin
          └── AdvancedStudent (inherits from Student + Mixins)
    """)

    print("\n✅ Inheritance demonstration complete!")