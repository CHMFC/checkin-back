from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        location=user.location,
        phone=user.phone,
        profile_visibility=user.profile_visibility,
        auto_checkin_visibility=user.auto_checkin_visibility,
        allow_messages_from=user.allow_messages_from,
        review_delay=user.review_delay,
        is_connectable=user.is_connectable,
        notifications_enabled=user.notifications_enabled,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first()


def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.User)
    if search:
        like = f"%{search}%"
        query = query.filter(models.User.name.ilike(like) | models.User.email.ilike(like))
    if sort_by in {"name", "created_at"}:
        column = getattr(models.User, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()


def update_user(db: Session, user_id, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# ===== Venues =====
def create_venue(db: Session, payload: schemas.VenueCreate):
    venue = models.Venue(**payload.dict(exclude_unset=True))
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def list_venues(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.Venue)
    if search:
        like = f"%{search}%"
        query = query.filter(models.Venue.name.ilike(like))
    if sort_by in {"name", "created_at", "rating", "total_reviews"}:
        column = getattr(models.Venue, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()


def get_venue(db: Session, venue_id):
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()


def update_venue(db: Session, venue_id, payload: schemas.VenueUpdate):
    venue = get_venue(db, venue_id)
    if not venue:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(venue, field, value)
    db.commit()
    db.refresh(venue)
    return venue


def delete_venue(db: Session, venue_id):
    db.query(models.Venue).filter(models.Venue.id == venue_id).delete()
    db.commit()


# ===== Groups =====
def create_group(db: Session, payload: schemas.GroupCreate, created_by):
    group = models.Group(**payload.dict(exclude_unset=True), created_by=created_by)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def list_groups(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.Group)
    if search:
        like = f"%{search}%"
        query = query.filter(models.Group.name.ilike(like))
    if sort_by in {"name", "created_at"}:
        column = getattr(models.Group, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()


def get_group(db: Session, group_id):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def update_group(db: Session, group_id, payload: schemas.GroupUpdate):
    group = get_group(db, group_id)
    if not group:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(group, field, value)
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_id):
    db.query(models.Group).filter(models.Group.id == group_id).delete()
    db.commit()


# ===== Interests =====
def create_interest(db: Session, payload: schemas.InterestCreate):
    interest = models.Interest(**payload.dict(exclude_unset=True))
    db.add(interest)
    db.commit()
    db.refresh(interest)
    return interest


def list_interests(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.Interest)
    if search:
        like = f"%{search}%"
        query = query.filter(models.Interest.name.ilike(like))
    if sort_by in {"name", "created_at"}:
        column = getattr(models.Interest, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()


def get_interest(db: Session, interest_id):
    return db.query(models.Interest).filter(models.Interest.id == interest_id).first()


def update_interest(db: Session, interest_id, payload: schemas.InterestUpdate):
    interest = get_interest(db, interest_id)
    if not interest:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(interest, field, value)
    db.commit()
    db.refresh(interest)
    return interest


def delete_interest(db: Session, interest_id):
    db.query(models.Interest).filter(models.Interest.id == interest_id).delete()
    db.commit()


# ===== Badges =====
def create_badge(db: Session, payload: schemas.BadgeCreate):
    badge = models.Badge(**payload.dict(exclude_unset=True))
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


def list_badges(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.Badge)
    if search:
        like = f"%{search}%"
        query = query.filter(models.Badge.name.ilike(like))
    if sort_by in {"name", "created_at"}:
        column = getattr(models.Badge, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()


def get_badge(db: Session, badge_id):
    return db.query(models.Badge).filter(models.Badge.id == badge_id).first()


def update_badge(db: Session, badge_id, payload: schemas.BadgeUpdate):
    badge = get_badge(db, badge_id)
    if not badge:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(badge, field, value)
    db.commit()
    db.refresh(badge)
    return badge


def delete_badge(db: Session, badge_id):
    db.query(models.Badge).filter(models.Badge.id == badge_id).delete()
    db.commit()


# ===== Associations =====
# User Interests
def user_exists(db: Session, user_id) -> bool:
    return db.query(models.User.id).filter(models.User.id == user_id).first() is not None


def group_exists(db: Session, group_id) -> bool:
    return db.query(models.Group.id).filter(models.Group.id == group_id).first() is not None


def interest_exists(db: Session, interest_id) -> bool:
    return db.query(models.Interest.id).filter(models.Interest.id == interest_id).first() is not None


def badge_exists(db: Session, badge_id) -> bool:
    return db.query(models.Badge.id).filter(models.Badge.id == badge_id).first() is not None


def user_interest_exists(db: Session, user_id, interest_id) -> bool:
    return (
        db.query(models.UserInterest.id)
        .filter(models.UserInterest.user_id == user_id, models.UserInterest.interest_id == interest_id)
        .first()
        is not None
    )


def list_user_interests(db: Session, user_id):
    return (
        db.query(models.Interest)
        .join(models.UserInterest, models.UserInterest.interest_id == models.Interest.id)
        .filter(models.UserInterest.user_id == user_id)
        .all()
    )


def add_user_interest(db: Session, user_id, interest_id):
    link = models.UserInterest(user_id=user_id, interest_id=interest_id)
    db.add(link)
    db.commit()
    return link


def remove_user_interest(db: Session, user_id, interest_id):
    db.query(models.UserInterest).filter(
        models.UserInterest.user_id == user_id,
        models.UserInterest.interest_id == interest_id,
    ).delete()
    db.commit()


# User Badges
def user_badge_exists(db: Session, user_id, badge_id) -> bool:
    return (
        db.query(models.UserBadge.id)
        .filter(models.UserBadge.user_id == user_id, models.UserBadge.badge_id == badge_id)
        .first()
        is not None
    )


def list_user_badges(db: Session, user_id):
    return (
        db.query(models.Badge)
        .join(models.UserBadge, models.UserBadge.badge_id == models.Badge.id)
        .filter(models.UserBadge.user_id == user_id)
        .all()
    )


def add_user_badge(db: Session, user_id, badge_id):
    link = models.UserBadge(user_id=user_id, badge_id=badge_id)
    db.add(link)
    db.commit()
    return link


def remove_user_badge(db: Session, user_id, badge_id):
    db.query(models.UserBadge).filter(
        models.UserBadge.user_id == user_id,
        models.UserBadge.badge_id == badge_id,
    ).delete()
    db.commit()


# Group Members
def group_member_exists(db: Session, group_id, user_id) -> bool:
    return (
        db.query(models.GroupMember.id)
        .filter(models.GroupMember.group_id == group_id, models.GroupMember.user_id == user_id)
        .first()
        is not None
    )


def list_group_members(db: Session, group_id):
    return db.query(models.GroupMember).filter(models.GroupMember.group_id == group_id).all()


def add_group_member(db: Session, group_id, user_id, role: Optional[str] = None):
    member = models.GroupMember(group_id=group_id, user_id=user_id, role=role or "member")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_group_member(db: Session, group_id, user_id, role: str):
    member = (
        db.query(models.GroupMember)
        .filter(models.GroupMember.group_id == group_id, models.GroupMember.user_id == user_id)
        .first()
    )
    if not member:
        return None
    member.role = role
    db.commit()
    db.refresh(member)
    return member


def remove_group_member(db: Session, group_id, user_id):
    db.query(models.GroupMember).filter(
        models.GroupMember.group_id == group_id,
        models.GroupMember.user_id == user_id,
    ).delete()
    db.commit()


# Group Interests
def group_interest_exists(db: Session, group_id, interest_id) -> bool:
    return (
        db.query(models.GroupInterest.id)
        .filter(models.GroupInterest.group_id == group_id, models.GroupInterest.interest_id == interest_id)
        .first()
        is not None
    )


def list_group_interests(db: Session, group_id):
    return (
        db.query(models.Interest)
        .join(models.GroupInterest, models.GroupInterest.interest_id == models.Interest.id)
        .filter(models.GroupInterest.group_id == group_id)
        .all()
    )


# ===== Events =====
from datetime import datetime
from typing import Optional


def _parse_dt(value: Optional[str]):
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return value  # deixa o DB validar se não for ISO


def create_event(db: Session, payload: schemas.EventCreate, created_by):
    data = payload.dict(exclude_unset=True)
    data["start_time"] = _parse_dt(data.get("start_time"))
    if data.get("end_time"):
        data["end_time"] = _parse_dt(data.get("end_time"))
    event = models.Event(**data, created_by=created_by)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    group_id=None,
    venue_id=None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
):
    query = db.query(models.Event)
    if group_id is not None:
        query = query.filter(models.Event.group_id == group_id)
    if venue_id is not None:
        query = query.filter(models.Event.venue_id == venue_id)
    if sort_by in {"start_time", "created_at"}:
        column = getattr(models.Event, sort_by)
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    else:
        query = query.order_by(models.Event.start_time.desc())
    return query.offset(skip).limit(limit).all()


def get_event(db: Session, event_id):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def update_event(db: Session, event_id, payload: schemas.EventUpdate):
    event = get_event(db, event_id)
    if not event:
        return None
    updates = payload.dict(exclude_unset=True)
    if "start_time" in updates:
        updates["start_time"] = _parse_dt(updates["start_time"])
    if "end_time" in updates and updates["end_time"] is not None:
        updates["end_time"] = _parse_dt(updates["end_time"])
    for field, value in updates.items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


# ===== Checkins =====
def create_checkin(db: Session, payload: schemas.CheckinCreate):
    checkin = models.Checkin(**payload.dict(exclude_unset=True))
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


def get_checkin(db: Session, checkin_id):
    return db.query(models.Checkin).filter(models.Checkin.id == checkin_id).first()


def update_checkin(db: Session, checkin_id, payload: schemas.CheckinUpdate):
    checkin = get_checkin(db, checkin_id)
    if not checkin:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(checkin, field, value)
    db.commit()
    db.refresh(checkin)
    return checkin


def delete_checkin(db: Session, checkin_id):
    db.query(models.Checkin).filter(models.Checkin.id == checkin_id).delete()
    db.commit()


def list_user_checkins(db: Session, user_id, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Checkin)
        .filter(models.Checkin.user_id == user_id)
        .order_by(models.Checkin.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_venue_checkins(db: Session, venue_id, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Checkin)
        .filter(models.Checkin.venue_id == venue_id)
        .order_by(models.Checkin.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# ===== Promotions =====
def create_promotion(db: Session, venue_id, payload: schemas.PromotionCreate):
    data = payload.dict(exclude_unset=True)
    data["start_date"] = _parse_dt(data.get("start_date"))
    data["end_date"] = _parse_dt(data.get("end_date"))
    promo = models.Promotion(**data, venue_id=venue_id)
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo


def list_venue_promotions(db: Session, venue_id, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Promotion)
        .filter(models.Promotion.venue_id == venue_id)
        .order_by(models.Promotion.start_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_promotion(db: Session, promotion_id):
    return db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()


def update_promotion(db: Session, promotion_id, payload: schemas.PromotionUpdate):
    promo = get_promotion(db, promotion_id)
    if not promo:
        return None
    updates = payload.dict(exclude_unset=True)
    if "start_date" in updates:
        updates["start_date"] = _parse_dt(updates["start_date"])
    if "end_date" in updates:
        updates["end_date"] = _parse_dt(updates["end_date"])
    for field, value in updates.items():
        setattr(promo, field, value)
    db.commit()
    db.refresh(promo)
    return promo


def delete_promotion(db: Session, promotion_id):
    db.query(models.Promotion).filter(models.Promotion.id == promotion_id).delete()
    db.commit()


# ===== Event Attendees (RSVP) =====
def event_exists(db: Session, event_id) -> bool:
    return db.query(models.Event.id).filter(models.Event.id == event_id).first() is not None


def list_event_attendees(db: Session, event_id):
    return db.query(models.EventAttendee).filter(models.EventAttendee.event_id == event_id).all()


def get_event_attendee(db: Session, event_id, user_id):
    return (
        db.query(models.EventAttendee)
        .filter(models.EventAttendee.event_id == event_id, models.EventAttendee.user_id == user_id)
        .first()
    )


def add_event_attendee(db: Session, event_id, user_id, status: Optional[str] = None):
    attendee = models.EventAttendee(event_id=event_id, user_id=user_id, status=status or "going")
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee


def update_event_attendee(db: Session, event_id, user_id, status: str):
    attendee = get_event_attendee(db, event_id, user_id)
    if not attendee:
        return None
    attendee.status = status
    db.commit()
    db.refresh(attendee)
    return attendee


def remove_event_attendee(db: Session, event_id, user_id):
    db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id, models.EventAttendee.user_id == user_id
    ).delete()
    db.commit()


# ===== Friendships =====
def create_friendship_request(db: Session, from_user_id, to_user_id):
    friendship = models.Friendship(user_id=from_user_id, friend_id=to_user_id, status="pending")
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


def get_friendship(db: Session, friendship_id):
    return db.query(models.Friendship).filter(models.Friendship.id == friendship_id).first()


def list_incoming_friend_requests(db: Session, user_id):
    return (
        db.query(models.Friendship)
        .filter(models.Friendship.friend_id == user_id, models.Friendship.status == "pending")
        .order_by(models.Friendship.created_at.desc())
        .all()
    )


def list_outgoing_friend_requests(db: Session, user_id):
    return (
        db.query(models.Friendship)
        .filter(models.Friendship.user_id == user_id, models.Friendship.status == "pending")
        .order_by(models.Friendship.created_at.desc())
        .all()
    )


def set_friendship_status(db: Session, friendship_id, status: str):
    friendship = get_friendship(db, friendship_id)
    if not friendship:
        return None
    friendship.status = status
    db.commit()
    db.refresh(friendship)
    return friendship


def delete_friendship(db: Session, friendship_id):
    db.query(models.Friendship).filter(models.Friendship.id == friendship_id).delete()
    db.commit()


def list_user_friends(db: Session, user_id):
    # Amizades aceitas onde user é owner ou friend
    friendships = db.query(models.Friendship).filter(
        models.Friendship.status == "accepted",
        (models.Friendship.user_id == user_id) | (models.Friendship.friend_id == user_id),
    )
    # Retorna lista de usuários
    friend_ids = []
    for f in friendships:
        friend_ids.append(f.friend_id if f.user_id == user_id else f.user_id)
    if not friend_ids:
        return []
    return db.query(models.User).filter(models.User.id.in_(friend_ids)).all()


# ===== Messages =====
def create_message(db: Session, sender_id, receiver_id, content: str):
    msg = models.Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def list_messages_between(db: Session, user_a, user_b, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Message)
        .filter(
            ((models.Message.sender_id == user_a) & (models.Message.receiver_id == user_b))
            | ((models.Message.sender_id == user_b) & (models.Message.receiver_id == user_a))
        )
        .order_by(models.Message.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_message_threads(db: Session, user_id):
    # threads simples por último contato com cada interlocutor
    subquery = (
        db.query(
            models.Message.sender_id.label("sender"),
            models.Message.receiver_id.label("receiver"),
            models.Message.created_at.label("created_at"),
            models.Message.id.label("id"),
        )
        .filter((models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id))
        .subquery()
    )

    # Agrupar por interlocutor
    # Esta implementação pode ser otimizada com SQL mais avançado se necessário
    messages = (
        db.query(models.Message)
        .filter((models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id))
        .order_by(models.Message.created_at.desc())
        .all()
    )
    threads = {}
    for m in messages:
        counterpart = m.receiver_id if m.sender_id == user_id else m.sender_id
        if counterpart not in threads:
            threads[counterpart] = {
                "last_message": m,
                "unread_count": 0,
            }
        if m.receiver_id == user_id and not m.is_read:
            threads[counterpart]["unread_count"] += 1
    # Transformar em lista
    result = []
    for counterpart, data in threads.items():
        result.append(
            schemas.MessageThread(
                user_id=counterpart, last_message=data["last_message"], unread_count=data["unread_count"]
            )
        )
    return result


def mark_message_read(db: Session, message_id):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        return None
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg


def mark_thread_read(db: Session, user_id, other_id):
    db.query(models.Message).filter(models.Message.sender_id == other_id, models.Message.receiver_id == user_id).update(
        {"is_read": True}
    )
    db.commit()


# ===== Notifications =====
def create_notification(db: Session, payload: schemas.NotificationCreate):
    notif = models.Notification(
        user_id=payload.user_id,
        type=payload.type,
        title=payload.title,
        message=payload.message,
        data=payload.data,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def list_notifications(db: Session, user_id, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_notification(db: Session, notification_id):
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()


def mark_notification_read(db: Session, notification_id):
    notif = get_notification(db, notification_id)
    if not notif:
        return None
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif


def mark_all_notifications_read(db: Session, user_id):
    db.query(models.Notification).filter(models.Notification.user_id == user_id).update({"is_read": True})
    db.commit()


def delete_notification(db: Session, notification_id):
    db.query(models.Notification).filter(models.Notification.id == notification_id).delete()
    db.commit()


# ===== Search / Discovery =====
def search_venues(
    db: Session,
    *,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    min_rating: Optional[float] = None,
    price_range: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(models.Venue)
    if category:
        query = query.filter(models.Venue.category == category)
    if tags:
        # Busca se contem todos os tags fornecidos
        for t in tags:
            query = query.filter(models.Venue.tags.any(t))
    if min_rating is not None:
        query = query.filter(models.Venue.rating >= min_rating)
    if price_range:
        query = query.filter(models.Venue.price_range == price_range)
    return query.offset(skip).limit(limit).all()


def search_events(
    db: Session,
    *,
    group_id=None,
    venue_id=None,
    start_from: Optional[str] = None,
    end_until: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(models.Event)
    if group_id is not None:
        query = query.filter(models.Event.group_id == group_id)
    if venue_id is not None:
        query = query.filter(models.Event.venue_id == venue_id)
    if start_from is not None:
        query = query.filter(models.Event.start_time >= _parse_dt(start_from))
    if end_until is not None:
        query = query.filter(models.Event.start_time <= _parse_dt(end_until))
    return query.order_by(models.Event.start_time.desc()).offset(skip).limit(limit).all()


# ===== Admin / Maintenance =====
def set_venue_active(db: Session, venue_id, active: bool):
    venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if not venue:
        return None
    venue.is_active = active
    db.commit()
    db.refresh(venue)
    return venue


def set_promotion_active(db: Session, promotion_id, active: bool):
    promo = db.query(models.Promotion).filter(models.Promotion.id == promotion_id).first()
    if not promo:
        return None
    promo.is_active = active
    db.commit()
    db.refresh(promo)
    return promo


def add_group_interest(db: Session, group_id, interest_id):
    link = models.GroupInterest(group_id=group_id, interest_id=interest_id)
    db.add(link)
    db.commit()
    return link


def remove_group_interest(db: Session, group_id, interest_id):
    db.query(models.GroupInterest).filter(
        models.GroupInterest.group_id == group_id,
        models.GroupInterest.interest_id == interest_id,
    ).delete()
    db.commit()