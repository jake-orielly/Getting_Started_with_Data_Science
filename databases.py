from __future__ import division
import math, random, re
from collections import defaultdict

class Table:
    def __init__(self, columns):
        self.columns = columns
        self.rows = []

    def __repr__(self):
        """pretty representation of the table: columns then rows"""
        return str(self.columns) + "\n" + "\n".join(map(str, self.rows))

    def insert(self, row_values):
        if len(row_values) != len(self.columns):
            raise TypeError("Wrong number of elements")
        row_dict = dict(zip(self.columns, row_values))
        self.rows.append(row_dict)
            
    def update(self, updates, predicate):
        for row in self.rows:
            if predicate(row):
                for column, new_value in updates.iteritems():
                    row[column] = new_value

    def delete(self, predicate=lambda row: True):
        """delete all rows matching predicate or all rows if no predicate supplied"""
        self.rows = [row for row in self.rows if not(predicate(row))]

    def select(self, keep_columns=None, additional_columns=None):
        if keep_columns is None:    #if no columns specified, return all columns
            keep_columns = self.columns

        if additional_columns is None:
            additional_columns = {}

        #new table for results
        result_table = Table(keep_columns + additional_columns.keys())

        for row in self.rows:
            new_row = [row[column] for column in keep_columns]
            for column_name, caluclation in additional_columns.iteritems():
                new_row.append(caluclation(row))
            result_table.insert(new_row)
        return result_table

    def where(self, predicate=lambda row: True):
        """return only the rows that satisfy the supplied predicate"""
        where_table = Table(self.columns)
        where_table.rows = filter(predicate, self.rows)
        return where_table

    def limit(self, num_rows):
        """return only the first num_rows rows"""
        limit_table = Table(self.columns)
        limit_table.rows = self.rows[:num_rows]
        return limit_table



users = Table(["user_id", "name", "num_friends"])
users.insert([0, "Hero", 0])
users.insert([1, "Dunn", 2])
users.insert([2, "Sue", 3])
users.insert([3, "Chi", 3])
users.insert([4, "Thor", 3])
users.insert([5, "Clive", 2])
users.insert([6, "Hicks", 3])
users.insert([7, "Devin", 2])
users.insert([8, "Kate", 2])
users.insert([9, "Klein", 3])
users.insert([10, "Jen", 1])
users.update({"num_friends" : 4}, #set num_friends = 3
             lambda row: row['user_id'] == 1) # in rows where user id = 1
users.delete(lambda row: row['user_id'] == 5)

#print(users.select(keep_columns=["user_id"]));
#print(users.where(lambda row: row["name"] == "Dunn").select(keep_columns=["user_id"]));
def name_length(row): return len(row["name"])
print(users.select(keep_columns=[],additional_columns={"name_length" : name_length}))
