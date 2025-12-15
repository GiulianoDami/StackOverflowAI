
from pydantic import BaseModel
from typing import List

class AIResponse(BaseModel):
    answer: str
    sources: List[int]
```

```plaintext
