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


def get_cogs() -> tuple[str, ...]:
    """
    Get all Cogs from the bot.

    Returns
    -------
    tuple[`str`, ...]
        The tuple with the names of the cogs.
    """
    def _get_python_files(path: str) -> tuple[str, ...]:
        python_files = list[str]()
        for file in listdir(path):
            if file.endswith(".py") and not file.startswith("_"):
                python_files.append(file.removesuffix('.py'))
        return tuple(python_files)

    cogs = ['jishaku']
    cog_folders = ['commands']

    for folder in cog_folders:
        cogs.extend(
            map(
                lambda file: f'{folder}.{file}',
                _get_python_files(f'{abspath("./")}/{folder}')
            )
        )

    return tuple(cogs)
