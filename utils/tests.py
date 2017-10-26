import course_scheduler


def scheduler_test(descriptions):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    scheduler = Scheduler()
    currentSemester = scheduler.get_current_semester()
    courses = [Course('CS', '1101'), Course('ECON', '1010'), Course('CHEM', '1010'), Course('ENGL', '1100'), Course('ENGL', '2200')]
    for course in courses:
        courseInfo = descriptions[course]
        scheduler.schedule_course(currentSemester, course, courseInfo)

    course2 = Course('CS', '2201')
    courseInfo2 = descriptions[course2]
    scheduler.find_term(course2, courseInfo2, courseInfo.prereqs)

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

def test_most_satisfied_mans(dictionary):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    courseInfo = dictionary[Course('CS', '3259')]
    completed = [Course('MATH', '2400')]
    print(courseInfo.prereqs)
    print(find_most_satisfied_ands(courseInfo.prereqs, completed))

def test_is_class(dictionary):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    courseInfo = dictionary[Course('CS', 'depthothera')]
    print(courseInfo.prereqs)
    print(is_class(courseInfo.prereqs))
