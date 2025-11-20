from enum import Enum

Service = "flink"
Version20210601 = "2021-06-01"
Version20220601 = "2022-06-01"
Host = "open.volcengineapi.com"
ContentType = "application/json"


class JobTypeEnum(str, Enum):
    FLINK_STREAMING_SQL = "FLINK_STREAMING_SQL"
    FLINK_BATCH_SQL = "FLINK_BATCH_SQL"
    FLINK_JOB_TYPE_ALL = "ALL"

    @classmethod
    def from_str(cls, value: str) -> "JobTypeEnum":
        """Convert a string to JobTypeEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported JobTypeEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class EngineVersionEnum(str, Enum):
    FLINK_VERSION_1_11 = "FLINK_VERSION_1_11"
    FLINK_VERSION_1_16 = "FLINK_VERSION_1_16"
    FLINK_VERSION_1_17 = "FLINK_VERSION_1_17"

    @classmethod
    def from_str(cls, value: str) -> "EngineVersionEnum":
        """Convert a string to EngineVersionEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported EngineVersionEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class PriorityEnum(str, Enum):
    LEVEL_1 = "1"  # 最高优先级
    LEVEL_2 = "2"
    LEVEL_3 = "3"
    LEVEL_4 = "4"
    LEVEL_5 = "5"  # 最低优先级

    @classmethod
    def from_str(cls, value: str) -> "PriorityEnum":
        """Convert a string to PriorityEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported PriorityEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class SchedulePolicyEnum(str, Enum):
    DRF = "DRF"
    GANG = "GANG"

    @classmethod
    def from_str(cls, value: str) -> "SchedulePolicyEnum":
        """Convert a string to SchedulePolicyEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported SchedulePolicyEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class StartTypeEnum(str, Enum):
    """Enum for GWS job start types"""
    FROM_NEW = "FROM_NEW"  # Start a new job (default)
    FROM_LATEST = "FROM_LATEST"  # Start from the latest state

    @classmethod
    def from_str(cls, value: str) -> "StartTypeEnum":
        """
        Safely convert a string to StartTypeEnum, case-insensitive.
        """
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported StartTypeEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class ComponentEnum(str, Enum):
    """Component type enumeration."""
    JOBMANAGER = "jobmanager"
    TASKMANAGER = "taskmanager"
    CLIENT = "client"

    @classmethod
    def from_str(cls, value: str) -> "ComponentEnum":
        """Convert a string to ComponentEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().lower()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported ComponentEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class LogLevelEnum(str, Enum):
    """Log level enumeration."""
    ALL = "ALL"
    FATAL = "FATAL"
    INFO = "INFO"
    WARN = "WARN"
    DEBUG = "DEBUG"
    ERROR = "ERROR"

    @classmethod
    def from_str(cls, value: str) -> "LogLevelEnum":
        """Convert a string to LogLevelEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported LogLevelEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value


class JobStateEnum(str, Enum):
    """Job State enumeration."""
    ALL = "ALL"
    CREATED = "CREATED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    SUCCEEDED = "SUCCEEDED"
    STOPPED = "STOPPED"

    @classmethod
    def from_str(cls, value: str) -> "JobStateEnum":
        """Convert a string to JobStateEnum (case-insensitive & safe)."""
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        normalized = value.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        raise ValueError(f"Unsupported JobStateEnum value: {value}")

    def __str__(self) -> str:
        """Return string representation of enum value."""
        return self.value
