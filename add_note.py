class datahandler():
    def __init__(self):
        import sqlite3
        self.conn = sqlite3.connect("all_notes.db")
        self.c = self.conn.cursor()
    

    def insert_data(self, title='', importance=-1, npath='', nlink=''):
        if npath != '':
            with open(npath) as f:
                inlink = f.readline()
        if npath!='' and nlink == '' and inlink[2:6]=='http':
            nlink = inlink[2:-2]
        else:
            npath = nlink
        self.c.execute("SELECT noteId FROM allNotes ORDER BY noteId DESC")
        noteId = self.c.fetchone()[0] + 1
        from datetime import datetime
        ndate = str(datetime.now())
        with self.conn:
            self.c.execute("INSERT INTO allNotes VALUES (:noteId, :title, :importance, :path, :date, :link)", {'noteId':noteId, 'title':title, 'importance':importance, 'path':npath, 'date':ndate, 'link':nlink})
        print("note added")

    def show_data(self):
        self.c.execute("SELECT * FROM allNotes")
        return self.c.fetchall()
    
    def today_schedule(self, today=-1):
        import datetime as dt
        if today==-1:
            today = str(dt.datetime.now().date())
        result = self.c.execute("SELECT * FROM allNotes")
        todaylist = []
        # print(result.fetchall())
        # print(today)
        for i in result.fetchall():
            note_day = dt.datetime.fromisoformat(i[-2])
            notedays = []
            day = 1
            while(day <= 128):
                notedays.append(str((note_day+dt.timedelta(days=day)).date()))
                day = day*2
            #print(notedays)
            if (today in notedays):
                todaylist.append((i[0], i[1], i[-2][11:16]))
                print(today,"will be retuned")
        return todaylist

    def delete_data(self, dnoteId):
        with self.conn:
            self.c.execute("DELETE FROM allNotes WHERE noteId=:noteId",{'noteId':dnoteId})
# import datetime as dt
# obj1 = datahandler()
# obj1.today_schedule(dt.datetime.fromisoformat("2021-08-21"))
# # obj1.insert_data(title='Check cycle', importance=7, npath='D:/GitHub/LearningProbs/LinkedLists/check_cycle.py')
# # obj1.delete_data(10002)
# print(obj1.show_data())
# import sqlite3

# conn = sqlite3.connect('all_notes.db')

# c = conn.cursor()

# # c.execute('DROP TABLE IF EXISTS allNotes')
# c.execute("""CREATE TABLE taskDates(
#     ? integer,
# ),(10001)""")

# # c.execute("INSERT INTO allNotes VALUES (10001,'Palindrome linked list', 9, 'D:/GitHub/LearningProbs/LinkedLists/isPalindrome_muchbetter.py','2021-08-04 22:40:04.141897', 'https://www.interviewbit.com/problems/palindrome-list/')")

# def insert_data(data):
#     pass

# c.execute("INSERT INTO allNotes VALUES (10002,'Get intersection node', 9, 'D:/GitHub/LearningProbs/linkedLists/getIntersectionNode.py','2021-08-04 22:48:31.355954', 'https://leetcode.com/problems/intersection-of-two-linked-lists/submissions/')")

# conn.commit()

# c.execute('SELECT * FROM allNotes WHERE importance=9')

# print(c.fetchall())

# conn.commit()

# conn.close()