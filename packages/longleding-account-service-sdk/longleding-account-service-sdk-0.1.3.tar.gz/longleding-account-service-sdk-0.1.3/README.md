Longleding Account Settings Service SDK

# Supported Python Versions

Python >= 3.6

# Installation

longleding-account-service-sdk is available for Linux, macOS, and Windows.

```shell script
$ pip install longleding-account-service-sdk
```

# Basic Usage

```python
# -*- coding: utf-8 -*-
from sdk import account_service

account_service_endpoint = "localhost:80"
source_name = "demo"

account_service.init_service(endpoint=account_service_endpoint, src=source_name)

if __name__ == '__main__':
    account_service.get_user_list([1, 3, 5])
    account_service.get_user_page_list(1, 10)
```

# Troubleshoot

If you encounter error messages similar to the following:

```shell script
...
TypeError: Couldn't build proto file into descriptor pool!
Invalid proto descriptor for file "common.proto":
  common.proto: A file with this name is already in the pool.
```

Setting an environment variable the following before running:

```shell script
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python'
```

See also
- [[Python] A file with this name is already in the pool.](#https://github.com/protocolbuffers/protobuf/issues/3002)
- [Python Generated Code](#https://developers.google.com/protocol-buffers/docs/reference/python-generated)