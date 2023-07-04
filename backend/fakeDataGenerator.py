from faker import Faker
import random
import json

fake = Faker()
numTeachers = 17
courses = []
teacherDict = {}

for year in range(1, 5):
    for course in range(1, 14, 2):
        courses.append(f'CST{year}{str(course).zfill(2)}')
# shuffle the courses
random.shuffle(courses)
# print(courses)
for i in range(numTeachers):
    teacherDict[fake.name()] = []

for teacher in teacherDict:
    # Assign five random courses to each teacher
    teacherDict[teacher] = random.sample(courses, 5)

classes = json.load(open('classes.json', 'r'))
# Classes index order: dept, year, section, course
# Get all courses from classes and check that that teacherdict has all of them
allCourses = set()
for dept in classes:
    for year in classes[dept]:
        for section in classes[dept][year]:
            for course in classes[dept][year][section]:
                allCourses.add(course)
taughtCourses = set()
for teacher in teacherDict:
    taughtCourses.update(teacherDict[teacher])
print(allCourses - taughtCourses)
json.dump(teacherDict, open('teachers.json', 'w'))