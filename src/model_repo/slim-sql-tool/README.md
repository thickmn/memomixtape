---
license: apache-2.0
---

# SLIM-SQL-TOOL

<!-- Provide a quick summary of what the model is/does. -->


**slim-sql-tool** is a 4_K_M quantized GGUF version of slim-sql-1b-v0, providing a small, fast inference implementation, optimized for multi-model concurrent deployment.  

[**slim-sql**](https://huggingface.co/llmware/slim-sql-1b-v0) is part of the SLIM ("**S**tructured **L**anguage **I**nstruction **M**odel") series, providing a set of small, specialized decoder-based LLMs, fine-tuned for function-calling.

*Note:  slim-sql is designed for small, fast, local prototyping and to be effective for 'one-table' lookups - it was not trained or optimized for complex joins and other sophisticated SQL queries.*  


To pull the model via API:  

    from huggingface_hub import snapshot_download           
    snapshot_download("llmware/slim-sql-tool", local_dir="/path/on/your/machine/", local_dir_use_symlinks=False)  
    

Load in your favorite GGUF inference engine, or try with llmware as follows:

    from llmware.models import ModelCatalog  
    
    # this one line will download the model and run a series of tests
    # includes two sample table schema - go to llmware github repo for end-to-end example  
    ModelCatalog().tool_test_run("slim-sql-tool", verbose=True)  


Slim models can also be orchestrated as part of multi-model, multi-step LLMfx calls:

    from llmware.agents import LLMfx

    llm_fx = LLMfx()
    llm_fx.load_tool("sql")
    response = llm_fx.sql(query, table_schema)  


Note: please review [**config.json**](https://huggingface.co/llmware/slim-sql-tool/blob/main/config.json) in the repository for prompt wrapping information, details on the model, and full test set.  

Note: two sample 'hello world' csv tables are included - this is fabricated data - any similarity with real people is coincidental.  


## Model Card Contact

Darren Oberst & llmware team  

[Any questions? Join us on Discord](https://discord.gg/MhZn5Nc39h)
