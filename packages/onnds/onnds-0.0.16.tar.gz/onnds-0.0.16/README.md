# OzNetNerd Deep Security

Convenience Python module for interacting with Trend Micro Deep Security

## Installation

```
pip3 install onnds
```

## Environment Variables

* `DS_ADDRESS`: Hostname or IP address of the DSM. (Default: `https://app.deepsecurity.trendmicro.com`)
* `DS_KEY`: REST API key. **Required** for methods which use the SDK
* `DS_USERNAME`: **Required** for methods which use the legacy REST API
* `DS_PASSWORD`: **Required** for methods which use the legacy REST API
* `DS_TENANT`: **Required** for methods which use the legacy REST API in a multi-tenant environment

## Examples

Example [code snippets](examples/).

# Contact

* Blog: oznetnerd.com
* Email: will@oznetnerd.com