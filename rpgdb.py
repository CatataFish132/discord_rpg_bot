#!/usr/bin/python
import psycopg2
from configparser import ConfigParser


class RpgDb:
    def __init__(self):
        parser = ConfigParser()
        parser.read('database.ini')
        params = parser.items("postgresql")
        db = {}
        for param in params:
            db[param[0]] = param[1]
        self.conn = psycopg2.connect(**db)

    def is_registered(self, discord_id):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM players WHERE discord_id = %s"
        cursor.execute(sql, (discord_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        return True

    def get_inventory(self, discord_id):
        """gets the inventory of the selected character

        RETURNS:
            DICT: {(item_id, item_name): amount}"""
        cursor = self.conn.cursor()
        sql = """SELECT items.item_id, items.item_name FROM inventory 
                  INNER JOIN players ON players.discord_id = %s
                  INNER JOIN items ON inventory.item_id = items.item_id
                  WHERE players.character_id = inventory.character_id"""
        cursor.execute(sql, (discord_id,))
        rows = cursor.fetchall()
        my_dict = {i: rows.count(i) for i in rows}
        return my_dict

    def create_class(self, name):
        cursor = self.conn.cursor()
        sql = "INSERT INTO classes(name) VALUES(%s)"
        cursor.execute(sql, (name,))
        self.conn.commit()
        cursor.close()

    def create_character(self, name, class_ID, player_ID):
        cursor = self.conn.cursor()
        sql = "INSERT INTO characters(name, class_id, discord_id) VALUES(%s,%s,%s)"
        cursor.execute(sql, (name, class_ID, player_ID))
        self.conn.commit()
        cursor.close()

    def create_player(self, discord_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO players(discord_id) VALUES(%s)"
        cursor.execute(sql, (discord_id,))
        self.conn.commit()
        cursor.close()

    def create_item(self):
        name = input("item_name: ")
        cursor = self.conn.cursor()
        sql = "INSERT INTO items(item_name) VALUES(%s)"
        cursor.execute(sql, (name,))
        self.conn.commit()
        cursor.close()

    def get_all_items(self):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM items"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def give_item(self, item_id, character_id):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO inventory(item_id, character_id) VALUES(%s,%s)"
            cursor.execute(sql, (item_id, character_id))
        except Exception as e:
            print(e)
        self.conn.commit()
        cursor.close()

    def get_all_character(self, discord_id):
        cursor = self.conn.cursor()
        sql = "SELECT characters.character_id, characters.name, characters.gold, characters.health, characters.mana, " \
              "classes.name FROM characters INNER JOIN classes ON characters.class_id = classes.class_id " \
              "WHERE characters.discord_id = %s;"
        cursor.execute(sql, (discord_id,))
        rows = cursor.fetchall()
        final_list = []
        for row in rows:
            values = {"character_id": row[0],
                      "name": row[1],
                      "gold": row[2],
                      "health": row[3],
                      "mana": row[4],
                      "class_name": row[5],
                      }
            final_list.append(values)
        return final_list

    def select_character(self, character_id, discord_id):
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE players SET character_id = %s WHERE discord_id = %s;"
            cursor.execute(sql, (character_id, discord_id))
            self.conn.commit()
        except:
            return False
        return True

    def get_selected_character_id(self, discord_id):
        cursor = self.conn.cursor()
        sql = "SELECT character_id from players WHERE discord_id = %s"
        cursor.execute(sql, (discord_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return row[0]

    def get_selected_character(self, discord_id):
        """"gets the selected character.

        RETURNS:
            dict: {name, health, mana, gold, class_name}"""

        cursor = self.conn.cursor()
        sql = """SELECT characters.name, characters.health, characters.mana, characters.gold, classes.name 
        FROM players INNER JOIN characters ON characters.character_id = players.character_id
         INNER JOIN classes ON classes.class_id = characters.class_id WHERE players.discord_id = %s;"""
        cursor.execute(sql, (discord_id,))
        rows = cursor.fetchone()
        values = {"name": rows[0],
                  "health": rows[1],
                  "mana": rows[2],
                  "gold": rows[3],
                  "class_name": rows[4]}
        return values

    def get_characters(self, discord_id):
        cursor = self.conn.cursor()
        sql = """SELECT classes.name, characters.name, characters.gold, characters.character_id 
        FROM characters INNER JOIN classes ON characters.class_id = classes.class_id 
        WHERE discord_id = %s"""
        cursor.execute(sql, (discord_id,))
        rows = cursor.fetchall()
        return rows

    def get_all_classes(self):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM classes"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def get_equipment(self, discord_id):
        cursor = self.conn.cursor()
        sql = """SELECT characters.weapon_id, characters.helmet_id, characters.chestplate_id, 
                 characters.pants_id, characters.shoes_id FROM characters WHERE characters.discord_id = %s;"""
        cursor.execute(sql, (discord_id,))
        weapon_id, helmet_id, chestplate_id, pants_id, shoes_id = cursor.fetchone()
        sql = "SELECT "

    def get_weapon(self, weapon_id):
        """gets weapon

        RETURNS:
                DICT: {id, damage_value}"""
        cursor = self.conn.cursor()
        sql = """SELECT weapons.weapon_id, items.item_name, weapons.damage_value 
                 FROM weapons INNER JOIN items ON weapons.weapon_id = items.weapon_id WHERE weapons.weapon_id = %s"""
        cursor.execute(sql, (weapon_id,))
        weapon_id, name, damage_value = cursor.fetchone()
        values = {"id": weapon_id, "damage_value": damage_value, "name": name}
        return values

    def add_weapon(self, name: str, damage_value: float):
        cursor = self.conn.cursor()
        sql = "INSERT INTO weapons(damage_value) VALUES(%s) RETURNING weapon_id;"
        cursor.execute(sql, (damage_value,))
        weapon_id, = cursor.fetchone()
        sql = """INSERT INTO items(is_weapon, item_name, weapon_id)
                 VALUES(True, %s, %s)"""
        cursor.execute(sql, (name, weapon_id))
        self.conn.commit()

    def add_armor(self, name: str, protection_value: float, is_helmet=False,
                  is_chestplate=False, is_pants=False, is_shoes=False):
        try:
            cursor = self.conn.cursor()
            sql = """INSERT INTO armor(is_helmet, is_chestplate, is_pant, is_shoes, protection_value) 
                     VALUES(%s, %s, %s, %s, %s) RETURNING armor_id"""
            cursor.execute(sql, (is_helmet, is_chestplate, is_pants, is_shoes, protection_value))
            armor_id, = cursor.fetchone()
            sql = """INSERT INTO items(is_armor, item_name, armor_id) VALUES(True, %s, %s)"""
            cursor.execute(sql, (name, armor_id))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

obj = RpgDb()
#print(obj.get_weapon(14))
obj.add_armor("iron chestplate", 20, is_chestplate=True)
#obj.add_weapon("godkiller sword", 500)
#print(obj.get_all_character(284769523020595200))