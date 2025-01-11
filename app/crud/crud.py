from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_by_id(model, id: int, db: Session):
    item = db.query(model).filter(model.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item

def get_all(model, skip: int, limit: int, db: Session):
    return db.query(model).offset(skip).limit(limit).all()

def create_item(model, schema, db: Session):
    data = schema.model_dump() if hasattr(schema, 'model_dump') else schema
    db_item = model(**data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(model, id: int, db: Session):
    item = get_by_id(model, id, db)
    db.delete(item)
    db.commit()
    return item

def update_item(model, id: int, schema, db: Session):
    db_item = get_by_id(model, id, db)
    for key, value in schema.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def clear_all(model, db: Session):
    db.query(model).delete()
    db.commit()
    return {"message": f"All {model.__name__} records deleted"}
