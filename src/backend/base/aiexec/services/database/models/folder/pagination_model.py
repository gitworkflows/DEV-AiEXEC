from fastapi_pagination import Page

from aiexec.helpers.base_model import BaseModel
from aiexec.services.database.models.flow.model import Flow
from aiexec.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[Flow]
