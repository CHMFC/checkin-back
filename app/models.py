"""SQLAlchemy ORM models aligned with the PostgreSQL schema."""

import uuid
from sqlalchemy import (
    Column,
    Text,
    Integer,
    Boolean,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from .database import Base


# ========= Nivel 0 =========
class Badge(Base):
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    icon = Column(Text)
    category = Column(Text)
    criteria = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Interest(Base):
    __tablename__ = "interests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    category = Column(Text)
    icon = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Venue(Base):
    __tablename__ = "venues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    category = Column(Text, nullable=False)
    address = Column(Text)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    phone = Column(Text)
    website = Column(Text)
    hours = Column(Text)
    price_range = Column(Text)
    rating = Column(Numeric, server_default="0")
    total_reviews = Column(Integer, server_default="0")
    image_url = Column(Text)
    tags = Column(ARRAY(Text))
    is_active = Column(Boolean, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    avatar_url = Column(Text)
    bio = Column(Text)
    location = Column(Text)
    birth_date = Column(Date)
    phone = Column(Text)
    is_connectable = Column(Boolean, server_default="true")
    profile_visibility = Column(Text, server_default="friends")
    auto_checkin_visibility = Column(Text, server_default="public")
    allow_messages_from = Column(Text, server_default="friends")
    review_delay = Column(Text, server_default="immediate")
    notifications_enabled = Column(Boolean, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


# ========= Nivel 1 =========
class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    avatar_url = Column(Text)
    radius_km = Column(Integer, server_default="5")
    is_public = Column(Boolean, server_default="true")
    max_members = Column(Integer)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"))
    title = Column(Text, nullable=False)
    description = Column(Text)
    discount_percentage = Column(Integer)
    discount_amount = Column(Numeric)
    min_purchase = Column(Numeric)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"))
    rating = Column(Integer)
    review = Column(Text)
    amount_spent = Column(Numeric)
    photos = Column(ARRAY(Text))
    is_anonymous = Column(Boolean, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="checkins_rating_range"),
    )


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    friend_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Text, server_default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSONB)
    is_read = Column(Boolean, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"))
    earned_at = Column(DateTime(timezone=True), server_default=func.now())


class UserInterest(Base):
    __tablename__ = "user_interests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    interest_id = Column(UUID(as_uuid=True), ForeignKey("interests.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ========= Nivel 2 =========
class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role = Column(Text, server_default="member")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())


class GroupInterest(Base):
    __tablename__ = "group_interests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    interest_id = Column(UUID(as_uuid=True), ForeignKey("interests.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    max_attendees = Column(Integer)
    is_public = Column(Boolean, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


# ========= Nivel 3 =========
class EventAttendee(Base):
    __tablename__ = "event_attendees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Text, server_default="going")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())