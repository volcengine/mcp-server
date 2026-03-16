from dataclasses import dataclass
from typing import List, Dict, Optional, Any


# Request models


@dataclass
class ListWorkspaceRequest:
    """Request for listing workspaces.
    
    Filters only support filtering by "Name" parameter for workspace names.
    """

    PageNumber: int = 1
    PageSize: int = 10
    Filters: Optional[Dict[str, str]] = None
    ProjectName: str = "default"
    ListGlobal: bool = False
    Region: Optional[str] = None


@dataclass
class GetWorkspaceInfoRequest:
    """Request for getting workspace information."""

    WorkspaceID: str
    Region: Optional[str] = None


@dataclass
class ListQueryClustersRequest:
    """Request for listing query clusters."""

    PageNumber: int = 1
    PageSize: int = 10
    Name: str = ""
    ProjectName: str = "default"
    Region: Optional[str] = None


@dataclass
class GetQueryClusterRequest:
    """Request for getting query cluster information."""

    ClusterID: str
    Region: Optional[str] = None


@dataclass
class ListPreaggRequest:
    """Request for listing preaggregation rules."""

    WorkspaceName: str
    PageNumber: int = 1
    PageSize: int = 10
    onlyShowMine: bool = True
    Region: Optional[str] = None


@dataclass
class InfluxQueryRequest:
    """Request for InfluxDB query."""

    Workspace: str
    Queries: List[str]
    Epoch: Optional[str] = None
    Region: Optional[str] = None


@dataclass
class MetricsQueryRequest:
    """Request for querying metrics data."""

    Workspace: str
    Queries: List[Dict[str, Any]]
    Start: str
    End: str
    Region: Optional[str] = None


# Response models


@dataclass
class WorkspaceInfo:
    """Workspace information."""
    
    ID: str
    Status: str
    CreateTime: str
    UpdateTime: str
    WorkspaceBasicInfo: Optional[Dict[str, Any]] = None
    Quota: Optional[Any] = None
    ChargeType: Optional[str] = None
    Privilege: Optional[str] = None
    LatestUpdateUserId: Optional[str] = None
    CurrentBlacklistMaxDimension: Optional[int] = None
    CurrentWquotaMB: Optional[int] = None
    LatestBPMUrl: Optional[str] = None
    ProjectName: Optional[str] = None

    def __init__(self, **kwargs):
        """Handle field name variations and nested structures from API responses."""
        
        # Handle field name variations
        if 'Id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('Id')
        if 'id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('id')

        if 'WorkspaceBasicInfo' not in kwargs:
            kwargs['WorkspaceBasicInfo'] = {}

        if 'CreateTime' in kwargs:
            if isinstance(kwargs['CreateTime'], int):
                try:
                    from datetime import datetime
                    kwargs['CreateTime'] = datetime.fromtimestamp(kwargs['CreateTime']).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            if not isinstance(kwargs['CreateTime'], str):
                kwargs['CreateTime'] = str(kwargs['CreateTime'])
        if 'UpdateTime' in kwargs:
            if isinstance(kwargs['UpdateTime'], int):
                try:
                    from datetime import datetime
                    kwargs['UpdateTime'] = datetime.fromtimestamp(kwargs['UpdateTime']).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            if not isinstance(kwargs['UpdateTime'], str):
                kwargs['UpdateTime'] = str(kwargs['UpdateTime'])
        
        # Set all fields directly on self (not a new object)
        fields = ['ID', 'Status', 'CreateTime', 'UpdateTime', 'WorkspaceBasicInfo', 
                  'Quota', 'ChargeType', 'Privilege', 'LatestUpdateUserId', 
                  'CurrentBlacklistMaxDimension', 'CurrentWquotaMB', 'LatestBPMUrl', 
                  'ProjectName']
        
        for field in fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                if field == 'WorkspaceBasicInfo':
                    setattr(self, field, {})
                elif field in ['Quota', 'ChargeType', 'Privilege', 'LatestUpdateUserId', 
                             'LatestBPMUrl', 'ProjectName']:
                    setattr(self, field, None)
                elif field in ['CurrentBlacklistMaxDimension', 'CurrentWquotaMB']:
                    setattr(self, field, 0)
                elif field in ['CreateTime', 'UpdateTime']:
                    setattr(self, field, "")
                else:
                    setattr(self, field, '')


