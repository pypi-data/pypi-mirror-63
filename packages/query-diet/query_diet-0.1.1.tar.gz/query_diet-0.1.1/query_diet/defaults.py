import platform
from contextvars import ContextVar

from django.conf import settings

# config

is_strict_relations_enabled = getattr(settings, "QUERY_DIET_STRICT_RELATIONS", True)
is_strict_columns_enabled = getattr(settings, "QUERY_DIET_STRICT_COLUMNS", True)
query_prefix = getattr(settings, "QUERY_DIET_MACHINE_PREFIX", platform.node())

# assertions
usage_threshold = getattr(settings, "QUERY_DIET_USAGE_THRESHOLD", 0)
n1_threshold = getattr(settings, "QUERY_DIET_N1_THRESHOLD", 0)
