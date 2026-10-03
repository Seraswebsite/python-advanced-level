import sqlite3
import hashlib
import secrets
import json
import csv
import logging
import threading
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path


# ============================================================
# NEXUS TASK MANAGER
# Advanced Python Project
# ============================================================

APP_NAME = "Nexus Task Manager"
VERSION = "1.0"

DATA_FOLDER = Path("nexus_data")
DATABASE = DATA_FOLDER / "nexus.db"
CONFIG_FILE = DATA_FOLDER / "config.json"
LOG_FILE = DATA_FOLDER / "nexus.log"

DATA_FOLDER.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {
    "theme": "default",
    "reminder_interval": 30,
    "page_size": 10,
    "auto_save": True
}


class Config:

    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):

        if not CONFIG_FILE.exists():
            self.save()
            return

        try:

            with open(CONFIG_FILE, "r") as file:
                saved = json.load(file)

            self.data.update(saved)

        except Exception as error:

            logging.error(error)

    def save(self):

        with open(CONFIG_FILE, "w") as file:
            json.dump(
                self.data,
                file,
                indent=4
            )

    def get(self, key, default=None):

        return self.data.get(
            key,
            default
        )

    def set(self, key, value):

        self.data[key] = value
        self.save()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def current_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    )

    return salt + "$" + password_hash.hex()


def check_password(password, stored_password):

    try:

        salt, original_hash = stored_password.split("$")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()

        return secrets.compare_digest(
            new_hash,
            original_hash
        )

    except Exception:

        return False


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class User:

    id: int
    username: str
    password: str
    created_at: str


@dataclass
class Task:

    id: int
    user_id: int
    title: str
    description: str
    category: str
    priority: int
    status: str
    due_date: str
    created_at: str
    updated_at: str
    completed_at: str


# ============================================================
# DATABASE
# ============================================================

class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.lock = threading.Lock()

        self.create_tables()

    # --------------------------------------------------------

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            description TEXT,

            category TEXT,

            priority INTEGER,

            status TEXT,

            due_date TEXT,

            created_at TEXT,

            updated_at TEXT,

            completed_at TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            action TEXT,

            data TEXT,

            created_at TEXT

        )
        """)

        self.connection.commit()

    # --------------------------------------------------------

    def create_user(
        self,
        username,
        password
    ):

        password = hash_password(password)

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, password, created_at)

            VALUES (?, ?, ?)
            """,
            (
                username,
                password,
                current_time()
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    # --------------------------------------------------------

    def find_user(self, username):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        return cursor.fetchone()

    # --------------------------------------------------------

    def add_task(
        self,
        user_id,
        title,
        description,
        category,
        priority,
        due_date
    ):

        now = current_time()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks(

                user_id,
                title,
                description,
                category,
                priority,
                status,
                due_date,
                created_at,
                updated_at,
                completed_at

            )

            VALUES(
                ?, ?, ?, ?, ?,
                'pending',
                ?, ?, ?, NULL
            )
            """,
            (
                user_id,
                title,
                description,
                category,
                priority,
                due_date,
                now,
                now
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    # --------------------------------------------------------

    def get_task(
        self,
        user_id,
        task_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tasks

            WHERE id = ?
            AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        )

        return cursor.fetchone()

    # --------------------------------------------------------

    def get_tasks(
        self,
        user_id,
        status=None
    ):

        cursor = self.connection.cursor()

        if status:

            cursor.execute(
                """
                SELECT *
                FROM tasks

                WHERE user_id = ?
                AND status = ?

                ORDER BY priority
                """,
                (
                    user_id,
                    status
                )
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM tasks

                WHERE user_id = ?

                ORDER BY priority
                """,
                (user_id,)
            )

        return cursor.fetchall()

    # --------------------------------------------------------

    def update_task(
        self,
        task_id,
        user_id,
        **changes
    ):

        allowed = [

            "title",
            "description",
            "category",
            "priority",
            "status",
            "due_date",
            "completed_at"

        ]

        parts = []

        values = []

        for key, value in changes.items():

            if key in allowed:

                parts.append(
                    key + " = ?"
                )

                values.append(value)

        parts.append(
            "updated_at = ?"
        )

        values.append(
            current_time()
        )

        values.extend(
            [
                task_id,
                user_id
            ]
        )

        query = f"""
        UPDATE tasks

        SET {", ".join(parts)}

        WHERE id = ?
        AND user_id = ?
        """

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            values
        )

        self.connection.commit()

    # --------------------------------------------------------

    def delete_task(
        self,
        task_id,
        user_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks

            WHERE id = ?
            AND user_id = ?
            """,
            (
                task_id,
                user_id
            )
        )

        self.connection.commit()

        return cursor.rowcount > 0

    # --------------------------------------------------------

    def search_tasks(
        self,
        user_id,
        keyword
    ):

        cursor = self.connection.cursor()

        keyword = "%" + keyword + "%"

        cursor.execute(
            """
            SELECT *
            FROM tasks

            WHERE user_id = ?

            AND (
                title LIKE ?
                OR description LIKE ?
                OR category LIKE ?
            )

            ORDER BY priority
            """,
            (
                user_id,
                keyword,
                keyword,
                keyword
            )
        )

        return cursor.fetchall()

    # --------------------------------------------------------

    def save_history(
        self,
        user_id,
        action,
        data
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO history(

                user_id,
                action,
                data,
                created_at

            )

            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                action,
                json.dumps(data),
                current_time()
            )
        )

        self.connection.commit()

    # --------------------------------------------------------

    def get_last_history(
        self,
        user_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM history

            WHERE user_id = ?

            ORDER BY id DESC

            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    # --------------------------------------------------------

    def statistics(
        self,
        user_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE user_id = ?
            """,
            (user_id,)
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks

            WHERE user_id = ?
            AND status = 'completed'
            """,
            (user_id,)
        )

        completed = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks

            WHERE user_id = ?
            AND status = 'pending'
            """,
            (user_id,)
        )

        pending = cursor.fetchone()[0]

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }


