# MIT License

# Copyright(c) 2021-2022 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import listdir
from os.path import abspath

import i18n

from configs import Configs


def setup_i18n() -> None:
    translations_path = f'{abspath("./")}/language/json'
    available_locales = list[str]()

    for file in listdir(translations_path):
        if file.endswith(".json") and not file.startswith("_"):
            available_locales.append(file.removesuffix('.json'))

    i18n.load_path.append(translations_path)
    i18n.set('available_locales', available_locales)
    i18n.set('error_on_missing_translation', True)
    i18n.set('fallback', Configs.default_language)
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('skip_locale_root_data', True)