@dataclass
class ListWorkspaceResponse:
    """Response for listing workspaces."""

    Items: List[WorkspaceInfo]
    TotalId: int
    ResponseMetadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Convert dictionary items to WorkspaceInfo objects if needed."""
        if self.Items:
            processed_items = []
            for item in self.Items:
                if isinstance(item, dict):
                    # Handle field name variations and nested structures
                    item = item.copy()
                    
                    if 'Id' in item and not 'ID' in item:
                        item['ID'] = item.pop('Id')
                    if 'id' in item and not 'ID' in item:
                        item['ID'] = item.pop('id')
                        
                    processed_items.append(WorkspaceInfo(**item))
                else:
                    processed_items.append(item)
            self.Items = processed_items


@dataclass
class GetWorkspaceInfoResponse:
    """Response for getting workspace information."""

    Workspace: WorkspaceInfo
    ResponseMetadata: Optional[Dict[str, Any]] = None
    Quota: Optional[Dict[str, Any]] = None
    AdvanceInfo: Optional[Dict[str, Any]] = None
    StorageInfo: Optional[Dict[str, Any]] = None
    PrivateAddr: Optional[str] = None
    PublicAddr: Optional[str] = None
    BlacklistMaxDimensionCurrent: Optional[int] = None
    WquotaMBUsage: Optional[int] = None
    ProjectName: Optional[str] = None

    def __init__(self, **kwargs):
        """Handle actual API response structure with Summary field."""
        # Handle case where Workspace info is in Summary field
        if 'Summary' in kwargs and not 'Workspace' in kwargs:
            kwargs['Workspace'] = kwargs.pop('Summary')
        
        # Initialize all fields
        fields = ['Workspace', 'ResponseMetadata', 'Quota', 'AdvanceInfo', 'StorageInfo',
                  'PrivateAddr', 'PublicAddr', 'BlacklistMaxDimensionCurrent',
                  'WquotaMBUsage', 'ProjectName']
        
        for field in fields:
            if field in kwargs:
                if field == 'Workspace' and isinstance(kwargs[field], dict):
                    # Convert to WorkspaceInfo object
                    workspace_dict = kwargs[field].copy()
                    if 'Id' in workspace_dict and not 'ID' in workspace_dict:
                        workspace_dict['ID'] = workspace_dict.pop('Id')
                    if 'id' in workspace_dict and not 'ID' in workspace_dict:
                        workspace_dict['ID'] = workspace_dict.pop('id')
                    setattr(self, field, WorkspaceInfo(**workspace_dict))
                else:
                    setattr(self, field, kwargs[field])
            else:
                # Set default values for optional fields
                if field in ['Quota', 'AdvanceInfo', 'StorageInfo']:
                    setattr(self, field, {})
                elif field in ['PrivateAddr', 'PublicAddr', 'ProjectName']:
                    setattr(self, field, None)
                elif field in ['BlacklistMaxDimensionCurrent', 'WquotaMBUsage']:
                    setattr(self, field, 0)
                elif field == 'ResponseMetadata':
                    setattr(self, field, None)


@dataclass
class QueryClusterInfo:
    """Query cluster information."""

    ID: str
    Name: str
    Status: str
    CreatedAt: str
    UpdatedAt: str
    Description: Optional[str] = None
    ProjectName: Optional[str] = None
    Region: Optional[str] = None
    NodeNum: Optional[int] = None
    NodeSpecificationId: Optional[int] = None
    NodeSpecificationName: Optional[str] = None
    AdvanceConfig: Optional[Dict[str, Any]] = None
    Workspaces: Optional[List[Dict[str, Any]]] = None
    DeployAZ: Optional[List[Dict[str, Any]]] = None
    StatusTicket: Optional[str] = None

    def __init__(self, **kwargs):
        """Handle field name variations and nested structures from API responses."""
        # Handle nested QueryClusterBasicInfo structure
        if 'QueryClusterBasicInfo' in kwargs:
            basic_info = kwargs.pop('QueryClusterBasicInfo')
            if basic_info:
                for key, value in basic_info.items():
                    if key not in kwargs:
                        kwargs[key] = value
        
        # Handle field name variations
        if 'Id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('Id')
        if 'id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('id')
        
        # Map API field names to model field names
        if 'ClusterName' in kwargs and 'Name' not in kwargs:
            kwargs['Name'] = kwargs.pop('ClusterName')
        
        # Keep time fields as string format
        if 'CreatedAt' in kwargs and not isinstance(kwargs['CreatedAt'], str):
            kwargs['CreatedAt'] = str(kwargs['CreatedAt'])
        if 'UpdatedAt' in kwargs and not isinstance(kwargs['UpdatedAt'], str):
            kwargs['UpdatedAt'] = str(kwargs['UpdatedAt'])
        
        if 'CreateTime' in kwargs and 'CreatedAt' not in kwargs:
            kwargs['CreatedAt'] = str(kwargs['CreateTime'])
        if 'UpdateTime' in kwargs and 'UpdatedAt' not in kwargs:
            kwargs['UpdatedAt'] = str(kwargs['UpdateTime'])
        
        # Set all fields directly on self (not a new object)
        fields = ['ID', 'Name', 'Status', 'CreatedAt', 'UpdatedAt', 
                 'Description', 'ProjectName', 'Region', 'NodeNum', 'NodeSpecificationId', 
                 'NodeSpecificationName', 'AdvanceConfig', 'Workspaces', 'DeployAZ', 'StatusTicket']
        
        for field in fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                if field == 'Description':
                    setattr(self, field, None)
                elif field in ['ProjectName', 'Region', 'NodeSpecificationName', 'StatusTicket']:
                    setattr(self, field, None)
                elif field in ['NodeNum', 'NodeSpecificationId']:
                    setattr(self, field, 0)
                elif field in ['AdvanceConfig', 'Workspaces', 'DeployAZ']:
                    setattr(self, field, None)
                elif field in ['CreatedAt', 'UpdatedAt']:
                    setattr(self, field, '')
                else:
                    setattr(self, field, '')


@dataclass
class ListQueryClustersResponse:
    """Response for listing query clusters."""

    Items: List[QueryClusterInfo]
    TotalId: int
    ResponseMetadata: Optional[Dict[str, Any]] = None

    def __init__(self, **kwargs):
        """Initialize ListQueryClustersResponse with support for Page.TotalCount."""
        if 'Items' in kwargs:
            self.Items = kwargs['Items']
        else:
            self.Items = []
            
        if 'TotalId' in kwargs:
            self.TotalId = kwargs['TotalId']
        elif 'Page' in kwargs and 'TotalCount' in kwargs['Page']:
            self.TotalId = kwargs['Page']['TotalCount']
        else:
            self.TotalId = 0
            
        if 'ResponseMetadata' in kwargs:
            self.ResponseMetadata = kwargs['ResponseMetadata']
        else:
            self.ResponseMetadata = None

    def __post_init__(self):
        """Convert dictionary items to QueryClusterInfo objects if needed."""
        if self.Items:
            processed_items = []
            for item in self.Items:
                if isinstance(item, dict):
                    item = item.copy()
                    
                    # Handle nested QueryClusterBasicInfo structure if exists
                    if 'QueryClusterBasicInfo' in item:
                        item.update(item.pop('QueryClusterBasicInfo'))
                    
                    if 'Id' in item and not 'ID' in item:
                        item['ID'] = item.pop('Id')
                    if 'id' in item and not 'ID' in item:
                        item['ID'] = item.pop('id')
                        
                    processed_items.append(QueryClusterInfo(**item))
                else:
                    processed_items.append(item)
            self.Items = processed_items


@dataclass
class GetQueryClusterResponse:
    """Response for getting query cluster information."""

    Cluster: QueryClusterInfo
    ResponseMetadata: Optional[Dict[str, Any]] = None

    def __init__(self, **kwargs):
        """Handle API response with Result field containing cluster data."""
        # Handle ResponseMetadata
        if 'ResponseMetadata' in kwargs:
            self.ResponseMetadata = kwargs['ResponseMetadata']
        else:
            self.ResponseMetadata = None
            
        # Handle cluster data from Result field
        if 'Result' in kwargs:
            cluster_data = kwargs['Result'].copy()
            
            # Handle field name variations
            if 'Id' in cluster_data and 'ID' not in cluster_data:
                cluster_data['ID'] = cluster_data.pop('Id')
            if 'id' in cluster_data and 'ID' not in cluster_data:
                cluster_data['ID'] = cluster_data.pop('id')
                
            self.Cluster = QueryClusterInfo(**cluster_data)
        else:
            self.Cluster = QueryClusterInfo(**{})

    def __post_init__(self):
        """Convert dictionary to QueryClusterInfo object if needed (backward compatibility)."""
        if isinstance(self.Cluster, dict):
            cluster = self.Cluster.copy()
            
            # Handle nested QueryClusterBasicInfo structure if exists
            if 'QueryClusterBasicInfo' in cluster:
                cluster.update(cluster.pop('QueryClusterBasicInfo'))
            
            if 'Id' in cluster and not 'ID' in cluster:
                cluster['ID'] = cluster.pop('Id')
            if 'id' in cluster and not 'ID' in cluster:
                cluster['ID'] = cluster.pop('id')
                
            self.Cluster = QueryClusterInfo(**cluster)


@dataclass
class PreaggRuleInfo:
    """Preaggregation rule information."""

    ID: int
    MetricName: str
    Tags: str
    WorkspaceName: str
    AggType: str
    DropOrigin: bool
    Owner: str
    EnableTimestamp: int
    Field: Optional[str] = None

    def __init__(self, **kwargs):
        """Handle field name variations from API responses."""
        # Handle field name variations
        if 'Id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('Id')
        if 'id' in kwargs and 'ID' not in kwargs:
            kwargs['ID'] = kwargs.pop('id')
        
        # Set all fields directly on self (not a new object)
        fields = ['ID', 'MetricName', 'Tags', 'WorkspaceName', 'AggType', 'DropOrigin', 
                 'Owner', 'EnableTimestamp', 'Field']
        
        for field in fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                if field == 'Field':
                    setattr(self, field, None)
                elif field == 'DropOrigin':
                    setattr(self, field, False)
                elif field == 'EnableTimestamp':
                    setattr(self, field, 0)
                else:
                    setattr(self, field, '')


@dataclass
class ListPreaggResponse:
    """Response for listing preaggregation rules."""

    Items: List[PreaggRuleInfo]
    TotalId: int
    ResponseMetadata: Optional[Dict[str, Any]] = None

    def __init__(self, **kwargs):
        """Handle API response with PreaggList and Total fields."""
        if 'PreaggList' in kwargs:
            items = kwargs['PreaggList']
            processed_items = []
            for item in items:
                if isinstance(item, dict):
                    item = item.copy()
                    if 'Id' in item and not 'ID' in item:
                        item['ID'] = item.pop('Id')
                    if 'id' in item and not 'ID' in item:
                        item['ID'] = item.pop('id')
                    processed_items.append(PreaggRuleInfo(**item))
                else:
                    processed_items.append(item)
            self.Items = processed_items
        else:
            self.Items = []
            
        if 'Total' in kwargs:
            self.TotalId = kwargs['Total']
        else:
            self.TotalId = 0
            
        if 'ResponseMetadata' in kwargs:
            self.ResponseMetadata = kwargs['ResponseMetadata']
        else:
            self.ResponseMetadata = None

    def __post_init__(self):
        """Convert dictionary items to PreaggRuleInfo objects if needed (fallback)."""
        if self.Items:
            processed_items = []
            for item in self.Items:
                if isinstance(item, dict):
                    item = item.copy()
                    if 'Id' in item and not 'ID' in item:
                        item['ID'] = item.pop('Id')
                    if 'id' in item and not 'ID' in item:
                        item['ID'] = item.pop('id')
                    processed_items.append(PreaggRuleInfo(**item))
                else:
                    processed_items.append(item)
            self.Items = processed_items


@dataclass
class InfluxQueryResponse:
    """Response for InfluxDB query."""

    Result: List[Dict[str, Any]]
    ResponseMetadata: Optional[Dict[str, Any]] = None


@dataclass
class MetricsQueryResponse:
    """Response for querying metrics data."""

    Result: List[Dict[str, Any]]
    ResponseMetadata: Optional[Dict[str, Any]] = None
