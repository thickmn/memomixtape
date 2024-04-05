---
license: cc-by-sa-4.0
---

# SLIM-EXTRACT-TOOL

<!-- Provide a quick summary of what the model is/does. -->


**slim-extract-tool** is a 4_K_M quantized GGUF version of slim-extract, providing a small, fast inference implementation, optimized for multi-model concurrent deployment.  

This model has been fine-tuned to implement a general-purpose extraction function that takes a custom key as input parameter, and generates a python dictionary consisting of that custom key with the value consisting of a list of the values associated with that key in the text.   

The intent of SLIMs is to forge a middle-ground between traditional encoder-based classifiers and open-ended API-based LLMs.


[**slim-extract**](https://huggingface.co/llmware/slim-extract) is part of the SLIM ("**S**tructured **L**anguage **I**nstruction **M**odel") series, providing a set of small, specialized decoder-based LLMs, fine-tuned for function-calling.

To pull the model via API:  

    from huggingface_hub import snapshot_download           
    snapshot_download("llmware/slim-extract-tool", local_dir="/path/on/your/machine/", local_dir_use_symlinks=False)  
    

Load in your favorite GGUF inference engine, or try with llmware as follows:

    from llmware.models import ModelCatalog  
    
    # to load the model and make a basic inference
    model = ModelCatalog().load_model("slim-extract-tool")
    response = model.function_call(text_sample)  

    # this one line will download the model and run a series of tests
    ModelCatalog().tool_test_run("slim-extract-tool", verbose=True)  


Note: please review [**config.json**](https://huggingface.co/llmware/slim-extract-tool/blob/main/config.json) in the repository for prompt wrapping information, details on the model, and full test set.  


## Model Card Contact

Darren Oberst & llmware team  

[Any questions? Join us on Discord](https://discord.gg/MhZn5Nc39h)