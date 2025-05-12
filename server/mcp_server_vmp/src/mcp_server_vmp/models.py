
from ast import Expression
from dataclasses import dataclass, field
from typing import List, Optional

from volcenginesdkcore.interceptor import RuntimeOption


@dataclass
class RequestBase:
    def __post_init__(self):
         self.build_swagger_types()
    
    def build_swagger_types(self):
        self.swagger_types = {attr_name:type(attr_value).__name__ for attr_name, attr_value in vars(self).items() if not attr_name.startswith('_') and not callable(attr_value)}
        self.attribute_map = {attr_name:attr_name for attr_name, attr_value in vars(self).items() if not attr_name.startswith('_') and not callable(attr_value)}

    def with_runtime_option(self, runtime_options: RuntimeOption):
        self._configuration = runtime_options
        return self

@dataclass
class ListWorkspacesRequest(RequestBase):
    PageNumber: int = 1
    PageSize: int = 100

@dataclass
class QueryInstantMetricsRequest(RequestBase):
    WorkspaceId: str
    Expression: str
    Time: Optional[str] = None

@dataclass
class QueryRangeMetricsRequest(RequestBase):
    WorkspaceId: str
    Expression: str
    Start: str
    End: str
    Step: Optional[str] = None
       
@dataclass
class QueryLabelValuesRequest(RequestBase):
    WorkspaceId: str
    Label: str
    Start: Optional[str] = None
    End: Optional[str] = None
    Match: Optional[List[str]] = None
    Limit: Optional[int] = None

@dataclass
class QueryLabelNamesRequest(RequestBase):
    WorkspaceId: str
    Start: Optional[str] = None
    End: Optional[str] = None
    Match: Optional[List[str]] = None
    Limit: Optional[int] = None

