"""
COMPREHENSIVE GUIDE TO AGGREGATION IN PYTHON OOP
================================================
Aggregation is a "HAS-A" relationship where one object contains
references to other objects, but the contained objects can exist
independently (weak relationship).

Key Differences:
- Composition: Strong relationship, parts cannot exist without the whole
- Aggregation: Weak relationship, parts can exist independently
- Association: General relationship between objects
"""


# ============================================================
# 1. BASIC AGGREGATION EXAMPLE
# ============================================================

class Professor:
    """Professor class - independent entity"""

    def __init__(self, name, employee_id, department):
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.courses_taught = []

    def assign_course(self, course_name):
        self.courses_taught.append(course_name)
        return f"{self.name} assigned to teach {course_name}"

    def __str__(self):
        return f"Professor({self.name}, Dept: {self.department})"

    def __repr__(self):
        return f"Professor('{self.name}', '{self.employee_id}')"


class Course:
    """Course class - independent entity"""

    def __init__(self, course_code, course_name, credits):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.professor = None  # Aggregation: professor can be assigned later

    def assign_professor(self, professor):
        """Assign a professor to this course (Aggregation)"""
        if isinstance(professor, Professor):
            self.professor = professor
            professor.assign_course(self.course_name)
            return f"{professor.name} assigned to {self.course_name}"
        raise ValueError("Invalid professor object")

    def get_professor_info(self):
        if self.professor:
            return f"Instructor: {self.professor.name}"
        return "No professor assigned yet"

    def __str__(self):
        return f"Course({self.course_code}: {self.course_name})"


# ============================================================
# 2. AGGREGATION WITH COLLECTIONS
# ============================================================

class Student:
    """Student class - independent entity"""

    def __init__(self, student_id, name, major):
        self.student_id = student_id
        self.name = name
        self.major = major
        self.enrolled_courses = []  # Aggregation: courses exist independently

    def enroll(self, course):
        """Enroll in a course (Aggregation)"""
        if isinstance(course, Course):
            self.enrolled_courses.append(course)
            return f"{self.name} enrolled in {course.course_name}"
        raise ValueError("Invalid course object")

    def drop_course(self, course):
        """Drop a course"""
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            return f"{self.name} dropped {course.course_name}"
        return f"{self.name} is not enrolled in {course.course_name}"

    def get_schedule(self):
        """Get all enrolled courses"""
        if not self.enrolled_courses:
            return f"{self.name} is not enrolled in any courses"

        schedule = [f"{self.name}'s Schedule:"]
        for course in self.enrolled_courses:
            schedule.append(f"  - {course.course_name} ({course.course_code})")
        return "\n".join(schedule)

    def __str__(self):
        return f"Student({self.name}, {self.student_id})"


class Department:
    """Department class - aggregates professors and courses"""

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.professors = []  # Aggregation: professors exist independently
        self.courses = []  # Aggregation: courses exist independently

    def add_professor(self, professor):
        """Add a professor to the department"""
        if isinstance(professor, Professor):
            self.professors.append(professor)
            return f"{professor.name} added to {self.name} department"
        raise ValueError("Invalid professor object")

    def add_course(self, course):
        """Add a course to the department"""
        if isinstance(course, Course):
            self.courses.append(course)
            return f"{course.course_name} added to {self.name} department"
        raise ValueError("Invalid course object")

    def get_professors(self):
        """Get all professors in department"""
        if not self.professors:
            return f"No professors in {self.name} department"

        prof_list = [f"Professors in {self.name}:"]
        for prof in self.professors:
            prof_list.append(f"  - {prof.name} ({prof.department})")
        return "\n".join(prof_list)

    def get_courses(self):
        """Get all courses in department"""
        if not self.courses:
            return f"No courses in {self.name} department"

        course_list = [f"Courses in {self.name}:"]
        for course in self.courses:
            course_list.append(f"  - {course.course_name} ({course.course_code})")
        return "\n".join(course_list)


# ============================================================
# 3. REAL-WORLD AGGREGATION: COMPANY EXAMPLE
# ============================================================

