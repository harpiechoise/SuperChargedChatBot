from typing import Callable

def feature_extractor_prompt(prompt, fallback):
    def decorator(func: Callable):
        func.prompt = prompt
        func.fallback = fallback
        return func
    return decorator

def feature_extraction_ordering(step_order: int):
    def decorator(func: Callable):
        func.priority = step_order
        return func
    return decorator

