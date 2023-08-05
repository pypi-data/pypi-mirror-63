"""
Huan(202003):
    Translated from TypeScript to Python
    See: https://github.com/wechaty/wechaty/blob/master/src/accessory.spec.ts
"""
from typing import (
    cast,
    Type,
)
import pytest   # type: ignore

from wechaty import (
    Wechaty,
)
from wechaty_puppet import (
    Puppet,
)
from .accessory import (
    Accessory,
)

EXPECTED_PUPPET1 = cast(Puppet, {'p': 1})
EXPECTED_PUPPET2 = cast(Puppet, {'p': 2})

EXPECTED_WECHATY1 = cast(Wechaty, {'w': 1})
EXPECTED_WECHATY2 = cast(Wechaty, {'w': 1})


def get_user_class() -> Type[Accessory]:
    """create a fixture"""

    class FixtureClass(Accessory):
        """fixture"""

    return FixtureClass


@pytest.fixture(name='user_class')
def fixture_user_class():
    """fixture for fixture class"""
    yield get_user_class()


def test_indenpendent_user_classes():
    """two child class should not be equal"""
    user_class1 = get_user_class()
    user_class2 = get_user_class()

    assert user_class1 != user_class2, 'two child class should not be equal'


def test_user_classes_should_share():
    """doc"""

    user_class = get_user_class()

    user_class.set_wechaty(EXPECTED_WECHATY1)
    user_class.set_puppet(EXPECTED_PUPPET1)

    child1 = user_class()
    child2 = user_class()

    assert child1.wechaty() == EXPECTED_WECHATY1, \
        'child1 should get the wechaty from static value'
    assert child2.wechaty() == EXPECTED_WECHATY1, \
        'child1 should get the wechaty from static value'


def test_indenpendent_user_classes_instances():
    """doc"""

    user_class1 = get_user_class()
    user_class2 = get_user_class()

    user_class1.set_wechaty(EXPECTED_WECHATY1)
    user_class1.set_puppet(EXPECTED_PUPPET1)

    user_class2.set_wechaty(EXPECTED_WECHATY2)
    user_class2.set_puppet(EXPECTED_PUPPET2)

    user_class1_instance = user_class1()
    user_class2_instance = user_class2()

    assert user_class1_instance.wechaty() == EXPECTED_WECHATY1, \
        'class1 instance should get wechaty1'
    assert user_class1_instance.puppet() == EXPECTED_PUPPET1, \
        'class1 instance should get puppet1'

    assert user_class2_instance.wechaty() == EXPECTED_WECHATY2, \
        'class2 instance should get wechaty2'
    assert user_class2_instance.puppet() == EXPECTED_PUPPET2, \
        'class2 instance should get puppet2'


def test_accessory_read_initialized_class(
        user_class: Type[Accessory],
):
    """
    should read excepted value by reading static wechaty & puppet after init
    """

    # reveal_type(accessory_class.wechaty)

    user_class.set_puppet(EXPECTED_PUPPET1)
    user_class.set_wechaty(EXPECTED_WECHATY1)

    accessory_instance = user_class()

    assert \
        accessory_instance.puppet() == EXPECTED_PUPPET1, \
        'should get puppet back by instance from static'
    assert \
        accessory_instance.wechaty() == EXPECTED_WECHATY1, \
        'should get wechaty back by instance from static'


def test_accessory_read_uninitialized_instance(
        user_class: Type[Accessory],
):
    """should throw if read instance wechaty & puppet before initialization"""
    # pytest.skip('tbd')

    instance = user_class()

    with pytest.raises(Exception) as e:
        assert instance.puppet()
    assert str(e.value) == 'puppet not set'

    with pytest.raises(Exception) as e:
        assert instance.wechaty()
    assert str(e.value) == 'wechaty not set'


def test_accessory_read_initialized_instance(
        user_class: Type[Accessory],
):
    """
    should get expected value by reading instance wechaty & puppet after init
    """

    user_class.set_puppet(EXPECTED_PUPPET1)
    user_class.set_wechaty(EXPECTED_WECHATY1)

    # reveal_type(accessory_class)
    accessory_instance = user_class()

    assert \
        accessory_instance.puppet() == EXPECTED_PUPPET1, \
        'should get puppet back'
    assert \
        accessory_instance.wechaty() == EXPECTED_WECHATY1, \
        'should get wechaty back'


def test_accessory_set_twice(
        user_class: Type[Accessory],
):
    """doc"""
    user_class.set_puppet(EXPECTED_PUPPET1)

    with pytest.raises(Exception) as e:
        user_class.set_puppet(EXPECTED_PUPPET1)
    assert str(e.value) == 'can not set twice'

    user_class.set_wechaty(EXPECTED_WECHATY1)
    with pytest.raises(Exception) as e:
        user_class.set_wechaty(EXPECTED_WECHATY1)
    assert str(e.value) == 'can not set twice'
