# from flask import session
import model


def get_user_id(username, password):
	"""Get the user_id and pass it through with every API call."""
	pass

"""Log-in"""

def get_user(username, password):
	"""Check if user exists; if exists, authenticate pw and return success msg"""
	pass



"""Sign-up"""

def create_teacher_user(first_name, last_name, email, username, password):
	"""Get form data and insert new user into users table"""
	pass



"""Settings"""

def get_teacher_cohorts(teacher_id):
	"""Get teacher's cohorts and students in those cohorts from the db.
	Use teacher_id to get cohort_ids associated with that teacher and
	return them. If none, return False."""
	pass

def get_students_in_cohort(cohort_id):
	"""Use cohort_ids associated with teacher_id to query studentcohorts
	to get student_ids for that cohort and query users for those students.
	If none, return False."""
	pass

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

def create_student(username, password, first_name, last_name):
	"""Create new student user in users table. Return user_id."""
	pass

def add_student_to_cohort(student_id, cohort_id):
	"""Use return values from add_new_cohort and create_student to add
	student to studentcohorts table."""
	pass



"""Reports"""

def check_if_data(teacher_id):
	"""Use teacher_id to query tests table and see if any tests exist for that
	teacher. Return boolean."""
	pass

def create_new_test(test_name, test_date):
	"""Create new test in tests using the name, date, and teacher_id of the
	logged in user. Return test_id."""
	pass

def parse_CSV(csv):
	"""Take CSV file that was uploaded and parse it. Match student names to users
	table and match CCSS to the standards table and get user_id and standard_id.
	Use test_id returned from create_new_test, user_id, and standard_id, and add
	score to scores table."""
	pass

def get_overall_cohort_data(teacher_id):
	"""Use teacher_id to get student_ids through the cohorts table. Get all scores
	for all students in all the cohorts associated with that teacher_id."""
	pass

def filter_overall_by_most_recent_test(all_cohorts_data):
	"""Take in data returned by get_overall_cohort_data. Filter by most recent
	test_id. Return filtered data."""
	pass

def aggregate_most_recent_for_overall_cohort(filtered_all_cohorts_data):
	"""Add up counts of M, A, and FB scores and return counts and percentages."""
	pass

def aggregate_all_tests_for_overall_cohort(all_cohorts_data):
	"""Take in data returned by get_overall_cohort_data. Add up counts of M, A,
	and FB scores and return counts and percentages for each test_id."""
	pass

def aggregate_most_recent_by_standard_overall_cohort(filtered_all_cohorts_data):
	"""Break out filtered data by standard. Aggregate M/A/FB scores by standard
	and return counts and percentages for each standard."""
	pass

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
	pass

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