# ============================================================
# AUTHENTICATION
# ============================================================

class Authentication:

    def __init__(self, database):

        self.database = database

        self.current_user = None

    # --------------------------------------------------------

    def register(
        self,
        username,
        password
    ):

        username = username.strip()

        if len(username) < 3:

            raise ValueError(
                "Username must contain at least 3 characters."
            )

        if len(password) < 6:

            raise ValueError(
                "Password must contain at least 6 characters."
            )

        if self.database.find_user(username):

            raise ValueError(
                "Username already exists."
            )

        user_id = self.database.create_user(
            username,
            password
        )

        self.current_user = User(
            user_id,
            username,
            "hidden",
            current_time()
        )

    # --------------------------------------------------------

    def login(
        self,
        username,
        password
    ):

        user = self.database.find_user(
            username
        )

        if user is None:

            return False

        if not check_password(
            password,
            user["password"]
        ):

            return False

        self.current_user = User(
            user["id"],
            user["username"],
            user["password"],
            user["created_at"]
        )

        return True

    # --------------------------------------------------------

    def logout(self):

        self.current_user = None


# ============================================================
# TASK MANAGER
# ============================================================

class TaskManager:

    def __init__(
        self,
        database,
        authentication
    ):

        self.database = database

        self.authentication = authentication

    # --------------------------------------------------------

    @property
    def user_id(self):

        if self.authentication.current_user is None:

            raise RuntimeError(
                "You are not logged in."
            )

        return self.authentication.current_user.id

    # --------------------------------------------------------

    def create_task(
        self,
        title,
        description="",
        category="General",
        priority=3,
        due_date=None
    ):

        task_id = self.database.add_task(

            self.user_id,

            title,

            description,

            category,

            priority,

            due_date

        )

        self.database.save_history(

            self.user_id,

            "create",

            {
                "task_id": task_id
            }

        )

        return task_id

    # --------------------------------------------------------

    def complete_task(
        self,
        task_id
    ):

        task = self.database.get_task(
            self.user_id,
            task_id
        )

        if task is None:

            raise ValueError(
                "Task not found."
            )

        self.database.update_task(

            task_id,

            self.user_id,

            status="completed",

            completed_at=current_time()

        )

        return True

    # --------------------------------------------------------

    def reopen_task(
        self,
        task_id
    ):

        task = self.database.get_task(
            self.user_id,
            task_id
        )

        if task is None:

            raise ValueError(
                "Task not found."
            )

        self.database.update_task(

            task_id,

            self.user_id,

            status="pending",

            completed_at=None

        )

    # --------------------------------------------------------

    def delete_task(
        self,
        task_id
    ):

        task = self.database.get_task(
            self.user_id,
            task_id
        )

        if task is None:

            raise ValueError(
                "Task not found."
            )

        self.database.save_history(

            self.user_id,

            "delete",

            dict(task)

        )

        self.database.delete_task(

            task_id,

            self.user_id

        )


# ============================================================
# EXPORT SYSTEM
# ============================================================

class ExportManager:

    def __init__(
        self,
        database,
        authentication
    ):

        self.database = database

        self.authentication = authentication

    # --------------------------------------------------------

    def export_json(
        self,
        filename
    ):

        user_id = self.authentication.current_user.id

        tasks = self.database.get_tasks(
            user_id
        )

        data = []

        for task in tasks:

            data.append(
                dict(task)
            )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # --------------------------------------------------------

    def export_csv(
        self,
        filename
    ):

        user_id = self.authentication.current_user.id

        tasks = self.database.get_tasks(
            user_id
        )

        if not tasks:

            return

        fields = tasks[0].keys()

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()

            for task in tasks:

                writer.writerow(
                    dict(task)
                )


