from easygui import passwordbox
from mysql.connector import connect, Error


db = connect(
  host=input("Enter Host: "),
  user=input("Enter User: "),
  password=passwordbox("Enter Password: ")
)


def create_db(chat_id):
    try:
        cursor = db.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `log_{chat_id}` DEFAULT CHARACTER SET utf8;"
                       f"USE `log_{chat_id}`)")
    except Error as e:
        print(e)


def create_members_table(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `Members` ("
                     f"`idMembers` VARCHAR(225) NOT NULL,"
                     f"`isCurator` TINYINT(1) NOT NULL,"
                     f"PRIMARY KEY (`idMembers`),"
                     f"UNIQUE INDEX `idMembers_UNIQUE` (`idMembers` ASC) VISIBLE)")
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def create_messages_table(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `Messages` ("
                       f"`idMessages` VARCHAR(225) NOT NULL,"
                       f"`fromMember` VARCHAR(225) NOT NULL,"
                       f"`text` MEDIUMTEXT NOT NULL,"
                       f"`date` DATE NOT NULL,"
                       f"`replied` TINYINT(1) NOT NULL,"
                       f"PRIMARY KEY (`idMessages`),"
                       f"INDEX `fk_Messages_Members_idx` (`fromMember` ASC) VISIBLE,"
                       f"UNIQUE INDEX `idMessages_UNIQUE` (`idMessages` ASC) VISIBLE,"
                       f"CONSTRAINT `fk_Messages_Members`"
                       f"FOREIGN KEY (`fromMember`)"
                       f"REFERENCES `Members` (`idMembers`)"
                       f"ON DELETE CASCADE "
                       f"ON UPDATE CASCADE)")
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def create_replies_table(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `Replies` ("
                       f"`idReplies` VARCHAR(225) NOT NULL,"
                       f"`fromMember` VARCHAR(225) NOT NULL,"
                       f"`text` MEDIUMTEXT NULL,"
                       f"`date` DATE NULL,"
                       f"`interval` DECIMAL(8,4) NULL,"
                       f"`replied_message` VARCHAR(225),"
                       f"PRIMARY KEY (`idReplies`),"
                       f"INDEX `fk_Replies_Members1_idx` (`fromMember` ASC) VISIBLE,"
                       f"UNIQUE INDEX `idReplies_UNIQUE` (`idReplies` ASC) VISIBLE,"
                       f"CONSTRAINT `fk_Replies_Members1` "
                       f"FOREIGN KEY (`fromMember`)"
                       f"REFERENCES `Members` (`idMembers`) "
                       f"ON DELETE CASCADE "
                       f"ON UPDATE CASCADE)")
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def insert_member(user_id, user_status, chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        member_insert = f"INSERT INTO `log_{chat_id}`.`Members` (" \
                        f"`idMembers`, `isCurator`)" \
                        f" VALUES (%s, %s);"
        values = (str(user_id), user_status)
        cursor.execute(member_insert, values)
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def insert_message(message_id, user_id, message_body, message_date, is_replied, chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        message_insert = f"INSERT INTO `log_{chat_id}`.`Messages` (" \
                        f"`idMessages`, `fromMember`, `text`, `date`, `replied`)" \
                        f" VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(message_insert, (message_id, user_id, message_body, message_date, is_replied))
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def insert_reply(reply_id, user_id, reply_body, reply_date, interval, message_id, chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        reply_insert = f"INSERT INTO `log_{chat_id}`.`Replies` (" \
                        f"`idReplies`, `fromMember`, `text`, `date`, `interval`, `replied_message`)" \
                        f" VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(reply_insert, (reply_id, user_id, reply_body, reply_date, interval, message_id))
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def update_message(message_id, is_replied, chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        message_update = f"UPDATE `log_{chat_id}`.`messages` SET " \
                          f"`replied` = (%s) WHERE (`idMessages` = (%s));"
        cursor.execute(message_update, (is_replied, message_id))
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def update_user(user_id, is_replied, chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        message_update = f"UPDATE `log_{chat_id}`.`members` SET " \
                          f"`isCurator` = (%s) WHERE (`idMembers` = (%s));"
        cursor.execute(message_update, (is_replied, user_id))
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def select_interval(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `fromMember`,`interval` "
                       f"FROM `log_{chat_id}`.`replies`;")
        db.commit()
        cursor.close()
    except Error as e:
        print(e)


def select_messages(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `idMessages`, `replied`"
                       f"FROM `log_{chat_id}`.`messages`;")
        result = cursor.fetchall()
        result_dict = {}
        for i in result:
            result_dict[i[0]] = i[1]
        db.commit()
        cursor.close()
        return result_dict
    except Error as e:
        print(e)


def get_nreplied(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `text` FROM "
                       f"`log_{chat_id}`.`messages` "
                       f"WHERE `replied` = 0;")
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(i)
        db.commit()
        cursor.close()
        return result_list
    except Error as e:
        print(e)


def select_students(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `idMembers` FROM "
                       f"`log_{chat_id}`.`members` "
                       f"WHERE `isCurator` = 0;")
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(str(i).strip("'(),"))
        db.commit()
        cursor.close()
        return result_list
    except Error as e:
        print(e)


def select_curators(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `idMembers` FROM "
                       f"`log_{chat_id}`.`members` "
                       f"WHERE `isCurator` = 1;")
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(str(i).strip("'(),"))
        db.commit()
        cursor.close()
        return result_list
    except Error as e:
        print(e)


def select_message_reply_interval(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `interval` FROM `log_{chat_id}`.`replies` "
                       f"WHERE `replied_message` IN "
                       f"(SELECT `idMessages` FROM `log_{chat_id}`.`messages`);")
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(float(i[0]))
        db.commit()
        cursor.close()
        return result_list
    except Error as e:
        print(e)


def select_curator_interval(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `idReplies`, `fromMember`, `interval` FROM `log_{chat_id}`.`replies` "
                       f"WHERE `fromMember` IN "
                       f"(SELECT `idMembers` FROM `log_{chat_id}`.members WHERE `isCurator` = 1);")
        result = cursor.fetchall()
        result_dict = {}
        for i in result:
            result_dict[i[0]] = [i[1], i[2]]
        db.commit()
        cursor.close()
        return result_dict
    except Error as e:
        print(e)


def select_messages_id(chat_id):
    try:
        db.connect(database=f"log_{chat_id}")
        cursor = db.cursor()
        cursor.execute(f"SELECT `idMessages` FROM `log_{chat_id}`.messages;")
        result = cursor.fetchall()
        result_list = []
        for i in result:
            result_list.append(str(i).strip("()',"))
        db.commit()
        cursor.close()
        return result_list
    except Error as e:
        print(e)


print(db)

