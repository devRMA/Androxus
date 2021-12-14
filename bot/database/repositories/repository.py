# MIT License

# Copyright(c) 2021 Rafael

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


from typing import List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.model import Model


class Repository:
    """
    The base repository class.

    Args:
        session (sqlalchemy.ext.asyncio.AsyncSession): The session to use to
        interact with the database.

    """

    model = Model

    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    async def __get_by_id(cls, session: AsyncSession,
                          model_id: int) -> Optional[Model]:
        """
        Get a model by its id

        Args:
            session (sqlalchemy.ext.asyncio.AsyncSession): The session to use
            to interact with the database.
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        model = cls.model
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

    """
    ------------------------------------------------------------
                        Read methods
    ------------------------------------------------------------
    """

    async def find(self, model_id: int) -> Optional[Model]:
        """
        Get a model by id

        Args:
            model_id (int): The id of the model to get.

        Returns:
            Optional[database.models.Model]: The model object.

        """
        async with self.session() as session:
            return await self.__get_by_id(session, model_id)

    async def find_or_create(self, model_id: int) -> Model:
        """
        Get a model by id, or create it if it doesn't exist

        Args:
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        model = await self.find(model_id)
        if model is None:
            model = await self.create(model_id)
        return model

    async def all(self) -> List[Model]:
        """
        Get all models

        Returns:
            List[database.models.Model]: The models.

        """
        async with self.session() as session:
            stmt = select(self.model)
            return tuple((await session.execute(stmt)).scalars())

    """
    ------------------------------------------------------------
                        Create methods
    ------------------------------------------------------------
    """

    async def create(self, model_id: int) -> Optional[Model]:
        """
        Create a new model with default values

        Args:
            model_id (int): The id of the model to create.

        Returns:
            database.models.Model: The model instance.

        """
        if await self.__exists(model_id):
            return await self.find(model_id)
        else:
            model = self.model(model_id)
            await self.save(model)
            return model

    async def create_many(self, model_ids: List[int]) -> List[Model]:
        """
        Create many models

        Args:
            model_ids (List[int]): The ids of the models to create.

        Returns:
            List[Model]: The models created.

        """
        models = []
        for model_id in model_ids:
            models.append(await self.create(model_id))
        return models

    async def save(self, model: Model):
        """
        Save a model to the database

        Args:
            model (database.models.Model): The model to save.

        """
        if not (await self.__exists(model.id)):
            # if not exists, create
            async with self.session() as session:
                session.add(model)
                await session.commit()
        else:
            # if exists, update
            await self.update(model)

    async def save_many(self, models: List[Model]):
        """
        Save many models

        Args:
            models (List[database.models.Model]): The models to save.

        """
        for model in models:
            await self.save(model)

    """
    ------------------------------------------------------------
                        Update methods
    ------------------------------------------------------------
    """

    async def update(self, model: Model):
        """
        Update a model in the database

        Args:
            model (database.models.Model): The model to update.

        """
        if await self.__exists(model.id):
            async with self.session() as session:
                db_model = await self.__get_by_id(session, model.id)
                db_model.merge(model)
                await session.commit()
        else:
            await self.save(model)

    """
    ------------------------------------------------------------
                        Delete methods
    ------------------------------------------------------------
    """

    async def delete(self, model: Union[Model, int]) -> bool:
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
        elif isinstance(model, Model):
            if await self.__exists(model.id):
                model_to_delete = model
            else:
                return False
        else:
            return False
        async with self.session() as session:
            await session.delete(model_to_delete)
            await session.commit()
            return True

    """
    ------------------------------------------------------------
                            Aliases
    ------------------------------------------------------------
    """

    async def find_by_id(self, model_id: int) -> Optional[Model]:
        """
        Get a model by id

        Args:
            model_id (int): The id of the model to get.

        Returns:
            Optional[database.models.Model]: The model object.

        """
        return await self.find(model_id)

    async def find_by_id_or_create(self, model_id: int) -> Model:
        """
        Get a model by id, or create it if it doesn't exist

        Args:
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        return await self.find_or_create(model_id)

    async def get_by_id(self, model_id: int) -> Optional[Model]:
        """
        Get a model by id

        Args:
            model_id (int): The id of the model to get.

        Returns:
            Optional[database.models.Model]: The model object.

        """
        return await self.find(model_id)

    async def get_by_id_or_create(self, model_id: int) -> Model:
        """
        Get a model by id, or create it if it doesn't exist

        Args:
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        return await self.find_or_create(model_id)

    async def get(self, model_id: int) -> Optional[Model]:
        """
        Get a model by id

        Args:
            model_id (int): The id of the model to get.

        Returns:
            Optional[database.models.Model]: The model object.

        """
        return await self.find(model_id)

    async def get_or_create(self, model_id: int) -> Model:
        """
        Get a model by id, or create it if it doesn't exist

        Args:
            model_id (int): The id of the model to get.

        Returns:
            database.models.Model: The model object.

        """
        return await self.find_or_create(model_id)

    async def sync(self, model: Model):
        """
        Save a model to the database

        Args:
            model (database.models.Model): The model to save.

        """
        return await self.save(model)

    async def destroy(self, model: Union[Model, int]) -> bool:
        """
        Delete a model

        Args:
            model (database.models.Model or int): The model (or id) to delete.

        Returns:
            bool: True if the model was deleted, False otherwise.

        """
        return await self.delete(model)

    async def truncate(self, model: Union[Model, int]) -> bool:
        """
        Delete a model

        Args:
            model (database.models.Model or int): The model (or id) to delete.

        Returns:
            bool: True if the model was deleted, False otherwise.

        """
        return await self.delete(model)
