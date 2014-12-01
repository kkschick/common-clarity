import model
import csv
from datetime import datetime
from operator import itemgetter


"""Error Handler"""

def clarity_error(error):
    """Handle API errors.

        error: (string) error message

        returns: dictionary error object.
    """

    return {
        "result": error,
    }


"""Log-in"""

def get_user(email, password):
    """Check if user exists; if exists, authenticate pw and return success msg"""

    user = model.User.query.filter_by(email=email).first()
    if user:
        return user

"""Log-out"""

def logout():
    """Clear session to log user out of site."""

    model.session.clear()

"""Sign-up"""

def create_teacher_user(user_type, email, password, first_name, last_name):
    """Get form data and add new user to users table"""

    # Check if user exists
    user = model.User.query.filter_by(email=email).first()

    # If user doesn't exist, create user
    if user == None:
        user = model.User(user_type=user_type, email=email, password=password, first_name=first_name, last_name=last_name)
        model.session.add(user)
        model.session.commit()


"""Settings"""

def get_teacher_cohorts(teacher_id):
    """Get teacher's cohorts and students in those cohorts from the db.
    Use teacher_id to get cohort_ids associated with that teacher and
    return them. If none, return False."""

    # Get all teacher's cohorts
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    all_cohorts = []

    # For each class, add the ID, name, and list of students
    for cohort in cohorts:
        full_class = {}
        students = get_students_in_cohort(cohort.id)
        full_class["cohort_id"] = cohort.id
        full_class["name"] = cohort.name
        full_class["students"] = students
        all_cohorts.append(full_class)

    # Sort list of dicts by cohort name
    all_cohorts.sort(key=itemgetter("name"))

    return all_cohorts

def get_students_in_cohort(cohort_id):
    """Use cohort_ids associated with teacher_id to query studentcohorts
    to get student names for that cohort. If none, return False."""

    # Get all students associated with each of a teacher's cohort ID
    students = model.StudentCohort.query.filter_by(cohort_id=cohort_id).all()

    student_names = []

    # For each student, add student name and ID
    for student in students:
        student_dict = {}
        student_dict["name"] = student.student.first_name + ' ' + student.student.last_name
        student_dict["id"] = student.student.id
        student_names.append(student_dict)

    # Sort list of dicts by student name
    student_names.sort(key=itemgetter("name"))

    return student_names

def add_new_cohort(name, teacher_id):
    """Create new cohort in cohorts table. Return cohort_id."""

    # Query cohorts to see if cohort exists
    cohort = model.Cohort.query.filter_by(name=name, teacher_id=teacher_id).first()

    # If cohort doesn't yet exist, create it and return the ID
    if cohort == None:
        cohort = model.Cohort(name=name, teacher_id=teacher_id)
        model.session.add(cohort)
        model.session.commit()
        new_cohort = model.Cohort.query.filter_by(name=name).first()
        return new_cohort.id

    # Otherwise, return the cohort's ID
    else:
        return cohort.id

def create_student(user_type, first_name, last_name):
    """Create new student user in users table. Return cohort_id."""

    # See if student already exists
    student = model.User.query.filter_by(first_name=first_name, last_name=last_name).first()

    # If student doesn't exist, add it and return ID
    if student == None:
        user = model.User(user_type=user_type, first_name=first_name, last_name=last_name)
        model.session.add(user)
        model.session.commit()
        new_user = model.User.query.filter_by(first_name=first_name, last_name=last_name).first()
        return new_user.id

    # Otherwise, return ID
    else:
        return student.id

def add_student_to_cohort(student_id, cohort_id):
    """Add newly-created student to studentcohorts table."""

    studentcohort = model.StudentCohort(student_id=student_id, cohort_id=cohort_id)
    model.session.add(studentcohort)
    model.session.commit()

