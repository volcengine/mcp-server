from dataclasses import dataclass


@dataclass
class ResponseError:
    code: str

    @classmethod
    def from_dict(cls, d: dict):
        if "Code" in d:
            return cls(code=d["Code"])


@dataclass
class ResponseMetaData:
    request_id: str
    error: ResponseError

    @classmethod
    def from_dict(cls, d: dict):
        c = cls(
            request_id="",
            error=ResponseError(
                code="",
            ),
        )
        if "RequestId" in d:
            c.request_id = d["RequestId"]
        if "Error" in d:
            c.error = ResponseError.from_dict(d["Error"])
        return c

    @staticmethod
    def get_default_response_metadata():
        return ResponseMetaData(
            request_id="",
            error=ResponseError(
                code="",
            ),
        )


@dataclass
class ApmplusServerListAlertRuleRequest:
    region_id: str
    keyword: str
    page_number: int
    page_size: int

    def to_dict(self):
        return {
            "keyword": self.keyword,
            "page_no": self.page_number,
            "page_size": self.page_size,
        }


@dataclass
class ApmplusServerListNotifyGroupRequest:
    region_id: str
    keyword: str
    page_number: int
    page_size: int

    def to_dict(self):
        return {
            "Keyword": self.keyword,
            "PageNo": self.page_number,
            "PageSize": self.page_size,
        }


@dataclass
class ApmplusServerQueryMetricsRequest:
    region_id: str
    start_time: int
    end_time: int
    query: str

    def to_dict(self):
        return {
            "graph": {
                "graph_type": "time_series",
                "time_series_conf": {
                    "simple_queries": [
                        {
                            "ispromql": True,
                            "Metric": "",
                            "metric_category": "custom_metric",
                            "promql": self.query,
                        },
                    ]
                },
            },
            "start_time": self.start_time,
            "end_time": self.end_time,
            "granularity": 0,
            "granularity_unit": "",
        }