# ============================================================
# REMINDER SYSTEM
# ============================================================

class ReminderSystem(threading.Thread):

    def __init__(
        self,
        manager
    ):

        super().__init__(
            daemon=True
        )

        self.manager = manager

        self.running = True

    # --------------------------------------------------------

    def run(self):

        while self.running:

            try:

                if self.manager.authentication.current_user:

                    tasks = self.manager.database.get_tasks(
                        self.manager.user_id,
                        "pending"
                    )

                    for task in tasks:

                        if task["due_date"]:

                            print(
                                "\n[REMINDER]"
                            )

                            print(
                                "Task:",
                                task["title"]
                            )

            except Exception as error:

                logging.error(
                    error
                )

            time.sleep(60)

    # --------------------------------------------------------

    def stop(self):

        self.running = False


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

class Application:

    def __init__(self):

        self.config = Config()

        self.database = Database()

        self.authentication = Authentication(
            self.database
        )

        self.manager = TaskManager(
            self.database,
            self.authentication
        )

        self.exporter = ExportManager(
            self.database,
            self.authentication
        )

        self.reminder = ReminderSystem(
            self.manager
        )

        self.running = True

    # --------------------------------------------------------

    def banner(self):

        print()
        print("=" * 60)
        print("             NEXUS TASK MANAGER")
        print("=" * 60)
        print("Advanced Python Project")
        print("=" * 60)

    # --------------------------------------------------------

    def start(self):

        self.banner()

        self.authentication_screen()

    # --------------------------------------------------------

    def authentication_screen(self):

        while (
            self.running
            and
            self.authentication.current_user is None
        ):

            print()
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input(
                "Choose: "
            ).strip()

            if choice == "1":

                self.login()

            elif choice == "2":

                self.register()

            elif choice == "3":

                self.running = False

            else:

                print(
                    "Invalid choice."
                )

        if self.authentication.current_user:

            self.reminder.start()

            self.main_loop()

    # --------------------------------------------------------

    def register(self):

        print()
        print("----- REGISTER -----")

        username = input(
            "Username: "
        )

        password = input(
            "Password: "
        )

        confirm = input(
            "Confirm password: "
        )

        if password != confirm:

            print(
                "Passwords do not match."
            )

            return

        try:

            self.authentication.register(
                username,
                password
            )

            print(
                "Account created!"
            )

        except Exception as error:

            print(
                "Registration failed:",
                error
            )

    # --------------------------------------------------------

    def login(self):

        print()
        print("----- LOGIN -----")

        username = input(
            "Username: "
        )

        password = input(
            "Password: "
        )

        if self.authentication.login(
            username,
            password
        ):

            print(
                "Login successful!"
            )

        else:

            print(
                "Invalid username or password."
            )

    # --------------------------------------------------------

    def main_loop(self):

        print()
        print(
            "Type 'help' to see commands."
        )

        while (
            self.running
            and
            self.authentication.current_user
        ):

            try:

                command = input(
                    "\nnexus> "
                ).strip()

            except KeyboardInterrupt:

                print()

                break

            if not command:

                continue

            self.execute_command(
                command
            )

    # --------------------------------------------------------

    def execute_command(
        self,
        command
    ):

        parts = command.split()

        name = parts[0].lower()

        arguments = parts[1:]

        try:

            if name == "help":

                self.help()

            elif name == "add":

                self.add_task()

            elif name == "list":

                self.list_tasks()

            elif name == "done":

                self.complete(
                    arguments
                )

            elif name == "reopen":

                self.reopen(
                    arguments
                )

            elif name == "delete":

                self.delete(
                    arguments
                )

            elif name == "search":

                self.search(
                    arguments
                )

            elif name == "stats":

                self.statistics()

            elif name == "export":

                self.export(
                    arguments
                )

            elif name == "logout":

                self.logout()

            elif name == "quit":

                self.quit()

            else:

                print(
                    "Unknown command."
                )

        except Exception as error:

            print(
                "Error:",
                error
            )

    # --------------------------------------------------------

    def help(self):

        print()
        print("COMMANDS")
        print("-" * 40)

        commands = {

            "add":
                "Create a task",

            "list":
                "Show tasks",

            "done ID":
                "Complete a task",

            "reopen ID":
                "Reopen a task",

            "delete ID":
                "Delete a task",

            "search TEXT":
                "Search tasks",

            "stats":
                "Show statistics",

            "export json FILE":
                "Export JSON",

            "export csv FILE":
                "Export CSV",

            "logout":
                "Logout",

            "quit":
                "Exit"

        }

        for command, description in commands.items():

            print(
                f"{command:<20} {description}"
            )

    # --------------------------------------------------------

    def add_task(self):

        print()
        print("----- NEW TASK -----")

        title = input(
            "Title: "
        ).strip()

        if not title:

            print(
                "Title cannot be empty."
            )

            return

        description = input(
            "Description: "
        )

        category = input(
            "Category: "
        )

        if not category:

            category = "General"

        priority_text = input(
            "Priority 1-5 [3]: "
        )

        if not priority_text:

            priority = 3

        else:

            priority = int(
                priority_text
            )

        if priority < 1 or priority > 5:

            print(
                "Priority must be 1-5."
            )

            return

        due_date = input(
            "Due date: "
        )

        task_id = self.manager.create_task(

            title,

            description,

            category,

            priority,

            due_date or None

        )

        print(
            f"Task #{task_id} created!"
        )

    # --------------------------------------------------------

    def list_tasks(self):

        tasks = self.database.get_tasks(
            self.authentication.current_user.id
        )

        print()

        if not tasks:

            print(
                "No tasks."
            )

            return

        print(
            f"{'ID':<5}"
            f"{'STATUS':<15}"
            f"{'PRI':<5}"
            f"{'CATEGORY':<15}"
            f"TITLE"
        )

        print(
            "-" * 70
        )

        for task in tasks:

            print(
                f"{task['id']:<5}"
                f"{task['status']:<15}"
                f"{task['priority']:<5}"
                f"{task['category']:<15}"
                f"{task['title']}"
            )

    # --------------------------------------------------------

    def complete(
        self,
        arguments
    ):

        if not arguments:

            print(
                "Usage: done ID"
            )

            return

        task_id = int(
            arguments[0]
        )

        self.manager.complete_task(
            task_id
        )

        print(
            "Task completed!"
        )

    # --------------------------------------------------------

    def reopen(
        self,
        arguments
    ):

        if not arguments:

            print(
                "Usage: reopen ID"
            )

            return

        task_id = int(
            arguments[0]
        )

        self.manager.reopen_task(
            task_id
        )

        print(
            "Task reopened!"
        )

    # --------------------------------------------------------

    def delete(
        self,
        arguments
    ):

        if not arguments:

            print(
                "Usage: delete ID"
            )

            return

        task_id = int(
            arguments[0]
        )

        task = self.database.get_task(
            self.authentication.current_user.id,
            task_id
        )

        if task is None:

            print(
                "Task not found."
            )

            return

        confirm = input(
            f"Delete '{task['title']}'? y/n: "
        )

        if confirm.lower() == "y":

            self.manager.delete_task(
                task_id
            )

            print(
                "Task deleted."
            )

        else:

            print(
                "Cancelled."
            )

    # --------------------------------------------------------

    def search(
        self,
        arguments
    ):

        if not arguments:

            print(
                "Usage: search TEXT"
            )

            return

        keyword = " ".join(
            arguments
        )

        tasks = self.database.search_tasks(

            self.authentication.current_user.id,

            keyword

        )

        print()

        for task in tasks:

            print(
                f"#{task['id']} - "
                f"{task['title']} "
                f"[{task['category']}]"
            )

        if not tasks:

            print(
                "No matching tasks."
            )

    # --------------------------------------------------------

    def statistics(self):

        data = self.database.statistics(

            self.authentication.current_user.id

        )

        print()
        print("----- STATISTICS -----")

        print(
            "Total:",
            data["total"]
        )

        print(
            "Completed:",
            data["completed"]
        )

        print(
            "Pending:",
            data["pending"]
        )

        if data["total"]:

            percentage = (
                data["completed"]
                /
                data["total"]
                *
                100
            )

            print(
                "Completion:",
                round(
                    percentage,
                    2
                ),
                "%"
            )

    # --------------------------------------------------------

    def export(
        self,
        arguments
    ):

        if len(arguments) < 2:

            print(
                "Usage: export json FILE"
            )

            return

        format_name = arguments[0]

        filename = arguments[1]

        if format_name == "json":

            self.exporter.export_json(
                filename
            )

            print(
                "JSON exported."
            )

        elif format_name == "csv":

            self.exporter.export_csv(
                filename
            )

            print(
                "CSV exported."
            )

        else:

            print(
                "Unknown format."
            )

    # --------------------------------------------------------

    def logout(self):

        self.authentication.logout()

        self.reminder.stop()

        print(
            "Logged out."
        )

        self.running = False

    # --------------------------------------------------------

    def quit(self):

        self.running = False

        self.reminder.stop()

        print(
            "Goodbye!" 
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

def main():

    application = Application()

    try:

        application.start()

    except Exception as error:

        logging.exception(
            "Application crashed"
        )

        print(
            "Fatal error:",
            error
        )


if __name__ == "__main__":

    main()