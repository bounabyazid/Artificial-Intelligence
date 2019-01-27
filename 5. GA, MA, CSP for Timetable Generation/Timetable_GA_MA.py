import random
import copy
import numpy as np
import matplotlib.pyplot as plt


def gen_random(n):
    return random.randint(1, n)


def print_tt(t):
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
                if p[0] != 0:
                    lis.append(p)
            m = np.array(lis)
            count = count + len(m) - len(np.unique(list(row[1] for row in m)))
            count = count + len(m) - len(np.unique(list(row[0] for row in m)))
    return count


def course_per_day_error(c):
    chromosome = copy.deepcopy(c)
    cost = 0
    list_ = np.zeros((5, courses), dtype=np.int)
    for day in range(len(chromosome)):
        for lecture_hall in range(len(chromosome[day])):
            for lecture in range(len(chromosome[day][lecture_hall])):
                if chromosome[day][lecture_hall][lecture][1] != 0:
                    list_[day][chromosome[day][lecture_hall][lecture][1] - 1] = list_[day][chromosome[day][lecture_hall][lecture][1] - 1] + 1
    for day in list_:
        for count in day:
            if count > coursesPerDay:
                cost = cost + (count - coursesPerDay)
    return cost, list_


def class_frequency_error(chromosome):
    cost = 0
    list_ = np.zeros(courses, dtype=np.int)
    for i in chromosome:
        for j in i:
            for k in j:
                if k[1] != 0:
                    list_[k[1] - 1] = list_[k[1] - 1] + 1
    for i in list_:
        if i < minClassCount:
            cost = cost + (minClassCount - i)
        if i > maxClassCount:
            cost = cost + (i - maxClassCount)
    return cost, list_


def fitness_value(chromosome):
    return lecture_collisions_z_axis(chromosome) + class_frequency_error(chromosome)[0] + course_per_day_error(chromosome)[0]


def evaluation_function(population):
    temp = []
    for i in population:
        collisions = fitness_value(i)
        temp.append([collisions, i])
    temp.sort(key=lambda x: x[0])
    return [row[1] for row in temp[:10]]


def initialise_population():
    print("\nGenerating Initial Population")
    initial_population = []
    for count in range(100):
        timetable = []
        for day in range(5):
            tt = []
            for slot in range(8):
                t = []
                for j in range(lectureHalls):
                    t.append(combinations[gen_random(len(combinations)) - 1])
                tt.append(t)
            timetable.append(tt)
        initial_population.append(timetable)
    return np.array(initial_population)


def perform_crossover(p, q, shape):
    previous_crossover = -1
    val = gen_random(2)
    p1, p2 = 0, 0
    for i in range(val):
        cross_point = gen_random(lectureHalls) - 1

        if val == 2:
            if previous_crossover == cross_point:
                return p1, p2

        p1 = np.zeros(shape, dtype=np.int)
        p2 = np.zeros(shape, dtype=np.int)
        # print(shape, cross_point)

        p1[:, :, :cross_point] = q[:, :, :cross_point]
        p1[:, :, cross_point:] = p[:, :, cross_point:]

        p2[:, :, :cross_point] = p[:, :, :cross_point]
        p2[:, :, cross_point:] = q[:, :, cross_point:]
        previous_crossover = cross_point

    return p1, p2


def crossover(population):
    shape = population[0].shape
    print("Performing Crossover")
    new_population = copy.deepcopy(population)
    temp = copy.deepcopy(population)
    for p in range(len(temp)):
        for q in range(len(temp)):
            if p != q:
                p1, p2 = perform_crossover(temp[p], temp[q], shape)
                new_population.append(p1)
                new_population.append(p2)
    return new_population


def perform_mutate(chromosome):
    c = copy.deepcopy(chromosome)
    for p in range(random.choice([1, 1, 1, 1, 1, 2, 2])):
        mutate_axis = gen_random(3)
        if mutate_axis == 1:
            rand_hall = gen_random(lectureHalls)
            timetable = []
            for day in range(5):
                tt = []
                for slot in range(8):
                    tt.append(combinations[gen_random(len(combinations)) - 1])
                timetable.append(tt)
            c[:, :, rand_hall - 1, :] = timetable
        if mutate_axis == 2:
            rand_day = gen_random(5)
            timetable = []
            for day in range(8):
                tt = []
                for slot in range(lectureHalls):
                    tt.append(combinations[gen_random(len(combinations)) - 1])
                timetable.append(tt)
            c[rand_day - 1, :, :, :] = timetable
        if mutate_axis == 3:
            rand_slot = gen_random(8)
            timetable = []
            for day in range(5):
                tt = []
                for slot in range(lectureHalls):
                    tt.append(combinations[gen_random(len(combinations)) - 1])
                timetable.append(tt)
            c[:, rand_slot - 1, :, :] = timetable
    return c


