# TODO: Move metadata functions to a Python Package server
from src.user_modules.example.lib.metadata_functions import feature_extractor_prompt
META_MODULE_NAME = "Example Module"
META_MODULE_DESCRIPTION = "An example module to test the funcion"
META_MODULE_VERSION = "1.0"
META_AUTHOR = "Psychecat"
META_LICENCE = """
(c) Copyright 2020 by Psychecat Inc.
  
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"Commons Clause" License Condition v1.0

The Software is provided to you by the Licensor under the License,
as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of
rights under the License will not include, and the License does not
grant to you, the right to Sell the Software.

For purposes of the foregoing, "Sell" means practicing any or all
of the rights granted to you under the License to provide to third
parties, for a fee or other consideration (including without
limitation fees for hosting or consulting/ support services related
to the Software), a product or service whose value derives, entirely
or substantially, from the functionality of the Software. Any license
notice or attribution required by the License must also include
this Commons Clause License Condition notice.

Software: All example associated files.
License: MIT
Licensor: Psychecat
"""
# Requerido
DESCRIPTION_PROMPT = "Un modulo para ejecutar scripts de Python"

@feature_extractor_prompt(prompt="¿Puedes indentificar la descripción de la función de Python a programar?",
                          fallback="No puedo ayudarte a resolver ese problema")
def module_feature_extractor(*args):
    print("Extracting_feature", args)
    return "Feature extracted"

def module_preprocess(*args):
    print("Preprocessing", args)
    return "Preprocessing_OUT"

def module_task_1(*args):
    print("Task1 Ejecutada", args)
    return "Task1_OUT"

def module_task_2(*args):
    print("Formating Input", args)
    return "Task2_OUT"
