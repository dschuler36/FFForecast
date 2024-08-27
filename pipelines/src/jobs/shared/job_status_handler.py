import psycopg2
from psycopg2 import sql
from datetime import datetime

from jobs.shared.settings import settings


# TODO: this feels like it should be driven from an api but it'll work for now
class JobStatusHandler:
    def __init__(self, job: str, status: str, season: int, week: int, stats_season: int, stats_week: int,
                 roster_season: int, roster_week: int, depth_season: int, depth_week: int, completed_time: datetime):
        self.job = job
        self.status = status
        self.season = season
        self.week = week
        self.stats_season = stats_season
        self.stats_week = stats_week
        self.roster_season = roster_season
        self.roster_week = roster_week
        self.depth_season = depth_season
        self.depth_week = depth_week
        self.completed_time = completed_time

    @staticmethod
    def create_connection():
        try:
            connection = psycopg2.connect(settings.POSTGRES_CONN_STRING)
            return connection
        except Exception as e:
            print(f"Error creating database connection: {e}")
            return None

    def insert_into_db(self):
        connection = self.create_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO job_tracker (job, status, season, week, stats_season, stats_week, 
                                             roster_season, roster_week, depth_season, depth_week, completed_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING job_id;
                """)

                cursor.execute(insert_query, (
                    self.job,
                    self.status,
                    self.season,
                    self.week,
                    self.stats_season,
                    self.stats_week,
                    self.roster_season,
                    self.roster_week,
                    self.depth_season,
                    self.depth_week,
                    self.completed_time
                ))

                connection.commit()
                job_id = cursor.fetchone()[0]
                return job_id

        except Exception as e:
            connection.rollback()
            print(f"Error inserting record: {e}")
            return None
