import sys
from collections import namedtuple
import course_dictionary
from scheduler import Scheduler
import warnings; warnings.simplefilter('ignore')

def scheduler_test(descriptions):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    scheduler = Scheduler()
    currentSemester = scheduler.get_current_semester()
    print(currentSemester)
    course = Course('CS', '1101')
    course2 = Course('CS', '2201')
    courseInfo = descriptions[course]
    courseInfo2 = descriptions[course2]
    scheduler.addCourse(currentSemester, course, courseInfo)
    scheduler.addCourse(currentSemester, course2, courseInfo2)
    for key in scheduler.planner:
        print(key, scheduler.planner[key])

def test_prereqs(descriptions):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    course = Course('CS', '3259')
    course1 = Course('CS', 'mathelective')
    courseInfo = descriptions[course]
    courseInfo1 = descriptions[course1]
    completed = [Course('CS', '2201'), Course('MATH', '2410')]
    completed1 = [Course('MATH', '2420')]
    prereq = find_first_prereq(courseInfo.prereqs, completed)
    prereq1 = find_first_prereq(courseInfo1.prereqs, completed1)
    print(course, courseInfo)
    print(course1, courseInfo1)
    print(prereq)
    print(prereq1)


def schedule(descriptions, goals, init):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    # need to define an operator in terms of courseName and courseInfo
    #semesters = [('Freshman', 'Fall'), ('Freshman', 'Spring'), ('Sophomore', 'Fall'),
    #            ('Sophomore', 'Spring'), ('Junior', 'Fall'), ('Junior', 'Spring'),
    #            ('Senior', 'Fall'), ('Senior', 'Spring')]
    #planner = {semester: [0,[]] for semester in semesters}

    scheduler = Scheduler()
    for goal in goals:
        print(goal)
        #dfs_i(descriptions, goal, init, scheduler)
        search(descriptions, goal, init, scheduler)

def find_first_prereq(prereqs, completed):
    # will return first prereq that is unsatisfied
    # if all prereqs are satisfied will return []
     for ors in prereqs:
         for ands in ors:
             if ands not in completed:
                 return ors
     return []

# check to see if the higher level req is a class
def is_class(prereqs):
    if all(len(ors) is 1 for ors in prereqs):
        return True
    return False

def test_is_class(dictionary):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    courseInfo = dictionary[Course('CS', 'depthothera')]
    print(courseInfo.prereqs)
    print(is_class(courseInfo.prereqs))

def search(dictionary, start, completed, scheduler):
    stack = [start]
    while stack:
        course = stack.pop()
        if course not in completed:
            courseInfo = dictionary[course]
            if courseInfo.credits is '0':
                # higher level requirement
                if (is_class(courseInfo.prereqs)):
                    prereqs = find_first_prereq(courseInfo.prereqs, completed)
                    if len(prereqs) is not 0:
                        # this should be size 1 so add prereq to completed and add higher level
                        for prereq in prereqs:
                            if prereq not in completed:
                                print(prereq, '  scheduled')
                                completed.append(prereq)
                                print(course, '  scheduled')
                                completed.append(course)

                    else:
                        completed.append(course)
                        print('This course is already satisfied')
                else:
                    # if not then look for an or where all ands are satisfied
                    # if thats not true then look for the most satisfied or and choose it
                    if is_satisfied(courseInfo.prereqs, completed):
                        # schedule
                        completed.append(course)
                        print(course, '  scheduled')
                    else:
                        # add course to the stack
                        stack.append(course)
                        # find most satisified or
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        # add each course to stack
                        tmpstack = []
                        for prereq in prereqs:
                            if prereq not in completed:
                                tmpstack.append(prereq)
                        while tmpstack:
                            stack.append(tmpstack.pop())
            else:
                # Our course is a course
                if len(courseInfo.prereqs) is 0:
                    completed.append(course)
                    print(course, ' scheduled')
                else:
                    # check if one of the ors is satisfied
                    if is_satisfied(courseInfo.prereqs, completed):
                        # schedule
                        completed.append(course)
                        print(course, ' scheduled')
                    else:
                        # add course to the stack
                        stack.append(course)
                        # find most satisified or
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        # add each course to stack
                        tmpstack = []
                        for prereq in prereqs:
                            if prereq not in completed:
                                tmpstack.append(prereq)
                        while tmpstack:
                            stack.append(tmpstack.pop())

def test_most_satisfied_mans(dictionary):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    courseInfo = dictionary[Course('CS', '3259')]
    completed = [Course('MATH', '2400')]
    print(courseInfo.prereqs)
    print(find_most_satisfied_ands(courseInfo.prereqs, completed))

def find_most_satisfied_ands(prereqs, completed):
    rv = []
    max_ands = -1
    for ors in prereqs:
        ands = find_ands(ors, completed)
        if ands > max_ands:
            rv = ors
            max_ands = ands
    return rv

def find_ands(ors, completed):
    count = 0
    for ands in ors:
        if ands in completed:
            count += 1
    return count

# Checks to see if a list of prerequisites has a satisfied listing
def is_satisfied(prereqs, completed):
    # an or is satisfied id ever and is in completed
    for ors in prereqs:
        if all(ands in completed for ands in ors):
            return True
    return False

def main(argv):
    test = course_dictionary.create_course_dict()


    Course = namedtuple('Course', 'program, designation')

    goals = [Course('CS', 'major')]
    print(test[Course('CS', 'major')])
    print(test[Course('CS', '3259')])
    # print(test[Course('CS', 'major')])
    init_state = []
    #scheduler_test(test)
    #course_dictionary.print_dict(test)
    schedule(test, goals, init_state)
    #test_prereqs(test)
    #test_most_satisfied_mans(test)
    #print(test[Course('CS', 'calculus')].prereqs)
    #test_is_class(test)
    print('Done')

if __name__ == "__main__":
    main(sys.argv)
