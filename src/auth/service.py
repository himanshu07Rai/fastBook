from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User
from .schema import UserCreateSchema
from .utils import generate_hashed_password
from src.konstants import USER_ROLE
from src.mail import send_email
from src.config import Config
from src.auth.utils import verify_confirmation_token, create_confirmation_token

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
    
    async def update_user(self,user:User, user_data: dict, session: AsyncSession):
        for key, value in user_data.items():
            setattr(user, key, value)
        await session.commit()
        return

    async def login(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user and user.password == password:
            return user
        return None

    async def send_email(self, email, *args, **kwargs):
        token = create_confirmation_token({"email": email})
        link = f"http://{Config.DOMAIN}/api/v1/auth/verify_email/{token}"
        template = f"""
            <h1>Welcome to Fast Book</h1>
            <p>Please click <a href="{link}">here</a> to confirm your email address</p>
        </html>
        """
        await send_email(email, "Welcome to the library",template=template)
    
    async def verify_email(self, token, session: AsyncSession):
        user_data = verify_confirmation_token(token)
        if not user_data:
            return False
        email = user_data.get('email')
        user = await self.get_user_by_email(email, session)
        if not user:
            return False
        await self.update_user(user,{'is_verified':True},session)
        return True