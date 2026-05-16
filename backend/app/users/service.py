from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User
from app.core.enums import UserRole
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

# ==================================================
# DB access (旧 repositoryの中身)
# ==================================================

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_active_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(
        User.email == email,
        User.is_active == True
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ==================================================
# Usecase / Service layer
# ==================================================

async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> tuple[User | None, str | None]:

    existing = await get_by_email(db, email)
    if existing:
        return None, "Email already registered"

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.USER,
        is_active=True,
    )

    created_user = await create(db, user)
    return created_user, None


async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> tuple[dict | None, str | None]:

    user = await get_active_by_email(db, email)
    if not user:
        return None, "Invalid credentials"

    if not verify_password(password, user.hashed_password):
        return None, "Invalid credentials"

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }, None


async def get_user_by_id_service(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    return await get_by_id(db, user_id)


# ==================================================
# Domain helper
# ==================================================

def is_admin(user: User) -> bool:
    return user.role == UserRole.ADMIN