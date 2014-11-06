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
	return them."""
	pass

def get_students_in_cohort(cohort_id):
	"""Use cohort_ids associated with teacher_id to query studentcohorts
	to get student_ids for that cohort and query users for those students."""
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
	pass

def create_student(username, password, first_name, last_name):
	"""Create new student user in users table. Return user_id."""
	pass

def add_student_to_class(student_id, cohort_id):
	"""Use return values from add_new_cohort and create_student to add
	student to studentcohorts table."""
	pass



"""Reports"""

