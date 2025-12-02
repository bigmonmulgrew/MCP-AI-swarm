from pydantic import BaseModel, Field
from typing import Any, Dict, List, Union

class SenderHistory(BaseModel):
    Hostname: List[str] # For debugging, allows a trace route of MCP drones

class Message(BaseModel):
    role: str           # Message sender type
    Msg: str            # Tha actual message
    stucturedMsg: List[Any] # Structured data strings
    Images: List[str]   # base64-encoded strings
    Files: List[str]    # could be filenames, URLs, or base64 strings
    Videos: List[str]   # same — filenames, URLs, or encoded data

class DroneQueryObject(BaseModel):
    Query: str
    RecursionDepth: int
    OriginalSPrompt: str
    MessageHistory: Dict[str, Union[SenderHistory, Message]]
    CurrentTime: float

class DroneOnlineObject(BaseModel):
    ToolServerName: str
    ToolServerAddress: str
    ToolServerPort: str
    ToolServerCategory: str
    Timeout:int
    
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
    
class AIQuery(BaseModel):
    prompt: str = Field(
        description=""
    )
    model: str = Field(
        description="The model to use"
    )
    options: Dict[str, Any] = Field(
        {}, description="Options provided to the AI backend"
    )
    temperature: float = Field(
        0.0, description="The temperature used to control ai reasoning. 0 = predicable results. Recommend 0.6-0.8 for better reasoning."
    )
    max_tokens: int = Field(
        10000, description="Token limit for the AI model. Can be used to help truncate messages or long requests"
    )

class BlocHubResponse(BaseModel):
    light_result: int = Field(
        description="The final result to send to bloc hub formatted as a json string. Red: 0, Amber: 1, Green: 2"
    )
    text_result: str = Field(
        description="Short advisory text sumamrising the results"
    )
    time: int = Field(
        description="The generation time of the response in UTC"
    )
    debug_data: str = Field(
        description="A JSON data structure containing summaries of data used in reasoning. Only provided when verbose = true"
    )