"""Module logic that provides a class for compiling and executing a user-defined module.

This module provides the ModuleMetadata class and the ModuleCompiler class. 
The ModuleMetadata class contains metadata information about the user-defined module.
The ModuleCompiler class compiles the user-defined module and creates a pipeline for execution.

Classes:
    ModuleMetadata: Class containing metadata information about the user-defined module.

    Methods:
        print_metadata: Method that prints the metadata information about the user-defined module.
        print_licence: Method that prints the licence information about the user-defined module.

    ModuleCompiler: Class that compiles a user-defined module and creates a pipeline for execution.

    Attributes:
        module_name (str): Name of the module to be imported.
        __user_module_main_file (module): Imported module containing user-defined functions.
        __fn_list (list): List of function names extracted from the user-defined module.
        __pipe (list): List of function names in order to be executed as a pipeline.
        module_metadata (ModuleMetadata): Instance of the ModuleMetadata class.

    Methods:
        __get_function_list: Private method that imports the user-defined module and extracts its functions.
        __make_pipeline: Private method that creates a pipeline based on the functions extracted from the module.
        __execute_function: Private method that executes a given function from the user-defined module.
        __metadata_extractor: Private method that extracts the metadata information from the user-defined module.
        execute_pipeline: Public method that executes the pipeline in order.
"""

from importlib import import_module
import gc
import os

class ModuleMetadata():
    """
    Class containing metadata information about the user-defined module.

    Attributes:
        module_name (str): Name of the module.
        module_description (str): Description of the module.
        module_version (str): Version of the module.
        module_author (str): Author of the module.
        module_licence (str): Licence information of the module.

    Methods:
        print_metadata: Method that prints the metadata information about the user-defined module.
        print_licence: Method that prints the licence information about the user-defined module.
    """
    
    def __init__(self):
        """Initializes a new instance of the ModuleMetadata class."""
        self.module_name = ""
        self.module_description = ""
        self.module_version = ""
        self.module_author = ""
        self.module_licence = ""

    def print_metadata(self):
        """Method that prints the metadata information about the user-defined module."""
        print(f"{self.module_name}")
        print(f"\n{self.module_description}")
        print(f"\nVersion:{self.module_version}")
        print(f"Author: {self.module_author}")
    
    def print_licence(self):
        """Method that prints the licence information about the user-defined module."""
        print(f"{self.module_licence}")

