'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from core.parameters import ParametersList, Parameter as P

classname = 'Info'
    
class Info(Module):
    """Collect system informations
    :system.info auto | whoami | hostname | basedir | document_root | client_ip
    """

    
    vectors = VectorList([
        Vector('shell.sh', 'whoami', "whoami"),
        Vector('shell.sh', 'hostname', "hostname"),
        Vector('shell.sh', 'basedir', "pwd"),
        Vector('shell.sh', 'uname', "uname -a"),
        Vector('shell.sh', 'os', "uname"),
        Vector('shell.php', 'document_root', "@print($_SERVER['DOCUMENT_ROOT']);"),
        Vector('shell.php', 'whoami', "@print(get_current_user());"),
        Vector('shell.php', 'hostname', "@print(gethostname());"),
        Vector('shell.php', 'basedir', "@print(getcwd());"),
        Vector('shell.php', 'safe_mode', "(ini_get('safe_mode') && print(1)) || print(0);"),
        Vector('shell.php', 'script', "@print($_SERVER['SCRIPT_NAME']);"),
        Vector('shell.php', 'client_ip', "@print($_SERVER['REMOTE_ADDR']);")
        ])


    
    params = ParametersList('Collect system informations', 
                            vectors,
                P(arg='info', help='', choices = vectors.get_names_list(), default='auto' )
                )

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.infos = {}
        
    def run_module( self, info):
        
        if info in self.infos:
            return self.infos[info]
        
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            
            if vector.name not in self.infos and (info == 'auto' or info == vector.name):
            
                response = self.__execute_payload(vector, [info])
                if response:
                    self.infos[vector.name] = response
                    
                    if info != 'auto':
                        self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                        return response
                    else:                
                        tabs = '\t'*(3-((len(vector.name)+1)/8))
                        self.mprint('%s:%s%s' % (vector.name, tabs, response))

        
        if info != 'auto':
            raise ModuleException("system.info",  "Information '%s' not supported." % (info))



    def __execute_payload(self, vector, parameters):
        return self.modhandler.load(vector.interpreter).run_module(vector.payloads[0])
        



    
    
    