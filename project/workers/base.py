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
            res = self.format(**result)
            return {
                "type": "instruction",
                "result": res,
                "name": self.name,
                "parent": self.parent
            }, True
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


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls.__name__]


class Manager(Singleton):

    _workers = {}

    def __init__(
            self,
            worker: BaseWorker = BaseWorker
    ):
        for subclass in worker.__subclasses__():
            self.register_worker(subclass)
            self.__init__(subclass)

    def register_worker(self, worker: Type[BaseWorker]):
        if worker.parent.lower() in self._workers:
            if worker.name.lower() in self._workers[worker.parent.lower()]:
                raise Exception(f"Duplicate name: name={worker.name} already use in {worker.__name__}")
        else:
            self._workers[worker.parent.lower()] = {}

        if not (worker.parent and worker.name):
            raise Exception("Empty values in parent or name")

        self._workers[worker.parent.lower()][worker.name.lower()] = worker

    def check_exists(self, parent: str, name: str):
        return bool(self._workers.get(parent.lower(), {}).get(name.lower()))

    def handle(self, parent: str, name: str, **kwargs):
        if self.check_exists(parent.lower(), name.lower()):
            worker = self._workers.get(parent.lower(), {}).get(name.lower())
            return worker().handle(**kwargs)

        raise Exception(f"Not found worker with {parent=} {name=}")