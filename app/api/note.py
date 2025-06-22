from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_active_user

from app.models.user import User
from app import schemas, crud

router = APIRouter(prefix="/api/v1/notes", tags=["Notes"])

@router.post("/", response_model=schemas.note.NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(note_in: schemas.note.NoteCreate, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return crud.note.create_note(db=db, note_in=note_in, user_id=current_user.id)

@router.get("/", response_model=List[schemas.note.NoteRead], status_code=status.HTTP_200_OK)
def list_notes(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return crud.note.get_notes(db=db, user_id=current_user.id)

@router.get("/{note_id}", response_model=schemas.note.NoteRead, status_code=status.HTTP_200_OK)
def get_note(note_id: int, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    note = crud.note.get_note_by_id(db=db, note_id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=schemas.note.NoteRead, status_code=status.HTTP_200_OK)
def update_note(note_id: int, note_in: schemas.note.NoteUpdate, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    note = crud.note.get_note_by_id(db=db, note_id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud.note.update_note(db=db, note=note, note_in=note_in)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    note = crud.note.get_note_by_id(db=db, note_id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    crud.note.delete_note(db=db, note=note)
    return {'message':'Note deleted', 'status':status.HTTP_204_NO_CONTENT }