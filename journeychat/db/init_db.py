import logging
from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.db import base  # noqa: F401

# from journeychat.recipe_data import RECIPES

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@journeychat.com"

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                username="SuperUser1",
                display_name="Initial Super User",
                email=FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        # if not user.recipes:
        #     for recipe in RECIPES:
        #         recipe_in = schemas.RecipeCreate(
        #             label=recipe["label"],
        #             source=recipe["source"],
        #             url=recipe["url"],
        #             submitter_id=user.id,
        #         )
        #         crud.recipe.create(db, obj_in=recipe_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )