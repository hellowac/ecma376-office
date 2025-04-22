import functools
import logging
from collections.abc import Callable
from typing import Generic, TypeVar, Union, overload

logger = logging.getLogger(__name__)


# 数据描述符的类型注解参考:
# https://stackoverflow.com/questions/54413434/type-hinting-with-descriptors

Instance = TypeVar('Instance')
Value = TypeVar('Value')
# Attribute = TypeVar("Attribute")


class lazyproperty(Generic[Instance, Value]):
    """类似 @property 的装饰器，但仅在首次访问时执行。

    # 参考自 https://github.com/scanny/python-pptx/blob/master/pptx/util.py#L128

    与 @property 类似，这个装饰器只能用于装饰仅有 `self` 参数的方法，并且像实例上的属性一样访问，即不使用尾随括号。与 @property 不同的是，被装饰的方法仅在首次访问时执行；结果值被缓存，并且在第二次及以后的访问中返回相同的值而不重新执行该方法。

    与 @property 类似，这个类产生一个 *数据描述符* 对象，该对象存储在类的 `__dict__` 中，名称为被装饰方法的名称（名义上为 'fget'）。缓存的值存储在实例的 `__dict__` 中，名称相同。

    由于它是一个数据描述符（而不是 *非数据描述符*），其 `__get__()` 方法在每次访问被装饰的属性时都会执行；相同名称的 `__dict__` 项被描述符“遮蔽”。

    虽然这可能在性能上比 property 有所改善，但它更大的好处在于它的其他特性。一个常见的用法是构造协作者对象，从而将“实际工作”从构造函数中移除，但仍然只执行一次。它还将客户端代码与任何顺序考虑解耦；如果它从多个位置访问，可以确保在需要时随时准备好。

    大致基于：https://stackoverflow.com/a/6849299/1902513。

    lazyproperty 是只读的。没有类似 @property 的可选 “setter”（或 deleter）行为。这对于保持其不可变性和幂等性保证至关重要。尝试给 lazyproperty 赋值会无条件地引发 AttributeError。

    以下方法中的参数名称对应于这个使用示例：

    ```python
    class Obj(object):
        @lazyproperty
        def fget(self):
            return 'some result'


    obj = Obj()
    ```

    不适合包装函数（而不是方法），因为它不可调用。
    """

    def __init__(self, fget: Callable[[Instance], Value]):
        """
        *fget* 是被装饰的方法（一个“getter”函数）。

        lazyproperty 是只读的，所以只有一个 *fget* 函数（一个常规的 @property 还可以有 fset 和 fdel 函数）。这个名称的选择是为了与 Python 的 `property` 类保持一致，因为它使用这个名称作为对应参数的名称。
        """
        # ---maintain a reference to the wrapped getter method
        self._fget = fget
        # ---adopt fget's __name__, __doc__, and other attributes
        functools.update_wrapper(self, fget)  # type: ignore

    @overload
    def __get__(self, instance: None, owner: type[Instance]) -> 'lazyproperty':
        # Called when an attribute is accessed via class not an instance
        ...

    @overload
    def __get__(self, instance: Instance, owner: type[Instance]) -> Value:
        # Called when an attribute is accessed on an instance variable
        ...

    def __get__(self, instance: Instance | None, owner: type[Instance]) -> Union[Value, 'lazyproperty']:
        # Full implementation is declared here
        """在类或实例上每次访问 'fget' 属性时调用。

        *self* 是这个 lazyproperty 描述符的实例，它“包装”了它所装饰的属性方法（名义上为 `fget`）。

        *instance* 是当从对象实例访问属性时的“宿主”对象实例，例如 `obj = Obj(); obj.fget`。当在类上访问时，*obj* 为 None，例如 `Obj.fget`。

        *type* 是在类和实例属性访问中托管被装饰 getter 方法 (`fget`) 的类。
        """
        # ---when accessed on class, e.g. Obj.fget, just return this
        # ---descriptor instance (patched above to look like fget).
        # 当在类上访问时，例如 `Obj.fget`，只返回这个描述符实例（如上所述，将其修补为看起来像 fget）。
        if instance is None:
            return self  # type: ignore

        # ---when accessed on instance, start by checking instance __dict__
        # 当在实例上访问时，首先检查实例的 __dict__。
        value = instance.__dict__.get(self.__name__)  # type: ignore
        if value is None:
            # ---on first access, __dict__ item will absent. Evaluate fget()
            # ---and store that value in the (otherwise unused) host-object
            # ---__dict__ value of same name ('fget' nominally)
            # 在首次访问时，__dict__ 项将不存在。
            # 执行 fget() 并将该值存储在（否则未使用的）宿主对象的 __dict__ 中，名称相同（名义上为 'fget'）。
            value = self._fget(instance)
            instance.__dict__[self.__name__] = value  # type: ignore

        return value

    def __set__(self, obj, value):
        """为了保持只读行为，无条件地引发异常。

        这个装饰器旨在实现不可变（和幂等）的对象属性。因此，必须明确禁止对该属性的赋值。

        如果没有这个 __set__ 方法，这个描述符将变成一个 *非数据描述符*。这看起来不错，因为一旦设置，缓存的值将被直接访问（在实例属性查找中，__dict__ 属性优先于非数据描述符）。问题是，这样就没有任何措施可以阻止对缓存值的赋值，这会覆盖 `fget()` 的结果，从而破坏这个装饰器的不可变性和幂等性保证。

        在一个 2.8GHz 的开发机器上测量时，带有这个 __set__() 方法的性能大约为每次访问 0.4 微秒；因此非常迅速，可能不是优化工作的一个重要目标。
        """
        msg = "can't set attribute"
        raise AttributeError(msg)  # pragma: no cover
