# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from uuid import UUID

from . import crud, models, schemas, auth
from .database import engine, get_db

# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CheckIn API",
    description="API para sistema de CheckIn",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para obter usuário atual
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API CheckIn!"}

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users", response_model=list[schemas.User])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: str | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_users(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: UUID = Path(...), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: UUID,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.id != user_id:
        # Sem papéis/admin definidos ainda; restringe a autoedição
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este usuário")
    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


# ===== Venues =====
@app.post("/venues", response_model=schemas.Venue)
def create_venue(payload: schemas.VenueCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.create_venue(db, payload)


@app.get("/venues", response_model=list[schemas.Venue])
def list_venues(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: str | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_venues(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)


@app.get("/venues/{venue_id}", response_model=schemas.Venue)
def get_venue(venue_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    venue = crud.get_venue(db, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return venue


@app.patch("/venues/{venue_id}", response_model=schemas.Venue)
def update_venue(venue_id: UUID, payload: schemas.VenueUpdate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    venue = crud.update_venue(db, venue_id, payload)
    if not venue:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return venue


@app.delete("/venues/{venue_id}")
def delete_venue(venue_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    venue = crud.get_venue(db, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    crud.delete_venue(db, venue_id)
    return {"status": "ok"}


# ===== Groups =====
@app.post("/groups", response_model=schemas.Group)
def create_group(payload: schemas.GroupCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_group(db, payload, created_by=current_user.id)


@app.get("/groups", response_model=list[schemas.Group])
def list_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: str | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_groups(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)


@app.get("/groups/{group_id}", response_model=schemas.Group)
def get_group(group_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return group


@app.patch("/groups/{group_id}", response_model=schemas.Group)
def update_group(group_id: UUID, payload: schemas.GroupUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este grupo")
    group = crud.update_group(db, group_id, payload)
    return group


@app.delete("/groups/{group_id}")
def delete_group(group_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para remover este grupo")
    crud.delete_group(db, group_id)
    return {"status": "ok"}


# ===== Interests =====
@app.post("/interests", response_model=schemas.Interest)
def create_interest(payload: schemas.InterestCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.create_interest(db, payload)


@app.get("/interests", response_model=list[schemas.Interest])
def list_interests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    search: str | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_interests(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)


@app.get("/interests/{interest_id}", response_model=schemas.Interest)
def get_interest(interest_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    interest = crud.get_interest(db, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    return interest


@app.patch("/interests/{interest_id}", response_model=schemas.Interest)
def update_interest(interest_id: UUID, payload: schemas.InterestUpdate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    interest = crud.update_interest(db, interest_id, payload)
    if not interest:
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    return interest


@app.delete("/interests/{interest_id}")
def delete_interest(interest_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    interest = crud.get_interest(db, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    crud.delete_interest(db, interest_id)
    return {"status": "ok"}


# ===== Badges =====
@app.post("/badges", response_model=schemas.Badge)
def create_badge(payload: schemas.BadgeCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.create_badge(db, payload)


@app.get("/badges", response_model=list[schemas.Badge])
def list_badges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    search: str | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_badges(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)


@app.get("/badges/{badge_id}", response_model=schemas.Badge)
def get_badge(badge_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    badge = crud.get_badge(db, badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge não encontrada")
    return badge


# ===== Associations =====
# User Interests
@app.get("/users/{user_id}/interests", response_model=list[schemas.Interest])
def get_user_interests(user_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.list_user_interests(db, user_id)


@app.post("/users/{user_id}/interests/{interest_id}")
def add_user_interest(user_id: UUID, interest_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar interesses deste usuário")
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not crud.interest_exists(db, interest_id):
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    if crud.user_interest_exists(db, user_id, interest_id):
        raise HTTPException(status_code=409, detail="Interesse já associado ao usuário")
    crud.add_user_interest(db, user_id, interest_id)
    return {"status": "ok"}


@app.delete("/users/{user_id}/interests/{interest_id}")
def delete_user_interest(user_id: UUID, interest_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar interesses deste usuário")
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not crud.interest_exists(db, interest_id):
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    crud.remove_user_interest(db, user_id, interest_id)
    return {"status": "ok"}


# User Badges
@app.get("/users/{user_id}/badges", response_model=list[schemas.Badge])
def get_user_badges(user_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.list_user_badges(db, user_id)


@app.post("/users/{user_id}/badges/{badge_id}")
def add_user_badge(user_id: UUID, badge_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar badges deste usuário")
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not crud.badge_exists(db, badge_id):
        raise HTTPException(status_code=404, detail="Badge não encontrada")
    if crud.user_badge_exists(db, user_id, badge_id):
        raise HTTPException(status_code=409, detail="Badge já associado ao usuário")
    crud.add_user_badge(db, user_id, badge_id)
    return {"status": "ok"}


@app.delete("/users/{user_id}/badges/{badge_id}")
def delete_user_badge(user_id: UUID, badge_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar badges deste usuário")
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not crud.badge_exists(db, badge_id):
        raise HTTPException(status_code=404, detail="Badge não encontrada")
    crud.remove_user_badge(db, user_id, badge_id)
    return {"status": "ok"}


# Group Members
@app.get("/groups/{group_id}/members", response_model=list[schemas.GroupMember])
def get_group_members(group_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.list_group_members(db, group_id)


@app.post("/groups/{group_id}/members", response_model=schemas.GroupMember)
def add_group_member(group_id: UUID, payload: schemas.GroupMemberCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para adicionar membros")
    if not crud.user_exists(db, payload.user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if crud.group_member_exists(db, group_id, payload.user_id):
        raise HTTPException(status_code=409, detail="Usuário já é membro do grupo")
    if payload.role and payload.role not in {"admin", "moderator", "member"}:
        raise HTTPException(status_code=422, detail="Role inválida")
    return crud.add_group_member(db, group_id, payload.user_id, payload.role)


@app.patch("/groups/{group_id}/members/{user_id}", response_model=schemas.GroupMember)
def update_group_member(group_id: UUID, user_id: UUID, payload: schemas.GroupMemberUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para alterar membros")
    if payload.role and payload.role not in {"admin", "moderator", "member"}:
        raise HTTPException(status_code=422, detail="Role inválida")
    member = crud.update_group_member(db, group_id, user_id, role=payload.role or "member")
    if not member:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    return member


@app.delete("/groups/{group_id}/members/{user_id}")
def delete_group_member(group_id: UUID, user_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para remover este membro")
    crud.remove_group_member(db, group_id, user_id)
    return {"status": "ok"}


# Group Interests
@app.get("/groups/{group_id}/interests", response_model=list[schemas.Interest])
def get_group_interests(group_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return crud.list_group_interests(db, group_id)


@app.post("/groups/{group_id}/interests/{interest_id}")
def add_group_interest(group_id: UUID, interest_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para alterar interesses do grupo")
    if not crud.interest_exists(db, interest_id):
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    if crud.group_interest_exists(db, group_id, interest_id):
        raise HTTPException(status_code=409, detail="Interesse já associado ao grupo")
    crud.add_group_interest(db, group_id, interest_id)
    return {"status": "ok"}


@app.delete("/groups/{group_id}/interests/{interest_id}")
def delete_group_interest(group_id: UUID, interest_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para alterar interesses do grupo")
    if not crud.interest_exists(db, interest_id):
        raise HTTPException(status_code=404, detail="Interesse não encontrado")
    crud.remove_group_interest(db, group_id, interest_id)
    return {"status": "ok"}


@app.patch("/badges/{badge_id}", response_model=schemas.Badge)
def update_badge(badge_id: UUID, payload: schemas.BadgeUpdate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    badge = crud.update_badge(db, badge_id, payload)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge não encontrada")
    return badge


@app.delete("/badges/{badge_id}")
def delete_badge(badge_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    badge = crud.get_badge(db, badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge não encontrada")
    crud.delete_badge(db, badge_id)
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ===== Events =====
@app.post("/events", response_model=schemas.Event)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Validar referências
    if payload.group_id and not crud.group_exists(db, payload.group_id):
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if payload.venue_id and not crud.get_venue(db, payload.venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.create_event(db, payload, created_by=current_user.id)


@app.get("/events", response_model=list[schemas.Event])
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    group_id: UUID | None = Query(None),
    venue_id: UUID | None = Query(None),
    sort_by: str | None = Query(None),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.list_events(
        db,
        skip=skip,
        limit=limit,
        group_id=group_id,
        venue_id=venue_id,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@app.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return event


@app.patch("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: UUID, payload: schemas.EventUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if event.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este evento")
    if payload.group_id and not crud.group_exists(db, payload.group_id):
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if payload.venue_id and not crud.get_venue(db, payload.venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.update_event(db, event_id, payload)


@app.get("/groups/{group_id}/events", response_model=list[schemas.Event])
def list_group_events(group_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.group_exists(db, group_id):
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return crud.list_events(db, skip=skip, limit=limit, group_id=group_id)


@app.get("/venues/{venue_id}/events", response_model=list[schemas.Event])
def list_venue_events(venue_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.get_venue(db, venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.list_events(db, skip=skip, limit=limit, venue_id=venue_id)


# ===== Checkins =====
@app.post("/checkins", response_model=schemas.Checkin)
def create_checkin(payload: schemas.CheckinCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != payload.user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para criar check-in por outro usuário")
    if not crud.user_exists(db, payload.user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not crud.get_venue(db, payload.venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.create_checkin(db, payload)


@app.get("/checkins/{checkin_id}", response_model=schemas.Checkin)
def get_checkin(checkin_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    checkin = crud.get_checkin(db, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in não encontrado")
    return checkin


@app.patch("/checkins/{checkin_id}", response_model=schemas.Checkin)
def update_checkin(checkin_id: UUID, payload: schemas.CheckinUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    checkin = crud.get_checkin(db, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in não encontrado")
    if checkin.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar este check-in")
    return crud.update_checkin(db, checkin_id, payload)


@app.delete("/checkins/{checkin_id}")
def delete_checkin(checkin_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    checkin = crud.get_checkin(db, checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in não encontrado")
    if checkin.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para excluir este check-in")
    crud.delete_checkin(db, checkin_id)
    return {"status": "ok"}


@app.get("/users/{user_id}/checkins", response_model=list[schemas.Checkin])
def list_user_checkins(user_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return crud.list_user_checkins(db, user_id, skip=skip, limit=limit)


@app.get("/venues/{venue_id}/checkins", response_model=list[schemas.Checkin])
def list_venue_checkins(venue_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.get_venue(db, venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.list_venue_checkins(db, venue_id, skip=skip, limit=limit)


# ===== Promotions =====
@app.post("/venues/{venue_id}/promotions", response_model=schemas.Promotion)
def create_promotion(venue_id: UUID, payload: schemas.PromotionCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.get_venue(db, venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.create_promotion(db, venue_id, payload)


@app.get("/venues/{venue_id}/promotions", response_model=list[schemas.Promotion])
def list_venue_promotions(venue_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.get_venue(db, venue_id):
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return crud.list_venue_promotions(db, venue_id, skip=skip, limit=limit)


@app.get("/promotions/{promotion_id}", response_model=schemas.Promotion)
def get_promotion(promotion_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    promo = crud.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    return promo


@app.patch("/promotions/{promotion_id}", response_model=schemas.Promotion)
def update_promotion(promotion_id: UUID, payload: schemas.PromotionUpdate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    promo = crud.update_promotion(db, promotion_id, payload)
    if not promo:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    return promo


@app.delete("/promotions/{promotion_id}")
def delete_promotion(promotion_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    promo = crud.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    crud.delete_promotion(db, promotion_id)
    return {"status": "ok"}


# ===== Event Attendees (RSVP) =====
@app.post("/events/{event_id}/attendees", response_model=schemas.EventAttendee)
def add_event_attendee(event_id: UUID, payload: schemas.EventAttendeeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.event_exists(db, event_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if not crud.user_exists(db, payload.user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para confirmar presença por outro usuário")
    if payload.status and payload.status not in {"going", "maybe", "not_going"}:
        raise HTTPException(status_code=422, detail="Status inválido")
    existing = crud.get_event_attendee(db, event_id, payload.user_id)
    if existing:
        raise HTTPException(status_code=409, detail="Usuário já possui RSVP neste evento")
    return crud.add_event_attendee(db, event_id, payload.user_id, payload.status)


@app.get("/events/{event_id}/attendees", response_model=list[schemas.EventAttendee])
def list_event_attendees(event_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.event_exists(db, event_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return crud.list_event_attendees(db, event_id)


@app.patch("/events/{event_id}/attendees/{user_id}", response_model=schemas.EventAttendee)
def update_event_attendee(event_id: UUID, user_id: UUID, payload: schemas.EventAttendeeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.event_exists(db, event_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para atualizar o seu RSVP")
    if payload.status and payload.status not in {"going", "maybe", "not_going"}:
        raise HTTPException(status_code=422, detail="Status inválido")
    attendee = crud.update_event_attendee(db, event_id, user_id, payload.status or "going")
    if not attendee:
        raise HTTPException(status_code=404, detail="RSVP não encontrado")
    return attendee


@app.delete("/events/{event_id}/attendees/{user_id}")
def delete_event_attendee(event_id: UUID, user_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.event_exists(db, event_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para remover o seu RSVP")
    crud.remove_event_attendee(db, event_id, user_id)
    return {"status": "ok"}


# ===== Friendships =====
@app.post("/friendships/requests", response_model=schemas.Friendship)
def create_friend_request(payload: schemas.FriendshipRequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, payload.to_user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if payload.to_user_id == current_user.id:
        raise HTTPException(status_code=422, detail="Não é possível enviar solicitação para si mesmo")
    # Evitar duplicatas simples: se já existe pendente em qualquer direção
    outgoing = crud.list_outgoing_friend_requests(db, current_user.id)
    if any(fr.friend_id == payload.to_user_id for fr in outgoing):
        raise HTTPException(status_code=409, detail="Solicitação já enviada")
    incoming = crud.list_incoming_friend_requests(db, current_user.id)
    if any(fr.user_id == payload.to_user_id for fr in incoming):
        raise HTTPException(status_code=409, detail="Você já possui uma solicitação deste usuário")
    return crud.create_friendship_request(db, current_user.id, payload.to_user_id)


@app.get("/friendships/requests/incoming", response_model=list[schemas.Friendship])
def list_incoming_requests(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_incoming_friend_requests(db, current_user.id)


@app.get("/friendships/requests/outgoing", response_model=list[schemas.Friendship])
def list_outgoing_requests(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_outgoing_friend_requests(db, current_user.id)


@app.post("/friendships/{friendship_id}/accept", response_model=schemas.Friendship)
def accept_friendship(friendship_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    friendship = crud.get_friendship(db, friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    if friendship.friend_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para aceitar esta solicitação")
    return crud.set_friendship_status(db, friendship_id, "accepted")


@app.post("/friendships/{friendship_id}/reject", response_model=schemas.Friendship)
def reject_friendship(friendship_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    friendship = crud.get_friendship(db, friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    if friendship.friend_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para rejeitar esta solicitação")
    crud.delete_friendship(db, friendship_id)
    return friendship


@app.post("/friendships/{friendship_id}/block", response_model=schemas.Friendship)
def block_friendship(friendship_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    friendship = crud.get_friendship(db, friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    # Permite bloqueio se é participante da relação
    if friendship.friend_id != current_user.id and friendship.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para bloquear")
    return crud.set_friendship_status(db, friendship_id, "blocked")


@app.delete("/friendships/{friendship_id}")
def delete_friendship(friendship_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    friendship = crud.get_friendship(db, friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    if friendship.friend_id != current_user.id and friendship.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para remover")
    crud.delete_friendship(db, friendship_id)
    return {"status": "ok"}


@app.get("/users/{user_id}/friends", response_model=list[schemas.User])
def list_user_friends(user_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return crud.list_user_friends(db, user_id)


# ===== Messages =====
@app.post("/messages", response_model=schemas.Message)
def create_message(payload: schemas.MessageCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, payload.receiver_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if payload.receiver_id == current_user.id:
        raise HTTPException(status_code=422, detail="Não é possível enviar mensagem para si mesmo")
    return crud.create_message(db, current_user.id, payload.receiver_id, payload.content)


@app.get("/messages/threads", response_model=list[schemas.MessageThread])
def get_threads(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_message_threads(db, current_user.id)


@app.get("/messages/with/{user_id}", response_model=list[schemas.Message])
def get_messages_with(user_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return crud.list_messages_between(db, current_user.id, user_id, skip=skip, limit=limit)


@app.post("/messages/{message_id}/read", response_model=schemas.Message)
def mark_message_read(message_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    msg = crud.mark_message_read(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    if msg.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para marcar como lida")
    return msg


@app.post("/messages/with/{user_id}/read")
def mark_thread_read(user_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    crud.mark_thread_read(db, current_user.id, user_id)
    return {"status": "ok"}


# ===== Notifications =====
@app.get("/notifications", response_model=list[schemas.Notification])
def get_notifications(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_notifications(db, current_user.id, skip=skip, limit=limit)


@app.post("/notifications", response_model=schemas.Notification)
def create_notification(payload: schemas.NotificationCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    if not crud.user_exists(db, payload.user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return crud.create_notification(db, payload)


@app.post("/notifications/{notification_id}/read", response_model=schemas.Notification)
def mark_notification_read(notification_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    notif = crud.get_notification(db, notification_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notif.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para marcar esta notificação")
    return crud.mark_notification_read(db, notification_id)


@app.post("/notifications/read-all")
def mark_all_notifications_read(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.mark_all_notifications_read(db, current_user.id)
    return {"status": "ok"}


@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    notif = crud.get_notification(db, notification_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    if notif.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para remover esta notificação")
    crud.delete_notification(db, notification_id)
    return {"status": "ok"}


# ===== Search / Discovery =====
@app.get("/venues/search", response_model=list[schemas.Venue])
def search_venues(
    category: str | None = Query(None),
    tags: list[str] | None = Query(None),
    min_rating: float | None = Query(None, ge=0, le=5),
    price_range: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.search_venues(
        db,
        category=category,
        tags=tags,
        min_rating=min_rating,
        price_range=price_range,
        skip=skip,
        limit=limit,
    )


@app.get("/events/search", response_model=list[schemas.Event])
def search_events(
    group_id: UUID | None = Query(None),
    venue_id: UUID | None = Query(None),
    start_from: str | None = Query(None),
    end_until: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return crud.search_events(
        db,
        group_id=group_id,
        venue_id=venue_id,
        start_from=start_from,
        end_until=end_until,
        skip=skip,
        limit=limit,
    )


# ===== Admin / Maintenance =====
@app.patch("/venues/{venue_id}/activate")
def activate_venue(venue_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    venue = crud.set_venue_active(db, venue_id, True)
    if not venue:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return {"status": "ok"}


@app.patch("/venues/{venue_id}/deactivate")
def deactivate_venue(venue_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    venue = crud.set_venue_active(db, venue_id, False)
    if not venue:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return {"status": "ok"}


@app.patch("/promotions/{promotion_id}/activate")
def activate_promotion(promotion_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    promo = crud.set_promotion_active(db, promotion_id, True)
    if not promo:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    return {"status": "ok"}


@app.patch("/promotions/{promotion_id}/deactivate")
def deactivate_promotion(promotion_id: UUID, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    promo = crud.set_promotion_active(db, promotion_id, False)
    if not promo:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    return {"status": "ok"}