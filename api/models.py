from pydantic import BaseModel

class User(BaseModel):
    """
    Represents a user with basic profile information.
    Attributes:
        login (str): The username or login identifier of the user.
        id (int): The unique identifier for the user.
        created_at (str): The timestamp when the user was created.
        avatar_url (str): The URL to the user's avatar image.
        bio (str, optional): A short biography or description of the user. Defaults to None.
    """

    login: str
    id: int
    created_at: str
    avatar_url: str
    bio: str | None = None
