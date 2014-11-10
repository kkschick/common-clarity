import model
import csv
from datetime import datetime

name = "Class 1 Interim"
date = datetime(2014, 01, 30)

def load_test_file(session, name, date):

    with open('seed_data/test_class1_interim.csv', 'rb') as f:

        test = model.Test(name=name, date=date)
        session.add(test)
        session.commit()

        reader = csv.reader(f, delimiter=',')

        headers = reader.next()
        students = headers[1:-5]

        standards = []
        scores = []
        for fields in reader:
            standard = fields[0].split(" ")
            standards.append(standard[0])
            scores.append(fields[1:-5])

        standard_ids = []
        for standard in standards:
            standard_id = (model.Standard.query.filter_by(code=standard).first()).id
            standard_ids.append(standard_id)

        student_ids = []
        for student in students:
            student = student.split(",")
            last_name = student[0].strip()
            first_name = student[1].strip()
            student_id = (model.User.query.filter_by(last_name=last_name, first_name=first_name).first()).id
            student_ids.append(student_id)

        test_id = (model.Test.query.filter_by(name=name).first()).id

        i = 0
        for student in student_ids:
            j = 0
            for i in range(len(standard_ids)):
                standard = standard_ids[j]
                score = scores[i][j]
                j += 1
                score = model.Score(student_id=student, test_id=test_id, standard_id=standard, score=score)
                session.add(score)
            i += 1

        session.commit()

def main(session):
    load_test_file(session, name, date)

if __name__ == "__main__":
    main(model.session)

# Create new test in tests table and get test_id
# Match CCSS with standards table and get standard_ids (put into a list?)
# Go through each student and match with users table and get ID
# Add each score using the student and CCSS and test_id