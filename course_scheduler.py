import sys
from collections import namedtuple
import course_dictionary
from scheduler import Scheduler
import warnings; warnings.simplefilter('ignore')

def start_scheduling(descriptions, goals, init):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    prereqDict = {}
    finalPlan = {}
    planner = search(descriptions, goals, init, prereqDict)
    for key in planner:
        #print(key, planner[key])
        for course in planner[key][1]:
            # construct a named tuple
            courseInfo = descriptions[course]
            finalPlan[course] = CourseInfo(courseInfo.credits, key, prereqDict[course])

    for course in finalPlan:
        print(course, finalPlan[course])


    #return finalPlan


def search(dictionary, start, completed, prereqDict):
    semesters = [('Freshman', 'Fall'), ('Freshman', 'Spring'), ('Sophomore', 'Fall'),
                ('Sophomore', 'Spring'), ('Junior', 'Fall'), ('Junior', 'Spring'),
                ('Senior', 'Fall'), ('Senior', 'Spring')]
    planner = {semester: [0,[]] for semester in semesters}
    stack = start
    while stack:
        #if (planner[semesters[7]][0] )
        course = stack.pop()
        if course not in completed:
            courseInfo = dictionary[course]
            if courseInfo.credits is '0':
                if (is_class(courseInfo.prereqs)):
                    prereqs = find_first_prereq(courseInfo.prereqs, completed)
                    if len(prereqs) is not 0:
                        for prereq in prereqs:
                            if prereq not in completed:
                                stack.append(prereq)
                                completed.append(course)
                    else:
                        completed.append(course)
                else:
                    if is_satisfied(courseInfo.prereqs, completed):
                        completed.append(course)
                    else:
                        stack.append(course)
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        push(stack, prereqs, completed)
            else:
                if len(courseInfo.prereqs) is 0:
                    prereqDict[course] = []
                    completed.append(course)
                    schedule(course, courseInfo, [], semesters, planner)
                else:
                    prereqs = is_satisfied(courseInfo.prereqs, completed)
                    if prereqs is not False:
                        prereqDict[course] = prereqs
                        completed.append(course)
                        schedule(course, courseInfo, prereqs, semesters, planner)
                    else:
                        stack.append(course)
                        prereqs = find_most_satisfied_ands(courseInfo.prereqs, completed)
                        prereqDict[course] = prereqs
                        push(stack, prereqs, completed)
    return planner

def find_first_prereq(prereqs, completed):
     for ors in prereqs:
         for ands in ors:
             if ands not in completed:
                 return ors
     return []

def is_class(prereqs):
    if all(len(ors) is 1 for ors in prereqs):
        return True
    return False

def push(stack, prereqs, completed):
    tmpstack = []
    for prereq in prereqs:
        if prereq not in completed:
            tmpstack.append(prereq)
    while tmpstack:
        stack.append(tmpstack.pop())

def check_hours(course, courseInfo, semester, semesters, planner):
    if (planner[semesters[semester]][0] + int(courseInfo.credits)) <= 18:
        return True
    print('check hours failed for course: ', course, ' for semester:', semester)
    return False

def check_offered(course, courseInfo, semester, semesters, planner):
    if semesters[semester][1] in courseInfo.terms:
        return True
    print('check offered failed for course: ', course, ' for semester: ', semester)
    return False

def schedule(course, courseInfo, prereqs, semesters, planner):
    first = -1

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
    # if we reach here then we know the course was unable to be scheduled

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
    for ors in prereqs:
        if all(ands in completed for ands in ors):
            return ors
    return False

def main(argv):
    test = course_dictionary.create_course_dict()
    Course = namedtuple('Course', 'program, designation')
    goals = [('CS', 'major')]
    init_state = []
    start_scheduling(test, goals, init_state)

    print('Done')

if __name__ == "__main__":
    main(sys.argv)