def create_student_from_csv(csv_path, cohort_id, user_type):
    """Parse CSV of new students and add each to users table in database."""

    # Read in CSV file of students
    with open(csv_path, 'rb') as f:

        # Split at the comma
        reader = csv.reader(f, delimiter=',')

        # Skip header row
        headers = reader.next()

        # Go through rows and add each student
        for row in reader:
            if row:

                # Check if student exists
                student = model.User.query.filter_by(first_name=row[0], last_name=row[1]).first()

                # If student doesn't exist, add student and add to student cohorts table
                if student == None:
                    user = model.User(user_type=user_type, first_name=row[0], last_name=row[1])
                    model.session.add(user)
                    model.session.commit()

                    # Get student's ID and add to studentcohorts table
                    student_id = (model.User.query.filter_by(first_name=row[0], last_name=row[1]).first()).id
                    studentcohort = model.StudentCohort(student_id=student_id, cohort_id=cohort_id)
                    model.session.add(studentcohort)
                    model.session.commit()


"""Reports"""

def parse_CSV(csv_path, name, date, cohort_id):
    """Take CSV file that was uploaded and parse it. Create new test in Tests table.
    Match student names to users table and match CCSS to the standards table and
    get user_id and standard_id. Use test_id returned from create_new_test, user_id,
    and standard_id, and add score to scores table."""

    # Format date object
    date = datetime.strptime(date, "%Y-%m-%d")

    # Open CSV file to read
    with open(csv_path, 'rb') as f:

        # Create new test in tests database
        test = model.Test(name=name, test_date=date, cohort_id=cohort_id)
        model.session.add(test)
        model.session.commit()

        # Split at comma
        reader = csv.reader(f, delimiter=',')

        # Create list with the headers and filter it into student names list and norms list
        headers = reader.next()
        students = headers[1:-2]
        norms = headers[-2:]

        # Read through the rest of the file and add the standards, scores, and normscores to lists
        standards = []
        scores = []
        norm_scores = []
        for row in reader:
            if row:
                standards.append(row[0])
                scores.append(row[1:-2])
                norm_scores.append(row[-2:])

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

            # Query the DB matching on the first and last name
            student = model.User.query.filter_by(last_name=last_name, first_name=first_name).first()

            # If student doesn't exist, add student and get ID
            if student == None:
                student = model.User(user_type="student", first_name=first_name, last_name=last_name)
                model.session.add(student)
                model.session.commit()
                student_id = (model.User.query.filter_by(last_name=last_name, first_name=first_name).first()).id
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
                model.session.add(new_score)
                i += 1
            j += 1

        # Iterate through the students, standards, and normscores, and add the normscores to the DB
        j = 0
        for item in norms:
            i = 0
            for standard in standard_ids:
                norm_score = norm_scores[i][j]
                new_norm_score = model.NormScore(cohort_name=item, test_id=test_id, standard_id=standard, score=float(norm_score))
                model.session.add(new_norm_score)
                i += 1
            j += 1

        model.session.commit()

def get_most_recent_tests(cohorts):

    """Get most recent test IDs for a teacher ID"""

    most_recent_tests = []
    for cohort in cohorts:
        test = model.Test.query.filter_by(cohort_id=cohort.id).order_by(model.Test.test_date.desc()).first()
        most_recent_tests.append(test.id)
    return most_recent_tests

def all_cohorts_top_struggle_standards(teacher_id):

    """Identify the top standards students are struggling with and which
    students have not met those standards."""

    scores_list = []

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    most_recent_tests = get_most_recent_tests(cohorts)

    student_ids = []
    standards_list = []

    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student)

    for test_id in most_recent_tests:
        scores = model.Score.query.filter_by(test_id=test_id, student_id=student_ids[0].student.id).all()
        for score in scores:
            standards_list.append(score.standard)

    for standard in standards_list:
        scores_by_standard = {}
        scores_by_standard["name"] = standard.code
        scores_by_standard["description"] = standard.description
        scores_by_standard["id"] = standard.id
        scores_by_standard["students"] = []
        total_scores = len(student_ids)

        for test_id in most_recent_tests:
            m_count = 0
            a_count = 0
            fb_count = 0

            scores = model.Score.query.filter_by(test_id=test_id, standard_id=standard.id).all()

            for score in scores:
                if score.score == "M":
                    m_count += 1
                elif score.score == "A":
                    a_count += 1
                elif score.score == "FB":
                    fb_count += 1
                    scores_by_standard["students"].append(score.student.first_name + " " + score.student.last_name)

        m_percent = (float(m_count) / float(total_scores)) * 100
        scores_by_standard["percent"] = m_percent
        scores_list.append(scores_by_standard)
        scores_by_standard["students"].sort()

    scores_list.sort(key=itemgetter("percent"))

    return scores_list

