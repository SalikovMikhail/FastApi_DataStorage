from typing import List
import os
import shutil
from datetime import datetime
import pandas as pd

from fastapi import UploadFile, Depends

from config import PATH_FILE

from src.file.repository import (
    add_file,
    check_file,
    delete_file,
    get_file, 
    get_keys_from_file,
    get_all_files_by_user
)
from src.file.schemas import FileCreate

from src.auth.database import get_async_session
from src.auth.auth import current_user
from sqlalchemy.ext.asyncio import AsyncSession


def get_data(df: pd.DataFrame) -> List:
    keys = df.keys()
    keys = list(keys.array)

    data = df.values.tolist()

    map_data = []

    for item in data:
        obj = dict()
        count = 0
        for key in keys:
            obj[key] = item[count]
            count += 1
        
        map_data.append(obj)

    result = {
        'keys': keys,
        'data': map_data
    }

    return result


async def write_file(file: UploadFile, id_user: int, session: AsyncSession = Depends(get_async_session)):
    """
    Write file in storage and DB
    """

    path_to_file = os.path.join(PATH_FILE, file.filename)

    file_exists = await check_file(filename=file.filename, session=session)


    if file_exists:
        return 'file already exists'

    try:
        with open(path_to_file, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        df = pd.read_csv(path_to_file)

        data = get_data(df=df)

        file_dict = {
            'name': file.filename,
            'download_at': datetime.utcnow(),
            'data': data,
            'user_id': id_user,
            'path': path_to_file
        }

        
        id = await add_file(file_create=file_dict, session=session)
        return id
    except Exception as e:
        print(e)
        return 'error'

async def delete_file_from_db_and_storage(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    path_file = await delete_file(
        file_id=file_id,
        session=session
    )

    if path_file is None:
        return 'file doesnt exists'

    path_file = path_file[0]

    try:
        os.remove(path_file)
    except Exception as e:
        print(e)
    
    return 'sucsess'


async def get_file_by_id(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    file = await get_file(
        file_id=file_id,
        session=session
    )

    if file is None:
        return 'file doesnt exist'

    file = {
        'id': file[0],
        'name': file[1],
        'download_at': file[2],
        'user': file[4],
        'path': file[5]
    }
    return file


async def get_keys_file_from_db(
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    data = await get_keys_from_file(
        file_id=file_id,
        session=session
    )
    print(data)
    return data[0]['keys']

async def get_all_users_files(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    """
    Get all files by users from DB
    """
    group_files = await get_all_files_by_user(
        user_id=user_id,
        session=session
    )
    print(group_files)
    result = []
    for f in group_files:
        obj = {
            'id': f[0],
            'name': f[1],
            'download_at': f[2],
            'user': f[4],
            'path': f[5]
        }
        result.append(obj)
    return result
