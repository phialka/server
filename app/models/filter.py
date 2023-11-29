from abc import ABCMeta, abstractmethod
from typing import Union, Any, Optional
from enum import Enum

from pydantic import BaseModel




class ConditionTranslator():
    __metaclass__ = ABCMeta

    @classmethod
    def eq(cls, left, right, **kwargs):
        """
        Реализует условие "==" 
        """

    @classmethod
    def ne(cls, left, right, **kwargs):
        """
        Реализует условие "!=" 
        """

    @classmethod
    def lt(cls, left, right, **kwargs):
        """
        Реализует условие "<" 
        """

    @classmethod
    def gt(cls, left, right, **kwargs):
        """
        Реализует условие ">" 
        """

    @classmethod
    def le(cls, left, right, **kwargs):
        """
        Реализует условие "<=" 
        """

    @classmethod
    def ge(cls, left, right, **kwargs):
        """
        Реализует условие ">=" 
        """

    @classmethod
    def and_(cls, left, right, **kwargs):
        """
        Реализует условие "&" 
        """

    @classmethod
    def or_(cls, left, right, **kwargs):
        """
        Реализует условие "|" 
        """

    @classmethod
    def build_condition(cls, node: 'ConditionTreeNode', **kwargs):
        """
        Выполняет сборку условия из семантического дерева для дальнейшего использования в запросе.
        """



class JsondbConditionTranslator(ConditionTranslator):

    @classmethod
    def eq(cls, objects: list[dict], left: str, right: str|int):
        """
        Implements the "==" condition for the json database
        """
        ret_objs = []
        for obj in objects:
            if obj[left] == right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def ne(cls, objects: list[dict], left: str, right: str|int):
        ret_objs = []
        for obj in objects:
            if obj[left] != right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def lt(cls, objects: list[dict], left: str, right: int):
        ret_objs = []
        for obj in objects:
            if obj[left] < right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def gt(cls, objects: list[dict], left: str, right: int):
        ret_objs = []
        for obj in objects:
            if obj[left] > right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def le(cls, objects: list[dict], left: str, right: int):
        ret_objs = []
        for obj in objects:
            if obj[left] <= right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def ge(cls, objects: list[dict], left: str, right: int):
        ret_objs = []
        for obj in objects:
            if obj[left] >= right:
                ret_objs.append(obj)
        return ret_objs


    @classmethod
    def and_(cls, objects: list[dict], left: list[dict], right: list[dict]):
        left_ids = {obj['id'] for obj in left}
        right_ids = {obj['id'] for obj in right}
        target_ids =  list(left_ids&right_ids)
        return [obj for obj in objects if obj['id'] in target_ids]


    @classmethod
    def or_(cls, objects: list[dict], left: list[dict], right: list[dict]):
        left_ids = {obj['id'] for obj in left}
        right_ids = {obj['id'] for obj in right}
        target_ids =  list(left_ids|right_ids)
        return [obj for obj in objects if obj['id'] in target_ids]
    

    @classmethod
    def build_condition(cls, node: 'ConditionTreeNode', models: list[dict]):
        if node.left.is_leaf() and node.right.is_leaf():
            return node.content(cls, objects=models, left=node.left.content, right=node.right.content)
        return node.content(cls, objects=models, left=cls.build_condition(node.left, models), right=cls.build_condition(node.right, models))



class PostgreConditionTranslator(ConditionTranslator):

    @classmethod
    def eq(cls, left: Any, right: Any):
        '''
        Implements the "==" condition for the json database
        '''
        return left == right


    @classmethod
    def ne(cls, left: Any, right: Any):
        if type(right) == type(None):
            return left.isnull(False)
        return (left < right)|(left > right)


    @classmethod
    def lt(cls, left: Any, right: Any):
        return left < right


    @classmethod
    def gt(cls, left: Any, right: Any):
        return left > right


    @classmethod
    def le(cls, left: Any, right: Any):
        return left <= right


    @classmethod
    def ge(cls, left: Any, right: Any):
        return left >= right


    @classmethod
    def and_(cls, left: Any, right: Any):
        return left & right


    @classmethod
    def or_(cls, left: Any, right: Any):
        return left | right
    

    @classmethod
    def build_condition(cls, stree: 'ConditionTreeNode', fields_display: dict):
        if stree.left.is_leaf() and stree.right.is_leaf():
            return stree.content(cls, left=fields_display[stree.left.content], right=stree.right.content)
        return stree.content(cls, left=cls.build_condition(stree.left, fields_display), right=cls.build_condition(stree.right, fields_display))



def eq(translator: ConditionTranslator, **kwargs):
    return translator.eq(**kwargs)
    
def ne(translator: ConditionTranslator, **kwargs):
    return translator.ne(**kwargs)

def lt(translator: ConditionTranslator, **kwargs):
    return translator.lt(**kwargs)

def gt(translator: ConditionTranslator, **kwargs):
    return translator.gt(**kwargs)

def le(translator: ConditionTranslator, **kwargs):
    return translator.le(**kwargs)

def ge(translator: ConditionTranslator, **kwargs):
    return translator.ge(**kwargs)

def and_(translator: ConditionTranslator, **kwargs):
    return translator.and_(**kwargs)

def or_(translator: ConditionTranslator, **kwargs):
    return translator.or_(**kwargs)



class ConditionTreeNode():
    """
    Узел семантического дерева условий
    """
    
    def __init__(self, content: Any, left: Optional['ConditionTreeNode'] = None, right: Optional['ConditionTreeNode'] = None) -> None:
        self.content = content
        self.left = left
        self.right = right


    def is_leaf(self):
        return (type(self.left) == type(None)) & (type(self.right) == type(None))
    

    def _typing(self, obj):
        if type(obj) != type(self):
            obj = ConditionTreeNode(obj)
        return obj


    def __eq__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=eq, left = self, right = other)


    def __ne__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=ne, left = self, right = other)


    def __lt__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=lt, left = self, right = other)


    def __gt__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=gt, left = self, right = other)


    def __le__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=le, left = self, right = other)


    def __ge__(self, other: 'ConditionTreeNode'):
        other = self._typing(other)
        return ConditionTreeNode(content=ge, left = self, right = other)
    

    def __and__(self, other: 'ConditionTreeNode'):
        return ConditionTreeNode(content=and_, left = self, right = other)
    

    def __or__(self, other: 'ConditionTreeNode'):
        return ConditionTreeNode(content=or_, left = self, right = other)
    

    def tree_to_dict(self):
        if self.is_leaf():
            return self.content
        else:
            current = {
            'content': self.content,
            'left': self.left.tree_to_dict(),
            'right': self.right.tree_to_dict()
            }
            return current
        

    @classmethod
    def create_accessor(cls, annotations: dict):
        class F():
            """
            Предоставляет доступ к полям модели
            Позволяет составлять условия типа WHERE для обращений к БД
            """
            
        for itm in annotations.items():
            setattr(F, itm[0], ConditionTreeNode(itm[0]))

        return F
        
    
def equal(a, b):
    return ConditionTreeNode(content=eq, left = a, right = b)














