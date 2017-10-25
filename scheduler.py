class Scheduler:
    def __init__(self, totalHours = 0, currentSemester = 0, semesters = None, planner = None):
        self.totalHours = totalHours
        self.currentSemester = currentSemester
        self.semesters = semesters if semesters is not None else [('Frosh', 'Fall'), ('Frosh', 'Spring'), ('Soph', 'Fall'),
                    ('Soph', 'Spring'), ('Jun', 'Fall'), ('Jun', 'Spring'),
                    ('Sen', 'Fall'), ('Sen', 'Spring')]
        self.planner = planner if planner is not None else {semester: [0,[]] for semester in self.semesters}

    def get_current_semester(self):
        return self.semesters[self.currentSemester]

    def addCourse (self, semester, course, courseInfo):
        if (self.tryCourse(semester, int(courseInfo.credits))):
            self.totalHours += int(courseInfo.credits)
            self.planner[semester][0] += int(courseInfo.credits)
            self.planner[semester][1].append(course)
            return True
        else:
            self.currentSemester += 1
            return False

    def tryCourse (self, semester, credits):
        if (self.planner[semester][0] + credits <= 18) and (self.totalHours <= 120):
            return True
        return False
