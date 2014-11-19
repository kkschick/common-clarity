import model
from flask import session
import csv
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import desc

"""Log-in"""

def get_user(username, password):
    """Check if user exists; if exists, authenticate pw and return success msg"""

    user = model.User.query.filter_by(username=username).first()
    return user

"""Log-out"""

def logout():
    """Clear session to log user out of site."""

    model.session.clear()

"""Sign-up"""

def create_teacher_user(user_type, first_name, last_name, email, username, password):
    """Get form data and add new user to users table"""

    user = model.User(user_type=user_type, first_name=first_name, last_name=last_name, email=email, username=username, password=password)
    model.session.add(user)
    model.session.commit()


"""Settings"""

def get_teacher_cohorts(teacher_id):
    """Get teacher's cohorts and students in those cohorts from the db.
    Use teacher_id to get cohort_ids associated with that teacher and
    return them. If none, return False."""

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    return cohorts

def get_students_in_cohort(cohort_id):
    """Use cohort_ids associated with teacher_id to query studentcohorts
    to get student names for that cohort. If none, return False."""

    students = model.StudentCohort.query.filter_by(cohort_id=cohort_id).all()
    student_names = []
    for student in students:
        student_dict = {}
        student_dict["name"] = student.student.first_name + ' ' + student.student.last_name
        student_dict["id"] = student.student.id
        student_names.append(student_dict)
    return student_names

def edit_student_info(student_id, new_field_value):
    """Change student first_name, last_name, username, or password.
    Go into users table, find student using id, and update field with
    new value."""

    pass

def delete_student(student_id):
    """Delete student from users and studentcohorts tables using the id."""

    pass

def add_new_cohort(name, teacher_id):
    """Create new cohort in cohorts table. Return cohort_id."""

    cohort = model.Cohort(name=name, teacher_id=teacher_id)
    model.session.add(cohort)
    model.session.commit()
    new_cohort = model.Cohort.query.filter_by(name=name).first()
    return new_cohort.id

def create_student(user_type, first_name, last_name, username, password):
    """Create new student user in users table. Return cohort_id."""

    user = model.User(user_type=user_type, first_name=first_name, last_name=last_name, username=username, password=password)
    model.session.add(user)
    model.session.commit()
    new_user = model.User.query.filter_by(username=username).first()
    return new_user.id

def add_student_to_cohort(student_id, cohort_id):
    """Add newly-created student to studentcohorts table."""

    studentcohort = model.StudentCohort(student_id=student_id, cohort_id=cohort_id)
    model.session.add(studentcohort)
    model.session.commit()

