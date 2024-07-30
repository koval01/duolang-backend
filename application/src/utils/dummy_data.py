from sqlalchemy import text
from fastapi_async_sqlalchemy import db

from ..models.profile import Profile


async def create_dummy_data():
    profile1 = Profile(
        displayName="Rusty Bar",
        telegram=1
    )
    profile2 = Profile(
        displayName="Bash Bar",
        telegram=2
    )
    profile3 = Profile(
        displayName="Python Bar",
        telegram=3
    )
    profile4 = Profile(
        displayName="Java Bar",
        telegram=4
    )
    profile5 = Profile(
        displayName="C++ Bar",
        telegram=5
    )
    profile6 = Profile(
        displayName="JavaScript Bar",
        telegram=6
    )
    profile7 = Profile(
        displayName="PHP Bar",
        telegram=7
    )
    profile8 = Profile(
        displayName="Ruby Bar",
        telegram=8
    )
    profile9 = Profile(
        displayName="Go Bar",
        telegram=9
    )
    profile10 = Profile(
        displayName="Assembly Bar",
        telegram=10
    )

    async with db():
        # Clean up database
        await db.session.execute(text("DELETE FROM profile;"))

        # Add dummy data
        db.session.add_all(
            [profile1, profile2, profile3, profile4, profile5, profile6, profile7, profile8, profile9, profile10]
        )
        await db.session.commit()