class Employee:
    """Employee class - independent entity"""

    def __init__(self, emp_id, name, position, salary):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.salary = salary
        self.projects = []  # Aggregation: projects exist independently

    def assign_to_project(self, project):
        """Assign employee to a project"""
        if isinstance(project, Project):
            self.projects.append(project)
            project.add_member(self)
            return f"{self.name} assigned to {project.name}"
        raise ValueError("Invalid project object")

    def remove_from_project(self, project):
        """Remove employee from project"""
        if project in self.projects:
            self.projects.remove(project)
            project.remove_member(self)
            return f"{self.name} removed from {project.name}"
        return f"{self.name} is not in {project.name}"

    def get_projects(self):
        if not self.projects:
            return f"{self.name} is not assigned to any projects"
        projects = [f"{self.name}'s Projects:"]
        for project in self.projects:
            projects.append(f"  - {project.name} ({project.status})")
        return "\n".join(projects)

    def __str__(self):
        return f"Employee({self.name}, {self.position})"


class Project:
    """Project class - independent entity"""

    def __init__(self, project_id, name, budget, deadline):
        self.project_id = project_id
        self.name = name
        self.budget = budget
        self.deadline = deadline
        self.status = "Planning"
        self.team_members = []  # Aggregation: employees exist independently
        self.tasks = []  # Aggregation: tasks exist independently

    def add_member(self, employee):
        """Add employee to project team"""
        if employee not in self.team_members:
            self.team_members.append(employee)
            return f"{employee.name} added to {self.name} team"
        return f"{employee.name} is already in the team"

    def remove_member(self, employee):
        """Remove employee from project team"""
        if employee in self.team_members:
            self.team_members.remove(employee)
            return f"{employee.name} removed from {self.name} team"
        return f"{employee.name} is not in the team"

    def add_task(self, task):
        """Add task to project"""
        if isinstance(task, Task):
            self.tasks.append(task)
            return f"Task '{task.name}' added to {self.name}"
        raise ValueError("Invalid task object")

    def update_status(self, new_status):
        """Update project status"""
        self.status = new_status
        return f"{self.name} status updated to {new_status}"

    def get_team_info(self):
        if not self.team_members:
            return f"No team members for {self.name}"

        team = [f"Team Members for {self.name}:"]
        for member in self.team_members:
            team.append(f"  - {member.name} ({member.position})")
        return "\n".join(team)

    def get_progress(self):
        if not self.tasks:
            return f"No tasks defined for {self.name}"

        completed = sum(1 for task in self.tasks if task.completed)
        total = len(self.tasks)
        percentage = (completed / total) * 100
        return f"{self.name}: {completed}/{total} tasks completed ({percentage:.1f}%)"

    def __str__(self):
        return f"Project({self.name}, Status: {self.status})"


class Task:
    """Task class - independent entity"""

    def __init__(self, task_id, name, description, priority="Medium"):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.priority = priority
        self.completed = False
        self.assigned_to = None  # Aggregation: employee exists independently

    def assign_to(self, employee):
        """Assign task to an employee"""
        if isinstance(employee, Employee):
            self.assigned_to = employee
            return f"Task '{self.name}' assigned to {employee.name}"
        raise ValueError("Invalid employee object")

    def complete(self):
        """Mark task as completed"""
        self.completed = True
        return f"Task '{self.name}' completed!"

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Task({self.name}, {status}, Priority: {self.priority})"


# ============================================================
# 4. LIBRARY SYSTEM AGGREGATION
# ============================================================

class Book:
    """Book class - independent entity"""

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.available = True
        self.current_borrower = None  # Aggregation: member exists independently

    def borrow(self, member):
        """Borrow book to a member"""
        if self.available:
            self.available = False
            self.current_borrower = member
            return f"'{self.title}' borrowed by {member.name}"
        return f"'{self.title}' is not available"

    def return_book(self):
        """Return book to library"""
        if not self.available:
            borrower_name = self.current_borrower.name if self.current_borrower else "Unknown"
            self.available = True
            self.current_borrower = None
            return f"'{self.title}' returned by {borrower_name}"
        return f"'{self.title}' is already available"

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.current_borrower.name if self.current_borrower else 'Unknown'}"
        return f"Book({self.title}, {status})"


