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
        dfs_i(descriptions, goal, init, scheduler)

def find_first_prereq(prereqs, completed):
    # will return first prereq that is unsatisfied
    # if all prereqs are satisfied will return []
     for prereq in prereqs:
         for option in prereq:
             if option not in completed:
                 return prereq
     return []


# def search(dictionary, start, discovered, scheduler):

def dfs_i(dictionary, start, discovered, scheduler):
    stack = [start]
    while stack:
        course = stack.pop()
        print(course)
        if course not in discovered:
            # get info
            courseInfo = dictionary[course]
            # check in terms
            discovered.append(course)
            #if its a course add it to the planner
            #if courseInfo.credits is not '0':
            if len(courseInfo.prereqs) is not 0:
                stack.append(course)
                tmpStack = []
                for prereq in find_first_prereq(courseInfo.prereqs):
                    if prereq not in discovered:
                        tmpStack.append(prereq)
                if len(tmpStack) is 0:
                    scheduler.addCourse(scheduler.currentSemester, course, courseInfo)
                else:
                    while tmpStack:
                        stack.append(tmpStack.pop())
    for key in scheduler.planner:
        print(key, scheduler.planner[key])

def main(argv):
    test = course_dictionary.create_course_dict()


    Course = namedtuple('Course', 'program, designation')

    goals = [Course('CS', 'major')]
    # print(test[Course('CS', 'major')])
    init_state = []
    #scheduler_test(test)
    course_dictionary.print_dict(test)
    #schedule(test, goals, init_state)
    test_prereqs(test)
    print(test[Course('CS', 'calculus')].prereqs)

    print('Done')

if __name__ == "__main__":
    main(sys.argv)
