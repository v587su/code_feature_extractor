# Code_Feature_Extracter

This is a tool for extracting human-made features from java code snippets at method level.

### Usage
#### get_api_sequence:
The format of api sequences follows the instruction in the paper "Deep Code Search"
```
    code_str = "public <T> T to(Class<T> targetClass) {\n    JsonElement json = DEFAULT_GSON.toJsonTree(toMap());\n    \n    if (targetClass == JsonElement.class) {\n      return targetClass.cast(json);\n    }\n    \n    return DEFAULT_GSON.fromJson(json, targetClass);\n  }"
    extractor = FeatureExtractor(code_str)
    api_sequence = extractor.get_api_sequence()

```