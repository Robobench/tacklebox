import argparse
import inspect
import collections
import parse

class CLICommands(object):        
    class SubCommand(object):
        def __init__(self, subparser, method):
            self.__which = method.__name__.replace('_','-')
            self.__parser = []
            self.__method = method
            self.__add_method_parser(method, subparser)

        def get_name(self):
            return self.__which

        def __call__(self, kwargs):
            self.__method(**kwargs)

        def __add_method_parser(self, method, subparser):
            """Add a method to the parser
        
            Add a method to the parser. Automatically add the relevant params.
        
            :param method: The unbound function method to make into a subcommand
            """
            aspec = inspect.getargspec(method)
            #make a default dict of default values with the default as none
            dd2 = collections.defaultdict()
            dd2.update(zip(reversed(aspec.args),
                           reversed(aspec.defaults)))
            methodhelp= method.__doc__
            possible_param_strings = methodhelp.splitlines()
            helpstr = methodhelp.split('\n')[0].strip().rstrip()
            self.__parser = subparser.add_parser(self.__which, help=helpstr)
            self.__parser.set_defaults(which=self.__which)
            arguments = dict()
            for s in possible_param_strings:
                try:
                    argname, helpstr = parse.parse(":param {}: {}",s.strip()).fixed
                    arguments[argname] = [helpstr]
                except Exception as e:
                    pass
                try:
                    argname, typstr = parse.parse(":type {}: {}",s.strip()).fixed 
                    arguments[argname].append(eval(typstr))
                except Exception as e:
                    pass
                
            for argname, argparams in arguments.iteritems():
                if argparams[1] is type(True):           
                    default=dd2.get(argname,[])
                    yes_help=argparams[0].strip()
                    no_help=""
                    if default:
                        yes_help = "[Default] " + yes_help
                    else:
                        no_help = "[Default] " + no_help
                        
                    self.__parser.add_argument('--%s'%(argname), help=yes_help, action='store_true', dest=argname)
                    self.__parser.add_argument('--no-%s'%(argname), help=no_help, action='store_false', dest=argname)               
                else:
                    self.__parser.add_argument('--%s'%(argname), help=argparams[0].strip(), default=dd2.get(argname,[]), type=argparams[1])


    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.main_description,
                                              usage=self.main_usage,
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # Keeping the metavar a long string produces prettier line breaks.
        self.subparser = self.parser.add_subparsers(title=None, description=self.sub_description,help=self.sub_help, metavar='Commands:          ')
        methods_list = [self.SubCommand(self.subparser, method[1]) for method in self.__get_command_methods()]
        self.subcommands = {meth.get_name():meth for meth in methods_list}

    def __get_command_methods(self):
        return inspect.getmembers(self, predicate=lambda(x):inspect.ismethod(x) and not x.__name__.startswith('_'))


    def _parse(self, arglist):
        if not arglist:
            self.parser.print_help()
            return
        result = self.parser.parse_args(arglist)
        result_dict = dict(result._get_kwargs())
        which = result_dict.pop('which')
        self.subcommands[which](result_dict)
