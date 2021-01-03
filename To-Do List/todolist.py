from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta


Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'Task({self.id} {self.task!r} {self.deadline!r})'


class ToDoList:
    today = datetime.today()

    def __init__(self, db_name):
        engine = create_engine(f'sqlite:///{db_name}.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def start(self):
        while True:
            option = int(input('''1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n4) Missed tasks
5) Add task\n6) Delete task\n0) Exit\n'''))
            if option == 1:
                self.show_today()
            elif option == 2:
                self.show_week()
            elif option == 3:
                self.show_all()
            elif option == 4:
                self.missed_tasks()
            elif option == 5:
                self.add_task()
            elif option == 6:
                self.delete_task()
            elif option == 0:
                print('Bye!')
                break

    def add_task(self):
        new_task = input('Enter task\n')
        new_task_date = input('Enter deadline\n')
        new_row = Table(task=new_task,
                        deadline=datetime.strptime(new_task_date, '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if len(rows) != 0:
            count = 1
            for row in rows:
                print(f'{count}. {row.task}. {datetime.strftime(row.deadline, "%d %b")}')
                count += 1
            choose = int(input(f'Choose the number of the task you want to delete:'))
            self.session.delete(rows[choose - 1])
            self.session.commit()
        else:
            print(f'Nothing to delete!\n')

    def missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < self.today.date()).all()
        if len(rows) != 0:
            count = 1
            for row in rows:
                print(f'{count}. {row.task}. {datetime.strftime(row.deadline, "%d %b")}')
                count += 1
            print()
        else:
            print(f'Missed tasks:\nNothing is missed!\n')

    def show_today(self):
        rows = self.session.query(Table).filter(Table.deadline == self.today.date()).all()
        if len(rows) != 0:
            count = 1
            for row in rows:
                print(f'{count}. {row.task}')
                count += 1
            print()
        else:
            print(f'Today {self.today.day} {self.today.strftime("%b")}:\nNothing to do!\n')

    def show_week(self):
        rows = self.session.query(Table)

        for i in range(7):
            day = self.today + timedelta(i)
            if len(rows.filter(Table.deadline == day.date()).all()) != 0:
                for row in rows.filter(Table.deadline == day.date()).all():
                    count = 1
                    print(f'{datetime.strftime(day, "%A %d %b")}:\n{count}. {row.task}\n')
                    count += 1
            else:
                print(f'{datetime.strftime(day, "%A %d %b")}:\nNothing to do!\n')

    def show_all(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if len(rows) != 0:
            count = 1
            for row in rows:
                print(f'{count}. {row.task}. {int(datetime.strftime(row.deadline, "%d"))} '
                      f'{datetime.strftime(row.deadline, "%b")}')
                count += 1
        else:
            print(f'Nothing to do!\n')


ToDoList('todo').start()