class LibraryMember:
    """Library Member class - independent entity"""

    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = []  # Aggregation: books exist independently

    def borrow_book(self, book):
        """Borrow a book from library"""
        if isinstance(book, Book):
            result = book.borrow(self)
            if "borrowed by" in result:
                self.borrowed_books.append(book)
            return result
        raise ValueError("Invalid book object")

    def return_book(self, book):
        """Return a borrowed book"""
        if book in self.borrowed_books:
            result = book.return_book()
            self.borrowed_books.remove(book)
            return result
        return f"{self.name} hasn't borrowed '{book.title}'"

    def get_borrowed_books(self):
        if not self.borrowed_books:
            return f"{self.name} has no borrowed books"

        books = [f"{self.name}'s Borrowed Books:"]
        for book in self.borrowed_books:
            books.append(f"  - {book.title} by {book.author}")
        return "\n".join(books)

    def __str__(self):
        return f"LibraryMember({self.name}, {self.member_id})"


class Library:
    """Library class - aggregates books and members"""

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []  # Aggregation: books exist independently
        self.members = []  # Aggregation: members exist independently

    def add_book(self, book):
        """Add a book to library"""
        if isinstance(book, Book):
            self.books.append(book)
            return f"Book '{book.title}' added to {self.name} library"
        raise ValueError("Invalid book object")

    def add_member(self, member):
        """Add a member to library"""
        if isinstance(member, LibraryMember):
            self.members.append(member)
            return f"Member {member.name} added to {self.name} library"
        raise ValueError("Invalid member object")

    def search_by_title(self, title):
        """Search for books by title"""
        results = [book for book in self.books if title.lower() in book.title.lower()]
        if results:
            return [str(book) for book in results]
        return ["No books found matching your search"]

    def search_by_author(self, author):
        """Search for books by author"""
        results = [book for book in self.books if author.lower() in book.author.lower()]
        if results:
            return [str(book) for book in results]
        return ["No books found by this author"]

    def get_available_books(self):
        """Get all available books"""
        available = [book for book in self.books if book.available]
        if available:
            return [str(book) for book in available]
        return ["No books available"]

    def get_total_books(self):
        return f"Total books: {len(self.books)}"

    def get_total_members(self):
        return f"Total members: {len(self.members)}"


# ============================================================
# 5. UNIVERSITY SYSTEM WITH AGGREGATION
# ============================================================

class University:
    """University class - top-level aggregate"""

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.departments = []  # Aggregation: departments exist independently
        self.students = []  # Aggregation: students exist independently
        self.courses = []  # Aggregation: courses exist independently

    def add_department(self, department):
        """Add a department to university"""
        if isinstance(department, Department):
            self.departments.append(department)
            return f"Department {department.name} added to {self.name}"
        raise ValueError("Invalid department object")

    def add_student(self, student):
        """Add a student to university"""
        if isinstance(student, Student):
            self.students.append(student)
            return f"Student {student.name} enrolled in {self.name}"
        raise ValueError("Invalid student object")

    def add_course(self, course):
        """Add a course to university"""
        if isinstance(course, Course):
            self.courses.append(course)
            return f"Course {course.course_name} added to {self.name}"
        raise ValueError("Invalid course object")

    def get_university_stats(self):
        """Get statistics about the university"""
        stats = [
            f"{'=' * 50}",
            f"UNIVERSITY: {self.name}",
            f"Location: {self.location}",
            f"Departments: {len(self.departments)}",
            f"Students: {len(self.students)}",
            f"Courses: {len(self.courses)}",
            f"{'=' * 50}"
        ]
        return "\n".join(stats)

    def get_department_details(self, department_name):
        """Get details of a specific department"""
        for dept in self.departments:
            if dept.name.lower() == department_name.lower():
                details = [
                    f"Department: {dept.name}",
                    f"Location: {dept.location}",
                    f"Professors: {len(dept.professors)}",
                    f"Courses: {len(dept.courses)}"
                ]
                return "\n".join(details)
        return f"Department '{department_name}' not found"


