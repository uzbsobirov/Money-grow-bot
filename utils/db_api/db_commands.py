from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        user_id BIGINT NOT NULL UNIQUE,
        join_date DATE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_user_data(self):
        sql = """
        CREATE TABLE IF NOT EXISTS UserData (
        id SERIAL PRIMARY KEY,
        user_id BigInt UNIQUE,
        balance BigInt,
        type_invest TEXT NULL,
        end_invest_date BigInt,
        parent_id BigInt,
        count BigInt,
        join_date DATE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_sponsor(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Sponsor (
        id SERIAL PRIMARY KEY,
        chat_id TEXT UNIQUE,
        chat_title TEXT,
        chat_type TEXT,
        chat_link TEXT,
        join_date DATE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name: str, username: str, user_id: int, join_date: str):
        sql = "INSERT INTO users (full_name, username, user_id, join_date) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, full_name, username, user_id, join_date, fetchrow=True)

    async def add_user_data(self, user_id: str, balance: str, type_invest: int, end_invest_date: int, parent_id, count, join_date: str):
        sql = "INSERT INTO UserData (user_id, balance, type_invest, end_invest_date, parent_id, count, join_date) " \
              "VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, user_id, balance, type_invest, end_invest_date, parent_id, count, join_date, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_sponsor(self):
        sql = "SELECT * FROM Sponsor"
        return await self.execute(sql, fetch=True)

    async def select_one_users(self, user_id):
        sql = "SELECT * FROM Users WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def select_user_data(self, user_id):
        sql = "SELECT * FROM UserData WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_issubs(self, issubs, user_id):
        sql = "UPDATE Users SET issubs=$1 WHERE user_id=$2"
        return await self.execute(sql, issubs, user_id, execute=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM Users WHERE user_id=$1"
        await self.execute(sql, user_id, execute=True)

    async def drop_courses(self):
        await self.execute("DROP TABLE Courses", execute=True)
