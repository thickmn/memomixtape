---
license: apache-2.0
---

# SLIM-NER-TOOL

<!-- Provide a quick summary of what the model is/does. -->


**slim-ner-tool** is a 4_K_M quantized GGUF version of slim-ner, providing a small, fast inference implementation, optimized for multi-model concurrent deployment.  

[**slim-ner**](https://huggingface.co/llmware/slim-ner) is part of the SLIM ("**S**tructured **L**anguage **I**nstruction **M**odel") series, providing a set of small, specialized decoder-based LLMs, fine-tuned for function-calling.

To pull the model via API:  

    from huggingface_hub import snapshot_download           
    snapshot_download("llmware/slim-ner-tool", local_dir="/path/on/your/machine/", local_dir_use_symlinks=False)  
    

Load in your favorite GGUF inference engine, or try with llmware as follows:

    from llmware.models import ModelCatalog  
    
    # to load the model and make a basic inference
    model = ModelCatalog().load_model("slim-ner-tool")
    response = model.function_call(text_sample)  

    # this one line will download the model and run a series of tests
    ModelCatalog().tool_test_run("slim-ner-tool", verbose=True)  


Slim models can also be orchestrated as part of a multi-model, multi-step LLMfx calls:

    from llmware.agents import LLMfx

    llm_fx = LLMfx()
    llm_fx.load_tool("ner")
    response = llm_fx.ner(text)  


Note: please review [**config.json**](https://huggingface.co/llmware/slim-ner-tool/blob/main/config.json) in the repository for prompt wrapping information, details on the model, and full test set.  


## Model Card Contact

Darren Oberst & llmware team  

[Any questions? Join us on Discord](https://discord.gg/MhZn5Nc39h)
