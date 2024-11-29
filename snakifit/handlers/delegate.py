import abc


class Delegate(abc.ABC):
    
    @abc.abstractmethod
    def invoke(self, *args, **kwargs):
        pass
    
    
    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)