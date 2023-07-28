from typing import Tuple, Union
from fastapi import Depends

from sqlalchemy import insert, select, values, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.file.models import file
from src.file.schemas import FileCreate

from src.auth.database import get_async_session


async def delete_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Union[Tuple, None]:
    """
    Delete file from DB
    """
    query = delete(file).where(file.c.id == file_id).returning(file.c.path)
    path_file = await session.execute(query)
    await session.commit()
    return path_file.fetchone()


async def get_keys_from_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    """
    Get data by file
    """
    query = select(file.c.data).where(file.c.id == file_id)
    data = await session.execute(query)
    data = data.fetchone()
    return data


async def get_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    """
    Get file from DB by id
    """
    query = select(file).where(file.c.id == file_id)
    file_ = await session.execute(query)
    file_ = file_.fetchone()
    return file_


async def get_all_files_by_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)       
) -> list:
    """
    Get all file by user
    """
    query = select(file).where(file.c.user_id == user_id)

    group_file = await session.execute(query)
    group_file = group_file.all()
    return group_file


async def check_file(
    filename: str,
    session: AsyncSession = Depends(get_async_session)
) -> bool:
    """
    Check file in DB
    """
    print(filename)
    query = select(file.c.id).where(file.c.name == filename)
    
    file_ = await session.execute(query)
    file_ = file_.fetchone()
    print(file_)
    if file_ is None:
        return False
    else:
        return True

async def add_file(
    file_create: FileCreate,
    session: AsyncSession = Depends(get_async_session)
) -> int:
    """
    Add data from file to DB File
    """
    query = insert(file).values(**file_create).returning(file.c.id)

    file_id = await session.execute(query)
    file_id = file_id.fetchone()
    await session.commit()
    return file_id[0]
