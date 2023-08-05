"""
Python Wechaty - https://github.com/wechaty/python-wechaty

2020-now @copyright Wechaty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import (
    # overload,
    # cast,
    Optional,
)
from wechaty_puppet import Puppet
from .config import (
    logging
)
from .wechaty import Wechaty

log = logging.getLogger('Accessory')


class Accessory:
    """
    Translate the function from TypeScript to Python
    See: https://github.com/wechaty/wechaty/blob/master/src/accessory.ts
    """

    _puppet : Optional[Puppet]  = None
    _wechaty: Optional[Wechaty] = None

    @classmethod
    def set_puppet(cls, new_puppet: Puppet):
        """doc"""
        if cls._puppet is not None:
            raise AttributeError('can not set twice')
        cls._puppet = new_puppet

    @classmethod
    def set_wechaty(cls, new_wechaty: Wechaty):
        """doc"""
        if cls._wechaty is not None:
            raise AttributeError('can not set twice')
        cls._wechaty = new_wechaty

    def puppet(self):
        """doc"""
        if self._puppet is None:
            raise AttributeError('puppet not set')
        return self._puppet

    def wechaty(self):
        """doc"""
        if self._wechaty is None:
            raise AttributeError('wechaty not set')
        return self._wechaty
