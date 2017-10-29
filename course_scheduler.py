# Breck Stodghill
# I worked with Max Montgomery and Cory Pitt on detailing the logic
# for this algorithm. We worked together in FGH for a few days
# to think through the psuedo code and the skeleton of the algorithm


import sys
import course_dictionary
from collections import namedtuple

# This method accepts a planner in the form of a dictionary
# And outputs each key:value pair to a file OUTPUT.txt
def output(planner):
    fout = "OUTPUT.txt"
    f = open(fout, "w")
    for key in planner:
        f.write(str(key) + ': ' + str(planner[key]) + "\n")
    f.close()

# This function initializes many of the variables for the DFS
# And formats the result of the search into a dictionary.
def course_scheduler(descriptions, goals, init):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    prereqDict = {}
    finalPlan = {}
    check = goals.copy()
    planner = search(descriptions, goals, init, prereqDict)
    for goal in check:
        if goal_fulfilled(goal, planner) is False:
            planner = {}

    for key in planner:
        for course in planner[key][1]:
            courseInfo = descriptions[course]
            finalPlan[Course(course[0], course[1])] = CourseInfo(courseInfo.credits, key, prereqDict[course])

    output(finalPlan)
    return finalPlan

# Accepts a goal and a planner
# Returns true if the goal is satisfied in the planner
# Returns false if the goal is not satisfied in the planner
def goal_fulfilled(goal, planner):
    for semester in planner:
        if goal in planner[semester][1]:
            return True
    return False

# Searches the planner for any semesters with courses sheduled but hours < 12
# Will go through the dictionary of courses to find a course that has not already
# Been taken and can be added to the schedule. Does this until each semester has
# At least 12 hours
def fill_dict(dictionary, completed, prereqDict, planner):
    for semester in planner:
        if (planner[semester][0] is not 0):
            while planner[semester][0] < 12:
                course = find_next_course(dictionary, completed, semester[0])
                toAdd = (course.program, course.designation)
                completed.append(course)
                courseInfo = dictionary[course]
                planner[semester][0] += int(courseInfo.credits)
                planner[semester][1].append(toAdd)
                prereqDict[toAdd] = []

# Returns the next course in the dictionary to be taken that has no prereqs
def find_next_course(dictionary, completed, semester):
    for course in dictionary:
        courseInfo = dictionary[course]
        if course not in completed and semester in courseInfo.terms and len(courseInfo.prereqs) is 0:
            return course

# This executes a depth first search to schedule courses
def search(dictionary, start, completed, prereqDict):
    # initialize a list of tuples that represent possibl semesters
    semesters = [('Fall', 'Frosh'), ('Spring', 'Frosh'), ('Fall', 'Sophomore'),
                ('Spring', 'Sophomore'), ('Fall', 'Junior'), ('Spring', 'Junior'),
                ('Fall', 'Senior'), ('Spring', 'Senior')]
    # initialize a dictionary to keep track of semester hours and courses being taken
    planner = {semester: [0,[]] for semester in semesters}
    # initialize a stack with the goals as the initial values
    stack = start
    while stack:
        course = stack.pop()
        courseInfo = dictionary[course]
        if course not in completed:
            # course must be a higher level requirement
            if courseInfo.credits is '0':
                # check to see if higher level requirement only has single course options
                if (is_class(courseInfo.prereqs)):
                    prereqs = find_first_prereq(courseInfo.prereqs, completed)
                    # course is a higher level requirement with unsatisfied prereqs
                    if len(prereqs) is not 0:
                        for prereq in prereqs:
                            if prereq not in completed:
                                stack.append(prereq)
                                planner[semesters[7]][1].append(course)
                                prereqDict[course] = prereqs
                                completed.append(course)
                    else:
                        # course is a higher level requirement with satisfied prereqs
                        completed.append(course)
                        planner[semesters[7]][1].append(course)
                        prereqDict[course] = prereqs
                else:
                    prereqs = is_satisfied(courseInfo.prereqs, completed)
                    # course is a higher level requirement with satisfied prereqs
                    if prereqs is not False:
                        completed.append(course)
                        planner[semesters[7]][1].append(course)
                        prereqDict[course] = prereqs
                    else:
                        # course is a higher level requirement with unsatisfied prereqs
                        # find the se tof prereqs that have the most satisfied courses in it
                        # so add it back to the stack and each of its unsatisfied prereqs
                        stack.append(course)
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        push(stack, prereqs, completed)
            else:
                # course is a single course with no prereqs so schedule it.
                if len(courseInfo.prereqs) is 0:
                    prereqDict[course] = []
                    schedule(course, courseInfo, [], semesters, planner)

                    completed.append(course)
                else:
                    prereqs = is_satisfied(courseInfo.prereqs, completed)
                    if prereqs is not False:
                        # course is a single course with satisfied prereqs so schedule it
                        prereqDict[course] = prereqs
                        schedule(course, courseInfo, prereqs, semesters, planner)
                        completed.append(course)
                    else:
                        # course is a single course with unsatisfied prereqs
                        # so add it back to the stack and each of its unsatisfied prereqs
                        stack.append(course)
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        prereqDict[course] = prereqs
                        push(stack, prereqs, completed)
    # once the stack is empty go through the planner and fill any semesters that have
    # courses scheduled.. but hours less than 12
    fill_dict(dictionary, completed, prereqDict, planner)
    return planner