def mutate(population):
    print("Performing Mutation")
    new_temp_pop = []
    for chromosome in population:
        new_temp_pop.append(perform_mutate(chromosome))
    return new_temp_pop


def deep_clean(c):
    chromosome = copy.deepcopy(c)
    list_ = course_per_day_error(chromosome)[1]
    for day in range(len(list_)):
        for count in range(len(list_[day])):
            if list_[day][count] > coursesPerDay:
                for i in range(len(chromosome[day])):
                    for k in range(len(chromosome[day][i])):
                        if chromosome[day][i][k][1] == count + 1 and gen_random(6) % 2 == 0:
                            chromosome[day][i][k] = combinations[gen_random(len(combinations)) - 1]

    list_ = class_frequency_error(chromosome)[1]
    for l in range(len(list_)):
        if list_[l] > maxClassCount:
            for day in range(len(chromosome)):
                for i in range(len(chromosome[day])):
                    for k in range(len(chromosome[day][i])):
                        if chromosome[day][i][k][1] == l + 1 and gen_random(6) % 2 == 0:
                            chromosome[day][i][k] = combinations[gen_random(len(combinations)) - 1]

    return chromosome


def ma_local_search(p):
    print("Performing MA Local Search")
    shape = p[0].shape
    for i in range(int(np.array(p).shape[0] / 2)):
        p1, p2 = perform_crossover(p[2 * i], p[(2 * i) + 1], shape)
        if lecture_collisions_z_axis(p1) < lecture_collisions_z_axis(p[2 * i]):
            p[2 * i] = p1
        if lecture_collisions_z_axis(p2) < lecture_collisions_z_axis(p[(2 * i) + 1]):
            p[(2 * i) + 1] = p2

    # for i in range(np.array(p).shape[0]):
    #     p1 = perform_mutate(p[i])

    for i in range(np.array(p).shape[0]):
        p1 = deep_clean(p[i])
        if fitness_value(p1) < fitness_value(p[i]):
            p[i] = p1
    return p


def print_chromosome(chromosome):
    print_tt(chromosome)
    print("\nCourses per day Error:", course_per_day_error(chromosome)[0], "\n", course_per_day_error(chromosome)[1])
    print("Course Frequency Error:", class_frequency_error(chromosome)[0], "\n", class_frequency_error(chromosome)[1])
    print("Lecture Z-Axis Collisions:", lecture_collisions_z_axis(chromosome))
    print("Total Collisions:", fitness_value(chromosome), "Fitness:", 1 / (1 + fitness_value(chromosome)))


# courses = 20
# lectureHalls = 6
# professors = 20
# ma = "1"
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

ma = input("Enter 1 for MA anything else for GA\n")

courses_list = list(range(1, courses + 1))
courses_split_for_each_professor = np.array_split(courses_list, professors)

combinations = []

combinations.append([0, 0])
combinations.append([0, 0])

for professor_ in range(1, len(courses_split_for_each_professor) + 1):
    for course_ in courses_split_for_each_professor[professor_ - 1]:
        combinations.append([professor_, course_])

initialPopulation = initialise_population()

if ma == "1":
    initialPopulation = ma_local_search(initialPopulation)

bestPopulation = evaluation_function(initialPopulation)

bestChromosome = bestPopulation[0]
current_best_performing = fitness_value(bestChromosome)

dump = []
dump.append(current_best_performing)

print_chromosome(bestChromosome)

generation = 0

while fitness_value(bestChromosome) > 0:
    generation = generation + 1
    combinations.append([0, 0])
    print("\n-------------- Generation", generation, "--------------")
    print("Current Collision: ", current_best_performing, "Fitness:", 1 / (1 + current_best_performing))
    new_pop = crossover(bestPopulation)
    new_pop = mutate(new_pop)

    if ma == "1":
        new_pop = ma_local_search(new_pop)

    bestPopulation = evaluation_function(new_pop)
    bestChromosomeN = bestPopulation[0]

    generated_best_performing = fitness_value(bestChromosomeN)

    dump.append(generated_best_performing)

    if current_best_performing > generated_best_performing:
        bestChromosome = bestPopulation[0]
        current_best_performing = generated_best_performing
        print_chromosome(bestChromosome)

print("\nConverged in", generation, "generation", "\nTimetable")

print_chromosome(bestChromosome)
dump.append(fitness_value(bestChromosome))
plt.plot(dump)
plt.ylabel("Converged in " + str(generation) + " generations")
plt.title(
    "MA:" + ma + " MinClassCount: " + str(minClassCount) + " Max: " + str(maxClassCount) + " courses: " + str(courses) + " prof: " + str(professors) + " Halls: " + str(lectureHalls) + " course/day:" + str(
        coursesPerDay))
plt.show()
