import sys
import os
sys.path.append(os.path.dirname('.'))


from w3bch3ck.domains import (
    check,
    pooled_check
)
from w3bch3ck.colorizers import (
    warn,
    notice,
    ok
)