class StudentProfile:
    def __init__(self, name, id, cgpa):
        self.name = name
        self._id = id
        self.__cgpa = cgpa

    def show_cgpa(self):
        return self.__cgpa


my_profile = StudentProfile("Sera", "210794", "5.00")

print(f"Profile Owner: {my_profile.name}")
print(f"Student ID: {my_profile._id}")
print(f"CGPA: {my_profile.show_cgpa()}")