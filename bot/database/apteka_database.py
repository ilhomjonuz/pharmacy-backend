from datetime import datetime

import aiomysql
import asyncio
from environs import Env

env = Env()
env.read_env('.env')


class Apteka_Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        # Create the connection pool
        self.pool = await aiomysql.create_pool(
            host=env.str('MYSQL_HOST'),
            port=env.int('MYSQL_PORT'),
            user=env.str('MYSQL_USER'),
            password=env.str('MYSQL_PASSWORD'),
            db=env.str('MYSQL_DATABASE'),
            autocommit=True
        )

    async def execute(self, query, args: tuple = (), fetchone=False, fetchall=False):
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                if fetchone:
                    return await cur.fetchone()
                elif fetchall:
                    return await cur.fetchall()
                else:
                    return None

    async def add_type(self, name_uz, name_ru, name_en, id=None, *args):
        query = ("INSERT INTO types (name, name_uz, name_ru, name_en, created_at, updated_at)"
                 "VALUES (%s, %s, %s, %s, %s, %s);")
        await self.execute(query, (name_uz, name_uz, name_ru, name_en, datetime.now(), datetime.now()))

    async def select_types(self):
        query = "SELECT id, name FROM types;"
        return await self.execute(query, fetchall=True)

    async def select_type(self, id):
        query = "SELECT id, name, name_ru, name_en FROM types WHERE id=%s;"
        return await self.execute(query, (id,), fetchone=True)

    async def delete_type(self, id):
        # Assuming `type_id` can be set to NULL or you have a default type_id
        update_query = "UPDATE pills SET type_id = NULL WHERE type_id = %s;"
        await self.execute(update_query, (id,))

        # Now, attempt to delete the type
        delete_query = "DELETE FROM types WHERE id = %s;"
        await self.execute(delete_query, (id,))

    async def update_type(self, id, name_uz, name_ru, name_en):
        query = "UPDATE types SET name = %s, name_uz = %s, name_ru = %s, name_en = %s WHERE id = %s;"
        await self.execute(query, (name_uz, name_uz, name_ru, name_en, id))

    async def category_add(self, name_uz, name_ru, name_en, id=None, *args):
        query = "INSERT INTO categories (name, name_uz, name_ru, name_en) VALUES (%s, %s, %s, %s);"
        await self.execute(query, (name_uz, name_uz, name_ru, name_en))

    async def select_categories(self):
        query = "SELECT id, name FROM categories;"
        return await self.execute(query, fetchall=True)

    async def select_category(self, id):
        query = "SELECT id, name, name_ru, name_en FROM categories WHERE id=%s;"
        return await self.execute(query, (id,), fetchone=True)

    async def delete_category(self, id):
        update_query = "UPDATE pills_categories SET category_id = NULL WHERE category_id = %s;"
        await self.execute(update_query, (id))

        # Now, attempt to delete the category
        delete_query = "DELETE FROM categories WHERE id = %s;"
        await self.execute(delete_query, (id))

    async def update_category(self, id, name_uz, name_ru, name_en):
        query = "UPDATE categories SET name = %s, name_uz = %s, name_ru = %s, name_en = %s WHERE id = %s;"
        await self.execute(query, (name_uz, name_uz, name_ru, name_en, id))

    # ---------------------------------------------------------->

    async def select_partners(self):
        query = "SELECT id, picture FROM partners"
        return await self.execute(query, fetchall=True)

    async def select_partner(self, id):
        query = "SELECT id, picture FROM partners WHERE id = %s"
        return await self.execute(query, (id,), fetchone=True)

    async def add_partner(self, image_id: str):
        query = "INSERT INTO partners (picture) VALUES (%s)"
        await self.execute(query, (str(image_id),))

    async def delete_partner(self, partner_id: int):
        query = "DELETE FROM partners WHERE id = %s"
        await self.execute(query, args=(partner_id,))

    async def execute_query(self, query: str, *params):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *params)

    async def update_partner(self, partner_id: int, image_path: str):
        query = "UPDATE partners SET picture = %s WHERE id = %s"
        await self.execute(query, (image_path, partner_id))

    # ---------------------------------------------------------->

    async def doctor_add(self, fullname, direction_uz, direction_ru, direction_en, call, body_uz, body_ru, body_en,
                         picture,
                         published, id=None, *args):
        query = (
            "INSERT INTO doctors (fullname, direction, direction_uz, direction_ru, direction_en, `call`, "
            "body, body_uz, body_ru, body_en, published, created_at, updated_at, picture) "
            "VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        await self.execute(query, (
            fullname, direction_uz, direction_uz, direction_ru, direction_en, call, body_uz, body_uz, body_ru, body_en,
            published, datetime.now(), datetime.now(), picture))

    async def select_doctors(self):
        query = "SELECT id, fullname FROM doctors;"
        return await self.execute(query, fetchall=True)

    async def select_doctor(self, id):
        query = ("SELECT fullname, direction_uz, direction_ru, direction_en, body_uz, body_ru, "
                 "body_en,`call`, published, picture FROM doctors WHERE id = %s;")
        return await self.execute(query, (id,), fetchone=True)

    async def delete_doctor(self, id: int):
        query = "DELETE FROM doctors WHERE id = %s"
        await self.execute(query, args=(id,))

    async def update_doctor(self, fullname, direction_uz, direction_ru, direction_en, call, body_uz, body_ru, body_en,
                            picture, published, id, *args):
        query = ("UPDATE doctors SET fullname = %s, direction_uz = %s, direction_ru = %s, direction_en = %s, "
                 "body_uz = %s, body_ru = %s, body_en = %s,`call` = %s, published = %s,  picture = %s,"
                 "updated_at = %s WHERE id = %s")
        await self.execute(query, (fullname, direction_uz, direction_ru, direction_en, body_uz, body_ru, body_en, call,
                                   published, picture, datetime.now(), id))

    # ---------------------------------------------------------->

    async def add_izoh(self, author, body):
        query = "INSERT INTO comments (author, body, created_at) VALUES (%s, %s, %s)"
        await self.execute(query, (author, body, datetime.now().date()))

    async def update_izoh(self, id, author, body):
        query = "UPDATE comments SET author = %s, body = %s WHERE id = %s"
        await self.execute(query, (author, body, id))

    async def select_izoh(self, id):
        query = ("SELECT id, author, body, created_at "
                 "FROM comments WHERE id = %s;")
        return await self.execute(query, (id,), fetchone=True)

    async def delete_izoh(self, id: int):
        query = "DELETE FROM comments WHERE id = %s"
        await self.execute(query, args=(id,))

    async def select_comments(self):
        query = ("SELECT id, author "
                 "FROM comments;")
        return await self.execute(query, fetchall=True)

        # ---------------------------------------------------------->

    async def add_medication(self, name_uz, name_ru, name_en, body_uz, body_ru, body_en,
                             information_uz, information_ru, information_en,
                             price, expiration_date, picture, rank=5, published=False, popular=False):
        query = """
            INSERT INTO pills (name, name_uz, name_ru, name_en, body, body_uz, body_ru, body_en, information, information_uz, information_ru, 
            information_en, price, expiration_date, created_at, updated_at, picture, `rank`, published, popular)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        await self.execute(query, (
            name_uz, name_uz, name_ru, name_en, body_uz, body_uz, body_ru, body_en, information_uz, information_uz,
            information_ru, information_en, price, expiration_date, datetime.now(), datetime.now(), picture, rank,
            published, popular))

    async def update_medication(self, id, name_uz, name_ru, name_en, body_uz, body_ru, body_en,
                                information_uz, information_ru, information_en,
                                price, expiration_date, picture, rank=5, published=False, popular=False):
        query = """
        UPDATE pills
        SET name = %s, name_uz = %s, name_ru = %s, name_en = %s, body = %s, body_uz = %s, body_ru = %s, body_en = %s, information = %s, information_uz = %s, information_ru = %s, 
            information_en = %s, price = %s, expiration_date = %s, created_at = %s, updated_at = %s, picture = %s, `rank` = %s, published = %s, popular = %s
        WHERE id = %s
        """
        await self.execute(query, (
            name_uz, name_uz, name_ru, name_en, body_uz, body_uz, body_ru, body_en, information_uz, information_uz,
            information_ru, information_en, price, expiration_date, datetime.now(), datetime.now(), picture, rank,
            published, popular, id))

    async def select_medication(self, id):
        query = """
        SELECT id, name_uz, name_ru, name_en, information_uz, price, picture, expiration_date, discount_price
        FROM pills WHERE id = %s;
        """
        return await self.execute(query, (id,), fetchone=True)

    async def delete_medication(self, id: int):
        query = "DELETE FROM pills WHERE id = %s"
        await self.execute(query, (id,))

    async def select_medications(self):
        query = """
        SELECT id, name
        FROM pills;
        """
        return await self.execute(query, fetchall=True)
