from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def create_note(db: Session, note_in: NoteCreate, user_id: int):
    note = Note(**note_in.dict(), user_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session, user_id: int):
    return db.query(Note).filter(Note.user_id == user_id).all()

def get_note_by_id(db: Session, note_id: int, user_id: int):
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()

def update_note(db: Session, note: Note, note_in: NoteUpdate):
    for field, value in note_in.dict(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note: Note):
    db.delete(note)
    db.commit()