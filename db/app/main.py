from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Основные команды
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User) #Создание юзера
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_name(db, name=user.name):
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_entity(db, models.User, **user.dict())

@app.get("/users/{user_id}", response_model=schemas.User) #Чтение юзера
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_entity(db, models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", status_code=204) #Удаление юзера
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_entity(db, models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_entity(db, db_user)
    return None

@app.get("/users/", response_model=list[schemas.User]) #Чтение всех юзеров(хз зачем по приколу)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_entities(db, models.User, skip=skip, limit=limit)

#Тестовые команды

@app.post("/roles/", 
          response_model=schemas.Role,
          status_code=status.HTTP_201_CREATED,
          summary="Create new role",
          description="Add new role into db")
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name already exist"
        )
    new_role = models.Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@app.get("/roles/", 
         response_model=List[schemas.Role],
         summary="Get list of roles",
         description="Get list of all roles")
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Role).offset(skip).limit(limit).all()

@app.get("/roles/{role_id}", 
         response_model=schemas.Role,
         summary="Get role by ID",
         description="Return data about role")
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role