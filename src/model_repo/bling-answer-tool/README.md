---
license: apache-2.0
---

# Model Card for Model ID

<!-- Provide a quick summary of what the model is/does. -->

**bling-answer-tool** is a quantized version of BLING Tiny-Llama 1B, with 4_K_M GGUF quantization, providing a very fast, very small inference implementation for use on CPUs.  

[**bling-tiny-llama**](https://huggingface.co/llmware/bling-tiny-llama-v0) is a fact-based question-answering model, optimized for complex business documents.  

To pull the model via API:  

    from huggingface_hub import snapshot_download           
    snapshot_download("llmware/bling-answer-tool", local_dir="/path/on/your/machine/", local_dir_use_symlinks=False)  
    

Load in your favorite GGUF inference engine, or try with llmware as follows:

    from llmware.models import ModelCatalog  
    model = ModelCatalog().load_model("bling-answer-tool")            
    response = model.inference(query, add_context=text_sample)  

Note: please review [**config.json**](https://huggingface.co/llmware/bling-answer-tool/blob/main/config.json) in the repository for prompt wrapping information, details on the model, and full test set.  


### Model Description

<!-- Provide a longer summary of what this model is. -->

- **Developed by:** llmware
- **Model type:** GGUF 
- **Language(s) (NLP):** English
- **License:** Apache 2.0
- **Quantized from model:** [llmware/bling-tiny-llama](https://huggingface.co/llmware/bling-tiny-llama-v0/)
  

## Model Card Contact

Darren Oberst & llmware team