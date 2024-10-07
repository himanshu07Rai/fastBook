from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User
from .schema import UserCreateSchema
from .utils import generate_hashed_password
from src.konstants import USER_ROLE

class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self,email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password = generate_hashed_password(new_user.password)
        new_user.role = USER_ROLE['NORMAL']
        session.add(new_user)
        await session.commit()
        return new_user

    async def login(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user and user.password == password:
            return user
        return None