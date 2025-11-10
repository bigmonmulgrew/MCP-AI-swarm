from pydantic import BaseModel, Field
from typing import Any, Dict, List

class DroneQueryObject(BaseModel):
    Query: str
    RecursionDepth: int
    OriginalSPrompt: str
    MessageHistory: Dict[str, Any]
    CurrentTime: float

class DroneOnlineObject(BaseModel):
    ToolServerName: str
    ToolServerAddress: str
    ToolServerPort: str
    ToolServerCategory: str
    Timeout:int

class Message(BaseModel):
    Msg: str
    Images: List[str]   # base64-encoded strings
    Files: List[str]    # could be filenames, URLs, or base64 strings
    Videos: List[str]   # same — filenames, URLs, or encoded data
    
class MessageHistory(BaseModel):
    Entity: str
    MessageObject: Message
    SenderHostname: List[str]
    
# Define a Pydantic model for the request body
class UserQuery(BaseModel):
    query: str
    system_prompt: str = Field(
        None, description="System prompt to use, overrides the default one."
    )
    chat_name: str = Field(None, description="Chat session identifier.")
    debug_test: bool = Field(
        False,
        description="If you set this to true making a request you will get a canned response back",
    )
    verbose: bool = Field(
        False,
        description="If set to true this will include some additional debugging information not required to function, such as the system prompt.",
    )