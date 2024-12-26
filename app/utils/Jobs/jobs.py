from contextlib import contextmanager
from datetime import datetime, timedelta
import threading
from app.models.LIke import Like
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from confluent_kafka import Consumer, KafkaException
from app.config import env_variables

keys = env_variables()

engine = create_engine(keys["DATABASE_URI"], pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

kafka_bootstrap_servers = "localhost:9092"
topic = "likes_topic"


class BackgroundTasks:
    def __init__(self):
        self.scheduler = None
        self.likes_count = 0

    @contextmanager
    def db_connection(self):
        db = SessionLocal()
        try:
            print("Opening db connection", db)
            db.begin()
            yield db
            db.commit()
        except Exception as e:
            print("Error in db_connection", e)
            db.rollback()
            raise
        finally:
            print("Closing db connection")
            db.close()

    def get_likes(self):
        try:
            with self.db_connection() as db:
                likes = db.query(Like).count()
                print(likes, "likes")
                self.likes_count = likes
                print(self.likes_count, "likes")

        except Exception as e:
            print("Error in 'deactivate_quizzes': ", e)

    @property
    def likes_count_value(self):
        return self.likes_count

    def consume_likes(self):
        consumer = Consumer(
            {
                "bootstrap.servers": kafka_bootstrap_servers,
                "group.id": "like-counter-group",
                "auto.offset.reset": "earliest",
            }
        )
        consumer.subscribe([topic])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                # Update like count
                self.likes_count += 1
                print(f"Total likes: {self.likes_count}")
        finally:
            consumer.close()

    def start(self):
        self.scheduler = BackgroundScheduler()
        # self.scheduler.get_likes()
        self.scheduler.add_job(self.get_likes, CronTrigger(hour=18, minute=13))
        self.scheduler.start()
        print("Scheduler started!")

        consumer_thread = threading.Thread(target=self.consume_likes, daemon=True)
        consumer_thread.start()
        print("Kafka consumer started!")
