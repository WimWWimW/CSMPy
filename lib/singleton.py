


class Singleton(type):
    """
    Singleton metaclass. Usage:
    
    > class C(object, metaclass = Singleton):
                     -------------
            ...
            
    Subclasses are NOT pooled with superclass by default.
    To change this, add a __group__ attribute to the superclass
    (see examples below)
    """
    
    instances = {}

    def __call__(cls, *args, **kwargs):  # @NoSelf
        tag = getattr(cls, "__group__", cls)
        
        if tag not in cls.instances:
            cls.instances[tag] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[tag]
    
    
    
    
if __name__ == '__main__':
            
    class Test(metaclass = Singleton):
        __group__ = "testers"
        
    class Test2(Test):
        pass
        
    print(Test2())
    print(Test())
