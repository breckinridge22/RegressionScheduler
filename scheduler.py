from collections import namedtuple

class Scheduler:

    def __init__(self, totalHours = 0, semesters = None, planner = None):
        self.totalHours = totalHours
        self.semesters = semesters if semesters is not None else [('Freshman', 'Fall'), ('Freshman', 'Spring'), ('Sophomore', 'Fall'),
                    ('Sophomore', 'Spring'), ('Junior', 'Fall'), ('Junior', 'Spring'),
                    ('Senior', 'Fall'), ('Senior', 'Spring')]
        self.planner = planner if planner is not None else {semester: [0,[]] for semester in self.semesters}


    def check_hours(self, courseInfo, semester):
        if (self.planner[self.semesters[semester]][0] + int(courseInfo.credits)) <= 15:
            return True
        return False

    def check_offered(self, courseInfo, semester):
        if self.semesters[semester] in courseInfo.terms:
            return True
        return False

    def schedule_course(self, course, courseInfo, prereqs):
        first = -1
        print(first)

        for x in range(8):
            for prereq in prereqs:
                if prereq in self.planner[self.semesters[x]][1]:
                    first = x

        for y in range(first+1, 8):
            if (self.check_offered(courseInfo, y) and self.check_hours(courseInfo, y)):
                self.planner[self.semesters[y]][0] += int(courseInfo.credits)
                self.planner[self.semesters[y]][1].append(course)
                return
