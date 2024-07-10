def computed_property(*dep_attrs):
    class ComputedPropertyClass:
        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc
            self._name = ""
            self._dep_attrs = {dep_attr: (None, False) for dep_attr in dep_attrs}
            self._cached_val = None

        def __set_name__(self, owner, name):
            self._name = name

        def _verify_recompute_need_and_update_store_attrs_values(self, obj):
            recompute = False
            for dep_attr_name, (stored_val, is_setted) in self._dep_attrs.items():
                try:
                    curr_val = getattr(obj, dep_attr_name)
                except AttributeError:
                    if is_setted:
                        self._dep_attrs[dep_attr_name] = (None, False)
                        recompute = True

                if (curr_val != stored_val and is_setted) or not is_setted:
                    self._dep_attrs[dep_attr_name] = (curr_val, True)
                    recompute = True

            return recompute

        def __get__(self, obj, owner=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError(
                    f"property {self._name!r} of {type(obj).__name__!r} object has no getter"
                )

            if not self._verify_recompute_need_and_update_store_attrs_values(obj=obj):
                return self._cached_val

            new_val = self.fget(obj)
            self._cached_val = new_val
            return new_val

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError(
                    f"property {self._name!r} of {type(obj).__name__!r} object has no setter"
                )
            self.fset(obj, value)

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def setter(self, fset):
            prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
            prop._name = self._name
            return prop

        def deleter(self, fdel):
            prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
            prop._name = self._name
            return prop

    return ComputedPropertyClass


if __name__ == "__main__":
    from math import sqrt

    class Vector:
        def __init__(self, x, y, z, color=None):
            self.x, self.y, self.z = x, y, z
            self.color = color

        @computed_property("x", "y", "z")
        def magnitude(self):
            print("computing magnitude")
            return sqrt(self.x**2 + self.y**2 + self.z**2)

    v = Vector(9, 2, 6)
    print(v.magnitude)

    v.color = "red"
    print(v.magnitude)

    v.y = 18
    print(v.magnitude)