def create_student_from_csv(csv_path, cohort_id, user_type):
    """Parse CSV of new students and add each to users table in database."""

    with open(csv_path, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        headers = reader.next()
        for row in reader:
            if row:
                user = model.User(user_type=user_type, first_name=row[0], last_name=row[1], username=row[2], password=row[3])
                model.session.add(user)
                model.session.commit()
                student_id = (model.User.query.filter_by(username=row[2]).first()).id
                studentcohort = model.StudentCohort(student_id=student_id, cohort_id=cohort_id)
                model.session.add(studentcohort)
                model.session.commit()


"""Reports"""

def parse_CSV(csv_path, name, date, cohort_id):
    """Take CSV file that was uploaded and parse it. Create new test in Tests table.
    Match student names to users table and match CCSS to the standards table and
    get user_id and standard_id. Use test_id returned from create_new_test, user_id,
    and standard_id, and add score to scores table."""

    date = datetime.strptime(date, "%Y-%m-%d")

    with open(csv_path, 'rb') as f:

    # Create new test in tests database
        test = model.Test(name=name, test_date=date, cohort_id=cohort_id)
        model.session.add(test)
        model.session.commit()

        reader = csv.reader(f, delimiter=',')

        # Create list with the headers and filter it to be just student names
        headers = reader.next()
        students = headers[1:-5]

        # Read through the rest of the file and add the standards and scores to lists
        standards = []
        scores = []
        for row in reader:
            standards.append(row[0])
            scores.append(row[1:-5])

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
                model.session.add(stan)
                model.session.commit()

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

            # Query the DB matching on the first and last name and return the ID
            student_id = (model.User.query.filter_by(last_name=last_name, first_name=first_name).first()).id

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
                model.session.add(new_score)
                i += 1
            j += 1

        model.session.commit()

def get_all_cohort_data_by_test(teacher_id):
    """Use teacher id to get all student scores by test and aggregate counts of
    M/A/FB by test."""

    # Get all teacher cohorts
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    # Make list of all tests associated with teacher's cohorts
    all_tests = []
    for cohort in cohorts:

        # Get all tests associated with that cohort id
        tests = model.Test.query.filter_by(cohort_id=cohort.id).all()

        for test in tests:
            all_tests.append(test)

    resp_list = []
    m_total = 0
    a_total = 0
    fb_total = 0

    total_dict = {"Name": "All Tests"}
    resp_list.append(total_dict)

    for test in all_tests:
        resp_dict = {}
        resp_dict["Name"] = test.name

        # Get all scores associated with each test id
        scores = model.Score.query.filter_by(test_id=test.id).all()

        m_count = 0
        a_count = 0
        fb_count = 0
        for score in scores:
            if score.score == 'M':
                m_count +=1
            elif score.score == 'A':
                a_count +=1
            elif score.score == 'FB':
                fb_count += 1

        m_total += m_count
        a_total += a_count
        fb_total += fb_count
        resp_dict["3"] = m_count
        resp_dict["2"] = a_count
        resp_dict["1"] = fb_count
        resp_list.append(resp_dict)

    total_dict["3"] = m_total
    total_dict["2"] = a_total
    total_dict["1"] = fb_total

    return resp_list

def get_one_cohort_data_by_test(cohort_id):
    """Use cohort id to get all student scores for that cohort by test and
    aggregate counts of M/A/FB by test."""

    # Get tests for that cohort
    tests = model.Test.query.filter_by(cohort_id=cohort_id).all()

    resp_list = []
    m_total = 0
    a_total = 0
    fb_total = 0

    total_dict = {"Name": "All Tests"}
    resp_list.append(total_dict)

    for test in tests:
        resp_dict = {}
        resp_dict["Name"] = test.name

        # Get all scores associated with each test id
        scores = model.Score.query.filter_by(test_id=test.id).all()

        m_count = 0
        a_count = 0
        fb_count = 0
        for score in scores:
            if score.score == 'M':
                m_count +=1
            elif score.score == 'A':
                a_count +=1
            elif score.score == 'FB':
                fb_count += 1

        m_total += m_count
        a_total += a_count
        fb_total += fb_count
        resp_dict["3"] = m_count
        resp_dict["2"] = a_count
        resp_dict["1"] = fb_count
        resp_list.append(resp_dict)

    total_dict["3"] = m_total
    total_dict["2"] = a_total
    total_dict["1"] = fb_total

    return resp_list

def get_one_student_data_by_test(student_id):

    cohorts = model.StudentCohort.query.filter_by(student_id=student_id).all()

    scores_list = []

    total_dict = {"Name": "All Tests"}
    scores_list.append(total_dict)
    m_total = 0
    a_total = 0
    fb_total = 0

    for cohort in cohorts:

        tests = model.Test.query.filter_by(cohort_id=cohort.cohort_id).all()
        for test in tests:
            scores_dict = {}
            scores_dict["Name"] = test.name
            scores = model.Score.query.filter_by(test_id=test.id, student_id=student_id).all()

            m_count = 0
            a_count = 0
            fb_count = 0
            for score in scores:
                if score.score == 'M':
                    m_count +=1
                elif score.score == 'A':
                    a_count +=1
                elif score.score == 'FB':
                    fb_count += 1

            m_total += m_count
            a_total += a_count
            fb_total += fb_count
            scores_dict["3"] = m_count
            scores_dict["2"] = a_count
            scores_dict["1"] = fb_count
            scores_list.append(scores_dict)

    total_dict["3"] = m_total
    total_dict["2"] = a_total
    total_dict["1"] = fb_total

    return scores_list


def aggregate_most_recent_by_standard_overall_cohort(teacher_id):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts for each standard."""

    scores_list = []

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    most_recent_tests = []
    for cohort in cohorts:
        test = model.Test.query.filter_by(cohort_id=cohort.id).order_by(model.Test.test_date.desc()).first()
        most_recent_tests.append(test.id)

    student_ids = []
    standards_list = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student.student.id)
    for test_id in most_recent_tests:
        scores = model.Score.query.filter_by(test_id=test_id, student_id=student_ids[0]).all()
        for score in scores:
            standards = model.Standard.query.filter_by(id=score.standard_id).all()
            for standard in standards:
                standards_list.append(standard)

    for standard in standards_list:
        scores_by_standard = {}
        scores_by_standard["Name"] = standard.code
        scores_by_standard["Description"] = standard.description
        scores_by_standard["ID"] = standard.id

        for test_id in most_recent_tests:
            m_count = 0
            a_count = 0
            fb_count = 0
            for student_id in student_ids:
                scores = model.Score.query.filter_by(student_id=student_id, test_id=test_id, standard_id=standard.id).all()

                for score in scores:

                    if score.score == "M":
                        m_count += 1
                    elif score.score == "A":
                        a_count += 1
                    elif score.score == "FB":
                        fb_count += 1

                scores_by_standard["3"] = m_count
                scores_by_standard["2"] = a_count
                scores_by_standard["1"] = fb_count

        scores_list.append(scores_by_standard)

    return scores_list


def aggregate_most_recent_by_standard_single_cohort(cohort_id):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts and percentages for each standard."""

    scores_list = []

    cohort = model.Cohort.query.filter_by(id=cohort_id).first()
    test = model.Test.query.filter_by(cohort_id=cohort_id).order_by(model.Test.test_date.desc()).first()

    student_ids = []
    standards_list = []

    students = cohort.studentcohorts
    for student in students:
        student_ids.append(student.student.id)

    scores = model.Score.query.filter_by(test_id=test.id, student_id=student_ids[0]).all()
    for score in scores:
        standards = model.Standard.query.filter_by(id=score.standard_id).all()
        for standard in standards:
            standards_list.append(standard)

    for standard in standards_list:
        scores_by_standard = {}
        scores_by_standard["Name"] = standard.code
        scores_by_standard["Description"] = standard.description
        scores_by_standard["ID"] = standard.id

        m_count = 0
        a_count = 0
        fb_count = 0
        for student_id in student_ids:
            scores = model.Score.query.filter_by(student_id=student_id, test_id=test.id, standard_id=standard.id).all()

            for score in scores:

                if score.score == "M":
                    m_count += 1
                elif score.score == "A":
                    a_count += 1
                elif score.score == "FB":
                    fb_count += 1

            scores_by_standard["3"] = m_count
            scores_by_standard["2"] = a_count
            scores_by_standard["1"] = fb_count

        scores_list.append(scores_by_standard)

    return scores_list


def top_struggle_standards_all_cohorts(teacher_id):

    """Identify the top standards students are struggling with, defined as
    standards where <25% of students have met standard."""

    scores_list = []

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    most_recent_tests = []
    for cohort in cohorts:
        test = model.Test.query.filter_by(cohort_id=cohort.id).order_by(model.Test.test_date.desc()).first()
        most_recent_tests.append(test.id)

    student_ids = []
    standards_list = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student.student.id)
    for test_id in most_recent_tests:
        scores = model.Score.query.filter_by(test_id=test_id, student_id=student_ids[0]).all()
        for score in scores:
            standards = model.Standard.query.filter_by(id=score.standard_id).all()
            for standard in standards:
                standards_list.append(standard)

    for standard in standards_list:
        scores_by_standard = {}

        for test_id in most_recent_tests:
            m_count = 0
            a_count = 0
            fb_count = 0
            total_scores = 0
            for student_id in student_ids:
                scores = model.Score.query.filter_by(student_id=student_id, test_id=test_id, standard_id=standard.id).all()
                total_scores +=1
                for score in scores:
                    if score.score == "M":
                        m_count += 1
                    elif score.score == "A":
                        a_count += 1
                    elif score.score == "FB":
                        fb_count += 1

                m_percent = float(m_count) / float(total_scores)

                if m_percent <= .25:
                    scores_by_standard["Name"] = standard.code
                    scores_by_standard["Description"] = standard.description
                    scores_by_standard["ID"] = standard.id
                    scores_by_standard["Percent"] = m_percent

        scores_list.append(scores_by_standard)

    return scores_list