class ModuleCompiler():
    """
    Class that compiles a user-defined module and creates a pipeline for execution.
    
    Args:
        module_name (str): Name of the module to be imported.
        
    Attributes:
        module_name (str): Name of the module to be imported.
        __user_module_main_file (module): Imported module containing user-defined functions.
        __fn_list (list): List of function names extracted from the user-defined module.
        __pipe (list): List of function names in order to be executed as a pipeline.
        
    Methods:
        __get_function_list: Private method that imports the user-defined module and extracts its functions.
        __make_pipeline: Private method that creates a pipeline based on the functions extracted from the module.
        __execute_function: Private method that executes a given function from the user-defined module.
        execute_pipeline: Public method that executes the pipeline in order.
    """
    
    def __init__(self, module_name: str) -> None:
        """
        Initializes the ModuleCompiler instance.
        
        Args:
            module_name (str): Name of the module to be imported.
        """
        self.__feature_extraction_functions = []
        self.__task_functions = []
        self.__preprocess_functions = []
        
        self.module_name = module_name
        self.__get_function_list()
        self.__pipe = self.__make_pipeline()
        self.module_metadata = ModuleMetadata()
        self.__metadata_extractor()
        self.description_prompt = getattr(self.__user_module_main_file, "DESCRIPTION_PROMPT")
        
        gc.collect() # Collect unused lists

    def __get_function_list(self):
        """Private method that imports the user-defined module and extracts its functions."""
        module_import = ".main"
        package = ".".join(["src", "user_modules" , self.module_name])
        self.__user_module_main_file = import_module(module_import, 
                                                   package=package)
        module_contents = dir(self.__user_module_main_file)
        self.__fn_list = filter(lambda x: "module_" in x, module_contents)
        self.__metadata = filter(lambda x: "META_" in x, module_contents)

    def __make_pipeline(self):
        """Private method that creates a pipeline based on the functions extracted from the module."""
        feature = []
        preprocess = []
        task = []

        for fn in self.__fn_list:
            function = getattr(self.__user_module_main_file, fn)
            if "task" in fn:
                self.__task_functions.append((function, function.priority))
            elif "preprocess" in fn:
                self.__preprocess_functions.append((function, function.priority))
            elif "feature" in fn:
                self.__feature_extraction_functions.append((function, function.priority))
        # Ordeing priority tuples
        self.__task_functions.sort(key=lambda x: x[1])
        self.__preprocess_functions.sort(key=lambda x: x[1])
        self.__feature_extraction_functions.sort(key=lambda x: x[1])

    def __execute_function(self, name: str, fn_input = None):
        """
        Private method that executes a given function from the user-defined module.
        
        Args:
            name (str): Name of the function to be executed.
            fn_input (optional): Input for the function. Defaults to None.
        
        Returns:
            Output of the function.
        """
        func = getattr(self.__user_module_main_file, name)
        if input:
            return func(fn_input)
        return func()
    
    def __metadata_extractor(self):
        """
        Extracts metadata from the user-defined module.

        This method reads the user-defined module and extracts metadata based on predefined tags.
        The metadata extracted includes module name, description, version, author and licence.
        The metadata is stored in a ModuleMetadata object as attributes.

        Args:
            None

        Returns:
            None
        """

        target = self.__user_module_main_file
        for meta_tag in self.__metadata:
            match meta_tag:
                case "META_MODULE_NAME":
                    self.module_metadata.module_name = getattr(target, meta_tag)
                case "META_AUTHOR":
                    self.module_metadata.module_author = getattr(target, meta_tag)
                case "META_MODULE_DESCRIPTION":
                    self.module_metadata.module_description = getattr(target, meta_tag)
                case "META_MODULE_VERSION":
                    self.module_metadata.module_version = getattr(target, meta_tag)
                case "META_AUTHOR":
                    self.module_metadata.module_author = getattr(target, meta_tag)
                case "META_LICENCE":
                    self.module_metadata.module_licence = getattr(target, meta_tag)
                
#    def execute_pipeline(self, fn_input = None):
#        """
#        Public method that executes the pipeline in order.
#        
#        Args:
#            fn_input (optional): Input for the pipeline. Defaults to None.
#        """
#        for fn in self.__pipe:
#            fn_input = self.__execute_function(fn, fn_input)

class ModuleManager:
    """
    Class that manages user modules located in a specified directory.

    Args:
    - module_locations (str): path to the directory where the user modules are located. Default is "./src/user_modules".

    Attributes:
    - module_locations (str): path to the directory where the user modules are located.
    - __modules (list): list of compiled user modules.
    - __descriptions (list): list of descriptions of the user modules.

    Methods:
    - __locate_modules(): private method that compiles the user modules and stores them in __modules.
    - return_descriptions(): method that returns a string with the descriptions of the user modules in __descriptions.

    """

    def __init__(self, module_locations="./src/user_modules"):
        """
        Constructor for the ModuleManager class.

        Args:
        - module_locations (str): path to the directory where the user modules are located. Default is "./src/user_modules".
        """
        self.module_locations = module_locations
        self.__modules = []
        self.__descriptions = []

        self.__locate_modules()


    def __locate_modules(self):
        """
        Private method that compiles the user modules and stores them in __modules.
        """
        for d in os.listdir(self.module_locations):
            compiled_module = ModuleCompiler(d)
            self.__modules.append(compiled_module)
            self.__descriptions.append(compiled_module.description_prompt)

        
    def return_descriptions(self):
        """
        Method that returns a string with the descriptions of the user modules in __descriptions.

        Returns:
        - descriptions_list (str): string with the descriptions of the user modules in __descriptions.
        """
        descriptions_list = ""
        i = 0
        for descr in self.__descriptions:
            i += 1
            descriptions_list += f"\t{i}. {descr}\n"
        descriptions_list += f"\t{i+1}. Chatbot\n"
        return descriptions_list[:-1], len(self.__descriptions)
