from fastapi import FastAPI

from auth.router import router as router_auth
from media.router import router as router_media
from reviews.router import router as router_reviews

app = FastAPI(
    title="Reviews "
)

app.include_router(router_auth)
app.include_router(router_media)
app.include_router(router_reviews)

# fake_users = [
#     {"id": 1, "name": "News", "ratings_qty": 5},
#     {"id": 2, "name": "Care", "ratings_qty": 0},
#     {"id": 3, "name": "Stuck", "ratings_qty": 28},
# ]

# class User(BaseModel):
#     id: int
#     name: str
#     ratings_qty: int


# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in fake_users if user.get("id") == user_id]


# fake_reviews = [
#     {"id": 1, "review": "Good Movie", "movie_id": 5, "user_id": 3},
#     {"id": 2, "review": "Bad Movie", "movie_id": 47, "user_id": 3},
#     {"id": 3, "review": "Average Movie", "movie_id": 19, "user_id": 1},
# ]


# @app.get("/reviews")
# def get_reviews(limit: int = 10, offset: int = 0):
#     return fake_reviews[offset:][:limit]


# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data": current_user}


# class Review(BaseModel):
#     id: int
#     review: str
#     movie_id: int = Field(ge=0)
#     user_id: int = Field(ge=0)


# @app.post("/reviews")
# def add_reviews(reviews: List[Review]):
#     fake_reviews.extend(reviews)
#     return {"status": 200, "data": fake_reviews}