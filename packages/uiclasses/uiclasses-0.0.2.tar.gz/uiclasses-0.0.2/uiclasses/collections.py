import itertools
from .base import Model, UserFriendlyObject
from .base import COLLECTION_TYPES
from typing import List, Set
from typing import Callable
from ordered_set import OrderedSet
from humanfriendly.tables import format_robust_table, format_pretty_table

ITERABLES = (list, tuple, itertools.chain, set, map, filter)


class IterableCollection(UserFriendlyObject):
    """Base mixin for ModelList and ModelSet, provides methods to
    manipulate iterable collections in ways take advantage of the
    behavior of models.


    For example it supports filtering by instance attributes through a cal to the
    :py:meth:`~uiclasses.base.Model.attribute_matches` method of each children.

    **Features:**

    - :py:meth:`~uiclasses.collections.IterableCollection.sorted_by` - sort by a single attribute
    - :py:meth:`~uiclasses.collections.IterableCollection.filter_by` - to filter by a single attribute
    - :py:meth:`~uiclasses.collections.IterableCollection.sorted` - alias to ``MyModel.List(sorted(my_model_collection))`` or ``.Set()``
    - :py:meth:`~uiclasses.collections.IterableCollection.filter` - alias to ``MyModel.List(filter(callback, my_model_collection))``
    - :py:meth:`~uiclasses.collections.IterableCollection.format_robust_table`
    - :py:meth:`~uiclasses.collections.IterableCollection.format_pretty_table`
    """

    __visible_attributes__ = ["model_class"]

    def __repr__(self):
        return f"<{self.__ui_name__()} {list(self)}>"

    def __str__(self):
        return f"{self.__ui_name__()}[length={len(self)}]"

    def sorted(self, **kw):
        """returns a new ``ModelList`` with this collections' children sorted.

        Example:

        .. code::

           x = ModelList([MyModel({"id": 2}), MyModel({"id": 3})])
           result = x.sorted(key=lambda model: model.id)

        """

        items = sorted(self, **kw)
        return self.__class__(items)

    def sorted_by(self, attribute: str, **kw):
        """sort by a single attribute of the model children.

        Example:

        .. code::

           x = ModelList([MyModel({"id": 2}), MyModel({"id": 3})])
           result = x.sort_by('id')

        """
        return self.sorted(
            key=lambda model: getattr(model, attribute, model.get(attribute)) or "",
            **kw,
        )

    def filter_by(self, attribute_name: str, fnmatch_pattern: str) -> List[Model]:
        """filter by a single attribute of the model children.

        Example:

        .. code::

           x = ModelList([MyModel({"name": 'chucknorris'}), MyModel({"name": 'foobar'})])
           result = x.filter_by('name', '*norris*')

        """
        return self.filter(
            lambda model: model.attribute_matches(attribute_name, fnmatch_pattern)
        )

    def filter(self, check: Callable[[Model], bool]) -> List[Model]:
        """returns a new ``ModelList`` with this collections' children filter.

        Example:

        .. code::

           x = ModelList([MyModel({"id": 2}), MyModel({"id": 3})])
           result = x.filter(key=lambda model: model.id)
        """
        results = filter(check, self)
        return self.__class__(results)

    def get_table_columns(self, columns: List[str] = None):
        """proxy to :py:meth:`~uiclasses.base.Model.get_table_columns`
        """
        available_columns = self.__of_model__.__visible_attributes__
        if not isinstance(columns, list):
            return available_columns

        return self.validate_columns(columns)

    def get_table_rows(self, columns: List[str] = None):
        """returns a list of values from the __ui_attributes__ of each child of this collection.

        Used by
        :py:meth:`~uiclasses.collections.IterableCollection.format_robust_table`
        and
        :py:meth:`~uiclasses.collections.IterableCollection.format_pretty_table`.

        """
        columns = self.get_table_columns(columns)
        return [
            [model.__ui_attributes__().get(key) for key in columns] for model in self
        ]

    def get_table_columns_and_rows(self, columns: List[str] = None):
        """returns a 2-item tuple with columns names and row values of each
        child of this collection.

        Used by
        :py:meth:`~uiclasses.collections.IterableCollection.format_robust_table`
        and
        :py:meth:`~uiclasses.collections.IterableCollection.format_pretty_table`.

        """
        columns = self.get_table_columns(columns)
        rows = self.get_table_rows(columns)
        return columns, rows

    def format_robust_table(self, columns: List[str] = None):
        """returns a string with a robust table ready to be printed on a terminal.

        powered by :py:func:`humanfriendly.tables.format_robust_table`
        """
        columns, rows = self.get_table_columns_and_rows(columns)
        return format_robust_table(rows, columns)

    def format_pretty_table(self, columns: List[str] = None):
        """returns a string with a pretty table ready to be printed on a terminal.

        powered by :py:func:`humanfriendly.tables.format_pretty_table`
        """
        columns, rows = self.get_table_columns_and_rows(columns)
        return format_pretty_table(rows, columns)

    def validate_columns(self, columns):

        mismatched_columns = set(columns).difference(
            self.__of_model__.__visible_attributes__
        )
        if mismatched_columns:
            raise ValueError(
                f"the following columns are not available "
                f"for {self.__of_model__}: {mismatched_columns}"
            )

        return columns

    def to_dict(self) -> List[dict]:
        """calls ``.to_dict()`` in each children of this collection."""
        return [m.to_dict() for m in self]


class ModelList(list, IterableCollection):
    """Implementation of :py:class:`~uiclasses.collections.IterableCollection` for the
    :py:class:`list` type.

    """

    def __init__(self, children: List[Model]):
        model_class = self.__of_model__

        if not isinstance(children, ITERABLES):
            raise TypeError(
                f"{self.__class__.__name__} requires the 'children' attribute to be "
                f"a valid iterable, got {children!r} {type(children)} instead"
            )
        items = []
        for index, child in enumerate(children):
            if isinstance(child, dict):
                child = self.__of_model__(child)
            if not isinstance(child, model_class):
                raise TypeError(
                    f"cannot create {self.__class__.__name__} because value at index [{index}] is not a {model_class}: {child!r} {type(child)}"
                )
            items.append(child)

        super().__init__(map(model_class, items))

    def unique(self) -> "ModelSet":
        """returns a :py:class:`~uiclasses.collections.ModelSet` of all unique items in this :py:class:`~uiclasses.collections.ModelList`"""
        return self.__of_model__.Set(self)


class ModelSet(OrderedSet, IterableCollection):
    """Implementation of :py:class:`~uiclasses.collections.IterableCollection` for the
    `OrderedSet <https://pypi.org/project/ordered-set/>`_ type.
    """

    def __init__(self, children: List[Model]):
        model_class = getattr(self, "__of_model__", None)

        if not isinstance(children, ITERABLES):
            raise TypeError(
                f"{self.__class__.__name__} requires the 'children' attribute to be "
                f"a valid iterable, got {children!r} {type(children)} instead"
            )
        items = []
        for index, child in enumerate(children):
            if isinstance(child, dict):
                child = self.__of_model__(child)

            if not isinstance(child, model_class):
                raise TypeError(
                    f"cannot create {self.__class__.__name__} because value at index [{index}] is not a {model_class}: {child!r} {type(child)}"
                )
            items.append(child)

        super().__init__(map(model_class, items))


COLLECTION_TYPES[list] = ModelList
COLLECTION_TYPES[set] = ModelSet
COLLECTION_TYPES[OrderedSet] = ModelSet
