def feature_extractor_prompt(prompt, fallback):
    def decorator(func):
        func.prompt = prompt
        func.fallback = fallback
        return func
    return decorator