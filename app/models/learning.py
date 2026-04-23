import sqlite3
from typing import List, Dict, Optional
import json

DATABASE_PATH = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Subject:
    @staticmethod
    def create(user_id: int, name: str) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subjects (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        conn.commit()
        subject_id = cursor.lastrowid
        conn.close()
        return subject_id

    @staticmethod
    def get_all_by_user(user_id: int) -> List[Dict]:
        conn = get_db_connection()
        subjects = conn.execute(
            "SELECT * FROM subjects WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(s) for s in subjects]

class Note:
    @staticmethod
    def create(user_id: int, original_text: str, summary: str, title: str = "", subject_id: Optional[int] = None) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (user_id, subject_id, title, original_text, summary) VALUES (?, ?, ?, ?, ?)",
            (user_id, subject_id, title, original_text, summary)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return note_id

    @staticmethod
    def get_by_id(note_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        note = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
        conn.close()
        return dict(note) if note else None

    @staticmethod
    def get_all_by_user(user_id: int) -> List[Dict]:
        conn = get_db_connection()
        notes = conn.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(n) for n in notes]

class Quiz:
    @staticmethod
    def create(user_id: int, note_id: int) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quizzes (user_id, note_id) VALUES (?, ?)",
            (user_id, note_id)
        )
        conn.commit()
        quiz_id = cursor.lastrowid
        conn.close()
        return quiz_id

    @staticmethod
    def update_score(quiz_id: int, score: int):
        conn = get_db_connection()
        conn.execute(
            "UPDATE quizzes SET score = ? WHERE id = ?",
            (score, quiz_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(quiz_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        quiz = conn.execute(
            "SELECT * FROM quizzes WHERE id = ?", (quiz_id,)
        ).fetchone()
        conn.close()
        return dict(quiz) if quiz else None

class Question:
    @staticmethod
    def create(quiz_id: int, question_text: str, options: list, correct_answer: str, explanation: str = "") -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO questions (quiz_id, question_text, options, correct_answer, explanation) VALUES (?, ?, ?, ?, ?)",
            (quiz_id, question_text, json.dumps(options), correct_answer, explanation)
        )
        conn.commit()
        question_id = cursor.lastrowid
        conn.close()
        return question_id

    @staticmethod
    def get_all_by_quiz(quiz_id: int) -> List[Dict]:
        conn = get_db_connection()
        questions = conn.execute(
            "SELECT * FROM questions WHERE quiz_id = ?", 
            (quiz_id,)
        ).fetchall()
        conn.close()
        
        results = []
        for q in questions:
            q_dict = dict(q)
            q_dict['options'] = json.loads(q_dict['options'])
            results.append(q_dict)
        return results

class UserAnswer:
    @staticmethod
    def create(quiz_id: int, question_id: int, user_answer: str, is_correct: bool) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_answers (quiz_id, question_id, user_answer, is_correct) VALUES (?, ?, ?, ?)",
            (quiz_id, question_id, user_answer, is_correct)
        )
        conn.commit()
        answer_id = cursor.lastrowid
        conn.close()
        return answer_id

    @staticmethod
    def get_all_by_quiz(quiz_id: int) -> List[Dict]:
        conn = get_db_connection()
        answers = conn.execute(
            "SELECT * FROM user_answers WHERE quiz_id = ?", 
            (quiz_id,)
        ).fetchall()
        conn.close()
        return [dict(a) for a in answers]
