> [!WARNING]
> **PLEASE NOTE:** We stopped further development on this client. You may still use it, but it will only receive bug fixes. Starting Q4/2024 we decided to focus all efforts on developing [ts-scan](https://github.com/trustsource/ts-scan), which also covers all capabilities of this solution. 

# TrustSource Python Client
[TrustSource](https://app.trustsource.io) - a platform to manage open source compliance - uses a two layered approach to scan and transfer dependencies from a package manager to TrustSource. The package manager specific impelmentation, e.g. PIP plugin, and an unspecific client handling data preparation, transfer and security.

This is the Python client. There is also a [Java Client](https://github.com/trustsource/ts-java-client) available.

# How to use
You actually should not require to use the client by itself. However, you may want to use it as the base for a new implementation. Currently the client is used by the following plugins:
  * [PIP](https://github.com/trustsource/ts-pip-plugin)
  * [SwiftPM](https://github.com/trustsource/ts-spm-plugin)

# Questions & Support
Please see our [support offering](https://www.trustsource.io/support) or checkout the [knowledgebase](https://support.trustsource.io) for more information.
