# file2.py - Student Management System
class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.courses = []
        self.grades = {}
    
    def enroll_course(self, course_name):
        if course_name not in self.courses:
            self.courses.append(course_name)
            self.grades[course_name] = None
            return f"Enrolled in {course_name}"
        return f"Already enrolled in {course_name}"
    
    def drop_course(self, course_name):
        if course_name in self.courses:
            self.courses.remove(course_name)
            del self.grades[course_name]
            return f"Dropped {course_name}"
        return f"Not enrolled in {course_name}"
    
    def assign_grade(self, course_name, grade):
        if course_name in self.courses:
            if 0 <= grade <= 100:
                self.grades[course_name] = grade
                return f"Assigned grade {grade} for {course_name}"
            else:
                return "Grade must be between 0 and 100"
        return f"Not enrolled in {course_name}"
    
    def get_gpa(self):
        if not self.grades:
            return 0.0
        
        total_grade = 0
        count = 0
        for course, grade in self.grades.items():
            if grade is not None:
                total_grade += grade
                count += 1
        
        return total_grade / count if count > 0 else 0.0
    
    def get_student_info(self):
        info = f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"
        info += f"\nGPA: {self.get_gpa():.2f}"
        info += f"\nCourses: {', '.join(self.courses) if self.courses else 'None'}"
        return info
    
    def is_passing(self, passing_grade=60):
        return self.get_gpa() >= passing_grade


class StudentManager:
    def __init__(self):
        self.students = {}
        self.next_id = 1
    
    def add_student(self, name, age, grade):
        student_id = f"S{self.next_id:03d}"
        student = Student(student_id, name, age, grade)
        self.students[student_id] = student
        self.next_id += 1
        return student_id
    
    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            return f"Removed student {student_id}"
        return f"Student {student_id} not found"
    
    def get_student(self, student_id):
        return self.students.get(student_id)
    
    def get_all_students(self):
        return list(self.students.values())
    
    def enroll_student_in_course(self, student_id, course_name):
        student = self.get_student(student_id)
        if student:
            return student.enroll_course(course_name)
        return f"Student {student_id} not found"
    
    def assign_grade_to_student(self, student_id, course_name, grade):
        student = self.get_student(student_id)
        if student:
            return student.assign_grade(course_name, grade)
        return f"Student {student_id} not found"
    
    def get_class_average(self):
        if not self.students:
            return 0.0
        
        total_gpa = 0
        count = 0
        for student in self.students.values():
            gpa = student.get_gpa()
            if gpa > 0:
                total_gpa += gpa
                count += 1
        
        return total_gpa / count if count > 0 else 0.0
    
    def get_failing_students(self, passing_grade=60):
        failing = []
        for student in self.students.values():
            if not student.is_passing(passing_grade):
                failing.append(student)
        return failing

# Example usage
if __name__ == "__main__":
    manager = StudentManager()
    
    # Add students
    s1 = manager.add_student("John Doe", 16, 10)
    s2 = manager.add_student("Jane Smith", 17, 11)
    
    # Enroll in courses
    manager.enroll_student_in_course(s1, "Mathematics")
    manager.enroll_student_in_course(s1, "Science")
    manager.enroll_student_in_course(s2, "Mathematics")
    manager.enroll_student_in_course(s2, "History")
    
    # Assign grades
    manager.assign_grade_to_student(s1, "Mathematics", 85)
    manager.assign_grade_to_student(s1, "Science", 92)
    manager.assign_grade_to_student(s2, "Mathematics", 78)
    manager.assign_grade_to_student(s2, "History", 88)
    
    # Display info
    for student in manager.get_all_students():
        print(student.get_student_info())
        print()
    
    print(f"Class average-V1: {manager.get_class_average():.2f}")