# ============================================================
# 6. AGGREGATION VS COMPOSITION COMPARISON
# ============================================================

class Engine:
    """Engine class - can exist independently"""

    def __init__(self, engine_type, horsepower):
        self.engine_type = engine_type
        self.horsepower = horsepower

    def start(self):
        return f"Engine {self.engine_type} started"

    def __str__(self):
        return f"Engine({self.engine_type}, {self.horsepower}HP)"


class Wheels:
    """Wheels class - can exist independently"""

    def __init__(self, size, brand):
        self.size = size
        self.brand = brand

    def rotate(self):
        return f"Wheels rotating"

    def __str__(self):
        return f"Wheels({self.size}\", {self.brand})"


class Car:
    """Car class with aggregation and composition"""

    def __init__(self, model, year):
        self.model = model
        self.year = year
        # Aggregation: engine exists independently
        self.engine = None
        # Aggregation: wheels exist independently
        self.wheels = None
        # Composition: parts cannot exist without car
        self._serial_number = self._generate_serial_number()

    def _generate_serial_number(self):
        """Private method - composition example"""
        return f"CAR-{self.model}-{self.year}-{id(self)}"

    def install_engine(self, engine):
        """Aggregation: install engine"""
        if isinstance(engine, Engine):
            self.engine = engine
            return f"Engine installed in {self.model}"
        raise ValueError("Invalid engine object")

    def install_wheels(self, wheels):
        """Aggregation: install wheels"""
        if isinstance(wheels, Wheels):
            self.wheels = wheels
            return f"Wheels installed on {self.model}"
        raise ValueError("Invalid wheels object")

    def start_car(self):
        if self.engine:
            return self.engine.start()
        return "No engine installed"

    def get_details(self):
        details = [
            f"Model: {self.model}",
            f"Year: {self.year}",
            f"Serial: {self._serial_number}",
            f"Engine: {self.engine if self.engine else 'Not installed'}",
            f"Wheels: {self.wheels if self.wheels else 'Not installed'}"
        ]
        return "\n".join(details)


# ============================================================
# 7. DEMONSTRATION AND USAGE
# ============================================================

