import model
import csv
from datetime import datetime

# These are hard-coded for now but will be passed in by the user in a form
name = "Class 1 Predictive"
date = datetime.strptime("2013-10-30", "%Y-%m-%d")
cohort_id = 1

def load_test_file(session, name, date, cohort_id):

    # Open file
    with open('seed_data/test_class1_predictive.csv', 'rb') as f:

        # Create new test in tests database
        test = model.Test(name=name, test_date=date, cohort_id=cohort_id)
        session.add(test)
        # session.commit()

        reader = csv.reader(f, delimiter=',')

        # Create list with the headers and filter it to be just student names
        headers = reader.next()
        students = headers[1:-2]
        norms = headers[-2:]

        # Read through the rest of the file and add the standards and scores to lists
        standards = []
        scores = []
        norm_scores = []
        for rows in reader:
            standards.append(rows[0])
            scores.append(rows[1:-2])
            norm_scores.append(rows[-2:])

        # Create list of standard IDs
        standard_ids = []
        for standard in standards:
            # Split standard on the space and only take the code
            standard_split = standard.split(" ")
            standard_code = standard_split[0]

            # Query the DB using the code to see if the standard exists
            standard = model.Standard.query.filter_by(code=standard_code).first()

            # If the standard doesn't exist, add it to the DB
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

                # Once it's added, get its ID and add to the standard IDs list
                standard = model.Standard.query.filter_by(code=standard_code).first()
                standard_id = standard.id
                standard_ids.append(standard_id)

            # If it already exists, get the ID and append it to the standard IDs list
            standard_id = standard.id
            standard_ids.append(standard_id)

        # Create list of student IDs
        student_ids = []
        for student in students:
            # Split student on the comma to get the first and last name
            student = student.split(",")
            last_name = student[0].strip()
            first_name = student[1].strip()

            # Query the DB matching on the first and last name
            student = model.User.query.filter_by(last_name=last_name, first_name=first_name).first()

            # If student doesn't exist, add student and get ID
            if student == None:
                student = model.User(user_type="student", first_name=first_name, last_name=last_name)
                session.add(student)
                session.commit()
                student.id = (model.User.query.filter_by(last_name=last_name, first_name=first_name).first()).id
            else:
                student_id = student.id

            # Add the ID to the student IDs list
            student_ids.append(student_id)

        # Get the ID of the test that was just created
        test_id = (model.Test.query.filter_by(name=name).first()).id

        # Iterate through the students, standards, and scores, and add the scores to the DB
        j = 0
        for student in student_ids:
            i = 0
            for standard in standard_ids:
                score = scores[i][j]
                new_score = model.Score(student_id=student, test_id=test_id, standard_id=standard, score=score)
                session.add(new_score)
                i += 1
            j += 1

        j = 0
        for item in norms:
            i = 0
            for standard in standard_ids:
                norm_score = norm_scores[i][j]
                new_norm_score = model.NormScore(cohort_name=item, test_id=test_id, standard_id=standard, score=float(norm_score))
                session.add(new_norm_score)
                i += 1
            j += 1

        session.commit()

def main(session):
    load_test_file(session, name, date, cohort_id)

if __name__ == "__main__":
    main(model.session)
