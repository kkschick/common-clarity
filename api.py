import model
from flask import session
from sqlalchemy.sql import func

"""Log-in"""

def get_user(username, password):
    """Check if user exists; if exists, authenticate pw and return success msg"""

    user = model.User.query.filter_by(username=username).first()
    return user

"""Log-out"""

def logout():
    session.clear()

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
        student_names.append(student.student.first_name + ' ' + student.student.last_name)
    return student_names

def get_student_by_id(student_id):
    """Get student object by student ID."""

    student = model.User.query.filter_by(id=student_id).first()
    return student

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

"""Reports"""

def check_if_data(teacher_id):
    """Use teacher_id to query tests table and see if any tests exist for that
    teacher. Return boolean."""

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    scores_exist = False
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_id = student.student.id
            scores = model.Score.query.filter_by(student_id=student_id).first()
            if scores != None:
                scores_exist = True
    return scores_exist


def parse_CSV(csv, name, date, cohort_id):
    """Take CSV file that was uploaded and parse it. Create new test in Tests table.
    Match student names to users table and match CCSS to the standards table and
    get user_id and standard_id. Use test_id returned from create_new_test, user_id,
    and standard_id, and add score to scores table."""

    with open('csv', 'rb') as f:

    # Create new test in tests database
        test = model.Test(name=name, test_date=date, cohort_id=cohort_id)
        session.add(test)
        session.commit()

        reader = csv.reader(f, delimiter=',')

        # Create list with the headers and filter it to be just student names
        headers = reader.next()
        students = headers[1:-5]

        # Read through the rest of the file and add the standards and scores to lists
        standards = []
        scores = []
        for rows in reader:
            standards.append(rows[0])
            scores.append(rows[1:-5])

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
                session.add(new_score)
                i += 1
            j += 1

        session.commit()

def get_overall_cohort_data(teacher_id):
    """Use teacher_id to get student_ids through the cohorts table. Get all scores
    for all students in all the cohorts associated with that teacher_id."""

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    for cohort in cohorts:
        students = cohort.studentcohorts
        stu_scores = []
        for student in students:
            student_id = student.student.id
            scores = model.Score.query.filter_by(student_id=student_id).all()
            for score in scores:
                new_score = score.score
                stu_scores.append(new_score)
    return stu_scores

def get_overall_by_most_recent_test(teacher_id):
    """Take in data returned by get_overall_cohort_data. Filter by most recent
    test_id. Return filtered data."""

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    tests = model.Test.query.filter(model.Test.test_date==func.max(model.Test.test_date).select()).all()
    test_ids = []
    student_ids = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student.student.id)
    for test in tests:
        test_ids.append(test.id)

    scores_list = []
    for test_id in test_ids:
        for student_id in student_ids:
            scores = model.Score.query.filter_by(student_id=student_id, test_id=test_id).all()
            for score in scores:
                scores_list.append(score.score)

    return scores_list

def get_counts_and_percents(data):
    """Take in a list of scores and output counts and percentages."""

    length = len(data)

    M_count = 0
    A_count = 0
    FB_count = 0

    most_recent_scores = {}

    for item in data:
        if item == 'M':
            M_count +=1
        elif item == 'A':
            A_count +=1
        elif item == 'FB':
            FB_count += 1

    most_recent_scores['M_count'] = M_count
    most_recent_scores['A_count'] = A_count
    most_recent_scores['FB_count'] = FB_count

    M_percent = (float(M_count) / float(length))
    A_percent = (float(A_count) / float(length))
    FB_percent = (float(FB_count) / float(length))

    most_recent_scores['M_percent'] = M_percent
    most_recent_scores['A_percent'] = A_percent
    most_recent_scores['FB_percent'] = FB_percent

    return most_recent_scores

def aggregate_most_recent_for_overall_cohort(teacher_id):
    """Add up counts of M, A, and FB scores and return counts and percentages."""

    data = filter_overall_by_most_recent_test(teacher_id)
    return get_counts_and_percents(data)


def aggregate_all_tests_for_overall_cohort(teacher_id):
    """Take in data returned by get_overall_cohort_data. Add up counts of M, A,
    and FB scores and return counts and percentages for each test_id."""

    data = get_overall_cohort_data(teacher_id)
    return get_counts_and_percents(data)


def aggregate_most_recent_by_standard_overall_cohort(teacher_id):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts and percentages for each standard."""

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    tests = model.Test.query.filter(model.Test.test_date==func.max(model.Test.test_date).select()).all()
    test_ids = []
    student_ids = []
    standard_ids = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student.student.id)
    for test in tests:
        test_ids.append(test.id)
        standards = model.Score.query.filter_by(test_id=test.id, student_id=student_ids[0]).all()
        for standard in standards:
            standard_ids.append(standard.standard_id)

    scores_by_standard = {}
    for test_id in test_ids:
        for student_id in student_ids:
            scores = model.Score.query.filter_by(student_id=student_id, test_id=test_id).all()
            for standard in standard_ids:
                scores_by_standard[standard] = []
                for score in scores:
                    scores_by_standard[standard].append(score.score)

    return scores_by_standard


def aggregate_all_tests_by_standard_overall_cohort(all_cohorts_data, standard):
    """Take in data returned by get_overall_cohort_data and filter it by the
    standard. Add up counts of M, A, and FB scores and return counts and
    percentages for each test_id."""
    pass

def get_single_cohort_data(cohort_id):
    """Query scores using cohort_id to get the student_ids. Get all scores for all
    students in the cohort."""
    pass

def filter_single_by_most_recent_test(single_cohort_data):
    """Take in data returned by get_single_cohort_data. Filter by most recent
    test_id. Return filtered data."""
    pass

def aggregate_most_recent_for_single_cohort(single_cohort_filtered_data):
    """Add up counts of M, A, and FB scores and return counts and percentages."""
    pass

def aggregate_all_tests_for_single_cohort(single_cohort_data):
    """Take in data returned by get_single_cohort_data. Add up counts of M, A,
    and FB scores and return counts and percentages for each test_id."""
    pass

def aggregate_most_recent_by_standard_single_cohort(single_cohort_filtered_data):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts and percentages for each standard."""
    pass

def aggregate_all_tests_by_standard_single_cohort(single_cohort_data, standard):
    """Take in data returned by get_single_cohort_data and filter it by the
    standard. Add up counts of M, A, and FB scores and return counts and
    percentages for each test_id."""
    pass

def get_student_scores(student_id):
    """Use student_id to get all scores for that student. Return score data."""

    scores = model.Score.query.filter_by(student_id=student_id).all()
    score_list = []
    for score in scores:
        score_list.append(score.score)
    return score_list

def aggregate_most_recent_for_student(student_data):
    """Filter data from get_student_scores by most recent test. Add up counts of
    M, A, and FB scores and return counts and percentages."""
    pass

def aggregate_all_tests_for_student(student_data):
    """Add up counts of M, A, and FB scores by test_id and return counts and
    percentages."""
    pass

def show_all_student_scores(student_data):
    """Take data from get_student_scores and display it in a table, by test and
    by standard."""
    pass





