class MultiCastDelegate:
    """
    Represents a multicast delegate that can hold multiple callable objects.
    
    
    """

    def __init__(self):
        """
        Initializes a new instance of the MultiCastDelegate class.
        
        Attributes:
        -----------
        delegates : list[Callable]
            The list of delegates to be called.
        
        Methods:
        -----------
        add(delegate):
            Adds a delegate to the list of delegates.
        remove(delegate):
            Removes a delegate from the list of delegates.
        invoke(*args, **kwargs):
            Invokes all delegates with the given arguments.
        __call__(*args, **kwargs):
            Invokes all delegates with the given arguments. Overrides the () operator.
        __iadd__(delegate):
            Adds a delegate using the += operator.
        __isub__(delegate):
            Removes a delegate using the -= operator.  
        """
        self.delegates = []

    def add(self, delegate):
        """
        Adds a delegate to the list of delegates.
        
        :param delegate: A callable object to be added.
        :raises ValueError: If the delegate is not callable.
        """
        if not callable(delegate):
            raise ValueError(f'{delegate} should be a callable')
        
        self.delegates.append(delegate)

    def remove(self, delegate):
        """
        Removes a delegate from the list of delegates.
        
        :param delegate: The callable object to be removed.
        """
        self.delegates.remove(delegate)
    
    def invoke(self, *args, **kwargs):
        """
        Invokes all delegates with the given arguments.
        
        :param args: Positional arguments to pass to the delegates.
        :param kwargs: Keyword arguments to pass to the delegates.
        """
        self(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Invokes all delegates with the given arguments. Overrides the () operator.
        
        :param args: Positional arguments to pass to the delegates.
        :param kwargs: Keyword arguments to pass to the delegates.
        :return: The result of the last delegate called.
        """
        result = None
        for delegate in self.delegates:
            result = delegate(*args, **kwargs)
        return result

    def __iadd__(self, delegate):
        """
        Adds a delegate using the += operator.
        
        :param delegate: The callable object to be added.
        :return: The instance of MultiCastDelegate.
        """
        self.add(delegate)
        return self

    def __isub__(self, delegate):
        """
        Removes a delegate using the -= operator.
        
        :param delegate: The callable object to be removed.
        :return: The instance of MultiCastDelegate.
        """
        self.remove(delegate)
        return self
    