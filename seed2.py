import model
import csv
from datetime import datetime

name = "Class 2 Predictive"
date = datetime.strptime("2013-10-30", "%Y-%m-%d")

def load_test_file(session, name, date):

    with open('seed_data/test_class2_predictive.csv', 'rb') as f:

        test = model.Test(name=name, test_date=date)
        session.add(test)
        session.commit()

        reader = csv.reader(f, delimiter=',')

        headers = reader.next()
        students = headers[1:-5]

        standards = []
        scores = []
        for rows in reader:
            standards.append(rows[0])
            scores.append(rows[1:-5])

        standard_ids = []
        for standard in standards:
            standard_split = standard.split(" ")
            standard_code = standard_split[0]
            standard = model.Standard.query.filter_by(code=standard_code).first()
            if standard == None:
                categories = {'RF': 'Foundational Skills',
                              'RI': 'Informational Text',
                              'L': 'Language',
                              'RL': 'Literature',
                              'SL': 'Speaking and Listening',
                              'W': 'Writing'}
                cat_code = (standard_code.split("."))[0]
                description = ' '.join(standard_split[1:])
                stan = model.Standard(category=categories[cat_code], code=standard_code, description=description)
                session.add(stan)
                session.commit()
                standard = model.Standard.query.filter_by(code=standard_code).first()
                standard_id = standard.id
                standard_ids.append(standard_id)
            standard_id = standard.id
            standard_ids.append(standard_id)

        student_ids = []
        for student in students:
            student = student.split(",")
            last_name = student[0].strip()
            first_name = student[1].strip()
            student_id = (model.User.query.filter_by(last_name=last_name, first_name=first_name).first()).id
            student_ids.append(student_id)

        test_id = (model.Test.query.filter_by(name=name).first()).id

        j = 0
        for student in student_ids:
            i = 0
            for standard in standard_ids:
                score = scores[i][j]
                new_score = model.Score(student_id=student, test_id=test_id, standard_id=standard, score=score)
                session.add(new_score)
                i += 1
            j += 1

        session.commit()

def main(session):
    load_test_file(session, name, date)

if __name__ == "__main__":
    main(model.session)

# Create new test in tests table and get test_id
# Match CCSS with standards table and get standard_ids (put into a list?)
# Go through each student and match with users table and get ID
# Add each score using the student and CCSS and test_id