# Development and publication

Prepare `.sdk` as a checkout of `feel8-fun/f8sdk` at a reviewed component-capable
commit. Inside the distribution checkout, run:

```sh
pixi run -e build-check python scripts/component_workspace.py prepare
```

Build dependencies live in `.ci/pixi.toml` and `.ci/pixi.lock`. Runtime dependencies
live in the repository's root workspace and lock. Environment names are local;
no Studio rule limits their names or number.

Publish independently:

```sh
pixi run --locked --manifest-path .ci/pixi.toml publish
```

The publisher builds this implementation's wheel, converts declared local library
inputs to wheels, locks the portable runtime and writes a ZIP plus SHA-256 in
`dist/`. No other application implementation is compiled. Configure the publisher
workflow with reviewed dependency commits; it uploads artifacts, not a remote release.

The `f8media_protocol/` directory publishes the client/contracts library separately
from the gateway implementation. Consumers may carry a compatible library version
in their own interpreter. The managed component uses an independently selected
endpoint and validates its actual media protocol during readiness checks.
