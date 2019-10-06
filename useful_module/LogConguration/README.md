## Usage

```python
from LogConguration import LogConfigurator
import logging

LogConfigurator.initialize_logger()

logger = logging.getLogger(__name__)


logger.info("LOG")
logger.error("LOG")
```


### All error level log save in log/error/error.log
### All info level log save in log/common/common.log