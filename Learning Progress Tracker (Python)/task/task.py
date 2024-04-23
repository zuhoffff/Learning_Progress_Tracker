from typing import List
import math
#TODO: notifications for stu
# if a student has accomplished a course it should be somehow marked
#ways to do so:
#parse students when notify command is entered
#  OR check at the stage of adding points whether some student has finished the course...
#!also the notification can't be sent twice so after first sending student shd b marked

class Tracker:
    def __init__(self):
        self.__students: List[Tracker.Student()] = []
        # course_names = ['Python', 'DSA', 'Databases', 'Flask']
        self.__courseStats = [
            {'Coursename': 'Python', 'Enrolled': 0, 'Tasks': 0, 'Score': 0},
            {'Coursename': 'DSA', 'Enrolled': 0, 'Tasks': 0, 'Score': 0},
            {'Coursename': 'Databases', 'Enrolled': 0, 'Tasks': 0, 'Score': 0},
            {'Coursename': 'Flask', 'Enrolled': 0, 'Tasks': 0, 'Score': 0}
        ]

    class Student:  #rewrite into dictionary (as below)
        def __init__(self):
            self.progress = {'Python':0,'DSA':0,'Databases':0,'Flask':0}
            self.completion = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
            self.course_gap = {'Python': 600, 'DSA': 400, 'Databases': 480, 'Flask': 550}
            self.name = ''
            self.surname = ''
            self.ID = ''

        # self.__students = [
        #     {
        #      'progress': {'Python':0,'DSA':0,'Databases':0,'Flask':0},
        #      'Name':'',
        #      'Surname':'',
        #      'ID':'',
        #      'completed': {'Python':False,'DSA':False,'Databases':False,'Flask':False},
        #      }
        # ]

    def mainLoop(self):
        print("Learning Progress Tracker")
        while True:
            m_input = input()
            match m_input:
                case _ if not m_input.strip():
                    print("No input")
                case "exit":
                    print("Bye!")
                    break
                case "add students":
                    print("Enter student credentials or 'back' to return")
                    amount = 0
                    while True:
                        m_input = input()
                        match m_input:
                            case "back":
                                print(f"Total {amount} students have been added.")
                                break
                            case _:
                                amount += self.credCheck(m_input,
                                                         self.__students)  #implement dependency injection here?
                case "add points":
                    print("Enter an id and points or 'back' to return.")
                    self.addPointsAndStats()
                case "list":
                    if len(self.__students):
                        print("Students:")
                        self.listStudents()
                    else:
                        print("No students found.")
                case "find":
                    print("Enter an id or \'back\' to return.")
                    self.findStudents()
                case "statistics":
                    self.getStatistics()
                    self.getTopLearners()
                case "notify":
                    self.getCompleted()
                case "back":
                    print("Enter 'exit' to exit the program")
                case _:
                    print("Error: unknown command")

    def getCompleted(self):
        #if the same students finished multiple cources it count as one notification
        counter = 0
        notes = []
        for student in self.__students:
            for course_completion in student.completion:
                if student.completion[course_completion] == 1:
                    counter += 0.25
                    # form message
                    note = 'To: '+student.email+'\n'+'Re: '+'Your Learning Progress\n'+\
                    'Hello, '+student.name+' '+student.surname+\
                    f'! You have accomplished our {course_completion} course!'
                    student.completion[course_completion] = 2 # 2 means: already notified
                    notes.append(note)
            counter = math.ceil(counter)
        for note in notes:
            print(note)
        print(f'Total {counter} students have been notified')

    def handleOverlap(self, max, min):
        # compare each2each
        for x1 in max:
            for x2 in min:
                if x1 == x2:
                    min.remove(x2)  # remove all list2 elements that are also in list1
        if not min:
            return ['n/a']
        else:
            return map(lambda course: self.__courseStats[course]['Coursename'], min)

    def getStatistics(self):
        print("Type the name of a course to see details or 'back' to quit")

        # этот пиздец можно спасти только функционалкой наверное #(TODO) завезти функционалку

        enrolled = [course['Enrolled'] for course in self.__courseStats[:4]]
        if enrolled == [0] * 4:
            print("Most popular: n/a")
            print("Least popular: n/a")
        else:
            enrolled_indices_max = [i for i, element in enumerate(enrolled) if element == max(enrolled)]
            enrolled_indices_min = [i for i, element in enumerate(enrolled) if element == min(enrolled)]
            # enrolled_indices can not overlap -> so we can erase overlapping one either from BOTH or from ONE list
            enrolled_indices_min = self.handleOverlap(enrolled_indices_max, enrolled_indices_min)
            print("Most popular: ", end='')
            print(*map(lambda course: self.__courseStats[course]['Coursename'], enrolled_indices_max), sep=', ')
            print("Least popular: ", end='')
            print(*enrolled_indices_min, sep=', ')

        tasks = [course['Enrolled'] for course in self.__courseStats[:4]]
        if tasks == [0] * 4:
            print("Highest activity: n/a")
            print("Lowest activity: n/a")
        else:
            tasks_indices_max = [i for i, element in enumerate(tasks) if element == max(tasks)]
            tasks_indices_min = [i for i, element in enumerate(tasks) if element == min(tasks)]
            tasks_indices_min = self.handleOverlap(tasks_indices_max, tasks_indices_min)
            print("Highest activity: ", end='')
            print(*map(lambda course: self.__courseStats[course]['Coursename'], tasks_indices_max), sep=', ')
            print("Lowest activity: ", end='')
            print(*tasks_indices_min, sep=', ')

        score = [course['Score'] for course in self.__courseStats[:4]]
        if score == [0] * 4:
            print("Easiest course: n/a")
            print("Hardest course: n/a")
        else:
            complexity = []
            for i in range(4):
                if tasks[i] != 0:
                    complexity.append(score[i] / tasks[i])
                else:
                    print("Easiest course: n/a")
                    print("Hardest course: n/a")
                    return
            complexity_indices_max = [i for i, element in enumerate(complexity) if element == max(complexity)]
            complexity_indices_min = [i for i, element in enumerate(complexity) if element == min(complexity)]
            complexity_indices_min = self.handleOverlap(complexity_indices_max, complexity_indices_min)
            print("Easiest course: ", end='')
            print(*map(lambda course: self.__courseStats[course]['Coursename'], complexity_indices_max), sep=', ')
            print("Hardest course: ", end='')
            print(*complexity_indices_min, sep=', ')

    def chartTopLearners(self, courseName):#access to self.__students
        top_learners = sorted(self.__students, key=lambda course: course.progress[courseName], reverse=True)

        print(courseName)
        if not top_learners:
            print('id	points	completed')
            return
        course_gap = {'Python':600,'DSA':400,'Databases':480,'Flask':550}
        max_id_len = max(len(str(learner.ID)) for learner in top_learners)
        max_score_len = max(len(str(learner.progress[courseName])) for learner in top_learners)

        adjust_id = max(len('id'), max_id_len) + 1
        print('id'.ljust(adjust_id), end='')
        adjust_score = max(len('points'), max_score_len) + 1
        print('points'.ljust(adjust_score), end='')
        adjust_comp = len('completed') + 1
        print('completed'.ljust(adjust_comp))
        for learner in top_learners:
            learner.completion = (lambda course: learner.progress[course] * 100 / course_gap[course])(courseName)
            print(str(learner.ID).ljust(adjust_id) +
                  str(learner.progress[courseName]).ljust(adjust_score) +
                  str('%.1f' % learner.completion + '%').
                  ljust(adjust_comp)
                  )

    def getTopLearners(self):
        while True:
            m_input = input()
            m_input  = m_input.lower()
            match m_input:
                case "python":
                    self.chartTopLearners('Python')
                case "dsa":
                    self.chartTopLearners('DSA')
                case "databases":
                    self.chartTopLearners('Databases')
                case "flask":
                    self.chartTopLearners('Flask')
                case "back":
                    return
                case _:
                    print('Unknown course.')

    def findStudents(self):
        while True:
            m_input = input()
            studentIndex = self.checkID(m_input)
            if m_input == 'back':
                return
            elif studentIndex < 0:
                print(f"No student is found for id={m_input}")
            else:
                print(f"{self.__students[studentIndex].ID} points: ", end='')
                print("Python={}; DSA={}; Databases={}; Flask={}".format(
                    *(self.__students[studentIndex].progress.values())))

    def addPointsAndStats(self):#access to self.__courseStats and self.__students
        while True:
            m_input = input()
            if m_input == 'back':
                return
            m_input = self.breakdown(m_input)
            ID = m_input[0]
            points = m_input[1:]
            studentIndex = self.checkID(ID)
            if studentIndex < 0:
                print(f"No student is found for id={ID}")
            elif not self.checkPoints(points):
                print("Incorrect points format.")
            else:
                for i, course in enumerate(self.__courseStats): #courseStats contain name of each course
                    if int(points[i]) != 0:
                        course['Tasks'] += 1
                        course['Score'] += int(points[i])
                        #check if its a new student
                        if self.__students[studentIndex].progress[course['Coursename']] == 0:
                            course['Enrolled'] += 1
                        #add points to student
                        self.__students[studentIndex].progress[course['Coursename']] \
                            += int(points[i])
                        #check completion trigger factor
                        if self.__students[studentIndex].progress[course['Coursename']]\
                                == self.__students[studentIndex].course_gap[course['Coursename']]:
                            self.__students[studentIndex].completion[course['Coursename']] = 1
                print("Points updated.")

    def checkID(self, ID: int) -> int:#access to self.__students
        for counter, student in enumerate(self.__students):
            if str(student.ID) == str(ID):
                return counter
        return -1

    def checkPoints(self, points):
        if len(points) != 4:
            return False

        for point in points:
            if not point.isdigit():
                return False
            if int(point) < 0:
                return False
        return True

    def listStudents(self):#access to self.__students
        for student in self.__students:
            print(student.ID)

    def isEnglishAlpha(self, char):
        ascii_value = ord(char)
        return (65 <= ascii_value <= 90) or (97 <= ascii_value <= 122)

    def isEnglishName(self, word):
        if len(word) < 2:
            return False
        if not self.isEnglishAlpha(word[0]):
            return False
        if not self.isEnglishAlpha(word[-1]):
            return False
        for i in range(1, len(word) - 1):
            if not (self.isEnglishAlpha(word[i])):
                if (word[i] == '\'' or word[i] == '-'):
                    if (word[i - 1] == '\'' or word[i - 1] == '-'):
                        return False
                else:
                    return False
        return True

    def isMail(self, word):
        if word.count('@') == 1:
            separator = word.find('@')
            if 0 < separator < len(word) - 1:
                if word[separator + 1:-1].find('.') > 0:
                    return True
        return False

    def breakdown(self, string):
        clean_string = string.split(' ')
        space = ' '
        empty = ''
        while space in clean_string:
            clean_string.remove(space)

        while empty in clean_string:
            clean_string.remove(empty)

        return clean_string

    def credCheck(self, credentials, students):#access to self.__student class
        words = self.breakdown(credentials)
        student = self.Student()
        if len(students) == 0:
            student.ID = 1  #id seed
        else:
            student.ID = students[-1].ID + 1

        if len(words) < 3:
            print("Incorrect credentials.")
            return 0
        if self.isEnglishName(words[0]):
            student.name = words[0]
        else:
            print("Incorrect first name")
            return 0

        for word in words[1:-1]:
            if self.isEnglishName(word):
                if student.surname:
                    student.surname+=' '
                student.surname+=word
            else:
                print("Incorrect last name")
                return 0

        if self.isMail(words[-1]):
            student.email = words[-1]
        else:
            print("Incorrect email")
            return 0

        if not self.checkIfNew(words[-1]):
            print("This email is already taken.")
            return 0

        print("The student has been added")
        students.append(student)
        return 1

    def checkIfNew(self, email) -> bool: #access to self.__students
        for student in self.__students:
            if student.email == email:
                return False
        return True

def main():
    studentTracker = Tracker()
    studentTracker.mainLoop()


if __name__ == '__main__':
    main()