def all_cohorts_pie_chart(teacher_id):
    """Aggregate M/A/FB scores from most recent test for pie chart."""

    # Create empty list to hold the score aggregation
    summed_scores = []

    # Get all cohorts associated with the teacher
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    # Create an empty list to hold the most recent test for each cohort
    most_recent_tests = []

    # Query the tests database to retrieve the test ID of the most recent test for each cohort
    for cohort in cohorts:
        test = model.Test.query.filter_by(cohort_id=cohort.id).order_by(model.Test.test_date.desc()).first()
        most_recent_tests.append(test.id)

    m_total = 0
    a_total = 0
    fb_total = 0

    # Loop through the most recent tests and get scores
    for test_id in most_recent_tests:
        scores = model.Score.query.filter_by(test_id=test_id).all()

        # Initialize counters at zero and make empty dict to hold final scores
        m_count = 0
        a_count = 0
        fb_count = 0

        # Loop through score objects and get score value, append to list
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

    total = m_total + a_total + fb_total
    m_perc = (float(m_total) / float(total)) * 100
    a_perc = (float(a_total) / float(total)) * 100
    fb_perc = (float(fb_total) / float(total)) * 100

    m_dict = {"score": "M", "value": m_perc}
    a_dict = {"score": "A", "value": a_perc}
    fb_dict = {"score": "FB", "value": fb_perc}

    summed_scores.append(m_dict)
    summed_scores.append(a_dict)
    summed_scores.append(fb_dict)

    return summed_scores

def all_cohorts_most_recent_comp_to_normscores(teacher_id):

    final_scores = []

    # Get most recent % of standards met by calling other function
    summed_scores = (all_cohorts_pie_chart(teacher_id))[0]
    summed_reformatted = {"cohortName": "My Students", "value": ((summed_scores["value"])/100)}
    final_scores.append(summed_reformatted)

    # Get most recent test IDs for teacher's cohorts
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    most_recent_tests = get_most_recent_tests(cohorts)

    # Get norm scores for those test IDs
    cohort_names = []

    for test_id in most_recent_tests:
        normscores = model.NormScore.query.filter_by(test_id=test_id).all()
        for normscore in normscores:
            if normscore.cohort_name not in cohort_names:
                cohort_names.append(normscore.cohort_name)

    for item in cohort_names:
        final_dict = {}
        final_dict["cohortName"] = item
        final_dict["value"] = 0
        item_total = 0
        for normscore in normscores:
            if normscore.cohort_name == item:
                final_dict["value"] += normscore.score
                item_total += 1
        final_dict["value"] = final_dict["value"] / float(item_total)
        final_scores.append(final_dict)

    final_scores.sort(key=itemgetter("cohortName"))

    return final_scores

def all_cohorts_data_by_test(teacher_id):
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

    # Initialize empty response list and counters
    resp_list = []
    m_total = 0
    a_total = 0
    fb_total = 0

    # Add total dict to response list
    total_dict = {"name": "All Tests"}
    resp_list.append(total_dict)

    # Loop through tests
    for test in all_tests:
        resp_dict = {}

        # Add test name to dict
        resp_dict["name"] = test.name

        # Get all scores associated with each test id
        scores = model.Score.query.filter_by(test_id=test.id).all()

        # Loop through scores and count values
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

        # Increment totals
        m_total += m_count
        a_total += a_count
        fb_total += fb_count

        # Add counts to dict for that test
        resp_dict["3"] = m_count
        resp_dict["2"] = a_count
        resp_dict["1"] = fb_count
        resp_list.append(resp_dict)

    # Add total counts to total dict
    total_dict["3"] = m_total
    total_dict["2"] = a_total
    total_dict["1"] = fb_total

    return resp_list

