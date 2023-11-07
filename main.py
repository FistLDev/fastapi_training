from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'You are pretty!'


@app.post('/post')
def post(id: int, timestamp: int):
    entity = Timestamp(id=id, timestamp=timestamp)
    post_db.append(entity)

    return 'Success'


@app.get('/dog')
def get_dogs(kind: Optional[str] = None):
    if kind is not None:
        matching_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        if matching_dogs:
            return matching_dogs
        else:
            raise HTTPException(status_code=404, detail=f'Dogs with kind type {kind} were not found')
    else:
        return list(dogs_db.values())


@app.post('/dog')
def add_dog(dog_data: Dog):
    new_pk = max(dogs_db.keys()) + 1
    dogs_db[new_pk] = dog_data

    return 'Success'


@app.get('/dog/{pk}')
def get_dog(pk: int):
    matching_dog = next((dog for dog in dogs_db.values() if dog.pk == pk), None)
    return matching_dog


@app.patch('/dog/{pk}')
def update_dog(pk: int, dog_data: Dog):
    dogs_db[pk] = dog_data

    return 'Success'
