from typing import List, Tuple, Annotated
from typing_extensions import TypedDict
from operator import add
from typing import TypedDict, Dict, List
from output_parsers import AstroData_Pydantic,AstroData_Typed,IntentSpec_Pydantic,IntentSpec_Typed
from typing import Dict, List, Optional, TypedDict


class GraphState(TypedDict):
    # inputs
    name: str
    dob: str
    tob: str
    place: str
    question: str
    # intermediate
    astro_data: Optional[AstroData_Pydantic]
    intent: Optional[IntentSpec_Pydantic]
    rag_query: Optional[str]
    context_docs: Optional[List[dict]]  # store docs (page_content + metadata)
    # output
    answer: Optional[str]