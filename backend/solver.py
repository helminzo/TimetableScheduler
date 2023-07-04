from z3 import *
import json
import time
teachers = json.load(open('teachers.json', 'r'))
classes = json.load(open('classes.json', 'r'))
start = time.time()
allVars = []
allConstraints = []

# Define variables
classVars = {} # index order: dept, year, section, course, hour
for dept in classes:
    classVars[dept] = {}
    for year in classes[dept]:
        classVars[dept][year] = {}
        for section in classes[dept][year]:
            classVars[dept][year][section] = {}
            for course in classes[dept][year][section]:
                classVars[dept][year][section][course] = {}
                for hour in range(30):
                    var =  Bool(f'CC-{dept}-{year}-{section}-{course}-{hour}')
                    classVars[dept][year][section][course][hour] = var
                    allVars.append(var)

teachingHourVars = {} # index order: teacher, class & course '-' separated name, hour
teachesClassVars = {} # index order: teacher, class & course '-' separated name
for teacher in teachers:
    teachingHourVars[teacher] = {}
    teachesClassVars[teacher] = {}
    for dept in classes:
        for year in classes[dept]:
            for section in classes[dept][year]:
                coursesRequired = set(classes[dept][year][section].keys())
                coursesPossible = set(teachers[teacher]).intersection(coursesRequired)
                for course in coursesPossible:
                    classKeyName = f'{dept}-{year}-{section}-{course}'
                    teachingHourVars[teacher][classKeyName] = {}
                    var = Bool(f'TC-{teacher}-{classKeyName}')
                    teachesClassVars[teacher][classKeyName] = var
                    allVars.append(var)
                    for hour in range(30):
                        var = Bool(f'TH-{teacher}-{dept}-{year}-{section}-{course}-{hour}')
                        teachingHourVars[teacher][classKeyName][hour] = var
                        allVars.append(var)

# Generate constraints

# Every class can have at most one course in an hour
for dept in classVars:
    for year in classVars[dept]:
        for section in classVars[dept][year]:
            for hour in range(30):  
                oneClassAtATime = []
                for course in classVars[dept][year][section]:
                    oneClassAtATime.append(classVars[dept][year][section][course][hour])
                allConstraints.append(AtMost(*oneClassAtATime, 1))

# Every class must have the prescribed number of hours in a week
for dept in classVars:
    for year in classVars[dept]:
        for section in classVars[dept][year]:
            for course in classVars[dept][year][section]:
                hourConstraints = []
                hoursRequired = classes[dept][year][section][course]
                for hour in range(30):
                    hourConstraints.append(classVars[dept][year][section][course][hour])
                # add to all constraints that exactly four of hourConstraints must be true using PbEq
                allConstraints.append(PbEq([(hourConstraints[i], 1) for i in range(30)], hoursRequired))

# Every teacher can teach at most one class in an hour
for teacher in teachingHourVars:
    for hour in range(30):
        oneClassTaughtAtATime = []
        for classKeyName in teachingHourVars[teacher]:
            oneClassTaughtAtATime.append(teachingHourVars[teacher][classKeyName][hour])
        if(len(oneClassTaughtAtATime) > 0):
            allConstraints.append(AtMost(*oneClassTaughtAtATime, 1))

# Constraints for teachingHoursVars
for teacher in teachingHourVars:
    for classKeyName in teachingHourVars[teacher]:
        for hour in range(30):
            dept, year, section, courseName = classKeyName.split('-')
            # if the class is not taught by the teacher, then the teachingHourVar must be false
            if courseName not in teachers[teacher]:
                allConstraints.append(Not(teachingHourVars[teacher][classKeyName][hour]))
            # if the class is taught by the teacher, then the teachingHourVar could be true
            else:
                classKeyName = f'{dept}-{year}-{section}-{courseName}'
                # FIXME: assumes one course is taught in one class only!
                cons = Implies(teachingHourVars[teacher][classKeyName][hour], teachesClassVars[teacher][classKeyName])
                allConstraints.append(cons)

# For each class, each course must be taught by at least one teacher
for dept in classVars:
    for year in classVars[dept]:
        for section in classVars[dept][year]:
            for course in classVars[dept][year][section]:
                courseName = f'{dept}-{year}-{section}-{course}'
                teacherConstraints = []
                for teacher in teachers:
                    if course in teachers[teacher]:
                        teacherConstraints.append(teachesClassVars[teacher][courseName])
                allConstraints.append(Or(*teacherConstraints))

