from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    telegram_id = Column(BigInteger, unique=True)
    full_name = Column(String)
    description = Column(String)
    disabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    open_to_collab = Column(Boolean, default=False) # do migration
    # is_admin = Column(Boolean, default=False) # do migration
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # projects = relationship("Projects", back_populates="owner")
    # groups = relationship("Groups", back_populates="owner")
    # tasks = relationship("Tasks", back_populates="owner")
    # comments = relationship("Comments", back_populates="owner")
    # attachments = relationship("Attachments", back_populates="owner")
    # notifications = relationship("Notifications", back_populates="owner")
    # activities = relationship("Activities", back_populates="owner")
    # roles = relationship("Roles", back_populates="owner")
    # permissions = relationship("Permissions", back_populates="owner")
    # tokens = relationship("Tokens", back_populates="owner")
    # settings = relationship("Settings", back_populates="owner")
    # logs = relationship("Logs", back_populates="owner")
    # messages = relationship("Messages", back_populates="owner")
    # contacts = relationship("Contacts", back_populates="owner")
    # addresses = relationship("Addresses", back_populates="owner")
    # phones = relationship("Phones", back_populates="owner")
    # emails = relationship("Emails", back_populates="owner")
    # websites = relationship("Websites", back_populates="owner")
    # socials = relationship("Socials", back_populates="owner")
    # images = relationship("Images", back_populates="owner")
    # files = relationship("Files", back_populates="owner")
    # videos = relationship("Videos", back_populates="owner")
    # audios = relationship("Audios", back_populates="owner")
    # events = relationship("Events", back_populates="owner")
    # schedules = relationship("Schedules", back_populates="owner")

    