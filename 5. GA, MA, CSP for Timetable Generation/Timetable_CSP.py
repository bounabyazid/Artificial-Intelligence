import random
import copy
import numpy as np


def gen_random(n):
    return random.randint(1, n)


def print_timetable(t):
    for i in t:
        print("")
        for p in i:
            print(p.tolist())


def lecture_collisions_z_axis(t):
    tt = np.array(t)
    count = 0
    for i in tt:
        for j in i:
            lis = []
            for p in j:
                if p[0] != -1 and p[0] != 0:
                    lis.append(p)
            m = np.array(lis)
            count = count + len(m) - len(np.unique(list(row[1] for row in m)))
            count = count + len(m) - len(np.unique(list(row[0] for row in m)))
    return count


def course_per_day_error(c):
    timetable = copy.deepcopy(c)
    cost = 0
    counter = np.zeros((5, courses), dtype=np.int)
    for day_ in range(len(timetable)):
        for lecture_hall in range(len(timetable[day_])):
            for lecture in range(len(timetable[day_][lecture_hall])):
                # print(timetable[day_][lecture_hall][lecture], "mm", timetable[day_][lecture_hall][lecture][1])
                if timetable[day_][lecture_hall][lecture][1] != 0 and timetable[day_][lecture_hall][lecture][1] != -1:
                    counter[day_][timetable[day_][lecture_hall][lecture][1] - 1] = counter[day_][timetable[day_][lecture_hall][lecture][1] - 1] + 1
    for day_ in counter:
        for count in day_:
            if count > coursesPerDay:
                cost = cost + (count - coursesPerDay)
    return cost, counter


def class_frequency_error(timetable, check):
    cost = 0
    counter = np.zeros(courses, dtype=np.int)
    for i in timetable:
        for j in i:
            for k in j:
                if k[1] != 0 and k[1] != -1:
                    counter[k[1] - 1] = counter[k[1] - 1] + 1
    for i in counter:
        if i < minClassCount and check == "min":
            return 1, 1
        if i > maxClassCount and check == "max":
            return 1, 1
    return cost, counter


def fitness_value(timetable):
    return lecture_collisions_z_axis(timetable) + course_per_day_error(timetable)[0] + class_frequency_error(timetable, "max")[0]


def print_timetable_details(timetable):
    print_timetable(timetable)
    print("\nCourses per day Error:", course_per_day_error(timetable)[0], "\n", course_per_day_error(timetable)[1])
    print("Course Frequency Error Max:", class_frequency_error(timetable, "max")[0], "\n", class_frequency_error(timetable, "max")[1])
    print("Course Frequency Error Min:", class_frequency_error(timetable, "min")[0], "\n", class_frequency_error(timetable, "min")[1])
    print("Total Collisisons:", fitness_value(timetable))


def get_free_slot(timetable):
    for day in range(len(timetable)):
        for slot in range(len(timetable[day])):
            for lecture in range(len(timetable[day][slot])):
                if timetable[day][slot][lecture][0] == 0:
                    return day, slot, lecture
    return -1


# courses = 10
# lectureHalls = 3
# professors = 6
#
# minClassCount = 2
# maxClassCount = 5
#
# coursesPerDay = 1


courses = int(input("Enter Number of Courses: "))
lectureHalls = int(input("Enter Number of Lecture Halls: "))
professors = int(input("Enter Number of Professors: "))

minClassCount = int(input("Enter Minimum Class Count: "))
maxClassCount = int(input("Enter Maximum Class Count: "))
coursesPerDay = int(input("Enter Course per Day Limit: "))

courses_list = list(range(1, courses + 1))
courses_split_for_each_professor = np.array_split(courses_list, professors)

combinations = []

combinations.append([-1, -1])

for professor_ in range(1, len(courses_split_for_each_professor) + 1):
    for course_ in courses_split_for_each_professor[professor_ - 1]:
        combinations.append([professor_, course_])

print(combinations)

stack = []

Timetable = np.zeros((5, 8, lectureHalls, 2), dtype=int)

get_free_slot(Timetable)

stack = []
extended_list = []
stack.append([Timetable, 0])

while stack:

    popped_array = stack.pop(0)

    extended_list.append(popped_array[0])

    f = get_free_slot(popped_array[0])

    for z in combinations:
        temp_data = copy.deepcopy(popped_array[0])

        temp_data[f[0]][f[1]][f[2]] = z

        collisions = fitness_value(temp_data)

        if collisions == 0:
            stack.insert(0, [temp_data, popped_array[1] + 1])
            p = get_free_slot(temp_data)
            if p == -1:
                if class_frequency_error(temp_data, "min")[0] == 0:
                    print_timetable_details(temp_data)
                    exit(0)
            print("Queue: ", len(stack), " Cost: ", popped_array[1] + 1)
