"""Build only Media Gateway and publish its owned runtime."""
from pathlib import Path
import hashlib
import subprocess
import sys
from typing import Literal

from f8pysdk.application_package import read_application
from f8pysdk.extension_packaging import build_extension


def main() -> None:
    root = Path(__file__).resolve().parent
    manifest = read_application(root)
    wheels = root / 'build/wheels'
    wheels.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, '-m', 'pip', 'wheel', '--no-deps', '--no-build-isolation',
                    '-w', str(wheels), str(root)], check=True)
    candidates = list(wheels.glob(f'f8media_gateway-{manifest.version}-*.whl'))
    if len(candidates) != 1:
        raise ValueError('Expected one Media Gateway wheel for this version')
    platform: Literal['linux-x86_64', 'windows-x86_64'] = 'windows-x86_64' if sys.platform == 'win32' else 'linux-x86_64'
    output = build_extension(root, root / f'dist/media-gateway-{manifest.version}-{platform}.zip', wheel=candidates[0])
    output.with_suffix('.zip.sha256').write_text(hashlib.sha256(output.read_bytes()).hexdigest() + '  ' + output.name + '\n')
    print(output)


if __name__ == '__main__':
    main()
