# MIT License

# Copyright(c) 2021-2022 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import TYPE_CHECKING, Generic, Iterable, Optional, Type, TypeAlias, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from database.models import Model

if TYPE_CHECKING:
    TSession: TypeAlias = sessionmaker[AsyncSession]
else:
    TSession: TypeAlias = AsyncSession

TModel = TypeVar('TModel', bound=Model)


class Repository(Generic[TModel]):
    """
    The base repository class.

    Args:
        session (sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]): The session
            to use to interact with the database.

    """

    model: Type[TModel]
    session: TSession

    def __init__(self, session: TSession):
        self.session = session

    async def __get_by_id(self, session: AsyncSession,
                          model_id: int) -> Optional[TModel]:
        """
        Get a model by its id

        Args:
            session (sqlalchemy.ext.asyncio.AsyncSession): The
                session to use to interact with the database.
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model or None: The model object.

        """
        model = self.model
        stmt = select(model).where(model.id == model_id)
        return (await session.execute(stmt)).scalars().first()

    async def __exists(self, model_id: int) -> bool:
        """
        Check if a model exists

        Args:
            model_id (int): The id of the model to check.

        Returns:
            bool: True if the model exists, False otherwise.

        """
        model = await self.find(model_id)
        return model is not None

    # ------------------------------------------------------------
    #                     Read methods
    # ------------------------------------------------------------

    async def find(self, model_id: int) -> Optional[TModel]:
        """
        Get a model by id

        Args:
            model_id (int): The id of the model to get.

        Returns:
            Optional[database.models.Model]: The model object.

        """
        async with self.session() as session:
            return await self.__get_by_id(session, model_id)

    async def find_or_create(self, model_id: int) -> TModel:
        """
        Get a model by id, or create it if it doesn't exist

        Args:
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        # the create method will return the model if it exists
        return await self.create(model_id)

    async def all(self) -> tuple[TModel, ...]:
        """
        Get all models

        Returns:
            tuple[database.models.Model]: The models.

        """
        async with self.session() as session:
            stmt = select(self.model)
            return tuple((await session.execute(stmt)).scalars())

    # ------------------------------------------------------------
    #                     Create methods
    # ------------------------------------------------------------

    async def create(self, model_id: int) -> TModel:
        """
        Create a new model with default values

        Args:
            model_id (int): The id of the model to create.

        Returns:
            database.models.Model: The model instance.

        """
        if await self.__exists(model_id):
            if (model := await self.find(model_id)):
                return model
        model = self.model(model_id)
        await self.save(model)
        return model

    async def create_many(self, model_ids: Iterable[int]) -> tuple[TModel, ...]:
        """
        Create many models

        Args:
            model_ids (Iterable[int]): The ids of the models to create.

        Returns:
            tuple[Model]: The models created.

        """
        models = list[TModel]()
        for model_id in model_ids:
            if (model := await self.create(model_id)):
                models.append(model)
        return tuple(models)

    async def save(self, model: TModel) -> None:
        """
        Save a model to the database

        Args:
            model (database.models.Model): The model to save.

        """
        if not await self.__exists(model.id):
            # if not exists, create
            async with self.session() as session:
                session.add(model)
                await session.commit()
        else:
            # if exists, update
            await self.update(model)

    async def save_many(self, models: Iterable[TModel]) -> None:
        """
        Save many models

        Args:
            models (Iterable[database.models.Model]): The models to save.

        """
        for model in models:
            await self.save(model)

    # ------------------------------------------------------------
    #                     Update methods
    # ------------------------------------------------------------

    async def update(self, model: TModel) -> None:
        """
        Update a model in the database

        Args:
            model (database.models.Model): The model to update.

        """
        if await self.__exists(model.id):
            async with self.session() as session:
                db_model = await self.__get_by_id(session, model.id)
                if db_model:
                    db_model.merge(model)
                    await session.commit()
        else:
            await self.save(model)

    # ------------------------------------------------------------
    #                     Delete methods
    # ------------------------------------------------------------

    async def delete(self, model: TModel | int) -> bool:
        """
        Delete a model

        Args:
            model (database.models.Model or int): The model (or id) to delete.

        Returns:
            bool: True if the model was deleted, False otherwise.

        """
        if isinstance(model, int):
            if await self.__exists(model):
                model_to_delete = await self.find(model)
            else:
                return False
        elif await self.__exists(model.id):
            model_to_delete = model
        else:
            return False
        async with self.session() as session:
            await session.delete(model_to_delete)
            await session.commit()
            return True

    # ------------------------------------------------------------
    #                         Aliases
    # ------------------------------------------------------------

    find_by_id = find
    get = find
    get_by_id = find
    find_by_id_or_create = find_or_create
    get_by_id_or_create = find_or_create
    get_or_create = find_or_create
    sync = save
    destroy = delete
    truncate = delete
