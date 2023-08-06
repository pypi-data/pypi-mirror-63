# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pincode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pincode',
    'version': '1.0.3',
    'description': 'A simple offline pincode validator for India',
    'long_description': '# india-pincode-regex ![Packagist Version](https://img.shields.io/packagist/v/captn3m0/pincode?style=plastic) [![Build Status](https://travis-ci.org/captn3m0/india-pincode-regex.svg?branch=master)](https://travis-ci.org/captn3m0/india-pincode-regex) ![npm](https://img.shields.io/npm/v/pincode-validator?style=plastic) ![GitHub package.json version](https://img.shields.io/github/package-json/v/captn3m0/india-pincode-regex?style=plastic) ![GitHub](https://img.shields.io/github/license/captn3m0/india-pincode-regex?style=plastic)\n\nValidate a [Postal Index Number][wiki] for India with a few regexes. The regexes are available in `regex.txt`. There is one regex per area code (the first digit of the PIN, which goes from 1-8).\n\n## Source\n\nThe source for the data is the ["All India Pincode Directory"](https://data.gov.in/resources/all-india-pincode-directory) dataset on data.gov.in.\n\n## Usage\n\nThe `regex.txt` file is 32KB in size, so you can easily use it wherever you want, including browsers.\n\n### PHP\n\nThe package is available on [`packagist`](https://packagist.org/packages/captn3m0/pincode).\n\nTo use the PHP package:\n\n```php\nuse PIN\\Validator as P;\nP::validate(\'110011\'); // returns true;\n```\n\n### Node.js\n\nThe package is available on [`npm`](https://www.npmjs.com/package/pincode-validator).\n\nTo use the package:\n\n```js\nconst P = require(\'pincode-validator\');\nP.validate(\'110011\'); // returns true\n````\n\n## Contributing\n\n- See [`HACKING.md`](HACKING.md) for some development details.\n- Pull requests are welcome for adding libraries in other languages (in the same repo).\n\n## License\n\nLicensed under the [MIT License](https://nemo.mit-license.org/). See LICENSE file for details.\n\n[wiki]: https://en.wikipedia.org/wiki/Postal_Index_Number\n',
    'author': 'Nemo',
    'author_email': 'python@captnemo.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/captn3m0/india-pincode-regex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
