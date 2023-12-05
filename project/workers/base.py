from abc import ABC, abstractmethod
from typing import Union, OrderedDict
from rest_framework.serializers import Serializer
from typing import Type


class AbstractBaseWorker(ABC):
    parent: Union[str, None] = None
    name: str = None
    serializer: Serializer = None

    @abstractmethod
    def handle(self, **kwargs):
        result = self.run(**kwargs)
        return self.format(**{**kwargs, **result})

    @abstractmethod
    def run(self, **kwargs):
        pass

    @abstractmethod
    def format(self, **kwargs):
        pass

    @abstractmethod
    def validate(self, **kwargs):
        pass


class BaseWorker(AbstractBaseWorker):
    parent = None
    name = None
    serializer: Type[Serializer] = None
    serialized_data: OrderedDict = {}

    def handle(self, **kwargs):
        validation_errors = self.validate(**kwargs)
        if validation_errors:
            return validation_errors, False
        try:
            result = self.run()
            return self.format(**result), True
        except Exception as ex:
            return f"{ex=}", False

    def run(self):
        return self.serialized_data

    def format(self, **kwargs):
        return kwargs

    def validate(self, **kwargs):
        serializer = self.serializer(data=kwargs)
        if serializer.is_valid():
            self.serialized_data = serializer.validated_data
            return
        return serializer.errors()