# def aggregate_all_tests_by_standard_overall_cohort(teacher_id):
#     """Take in data returned by get_overall_cohort_data and filter it by the
#     standard. Add up counts of M, A, and FB scores and return counts and
#     percentages for each test_id."""

#     cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
#     test_ids = []
#     student_ids = []
#     standard_ids = []
#     for cohort in cohorts:
#         students = cohort.studentcohorts
#         tests = model.Test.query.all()
#         for student in students:
#             student_ids.append(student.student.id)
#     for test in tests:
#         test_ids.append(test.id)
#         standards = model.Score.query.filter_by(test_id=test.id, student_id=student_ids[0]).all()
#         for standard in standards:
#             standard_ids.append(standard.standard_id)

#     scores_by_standard = {}
#     for standard in standard_ids:
#         scores_by_standard[standard] = []

#     for test_id in test_ids:
#         for student_id in student_ids:
#             for standard_id in standard_ids:
#                 scores = model.Score.query.filter_by(student_id=student_id, test_id=test_id, standard_id=standard_id).all()
#                 for score in scores:
#                     scores_by_standard[standard_id].append(score.score)

#     for standard_id in standard_ids:
#         scores_by_standard[standard_id] = get_counts_and_percents(scores_by_standard[standard_id])

#     return scores_by_standard

