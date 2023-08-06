from localstack.utils.aws import aws_models
djnEi=super
djnEX=None
djnEA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  djnEi(LambdaLayer,self).__init__(arn)
  self.cwd=djnEX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,djnEA,env=djnEX):
  djnEi(RDSDatabase,self).__init__(djnEA,env=env)
 def name(self):
  return self.djnEA.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
