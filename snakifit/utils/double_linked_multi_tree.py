import builtins
import functools
from typing import Callable


class DoubleLinkedMultiTree:
    """
    A class representing a node in a double-linked multi-tree structure.

    Attributes:
    -----------
    parent : DoubleLinkedMultiTree
        The parent node of the current node.
    children : list[DoubleLinkedMultiTree]
        The list of children nodes of the current node.
    value : any
        The value stored in the current node.

    Methods:
    --------
    __init__(parent=None, value=None):
        Initializes a new node with an optional parent and value.
    parent:
        Gets or sets the parent node.
    children:
        Gets the list of children nodes.
    value:
        Gets or sets the value of the node.
    __repr__(level=0):
        Returns a string representation of the tree starting from the current node.
    """
    
    def __init__(self, parent: 'DoubleLinkedMultiTree' = None, value=None):
        """
        Initializes a new node with an optional parent and value.
        
        Parameters:
        -----------
        :param parent: DoubleLinkedMultiTree, optional The parent node of the current node (default is None).
        :param value: any, optional The value stored in the current node (default is None).
        """
        self._parent = parent
        self._children = []
        self._value = value
    
    @property
    def parent(self) -> 'DoubleLinkedMultiTree':
        """
        Gets the parent node of the current node.

        DoubleLinkedMultiTree
            The parent node.
        """
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        """
        Sets the parent node of the current node.

        :param parent: DoubleLinkedMultiTree
            The new parent node.
        """
        self._parent = parent
        if parent:
            parent.children.append(self)
    
    @property
    def children(self) -> list['DoubleLinkedMultiTree']:
        """
        Gets the list of children nodes of the current node.

        :return: list[DoubleLinkedMultiTree]: The list of children nodes.
        
        """
        return self._children
    
    @property
    def value(self):
        """
        Gets the value stored in the current node.

        :return: any The value of the node.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        """
        Sets the value of the current node.

        :param value: any The new value of the node.
        :return: None
        """
        self._value = value
    
    def __repr__(self, level=0) -> str:
        """
        Returns a string representation of the tree starting from the current node.
        
        :param level: int, optional, The current level in the tree (default is 0).
        :return: str The string representation of the tree.
        """
        display_name = self._value.__name__ if self.value is not None else "None"
        ret = "\t" * level + repr(display_name) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
