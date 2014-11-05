import model
import csv

def load_standards(session):

    with open('seed_data/ccss.tsv', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            standard = model.User(id = row[0], category = row[1], code = row[2], description = row[3])
            session.add(standard)

    session.commit()

def main(session):
    load_standards(None)

if __name__ == "__main__":
    s = model.connect()
    main(s)