# Connect teachingHourVars and classVars
for dept in classVars:
    for year in classVars[dept]:
        for section in classVars[dept][year]:
            for course in classVars[dept][year][section]:
                classCourseName = f'{dept}-{year}-{section}-{course}'
                for hour in range(30):
                    for teacher in teachers:
                        if course in teachers[teacher]:
                            prec = teachingHourVars[teacher][classCourseName][hour]
                            ante = classVars[dept][year][section][course][hour]
                            allConstraints.append(Implies(prec, ante))

#If a teacher teaches a course, they must fulfill the hours required
for teacher in teachesClassVars:
    for classCourseName in teachesClassVars[teacher]:
        dept, year, section, courseName = classCourseName.split('-')
        classCourseName = f'{dept}-{year}-{section}-{courseName}'
        try:
            hoursRequired = classes[dept][year][section][courseName]
        except KeyError:
            hoursRequired = 0
        if(hoursRequired > 0):
            teacherConstraints = []
            for hour in range(30):
                teacherConstraints.append(teachingHourVars[teacher][classCourseName][hour])
            ante = PbEq([(teacherConstraints[i], 1) for i in range(30)], hoursRequired)
            cons = Implies(teachesClassVars[teacher][classCourseName], ante)
            allConstraints.append(cons) 

print("Created variables and constraints")
print(f"No. of variables: {len(allVars)}\nNo. of constraints: {len(allConstraints)}")

solver = Solver()
solver.add(allConstraints)
print("Added constraints to solver")
print(solver.check())
model = solver.model()

computedSchedule = {}
# Print a 30 hour timetable for each class
for dept in classVars:
    computedSchedule[dept] = {}
    for year in classVars[dept]:
        computedSchedule[dept][year] = {}
        for section in classVars[dept][year]:
            computedSchedule[dept][year][section] = []
            for hour in range(30):
                flag = False
                for course in classVars[dept][year][section]:
                    if model[classVars[dept][year][section][course][hour]]:
                        if flag == False:
                            computedSchedule[dept][year][section].append(course)
                            flag = True
                        else:
                            raise Exception
                if flag == False:
                    computedSchedule[dept][year][section].append('FREE')

week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
# print("********************\nCLASS TIMETABLES\n********************")
# for dept in computedSchedule:
#     for year in computedSchedule[dept]:
#         for section in computedSchedule[dept][year]:
#             className = f'{dept}-{year}-{section}'
#             f = open(f'Schedules/{className}.csv', 'w')
#             f.write(',1,2,3,4,5,6\n')

#             print(className)
#             for i in range(5):
#                 f.write(f'{week[i]},')
#                 for j in range(6):
#                     print(computedSchedule[dept][year][section][i*6+j], end=' ')
#                     f.write(f'{computedSchedule[dept][year][section][i*6+j]},')
#                 f.write('\n')


# print("********************\nSTAFF ALLOCATION\n********************")
# for teacher in teachesClassVars:
#     for classCourseName in teachesClassVars[teacher]:
#         if model[teachesClassVars[teacher][classCourseName]]:
#             dept, year, section, courseName = classCourseName.split('-')
#             print(f'{teacher} teaches {courseName} for {dept}-{year}-{section}')

computedTeacherSchedule = {}
for teacher in teachingHourVars:
    computedTeacherSchedule[teacher] = []
    for hour in range(30):
        flag = False
        for classCourseName in teachingHourVars[teacher]:
            if model[teachingHourVars[teacher][classCourseName][hour]]:
                if not flag:
                    dept, year, section, courseName = classCourseName.split('-')
                    computedTeacherSchedule[teacher].append(classCourseName)
                    flag = True
                else:
                    raise Exception
        if(flag == False):
            computedTeacherSchedule[teacher].append('FREE')

# print("********\nSTAFF TIME TABLES ********\n")
# for teacher in computedTeacherSchedule:
#     f = open('Schedules/' + teacher + '.csv', 'w')
#     f.write(',1,2,3,4,5,6\n')
#     print(teacher)
#     for i in range(5):
#         f.write(f'{week[i]},')
#         for j in range(6):
#             print(computedTeacherSchedule[teacher][i*6+j], end=' ')
#             f.write(f'{computedTeacherSchedule[teacher][i*6+j]},')
#         f.write('\n')
#     print()

end = time.time()

print(f"Time taken: {end-start} seconds")
                