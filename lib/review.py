from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:
    all_reviews = {}

    def __init__(self, year, summary, employee_id):
        self.id = None
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return f"<Review id={self.id}, year={self.year}, summary={self.summary}, employee_id={self.employee_id}>"

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                summary TEXT NOT NULL,
                employee_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS reviews')
        CONN.commit()

    def save(self):
        CURSOR.execute('''
            INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?)
        ''', (self.year, self.summary, self.employee_id))
        self.id = CURSOR.lastrowid
        Review.all_reviews[self.id] = self
        CONN.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        if row[0] in cls.all_reviews:
            return cls.all_reviews[row[0]]
        else:
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all_reviews[review.id] = review
            return review

    @classmethod
    def find_by_id(cls, review_id):
        CURSOR.execute('SELECT * FROM reviews WHERE id = ?', (review_id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self, year=None, summary=None, employee_id=None):
        if year: self.year = year
        if summary: self.summary = summary
        if employee_id: self.employee_id = employee_id
        CURSOR.execute('''
            UPDATE reviews SET year = ?, summary = ?, employee_id = ? WHERE id = ?
        ''', (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute('DELETE FROM reviews WHERE id = ?', (self.id,))
        del Review.all_reviews[self.id]
        self.id = None
        CONN.commit()

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM reviews')
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

