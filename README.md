CommonClarity
=============

CommonClarity transforms standardized test data into a visual, interactive reporting dashboard for teachers, to help inform and target instruction.

####The Project

Teachers are inundated with data from standardized tests but lack the tools and time to make sense of it. CommonClarity makes it easy for teachers to upload their data and instantly generate a dashboard of reports, showing their students' strengths and weaknesses according to Common Core State Standards. Data are grouped in useful ways to expose patterns and track progress, so that teachers can better help students improve.

CommonClarity was written using AngularJS, D3, JavaScript, Python, Flask, HTML5, CSS3, jQuery, Sass, SQLAlchemy, and Postgresql.

![Reporting dashboard](/static/screenshots/all_cohorts_dashboard.png)

####Product Features
- [Student set-up](#student-set-up)
- [Easy data import](#easy-data-import)
- [Reporting dashboard](#reporting-dashboard)
####Getting Started

###Product Features

####Student set-up

Quickly set up your classes of students, either by uploading a CSV file or by manually entering each name:

![Student set-up](/static/screenshots/set_up_students.png)

####Easy data import

Easily import your standardized test data into the system:

![Data import](/static/screenshots/import_test_data.png)

####Reporting dashboard

Once your data is imported, the reporting dashboard will automatically update with your new data. This dashboard will show you 1) the top Common Core State Standards needing improvement and which students have not met each standard; 2) an overview of student performance on the last test; 3) student performance compared to the rest of your school and district; 4) student performance broken out by test and by Common Core State Standard; 5) the standards tested on the last test; and 6) students requiring the most help.

![Reporting dashboard](/static/screenshots/all_cohorts_dashboard.png)

Use the drill-down menus to view all your classes at once, one class individually, or one particular student: 

![Drill-down](/static/screenshots/drill_down.png)

Target an individual student to see how that student is performing:

![Student dashboard](/static/screenshots/student_dashboard.png)

See how students are performing, according to specific Common Core State Standards:

![Standard report](/static/screenshots/standards_report.png)

Get a visual overview of how all the students in a class are performing:

![By student](/static/screenshots/class_perf_by_student.png)


#### Getting Started

1. Clone the repository:

    <code>$ git clone https://github.com/kkschick/CommonClarity.git</code>

2. Create and activate a new virtual environment:

    <code>$ virtualenv env</code>
    
    <code>$ . env/bin/activate/</code>
    
3. Install required packages:

    <code>$ pip install -r requirements.txt</code>

3. Run the app:

    <code>$ python app.py</code>

4. Point your browser to:

    <code>http://localhost:5000/</code>