# def get_single_cohort_data(cohort_id):
#     """Query scores using cohort_id to get the student_ids. Get all scores for all
#     students in the cohort."""
#     pass

# def filter_single_by_most_recent_test(single_cohort_data):
#     """Take in data returned by get_single_cohort_data. Filter by most recent
#     test_id. Return filtered data."""
#     pass

# def aggregate_most_recent_for_single_cohort(single_cohort_filtered_data):
#     """Add up counts of M, A, and FB scores and return counts and percentages."""
#     pass

# def aggregate_all_tests_for_single_cohort(single_cohort_data):
#     """Take in data returned by get_single_cohort_data. Add up counts of M, A,
#     and FB scores and return counts and percentages for each test_id."""
#     pass

# def aggregate_most_recent_by_standard_single_cohort(single_cohort_filtered_data):
#     """Break out filtered data by standard. Aggregate M/A/FB scores by standard
#     and return counts and percentages for each standard."""
#     pass

# def aggregate_all_tests_by_standard_single_cohort(single_cohort_data, standard):
#     """Take in data returned by get_single_cohort_data and filter it by the
#     standard. Add up counts of M, A, and FB scores and return counts and
#     percentages for each test_id."""
#     pass

# def get_student_scores(student_id):
#     """Use student_id to get all scores for that student. Return score data."""

#     scores = model.Score.query.filter_by(student_id=student_id).all()
#     score_list = []
#     for score in scores:
#         score_list.append(score.score)
#     return score_list

# def aggregate_most_recent_for_student(student_data):
#     """Filter data from get_student_scores by most recent test. Add up counts of
#     M, A, and FB scores and return counts and percentages."""
#     pass

# def aggregate_all_tests_for_student(student_data):
#     """Add up counts of M, A, and FB scores by test_id and return counts and
#     percentages."""
#     pass

# def show_all_student_scores(student_data):
#     """Take data from get_student_scores and display it in a table, by test and
#     by standard."""
#     pass





