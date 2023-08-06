from inspect import stack

class Utilities(object):

    #region Static Methods
    
    @staticmethod
    def get_function_caller_name():
        
        callerName = stack()[1][3]

        return callerName
    
    #endregion
