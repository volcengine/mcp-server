from pydantic import BaseModel, Field
from typing import Optional

class Dimension(BaseModel):
    Name: str = Field(description="检索指标的KEY, 例如: ResourceID")
    Value: str = Field(description="对应KEY的值, 例如: eip-13fxxxx")


class Instance(BaseModel):
    Dimensions: list[Dimension] = Field(
        description="要查询的指标维度。每个Dimension里只包含一组KV。存在多个Dimension时,Dimension和Dimension之间的逻辑关系是and。"
    )

class GetMetricsDataFilter(BaseModel):
    Value: float = Field(description="运算符右侧的值")
    Operator: str = Field(
        description="检索条件的运算符, 支持: >、 =、 <、 !=、 >=、 <="
    )

class GetMetricsDataRequest(BaseModel):
    StartTime: Optional[int] = Field(
        None, description="查询的时间选段的开始时间,秒级时间戳,例如1632904500"
    )
    EndTime: Optional[int] = Field(
        None,
        description="""查询的时间选段的结束时间,秒级时间戳,例如1632904801。
EndTime > StartTime。
EndTime不能输入未来时间。
EndTime - StartTime <= 86400。""",
    )
    Instances: Optional[list[Instance]] = Field(
        None,
        description="""要查询的监控指标信息。
存在多个instance时,instance和instance之间的逻辑关系是or。
如果不传instance参数,会返回该地域下所有实例的监控数据。""",
    )
    MetricName: str = Field(..., description="要查询的监控指标名称")
    Namespace: str = Field(..., description="要查询的监控指标所属的产品空间")
    SubNamespace: str = Field(..., description="要查询的指标所属的维度")
    Period: Optional[str] = Field(
        "1m",
        description="""查询数据的间隔粒度,支持分钟(m)、时(h)、天(d)和周(w)粒度。
Period取值参考: StartTime与EndTime的差值除以Period的值不超过30, 举例如下:
1. 当StartTime和EndTime的时间差小于等于30分钟, Period取值为 1m。
2. 当StartTime和EndTime的时间差大于30分钟, 小于1小时, Period建议取值为 2m。
3. 当StartTime和EndTime的时间差大于1小时, 小于等于2小时, Period建议取值为 5m。
""",
    )
    GroupBy: Optional[list[str]] = Field(
        None,
        description="""要查询的指标所使用的分组维度。
如果指标的Dimension列未标注可选,说明不存在可选Dimension,默认所有Dimension都是必选,都会作为指标分组维度。
必选的含义是无论是否传递这些Dimension参数,返回的维度都会以这些Dimension进行分组。
例如,缓存数据库Redis版的指标AggregatedTotalQps,Dimension列为ResourceID,Node。
当Dimension参数传递Node,不传递ReourceID。
查询条件:Node=xxx and ResourceID=*
分组维度:Node,ResourceId
当Dimension参数传递Node和ReourceID。
查询条件:Node=xxx and ResouceId=yyy
分组维度:Node,ResourceId
如果指标的Dimension列标注了可选,说明存在可选Dimension,使用时需要额外指定GroupBy参数。""",
    )
    Filter: Optional[GetMetricsDataFilter] = Field(
        None,
        description="""过滤条件，当指定了过滤条件时，仅会返回满足过滤条件的数据。""",
    )