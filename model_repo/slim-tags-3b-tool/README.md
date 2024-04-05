---
license: cc-by-sa-4.0
---

# SLIM-TAGS-3B-TOOL

<!-- Provide a quick summary of what the model is/does. -->


**slim-tags-3b-tool** is a 4_K_M quantized GGUF version of [**slim-tags-3b**](https://huggingface.co/llmware/slim-tags-3b) providing a small, fast inference implementation, optimized for multi-model concurrent deployment.  

slim-tags-3b is a small, specialized function-calling model fine-tuned to extract and generate meaningful tags from a chunk of text.

Tags generally correspond to named entities, but will also include key objects, entities and phrases that contribute meaningfully to the semantic meaning of the text.

The model is invoked as a specialized 'tags' classifier function that outputs a python dictionary in the form of:

    {'tags': ['NASDAQ', 'S&P', 'Dow', 'Verizon', 'Netflix, ... ']}

with the value items in the list generally being extracted from the source text.

The intended use of the model is to auto-generate tags to text that can be used to enhance search retrieval, categorization, or to extract named entities that can be used programmatically in follow-up queries or prompts. It can also be used for fact-checking as a secondary validation on a longer (separate) LLM output.  


To pull the model via API:  

    from huggingface_hub import snapshot_download           
    snapshot_download("llmware/slim-tags-3b-tool", local_dir="/path/on/your/machine/", local_dir_use_symlinks=False)  
    

Load in your favorite GGUF inference engine, or try with llmware as follows:

    from llmware.models import ModelCatalog  
    
    # to load the model and make a basic inference
    model = ModelCatalog().load_model("slim-tags-3b-tool")
    response = model.function_call(text_sample)  

    # this one line will download the model and run a series of tests
    ModelCatalog().tool_test_run("slim-tags-3b-tool", verbose=True)  


Note: please review [**config.json**](https://huggingface.co/llmware/slim-tags-3b-tool/blob/main/config.json) in the repository for prompt wrapping information, details on the model, and full test set.  


## Model Card Contact

Darren Oberst & llmware team  

[Any questions? Join us on Discord](https://discord.gg/MhZn5Nc39h)