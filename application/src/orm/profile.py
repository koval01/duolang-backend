import uuid
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy import select, delete, update
from fastapi_async_sqlalchemy import db

from application.src.models import Profile, RoleEnum
from application.src.schemas import ProfileItemCreate, ProfileItemUpdate


class ProfileORM:
    """
    A class to handle operations related to the `Profile` model using SQLAlchemy ORM.

    This class provides methods to fetch, delete, update, and initialize user profiles
    from a database. It also includes utility methods to check if a user exists and if a
    user is an admin.

    Attributes:
        web_app_init_data (WebAppInitData): Initialization data from a Telegram WebApp.
    """

    def __init__(self, web_app_init_data: WebAppInitData) -> None:
        """
        Initializes the ProfileORM with the provided WebAppInitData.

        Args:
            web_app_init_data (WebAppInitData): Initialization data from a Telegram WebApp.
        """
        self.web_app_init_data = web_app_init_data

    async def fetch_user(self, all_users: bool = False, by_id: uuid.UUID | None = None) -> Profile or list[Profile]:
        """
        Fetches a user profile or list of profiles from the database.

        Args:
            all_users (bool, optional): If True, fetches all user profiles. Defaults to False.
            by_id (uuid.UUID, optional): If provided, fetches the user by this specific ID. Defaults to None.

        Returns:
            Profile or list[Profile]: The fetched profile(s) from the database.
        """
        query = select(Profile).where(
            Profile.telegram == self.web_app_init_data.user.id \
            if not by_id else \
            Profile.id == by_id
        )
        result = await db.session.execute(query)
        scalars = result.scalars()
        return scalars.all() if all_users else scalars.first()

    async def delete_user(self) -> bool:
        """
        Deletes a user profile from the database based on the Telegram ID.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        query = delete(Profile).where(Profile.telegram == self.web_app_init_data.user.id)
        result = await db.session.execute(query)
        await db.session.commit()

        return True if result else False

    async def update_user(self, body: ProfileItemUpdate) -> Profile:
        """
        Updates a user profile in the database with the provided data.

        Args:
            body (ProfileItemUpdate): The update data for the profile.

        Returns:
            Profile: The updated profile from the database.
        """
        query = (
            update(Profile)
            .where(Profile.telegram == self.web_app_init_data.user.id)
            .values(**body.model_dump(exclude_none=True))
            .returning(Profile)
        )
        result = await db.session.execute(query)
        updated_profile = result.scalars().first()
        await db.session.commit()

        return updated_profile

    async def exists(self) -> bool:
        """
        Checks if the user profile exists in the database.

        Returns:
            bool: True if the profile exists, False otherwise.
        """
        profile = await self.fetch_user()
        if profile:
            return True

        return False

    @staticmethod
    def is_admin(profile: Profile) -> bool:
        """
        Checks if the provided profile has an admin role.

        Args:
            profile (Profile): The profile to check.

        Returns:
            bool: True if the profile is an admin, False otherwise.
        """
        return profile.role is RoleEnum.admin

    async def init_user(self, display_name: str) -> uuid.UUID:
        """
        Initializes a new user profile if it doesn't exist, or returns the existing profile's ID.

        Args:
            display_name (str): The display name for the new user profile.

        Returns:
            uuid.UUID: The ID of the initialized or existing user profile.
        """
        profile = await self.fetch_user()
        if profile:
            return profile.id

        new_profile = ProfileItemCreate(
            displayName=display_name,
            telegram=self.web_app_init_data.user.id,
        )
        new_profile = Profile(**new_profile.model_dump())
        db.session.add(new_profile)
        await db.session.commit()
        await db.session.refresh(new_profile)

        return new_profile.id
