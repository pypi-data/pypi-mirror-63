import yaml
import logging.config
import logging
from .io import load_yaml 

modules = ['development', 'production']

class Logger(object):
    mode = 'development'
    loggers = []
    info = logging.getLogger(mode).info
    debug = logging.getLogger(mode).debug
    error = logging.getLogger(mode).error
    critical = logging.getLogger(mode).critical

    @staticmethod
    def load_config_from_yaml_file(source_location = None, default_type = None, default_location = None):

        try:
            log_config = load_yaml(source_location)
            logging.config.dictConfig(log_config)
            
            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return Logger.source_option(default_type, default_location)

        
    @staticmethod
    def load_config_from_consulkv(source_location = None, default_type = None, default_location = None):

        from ..hashicorp.consul_config import ConsulCon

        try:
            consul_con = ConsulCon() if consul_con == None else consul_con
            consul_con.exception_dict['path'] = source_location

            config = consul_con.get_kv('yaml')

            logging.config.dictConfig(config)

            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return Logger.source_option(default_type, default_location)
 

    @staticmethod
    def load_config_from_dict(source_location = None, default_type = None, default_location = None, config_dict = {}):
        try:
            log_config = {} 

            if config_dict == {}:
                import importlib

                temp = importlib.import_module(source_location)
                log_config = temp.logging
            else:
                log_config = config_dict

            logging.config.dictConfig(log_config)
            
            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return Logger.source_option(default_type, default_location)


    @staticmethod
    def load_config_from_json_file(source_location = None, default_type = None, default_location = None):

        try:
            import json
            with open(source_location, 'rt') as f:
                log_config = json.loads(f.read())
            logging.config.dictConfig(log_config)

            loggers = [name for name in logging.root.manager.loggerDict]
            return loggers
        except Exception as ex:
            return Logger.source_option(default_type, default_location)


    @staticmethod
    def setup_log(mode = 'development', source_type = None, 
                  source_location = None, consul_con = None, config_dict = None,
                  default_type = 'yaml_file', default_location = 'conf/logging.yaml'):
        Logger.mode = mode
        Logger.loggers = Logger.source_option(source_type, source_location, default_type, default_location)
        if Logger.mode not in Logger.loggers:
            raise Exception('modules for mode '+ Logger.mode +' is not found!!') 
     
    @staticmethod
    def source_option(source_type = None, source_location = None, default_type = None, default_location = None):
        mode_enum = {
            'yaml_file' : lambda x, y, z: Logger.load_config_from_yaml_file(x, y, z),
            'consulkv' : lambda x, y, z: Logger.load_config_from_consulkv(x, y, z),
            'dictionary' : lambda x, y, z: Logger.load_config_from_dict(x, y, z),
            'json_file' : lambda x, y, z: Logger.load_config_from_json_file(x, y, z)
        }

        return mode_enum[source_type](source_location, default_type, default_location)

 