# Finds the first unsatisfied prerequisite in the tuple prereqs and returns it
# If all prereqs are satisfied then returns an empty list
def find_first_prereq(prereqs, completed):
     for ors in prereqs:
         for ands in ors:
             if ands not in completed:
                 return ors
     return []

# Returns true if prereqs only has single class options
# I.E. if each or'd set of prereqs has a length of 1
def is_class(prereqs):
    if all(len(ors) is 1 for ors in prereqs):
        return True
    return False

# uses a temporary stack to push prereqs onto the stack of courses in the DFS
def push(stack, prereqs, completed):
    tmpstack = []
    for prereq in prereqs:
        if prereq not in completed:
            tmpstack.append(prereq)
    while tmpstack:
        stack.append(tmpstack.pop())

# checks to see if it is allowable for the scheduler to schedule a class
# during the given semester. Only checks to see if current hours + course.credits
# <= 18. Returns true if true, false if not.
def check_hours(course, courseInfo, semester, semesters, planner):
    if (planner[semesters[semester]][0] + int(courseInfo.credits)) <= 18:
        return True
    return False

# checks to see if a given class is offered during the semester that the scheduler
# is currently trying to schedule it during. Returns true if true, false if not.
def check_offered(course, courseInfo, semester, semesters, planner):
    if semesters[semester][0] in courseInfo.terms:
        return True
    return False

# given a course, its info, prereqs, and the list of semesters and the planner
# this function will find the first available semester to take the course based
# on where its prereqs have been scheduled, then it will try to find the first semester
# that offers the course and is not already full.
def schedule(course, courseInfo, prereqs, semesters, planner):
    first = -1
    #print(course, "scheduled")
    for x in range(8):
        for prereq in prereqs:
            if prereq in planner[semesters[x]][1]:
                first = x
    for y in range((first+1), 8):
        if (check_offered(course, courseInfo, y, semesters, planner)):
            if (check_hours(course, courseInfo, y, semesters, planner)):
                planner[semesters[y]][0] += int(courseInfo.credits)
                planner[semesters[y]][1].append(course)
                return

# this function finds the set of prerequisites in prereqs that is most satisfied
# this is the heuristic that my function uses to choose the set of prereqs to add to the
# DFS path
def find_most_satisfied_ands(prereqs, completed):
    rv = []
    max_ands = -1
    for ors in prereqs:
        ands = find_ands(ors, completed)
        if ands > max_ands:
            rv = ors
            max_ands = ands
    return rv

# this function counts the number of completed prereqs in a conjunction of prereqs
def find_ands(ors, completed):
    count = 0
    for ands in ors:
        if ands in completed:
            count += 1
    return count

# Checks to see if a list of prerequisites has a satisfied listing
def is_satisfied(prereqs, completed):
    for ors in prereqs:
        if all(ands in completed for ands in ors):
            return ors
    return False

def main(argv):
    test = course_dictionary.create_course_dict()
    Course = namedtuple('Course', 'program, designation')
    #goals = [('CS', '2231'), ('CS', '3251'), ('CS', 'statsprobability')]
    #init_state = [('MATH', '2810'), ('MATH', '2820'), ('MATH', '3640')]
    #goals = [('CS', 'core'), ('CS', '1101')]
    #goals = [('CS', 'major'), ('ANTH', '4345'), ('ARTS', '3600'), ('ASTR', '3600'), ('BME', '4500'), ('BUS', '2300'), ('CE', '3705'), ('LAT', '3140'),
    #('JAPN', '3891')]
    #goals = [('CS', 'major'), ('JAPN', '3891')]
    #goals = [('CS', 'major')]
    #init_state = [('CS', '1101')]
    #init_state = []
    goals = [('CS', '1101')]
    init_state = []
    plan = course_scheduler(test, goals, init_state)
    for key in plan:
        print(key, plan[key])

    print('Done')

if __name__ == "__main__":
    main(sys.argv)
