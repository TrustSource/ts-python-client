[![Gitter](https://badges.gitter.im/TrustSource/community.svg)](https://gitter.im/TrustSource/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# TrustSource Python Client
[TrustSource](https://app.trustsource.io) - a platform to manage open source compliance - uses a two layered approach to scan and transfer dependencies from a package manager to TrustSource. The package manager specific impelmentation, e.g. PIP plugin, and an unspecific client handling data preparation, transfer and security.

This is the Python client. There is also a [Java Client](https://github.com/trustsource/ts-java-client) available.

# How to use
You actually should not require to use the client by itself. However, you may want to use it as the base for a new implementation. Currently the client is used by the following plugins:
  * [PIP](https://github.com/trustsource/ts-pip-plugin)
  * [SwiftPM](https://github.com/trustsource/ts-spm-plugin)

# Questions & Support
Please see our [support offering](https://www.trustsource.io/support) or checkout the [knowledgebase](https://support.trustsource.io) for more information.
