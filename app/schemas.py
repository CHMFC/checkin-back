# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[str] = None  # ISO date string
    phone: Optional[str] = None
    is_connectable: Optional[bool] = True
    profile_visibility: Optional[str] = "friends"
    auto_checkin_visibility: Optional[str] = "public"
    allow_messages_from: Optional[str] = "friends"
    review_delay: Optional[str] = "immediate"
    notifications_enabled: Optional[bool] = True


class UserCreate(UserBase):
    id: UUID


class User(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[str] = None
    phone: Optional[str] = None
    is_connectable: Optional[bool] = None
    profile_visibility: Optional[str] = None
    auto_checkin_visibility: Optional[str] = None
    allow_messages_from: Optional[str] = None
    review_delay: Optional[str] = None
    notifications_enabled: Optional[bool] = None


class LoginRequest(BaseModel):
    email: EmailStr


# ========= Venues =========
class VenueBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None
    total_reviews: Optional[int] = None
    image_url: Optional[str] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None
    total_reviews: Optional[int] = None
    image_url: Optional[str] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None


class Venue(VenueBase):
    id: UUID

    class Config:
        from_attributes = True


# ========= Groups =========
class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    radius_km: Optional[int] = 5
    is_public: Optional[bool] = True
    max_members: Optional[int] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    radius_km: Optional[int] = None
    is_public: Optional[bool] = None
    max_members: Optional[int] = None


class Group(GroupBase):
    id: UUID
    created_by: Optional[UUID] = None

    class Config:
        from_attributes = True


# ========= Interests =========
class InterestBase(BaseModel):
    name: str
    category: Optional[str] = None
    icon: Optional[str] = None


class InterestCreate(InterestBase):
    pass


class InterestUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None


class Interest(InterestBase):
    id: UUID

    class Config:
        from_attributes = True


# ========= Badges =========
class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    criteria: Optional[dict[str, Any]] = None


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    criteria: Optional[dict[str, Any]] = None


class Badge(BadgeBase):
    id: UUID

    class Config:
        from_attributes = True


# ========= Associations (lightweight) =========
class GroupMemberBase(BaseModel):
    role: Optional[str] = None


class GroupMemberCreate(GroupMemberBase):
    user_id: UUID


class GroupMemberUpdate(BaseModel):
    role: Optional[str] = None


class GroupMember(BaseModel):
    id: UUID
    group_id: UUID
    user_id: UUID
    role: str
    joined_at: Optional[str] = None

    class Config:
        from_attributes = True


# ========= Events =========
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    venue_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    start_time: str
    end_time: Optional[str] = None
    max_attendees: Optional[int] = None
    is_public: Optional[bool] = True


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    venue_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    max_attendees: Optional[int] = None
    is_public: Optional[bool] = None


class Event(EventBase):
    id: UUID
    created_by: Optional[UUID] = None

    class Config:
        from_attributes = True


# ========= Checkins =========
class CheckinBase(BaseModel):
    user_id: UUID
    venue_id: UUID
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    review: Optional[str] = None
    amount_spent: Optional[float] = None
    photos: Optional[list[str]] = None
    is_anonymous: Optional[bool] = False


class CheckinCreate(CheckinBase):
    pass


class CheckinUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    review: Optional[str] = None
    amount_spent: Optional[float] = None
    photos: Optional[list[str]] = None
    is_anonymous: Optional[bool] = None


class Checkin(CheckinBase):
    id: UUID

    class Config:
        from_attributes = True


# ========= Promotions =========
class PromotionBase(BaseModel):
    title: str
    description: Optional[str] = None
    discount_percentage: Optional[int] = None
    discount_amount: Optional[float] = None
    min_purchase: Optional[float] = None
    start_date: str
    end_date: str
    is_active: Optional[bool] = True


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[int] = None
    discount_amount: Optional[float] = None
    min_purchase: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: Optional[bool] = None


class Promotion(PromotionBase):
    id: UUID
    venue_id: Optional[UUID] = None

    class Config:
        from_attributes = True


# ========= Event Attendees (RSVP) =========
class EventAttendeeBase(BaseModel):
    status: Optional[str] = None  # going | maybe | not_going


class EventAttendeeCreate(EventAttendeeBase):
    user_id: UUID


class EventAttendeeUpdate(BaseModel):
    status: Optional[str] = None


class EventAttendee(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    status: str
    joined_at: Optional[str] = None

    class Config:
        from_attributes = True


# ========= Friendships =========
class Friendship(BaseModel):
    id: UUID
    user_id: UUID
    friend_id: UUID
    status: str  # pending | accepted | blocked
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class FriendshipRequestCreate(BaseModel):
    to_user_id: UUID


# ========= Messages =========
class MessageCreate(BaseModel):
    receiver_id: UUID
    content: str


class Message(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    is_read: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class MessageThread(BaseModel):
    user_id: UUID  # counterpart user id
    last_message: Message
    unread_count: int


# ========= Notifications =========
class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    data: Optional[dict] = None


class NotificationCreate(NotificationBase):
    user_id: UUID


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    is_read: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True