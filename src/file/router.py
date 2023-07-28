from typing import Annotated, List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse

from src.auth.database import User, get_async_session
from src.auth.auth import current_user

from src.file.service import (
    write_file,
    delete_file_from_db_and_storage,
    get_file_by_id,
    get_keys_file_from_db,
    get_all_users_files
)

from src.file.schemas import FileCreate, FileGet

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/file",
    tags=["file"]
)


@router.get("/", response_model=List[FileGet])
async def get_files_by_user(
    user: Annotated[User, Depends(current_user)],
    session: AsyncSession = Depends(get_async_session)
) -> any:
    group_files = await get_all_users_files(
        user_id=user.id,
        session=session
    )
    return group_files



@router.post("/", response_model=None)
async def add_new_file(
    user: Annotated[User, Depends(current_user)], 
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    id_user = user.id
    response = await write_file(file=file, id_user=id_user, session=session)

    if response == 'error':
        return {"error": file.filename}

    if response == 'file already exists':
        return {'error': 'file already exists'}

    return {"filename": file.filename, "file_id": response}


@router.delete("/{file_id}", response_model=None)
async def delete_file(
    user: Annotated[User, Depends(current_user)],
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    status = await delete_file_from_db_and_storage(
        file_id=file_id,
        session=session
    )

    return {"status": status}


@router.get("/{file_id}", response_model=FileGet)
async def get_file(
    user: Annotated[User, Depends(current_user)],
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    file = await get_file_by_id(
        file_id=file_id,
        session=session
    )

    if file == 'file doesnt exist':
        raise HTTPException(status_code=404, detail='item not found')
    print(file)
    return file


@router.get('/keys/{file_id}', response_model=None)
async def get_keys_by_file(
    user: Annotated[User, Depends(current_user)],
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    data = await get_keys_file_from_db(
        file_id=file_id,
        session=session
    )
    print(data)
    return data


@router.get('/download/{file_id}', response_model=None)
async def download_file_by_id(
    user: Annotated[User, Depends(current_user)],
    file_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> any:
    file = await get_file_by_id(
        file_id=file_id,
        session=session
    )

    if file == 'file doesnt exist':
        raise HTTPException(status_code=404, detail='item not found')
    
    return FileResponse(
        path=file['path'], filename=file['name'], media_type='text/csv'
    )
