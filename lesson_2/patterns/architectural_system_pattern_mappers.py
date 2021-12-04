import copy
import sqlite3


class Mapper:
    def __init__(self, connection: sqlite3.Connection, class_):
        self.connection = connection
        self.class_ = class_
        self.tablename = class_.__tablename__

    def __object_list_from_cursor(self, cursor):
        result = []
        column_names = list(map(lambda x: x[0], cursor.description))
        for item in cursor.fetchall():
            obj = self.class_()
            for idx, column in enumerate(column_names):
                if hasattr(obj, column):
                    setattr(obj, column, item[idx])
            result.append(obj)
        return result

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        cursor = self.connection.cursor()
        cursor.execute(statement)

        return self.__object_list_from_cursor(cursor)

    def find_by_id(self, id):
        statement = f"SELECT * FROM {self.tablename} WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(statement, (id,))
        # result = cursor.fetchone()
        result = self.__object_list_from_cursor(cursor)
        if result:
            return result[0]
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        dict_obj = copy.deepcopy(obj.__dict__)
        # Исключаем id
        if 'id' in dict_obj:
            del dict_obj['id']
        for i in copy.deepcopy(dict_obj):
            if isinstance(dict_obj[i], list):
                del dict_obj[i]

        col_names = list(dict_obj.keys())
        statement = f"INSERT INTO {self.tablename} ({', '.join(col_names)}) VALUES ({', '.join('?' for _ in col_names)})"
        cursor = self.connection.cursor()
        cursor.execute(statement, tuple(dict_obj.values()))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        dict_obj = copy.deepcopy(obj.__dict__)
        # Исключаем id
        if 'id' in dict_obj:
            del dict_obj['id']
        col_names = list(dict_obj.keys())
        set_names = [f'{x}=?' for x in col_names]

        statement = f"UPDATE {self.tablename} SET {', '.join(set_names)} WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        cursor = self.connection.cursor()
        values = list(dict_obj.values())
        values.append(obj.id)
        cursor.execute(statement, tuple(values))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


def main():
    connection = sqlite3.connect('patterns.sqlite')
    from patterns.сreational_patterns import User
    c = Mapper(connection, User)
    c.all()
    # obj = c.find_by_id(1)
    # obj.name = 'user2'
    # c.insert(obj)
    obj = c.find_by_id(2)
    obj.name = 'user3'
    c.update(obj)

    c.delete(obj)

    print()


if __name__ == '__main__':
    main()
