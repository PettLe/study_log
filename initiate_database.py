import sqlite3

# This file should be run only first time in order to create tables to the database

# FIRST TIME create a table
# Establish db connection or create new
conn = sqlite3.connect("course_data.db")

# create cursor
c = conn.cursor()

c.execute(
    """
          CREATE TABLE courses (
              name TEXT,
              osp INTEGER,
              grade TEXT,
              category TEXT
          )
          """
)

c.execute(
    """
CREATE TABLE notes (
    course_id INTEGER,
    note TEXT
)
"""
)
