# Craft Blueprints for ownCloud

<!-- OSPO-managed README | Generated: 2026-04-16 | v2 -->

[![License](https://img.shields.io/badge/License-See%20Repository-blue.svg)](LICENSE) [![ownCloud OSPO](https://img.shields.io/badge/OSPO-ownCloud-blue)](https://kiteworks.com/opensource)

This repository provides [KDE Craft](https://community.kde.org/Craft) blueprints for building the ownCloud Desktop Client and its dependencies. KDE Craft is a meta build system that automates downloading, configuring, building, and installing software packages. These blueprints define the build recipes for ownCloud components within the Craft framework.

## Part of Infrastructure / Tooling

This repository supports the build infrastructure for the [ownCloud Desktop Client](https://github.com/owncloud/client). Craft blueprints are used to manage the complex dependency chain required to build the desktop sync client across Windows, macOS, and Linux.

## Getting Started

1. Set up [KDE Craft](https://community.kde.org/Craft)
2. Add this blueprint repository:
   ```bash
   craft --add-blueprint-repository https://github.com/owncloud/craft-blueprints-owncloud.git
   ```
3. Build the ownCloud client:
   ```bash
   craft owncloud-client
   ```

## Documentation

- [KDE Craft documentation](https://community.kde.org/Craft)
- [ownCloud Desktop Client](https://github.com/owncloud/client)

## Community & Support

**[Star](https://github.com/owncloud/craft-blueprints-owncloud)** this repo and **Watch** for release notifications!

- [ownCloud Website](https://owncloud.com)
- [Community Discussions](https://github.com/orgs/owncloud/discussions)
- [Matrix Chat](https://app.element.io/#/room/#owncloud:matrix.org)
- [Documentation](https://doc.owncloud.com)
- [Enterprise Support](https://owncloud.com/contact-us/)
- [OSPO Home](https://kiteworks.com/opensource)

## Contributing

We welcome contributions! Please read the [Contributing Guidelines](CONTRIBUTING.md)
and our [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

### Workflow

- **Rebase Early, Rebase Often!** We use a rebase workflow. Always rebase on the target branch before submitting a PR.
- **Dependabot**: Automated dependency updates are managed via Dependabot. Review and merge dependency PRs promptly.
- **Signed Commits**: All commits **must** be PGP/GPG signed. See [GitHub's signing guide](https://docs.github.com/en/authentication/managing-commit-signature-verification).
- **DCO Sign-off**: Every commit must carry a `Signed-off-by` line:
  ```
  git commit -s -S -m "your commit message"
  ```
- **GitHub Actions Policy**: Workflows may only use actions that are (a) owned by `owncloud`, (b) created by GitHub (`actions/*`), or (c) verified in the GitHub Marketplace.

## Security

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities at **<https://security.owncloud.com>** -- see [SECURITY.md](SECURITY.md).

Bug bounty: [YesWeHack ownCloud Program](https://yeswehack.com/programs/owncloud-bug-bounty-program)

## License

See [LICENSE](LICENSE) for license details.

## About the ownCloud OSPO

The [Kiteworks Open Source Program Office](https://kiteworks.com/opensource), operating under
the [ownCloud](https://owncloud.com) brand, launched on May 5, 2026, to steward the open source
ecosystem around ownCloud's products. The OSPO ensures transparent governance, license compliance,
community health, and sustainable collaboration between the open source community and
[Kiteworks](https://www.kiteworks.com), which acquired ownCloud in 2023.

- **OSPO Home**: <https://kiteworks.com/opensource>
- **GitHub**: <https://github.com/owncloud>
- **ownCloud**: <https://owncloud.com>

For questions about the OSPO or licensing, contact ospo@kiteworks.com.

### License Migration to Apache 2.0

The OSPO is driving a strategic relicensing of ownCloud repositories toward the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), following
the [Apache Software Foundation's third-party license policy](https://www.apache.org/legal/resolved.html).

Individual repositories will migrate as their audit is completed. The LICENSE file
in each repo reflects its **current** license status (not the target).

**Current license: Not detected.** The OSPO will determine the current license status of this
repository before planning any migration steps. If you know the intended license, please open an
issue or contact ospo@kiteworks.com.
