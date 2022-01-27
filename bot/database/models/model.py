# MIT License

# Copyright(c) 2021 Rafael

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


class Model:
    """
    The base model class.
    """
    def __str__(self) -> str:
        return f'<{self.__class__.__name__} ID: {self.id}>'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ID: {self.id}>'

    def diff_in_dict(self, other) -> dict:
        """
        Returns a dictionary representation of the difference between the
        model and another model.

        Args:
            other (database.models.Model): The model to compare to.

        Returns:
            dict: The model's dictionary representation.

        """
        # check if it has the same id and is of the same class
        if self != other:
            return {}
        other_dict = other.to_dict()
        self_dict = self.to_dict()
        diff_dict = {}
        for key in other_dict.keys():
            if self_dict[key] != other_dict[key]:
                diff_dict[key] = other_dict[key]
        return diff_dict

    def fill(self, params: dict):
        """
        Update the model with the given parameters.

        Args:
            params (dict): The parameters to update the model with.

        """
        for key, value in params.items():
            if key == 'id':
                continue
            setattr(self, key, value)

    def merge(self, other):
        """
        Merge the model with another model.

        Args:
            other (database.models.Model): The model to merge with.

        """
        self.fill(self.diff_in_dict(other))