def demonstrate_aggregation():
    """Comprehensive demonstration of aggregation"""

    print("=" * 70)
    print("AGGREGATION DEMONSTRATION")
    print("=" * 70)

    # 1. University System
    print("\n1. UNIVERSITY SYSTEM WITH AGGREGATION")
    print("-" * 50)

    # Create independent entities
    cs_dept = Department("Computer Science", "Building A")
    math_dept = Department("Mathematics", "Building B")

    prof1 = Professor("Dr. Smith", "P001", "Computer Science")
    prof2 = Professor("Dr. Johnson", "P002", "Mathematics")
    prof3 = Professor("Dr. Lee", "P003", "Computer Science")

    course1 = Course("CS101", "Introduction to Programming", 3)
    course2 = Course("CS201", "Data Structures", 4)
    course3 = Course("MATH101", "Calculus I", 3)

    # Add to departments (Aggregation)
    cs_dept.add_professor(prof1)
    cs_dept.add_professor(prof3)
    cs_dept.add_course(course1)
    cs_dept.add_course(course2)

    math_dept.add_professor(prof2)
    math_dept.add_course(course3)

    # Assign professors to courses (Aggregation)
    course1.assign_professor(prof1)
    course2.assign_professor(prof3)
    course3.assign_professor(prof2)

    # Create university and add departments (Aggregation)
    university = University("Tech University", "New York")
    university.add_department(cs_dept)
    university.add_department(math_dept)
    university.add_course(course1)
    university.add_course(course2)
    university.add_course(course3)

    # Create students
    student1 = Student("S001", "Alice Brown", "Computer Science")
    student2 = Student("S002", "Bob Wilson", "Mathematics")
    student3 = Student("S003", "Charlie Davis", "Computer Science")

    # Add students to university (Aggregation)
    university.add_student(student1)
    university.add_student(student2)
    university.add_student(student3)

    # Enroll students in courses (Aggregation)
    student1.enroll(course1)
    student1.enroll(course2)
    student2.enroll(course3)
    student3.enroll(course1)
    student3.enroll(course3)

    # Display university structure
    print(university.get_university_stats())
    print("\n" + cs_dept.get_professors())
    print("\n" + cs_dept.get_courses())
    print("\n" + student1.get_schedule())
    print("\n" + student2.get_schedule())

    # 2. Company System
    print("\n2. COMPANY PROJECT MANAGEMENT")
    print("-" * 50)

    # Create employees (Independent)
    emp1 = Employee("E001", "John Doe", "Software Engineer", 75000)
    emp2 = Employee("E002", "Jane Smith", "Project Manager", 85000)
    emp3 = Employee("E003", "Bob Johnson", "Designer", 65000)

    # Create projects (Independent)
    project1 = Project("P001", "E-commerce Platform", 500000, "2024-12-31")
    project2 = Project("P002", "Mobile App", 300000, "2024-10-15")

    # Create tasks (Independent)
    task1 = Task("T001", "Database Design", "Design database schema", "High")
    task2 = Task("T002", "Frontend Development", "Build React components", "High")
    task3 = Task("T003", "Backend API", "Develop REST API", "Medium")

    # Assign tasks to projects (Aggregation)
    project1.add_task(task1)
    project1.add_task(task2)
    project2.add_task(task3)

    # Assign employees to projects (Aggregation)
    emp1.assign_to_project(project1)
    emp2.assign_to_project(project1)
    emp3.assign_to_project(project2)

    # Assign tasks to employees (Aggregation)
    task1.assign_to(emp1)
    task2.assign_to(emp3)
    task3.assign_to(emp2)

    # Complete tasks
    task1.complete()
    task2.complete()

    # Display project information
    print(project1.get_team_info())
    print("\n" + project1.get_progress())
    print("\n" + emp1.get_projects())
    print("\n" + str(task1))
    print(str(task2))

    # 3. Library System
    print("\n3. LIBRARY SYSTEM")
    print("-" * 50)

    # Create library
    library = Library("Central Library", "Main Street")

    # Create books (Independent)
    book1 = Book("978-0132350884", "Clean Code", "Robert C. Martin", 2008)
    book2 = Book("978-0201633610", "Design Patterns", "Gang of Four", 1994)
    book3 = Book("978-1491950357", "Fluent Python", "Luciano Ramalho", 2015)

    # Create members (Independent)
    member1 = LibraryMember("M001", "Sarah Lee", "sarah@email.com")
    member2 = LibraryMember("M002", "Mike Chen", "mike@email.com")

    # Add books to library (Aggregation)
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # Add members to library (Aggregation)
    library.add_member(member1)
    library.add_member(member2)

    # Borrow books (Aggregation)
    member1.borrow_book(book1)
    member1.borrow_book(book2)
    member2.borrow_book(book3)

    # Display library status
    print(f"Library: {library.name}")
    print(library.get_total_books())
    print(library.get_total_members())
    print("\n" + member1.get_borrowed_books())
    print("\n" + member2.get_borrowed_books())
    print("\nAvailable Books:")
    for book in library.get_available_books():
        print(f"  {book}")

    # 4. Car Example (Aggregation vs Composition)
    print("\n4. CAR: AGGREGATION VS COMPOSITION")
    print("-" * 50)

    # Create independent parts
    engine = Engine("V6", 300)
    wheels = Wheels(18, "Michelin")

    # Create car
    car = Car("Mustang", 2024)

    # Install parts (Aggregation)
    car.install_engine(engine)
    car.install_wheels(wheels)

    # Start car
    print(car.start_car())
    print("\n" + car.get_details())

    # Show that parts exist independently
    print(f"\nEngine still exists independently: {engine}")
    print(f"Wheels still exist independently: {wheels}")

    # 5. Aggregation vs Composition Comparison
    print("\n5. AGGREGATION VS COMPOSITION COMPARISON")
    print("-" * 50)
    print("""
    AGGREGATION (Weak Relationship):
    - Parts can exist independently
    - Whole doesn't own the parts
    - Parts are shared among wholes
    - Deleting whole doesn't delete parts
    Examples:
      - Car and Engine (engine can exist without car)
      - University and Students (students can exist without university)
      - Library and Books (books can exist without library)

    COMPOSITION (Strong Relationship):
    - Parts cannot exist without the whole
    - Whole owns the parts
    - Parts are exclusive to the whole
    - Deleting whole deletes parts
    Examples:
      - Car and Serial Number (serial number only exists for car)
      - House and Rooms (rooms can't exist without house)
      - Order and Order Items (items can't exist without order)
    """)