def all_cohorts_data_most_recent_by_standard(teacher_id):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts for each standard."""

    scores_list = []

    # Get teacher's classes and most recent tests
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()
    most_recent_tests = get_most_recent_tests(cohorts)

    # Get all students in each class
    student_ids = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_ids.append(student.student.id)

    # Get all standards tested on the most recent tests
    standards_list = []
    for test_id in most_recent_tests:
        scores = model.Score.query.filter_by(test_id=test_id, student_id=student_ids[0]).all()
        for score in scores:
            standards_list.append(score.standard)

    # Loop through standards and add each to a dict
    for standard in standards_list:
        scores_by_standard = {}
        scores_by_standard["name"] = standard.code
        scores_by_standard["description"] = standard.description
        scores_by_standard["id"] = standard.id

        # Loop through tests and get scores, count num of each score
        for test_id in most_recent_tests:
            m_count = 0
            a_count = 0
            fb_count = 0
            total_length = 0

            scores = model.Score.query.filter_by(test_id=test_id, standard_id=standard.id).all()
            for score in scores:
                total_length += 1
                if score.score == "M":
                    m_count += 1
                elif score.score == "A":
                    a_count += 1
                elif score.score == "FB":
                    fb_count += 1

        # Add score counts to dict, along with percentage of Ms to sort by
        scores_by_standard["3"] = m_count
        scores_by_standard["2"] = a_count
        scores_by_standard["1"] = fb_count
        scores_by_standard["percent"] = (m_count / float(30))

        scores_list.append(scores_by_standard)

    # Sort list of dicts by percent of Ms
    scores_list.sort(key=itemgetter("percent"))
    scores_list.reverse()

    # Remove percentage from each dict in the list
    for dict in scores_list:
        if 'percent' in dict:
            del dict['percent']

    return scores_list

def all_cohorts_top_struggle_students(teacher_id):
    """Identify the students who are struggling with the most standards and
    require the most additional help."""

    scores_list = []

    # Get teacher's cohorts
    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    # Get students in those cohorts
    student_list = []
    for cohort in cohorts:
        students = cohort.studentcohorts
        for student in students:
            student_list.append(student)

    # Get each student's scores and sum up counts of each score
    for student in student_list:
        scores = model.Score.query.filter_by(student_id=student.student.id).all()
        total_scores = len(scores)
        m_count = 0
        a_count = 0
        fb_count = 0
        for score in scores:
            if score.score == "M":
                m_count += 1
            elif score.score == "A":
                a_count += 1
            elif score.score == "FB":
                fb_count += 1

        # Calculate total percentages of As and FBs
        a_percent = (float(a_count) / float(total_scores)) * 100
        fb_percent = (float(fb_count) / float(total_scores)) * 100

        # Add student to dict with name, percent of As, FBs, and totals
        scores_by_student = {}
        scores_by_student["name"] = student.student.first_name + " " + student.student.last_name
        scores_by_student["A"] = a_percent
        scores_by_student["FB"] = fb_percent
        scores_by_student["total"] = a_percent + fb_percent
        scores_list.append(scores_by_student)

    # Sort list of dicts by the total percentage of As plus FBs and reverse list
    scores_list.sort(key=itemgetter("total"))
    scores_list.reverse()

    return scores_list

def all_single_cohort_data(teacher_id):
    """Run all single cohort functions and compile into one giant JSON to send
    back to Angular."""

    all_cohort_data_by_cohort = {}

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    for cohort in cohorts:
        cohort_list = []
        temp_dict = {}
        temp_dict["report1"] = single_cohort_top_struggle_standards(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report2"] = single_cohort_pie_chart(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report3"] = single_cohort_most_recent_comp_to_normscores(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report4"] = single_cohort_data_by_test(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report5"] = single_cohort_data_most_recent_by_standard(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report6"] = single_cohort_top_struggle_students(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report7"] = single_cohort_scores_by_student(cohort.id)
        cohort_list.append(temp_dict)
        temp_dict = {}
        temp_dict["report8"] = single_cohort_data_most_recent_by_standard(cohort.id)
        cohort_list.append(temp_dict)
        cohort_data = {"dataValues": cohort_list, "cohortName": cohort.name}
        all_cohort_data_by_cohort[cohort.id] = cohort_data

    return all_cohort_data_by_cohort

def all_single_student_data(teacher_id):
    """Run all single student functions and compile into one giant JSON to send
    back to Angular."""

    all_student_data_by_student = {}

    cohorts = model.Cohort.query.filter_by(teacher_id=teacher_id).all()

    for cohort in cohorts:
        for studentcohort in cohort.studentcohorts:
            student = studentcohort.student
            student_list = []
            temp_dict = {}
            temp_dict["report1"] = student_pie_chart(student.id)
            student_list.append(temp_dict)
            temp_dict = {}
            temp_dict["report2"] = student_top_struggle_standards(student.id)
            student_list.append(temp_dict)
            temp_dict = {}
            temp_dict["report3"] = student_most_recent_comp_to_normscores(student.id)
            student_list.append(temp_dict)
            temp_dict = {}
            temp_dict["report4"] = student_data_by_test(student.id)
            student_list.append(temp_dict)
            temp_dict = {}
            temp_dict["report5"] = student_improvement(student.id)
            student_list.append(temp_dict)
            temp_dict = {}
            temp_dict["report6"] = student_falling_behind_score_count(student.id)
            student_list.append(temp_dict)
            full_name = student.first_name + " " + student.last_name
            student_data = {"dataValues": student_list, "firstName": student.first_name, "fullName": full_name}
            all_student_data_by_student[student.id] = student_data

    return all_student_data_by_student

def get_most_recent_test(cohort_id):

    # Get most recent test for the cohort
    test = model.Test.query.filter_by(cohort_id=cohort_id).order_by(model.Test.test_date.desc()).first()
    return test

def get_students_in_class(cohort_id):

    # Get all the students in that cohort
    students = model.StudentCohort.query.filter_by(cohort_id=cohort_id).all()
    return students

def single_cohort_top_struggle_standards(cohort_id):

    """Identify the top standards students in a cohort are struggling with
    and which students have not met those standards."""

    scores_list = []

    # Get most recent test for the cohort
    test = get_most_recent_test(cohort_id)

    # Get all the students in that cohort
    students = get_students_in_class(cohort_id)

    # Get the standards students were tested on in most recent test
    standards_list = []
    scores = model.Score.query.filter_by(test_id=test.id, student_id=students[0].student.id).all()
    for score in scores:
        standards_list.append(score.standard)

    # Go through standards and add metadata about each to dictionary
    for standard in standards_list:
        scores_by_standard = {}
        scores_by_standard["name"] = standard.code
        scores_by_standard["description"] = standard.description
        scores_by_standard["id"] = standard.id
        scores_by_standard["students"] = []
        total_scores = len(students)

        m_count = 0
        a_count = 0
        fb_count = 0

        # Loop through scores and add up counts of each
        scores = model.Score.query.filter_by(test_id=test.id, standard_id=standard.id).all()

        for score in scores:
            if score.score == "M":
                m_count += 1
            elif score.score == "A":
                a_count += 1
            elif score.score == "FB":
                fb_count += 1
                scores_by_standard["students"].append(score.student.first_name + " " + score.student.last_name)

        # Calculate percentage of Ms
        m_percent = (float(m_count) / float(total_scores)) * 100
        scores_by_standard["percent"] = m_percent
        scores_list.append(scores_by_standard)
        scores_by_standard["students"].sort()

    # Sort list of dicts by percent of Ms
    scores_list.sort(key=itemgetter("percent"))

    return scores_list

def single_cohort_pie_chart(cohort_id):
    """Aggregate M/A/FB scores from most recent test for pie chart.
    for single class."""

    # Create empty list to hold the score aggregation
    summed_scores = []

    # Get most recent test for the cohort
    test = get_most_recent_test(cohort_id)

    m_total = 0
    a_total = 0
    fb_total = 0

    # Get scores for most recent test
    scores = model.Score.query.filter_by(test_id=test.id).all()

    # Initialize counters at zero
    m_count = 0
    a_count = 0
    fb_count = 0

    # Loop through score objects and get score value, append to list
    for score in scores:
        if score.score == 'M':
            m_count +=1
        elif score.score == 'A':
            a_count +=1
        elif score.score == 'FB':
            fb_count += 1

    # Increment totals
    m_total += m_count
    a_total += a_count
    fb_total += fb_count

    # Calculate total and find percentages of each score
    total = m_total + a_total + fb_total
    m_perc = (float(m_total) / float(total)) * 100
    a_perc = (float(a_total) / float(total)) * 100
    fb_perc = (float(fb_total) / float(total)) * 100

    # Add each percentage to dict
    m_dict = {"score": "M", "value": m_perc}
    a_dict = {"score": "A", "value": a_perc}
    fb_dict = {"score": "FB", "value": fb_perc}

    # Add dicts to response list
    summed_scores.append(m_dict)
    summed_scores.append(a_dict)
    summed_scores.append(fb_dict)

    return summed_scores

def single_cohort_most_recent_comp_to_normscores(cohort_id):

    final_scores = []

    # Get most recent % of standards met by calling other function
    summed_scores = (single_cohort_pie_chart(cohort_id))[0]
    summed_reformatted = {"cohortName": "My Students", "value": ((summed_scores["value"])/100)}
    final_scores.append(summed_reformatted)

    # Get most recent test ID for cohort
    test = get_most_recent_test(cohort_id)

    # Get norm scores for those test IDs
    cohort_names = []

    normscores = model.NormScore.query.filter_by(test_id=test.id).all()
    for normscore in normscores:
        if normscore.cohort_name not in cohort_names:
            cohort_names.append(normscore.cohort_name)

    # Loop through cohort names and add name and sum up values
    for item in cohort_names:
        final_dict = {}
        final_dict["cohortName"] = item
        final_dict["value"] = 0
        item_total = 0

        # Loop thorugh normscores and increment values
        for normscore in normscores:
            if normscore.cohort_name == item:
                final_dict["value"] += normscore.score
                item_total += 1

        # Calculate percentage and add to final dict
        final_dict["value"] = final_dict["value"] / float(item_total)

        # Add final dict to list
        final_scores.append(final_dict)

    # Sort list of dicts by cohort name
    final_scores.sort(key=itemgetter("cohortName"))

    return final_scores

def single_cohort_data_by_test(cohort_id):
    """Use cohort id to get all student scores for that cohort by test and
    aggregate counts of M/A/FB by test."""

    # Get tests for that cohort
    tests = model.Test.query.filter_by(cohort_id=cohort_id).all()

    # Initialize empty response list and set counters to zero
    resp_list = []
    m_total = 0
    a_total = 0
    fb_total = 0

    # Add total dict to response list
    total_dict = {"name": "All Tests"}
    resp_list.append(total_dict)

    # Loop through tests
    for test in tests:
        resp_dict = {}
        resp_dict["name"] = test.name

        # Get all scores associated with each test id
        scores = model.Score.query.filter_by(test_id=test.id).all()

        # Loop through scores and count up each score
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

        # Increment totals
        m_total += m_count
        a_total += a_count
        fb_total += fb_count

        # Add counts to response dict
        resp_dict["3"] = m_count
        resp_dict["2"] = a_count
        resp_dict["1"] = fb_count
        resp_list.append(resp_dict)

    # Add totals to total dict
    total_dict["3"] = m_total
    total_dict["2"] = a_total
    total_dict["1"] = fb_total

    return resp_list

def single_cohort_data_most_recent_by_standard(cohort_id):
    """Break out filtered data by standard. Aggregate M/A/FB scores by standard
    and return counts and percentages for each standard."""

    scores_list = []

    # Get most recent test
    test = get_most_recent_test(cohort_id)

    # Get students in class
    students = get_students_in_class(cohort_id)

    # Get standards from test and add to list
    standards_list = []
    scores = model.Score.query.filter_by(test_id=test.id, student_id=students[0].student.id).all()
    for score in scores:
        standards_list.append(score.standard)

    # Loop through standards
    for standard in standards_list:

        # Add standard metadata to dict
        scores_by_standard = {}
        scores_by_standard["name"] = standard.code
        scores_by_standard["description"] = standard.description
        scores_by_standard["id"] = standard.id

        # Initialize counters at zero
        m_count = 0
        a_count = 0
        fb_count = 0

        # Get scores and loop through, counting up each score
        scores = model.Score.query.filter_by(test_id=test.id, standard_id=standard.id).all()
        for score in scores:
            if score.score == "M":
                m_count += 1
            elif score.score == "A":
                a_count += 1
            elif score.score == "FB":
                fb_count += 1

        # Add counts to dict and calculate percentage of Ms, add dict to list
        scores_by_standard["3"] = m_count
        scores_by_standard["2"] = a_count
        scores_by_standard["1"] = fb_count
        scores_by_standard["percent"] = (m_count / float(30))
        scores_list.append(scores_by_standard)

    # Sort list of dicts by percentage of Ms and reverse it
    scores_list.sort(key=itemgetter("percent"))
    scores_list.reverse()

    # Remove percentage of Ms from each dict
    for dict in scores_list:
        if "percent" in dict:
            del dict["percent"]

    return scores_list

def single_cohort_top_struggle_students(cohort_id):
    """Identify the students who are struggling with the most standards and
    require the most additional help."""

    scores_list = []

    # Get all students in class
    students = get_students_in_class(cohort_id)

    # Loop through students and get scores
    for student in students:
        scores = model.Score.query.filter_by(student_id=student.student.id).all()
        total_scores = len(scores)

        # Loop through scores and add up counts of each score
        m_count = 0
        a_count = 0
        fb_count = 0
        for score in scores:
            if score.score == "M":
                m_count += 1
            elif score.score == "A":
                a_count += 1
            elif score.score == "FB":
                fb_count += 1

        # Calculate percentages of As and FBs
        a_percent = (float(a_count) / float(total_scores)) * 100
        fb_percent = (float(fb_count) / float(total_scores)) * 100

        # Add scores to dict, add dict to response list
        scores_by_student = {}
        scores_by_student["name"] = student.student.first_name + " " + student.student.last_name
        scores_by_student["A"] = a_percent
        scores_by_student["FB"] = fb_percent
        scores_by_student["total"] = a_percent + fb_percent
        scores_list.append(scores_by_student)

    # Sort and reverse list of dicts by total percentage of As and FBs
    scores_list.sort(key=itemgetter("total"))
    scores_list.reverse()

    return scores_list

def single_cohort_scores_by_student(cohort_id):

    # Get students in class
    students = get_students_in_class(cohort_id)

    student_scores_list = []

    for student in students:

        student_score_dict = {}

        # Get student scores
        scores = model.Score.query.filter_by(student_id=student.student.id).all()

        m_count = 0
        a_count = 0
        fb_count = 0

        # Loop through scores and sum up counts of each
        for score in scores:
            if score.score == "M":
                m_count += 1
            elif score.score == "A":
                a_count += 1
            elif score.score == "FB":
                fb_count += 1

        # Add scores to dict, add dict to list
        student_score_dict["studentName"] = student.student.first_name + " " + student.student.last_name
        student_score_dict["3"] = m_count
        student_score_dict["2"] = a_count
        student_score_dict["1"] = fb_count
        student_scores_list.append(student_score_dict)

    # Sort list of dicts by student name
    student_scores_list.sort(key=itemgetter("studentName"))

    return student_scores_list

def student_pie_chart(student_id):
    """Aggregate M/A/FB scores from most recent test for pie chart.
    for single student."""

    # Create empty list to hold the score aggregation
    summed_scores = []

    # Get student cohort ID
    cohort_id = (model.StudentCohort.query.filter_by(student_id=student_id).first()).cohort_id

    # Get most recent test for the cohort
    test = model.Test.query.filter_by(cohort_id=cohort_id).order_by(model.Test.test_date.desc()).first()

    m_total = 0
    a_total = 0
    fb_total = 0

    # Get scores for most recent test
    scores = model.Score.query.filter_by(test_id=test.id, student_id=student_id).all()

    # Initialize counters at zero
    m_count = 0
    a_count = 0
    fb_count = 0

    # Loop through score objects and get score value, append to list
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

    total = m_total + a_total + fb_total
    m_perc = (float(m_total) / float(total)) * 100
    a_perc = (float(a_total) / float(total)) * 100
    fb_perc = (float(fb_total) / float(total)) * 100

    m_dict = {"score": "M", "value": m_perc}
    a_dict = {"score": "A", "value": a_perc}
    fb_dict = {"score": "FB", "value": fb_perc}

    summed_scores.append(m_dict)
    summed_scores.append(a_dict)
    summed_scores.append(fb_dict)

    return summed_scores

def student_top_struggle_standards(student_id):

    """Identify the top standards students are struggling with."""

    scores_list = []

    # Get most recent test for the cohort
    cohort_id = (model.StudentCohort.query.filter_by(student_id=student_id).first()).cohort_id
    test = model.Test.query.filter_by(cohort_id=cohort_id).order_by(model.Test.test_date.desc()).first()

    # Get student scores for most recent test
    scores = model.Score.query.filter_by(test_id=test.id, student_id=student_id).all()

    for score in scores:
        if score.score == "A" or score.score == "FB":
            score_dict = {}
            score_dict["name"] = score.standard.code
            score_dict["description"] = score.standard.description
            score_dict["score"] = score.score
            scores_list.append(score_dict)

    scores_list.sort(key=itemgetter("score"))
    scores_list.reverse()

    return scores_list

def student_most_recent_comp_to_normscores(student_id):

    final_scores = []

    # Get student name
    student = model.User.query.filter_by(id=student_id).first()
    student_name = student.first_name + " " + student.last_name

    # Get most recent % of standards met for student
    summed_scores = (student_pie_chart(student_id))[0]
    summed_reformatted = {"cohortName": student_name, "value": ((summed_scores["value"])/100)}
    final_scores.append(summed_reformatted)

    # Get most recent % of standards met for class overall
    cohort_id = (model.StudentCohort.query.filter_by(student_id=student_id).first()).cohort_id
    summed_scores = (single_cohort_pie_chart(cohort_id))[0]
    summed_reformatted = {"cohortName": "My Students", "value": ((summed_scores["value"])/100)}
    final_scores.append(summed_reformatted)

    # Get most recent test ID for cohort
    test = model.Test.query.filter_by(cohort_id=cohort_id).order_by(model.Test.test_date.desc()).first()

    # Get norm scores for those test IDs
    cohort_names = []

    normscores = model.NormScore.query.filter_by(test_id=test.id).all()
    for normscore in normscores:
        if normscore.cohort_name not in cohort_names:
            cohort_names.append(normscore.cohort_name)
    for item in cohort_names:
        final_dict = {}
        final_dict["cohortName"] = item
        final_dict["value"] = 0
        item_total = 0
        for normscore in normscores:
            if normscore.cohort_name == item:
                final_dict["value"] += normscore.score
                item_total += 1
        final_dict["value"] = final_dict["value"] / float(item_total)
        final_scores.append(final_dict)

    final_scores.reverse()

    return final_scores

def student_data_by_test(student_id):

    cohorts = model.StudentCohort.query.filter_by(student_id=student_id).all()

    scores_list = []

    total_dict = {"name": "All Tests"}
    scores_list.append(total_dict)
    m_total = 0
    a_total = 0
    fb_total = 0

    for cohort in cohorts:

        tests = model.Test.query.filter_by(cohort_id=cohort.cohort_id).all()
        for test in tests:
            scores_dict = {}
            scores_dict["name"] = test.name
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

def student_improvement(student_id):

    """Get student scores for all tests and compare # of standards met
    from most recent test to prior test."""

    student_scores = student_data_by_test(student_id)

    most_recent_test = student_scores[-1]
    one_prior_test = student_scores[-2]

    recent_num_m = most_recent_test["3"]
    prior_num_m = one_prior_test["3"]

    if recent_num_m < prior_num_m:
        response = "scores decreased on the most recent test, from " + str(prior_num_m) + " standards met to only " + str(recent_num_m) + "."
    elif recent_num_m > prior_num_m:
        response = "scores improved on the most recent test, from " + str(prior_num_m) + " standards met to " + str(recent_num_m) + "."
    else:
        response = "scores remained the same on the most recent test, with " + str(recent_num_m) + " standards met."

    return {"message": response}

def student_falling_behind_score_count(student_id):

    """Get the number of standards the student is falling behind on."""

    student_scores = student_data_by_test(student_id)

    fb_count = student_scores[-1]["1"]

    return {"count": fb_count}

