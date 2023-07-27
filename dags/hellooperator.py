from airflow.models.baseoperator import BaseOperator

#HelloOperator inherits from BaseOperator
class HelloOperator(BaseOperator):
    
    #kwargs: Other attributes
    def __init__(self, name:str, **kwargs):
        super().__init__(**kwargs)
        
        #initialize name variable
        self.name = name

    #execute method
    def execute(self, context):
        print(f"Hola {self.name}")