# ============================================================
# 8. ADDITIONAL: AGGREGATION WITH DATA PERSISTENCE
# ============================================================

import json
from typing import List, Optional


class SerializableAggregate:
    """Mixin for serialization of aggregate objects"""

    def to_dict(self) -> dict:
        """Convert object to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') else str(item)
                               for item in value]
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def to_json(self) -> str:
        """Convert object to JSON"""
        return json.dumps(self.to_dict(), default=str, indent=2)


class Organization(SerializableAggregate):
    """Organization with aggregation"""

    def __init__(self, name: str):
        self.name = name
        self.departments: List['Department'] = []
        self.employees: List['Employee'] = []

    def add_department(self, dept: 'Department') -> str:
        self.departments.append(dept)
        return f"Department {dept.name} added to {self.name}"

    def add_employee(self, emp: 'Employee') -> str:
        self.employees.append(emp)
        return f"Employee {emp.name} added to {self.name}"

    def get_stats(self) -> dict:
        return {
            'organization': self.name,
            'departments': len(self.departments),
            'employees': len(self.employees),
            'total_salary': sum(emp.salary for emp in self.employees)
        }


def demonstrate_persistence():
    """Demonstrate aggregation with data persistence"""
    print("\n" + "=" * 60)
    print("AGGREGATION WITH DATA PERSISTENCE")
    print("=" * 60)

    # Create organization structure
    org = Organization("Tech Innovations Inc.")

    # Create departments
    engineering = Department("Engineering", "3rd Floor")
    marketing = Department("Marketing", "2nd Floor")

    # Create employees
    emp1 = Employee("E001", "Alice Johnson", "Senior Developer", 90000)
    emp2 = Employee("E002", "Bob Williams", "Product Manager", 85000)
    emp3 = Employee("E003", "Carol Martinez", "Marketing Specialist", 70000)

    # Build organization
    org.add_department(engineering)
    org.add_department(marketing)
    org.add_employee(emp1)
    org.add_employee(emp2)
    org.add_employee(emp3)

    # Show serialization
    print("Serialized Organization Data:")
    print("-" * 40)
    print(org.to_json())

    print("\nOrganization Statistics:")
    stats = org.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run main demonstration
    demonstrate_aggregation()

    # Run persistence demonstration
    demonstrate_persistence()

    # Summary
    print("\n" + "=" * 70)
    print("AGGREGATION KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ AGGREGATION IS A "HAS-A" RELATIONSHIP
       - One object contains references to others

    ✅ WEAK RELATIONSHIP
       - Contained objects can exist independently
       - No ownership or lifecycle dependency

    ✅ REUSABILITY
       - Same object can be shared among multiple containers
       - Objects are reusable across different contexts

    ✅ FLEXIBILITY
       - Can add/remove parts at runtime
       - Loose coupling between components

    ✅ COMMON USES
       - Collections (List, Set, Dictionary)
       - University - Students - Courses
       - Company - Employees - Projects
       - Library - Books - Members
       - Shopping Cart - Items

    ✅ VS COMPOSITION
       - Composition: Strong, parts die with whole
       - Aggregation: Weak, parts live independently

    ✅ VS ASSOCIATION
       - Association: General relationship
       - Aggregation: Special "part-of" relationship

    ✅ BEST PRACTICES
       - Use lists/sets for collections of independent objects
       - Allow parts to be shared (if appropriate)
       - Implement methods to add/remove parts
       - Serialize/deserialize aggregate structures
       - Maintain reference integrity
    """)

    print("=" * 70)
    print("✅ AGGREGATION DEMONSTRATION COMPLETE!")
    print("=" * 70)