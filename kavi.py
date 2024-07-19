#!/usr/bin/python

from llama_cpp import Llama
from typing import Dict, List
import json, os, sys
import gradio as gr

# some global varibles
home_dir = os.path.expanduser('~')
kavi_dir = os.path.join(home_dir,".kavi")
kavi_config = os.path.join(kavi_dir,"config.json")
config = None
prompt_template = None

def check_config_dir():
    """
    function will check if config-dir and config-file exist else create one.
    ~/.kavi/config.json
    """
    global config

    try:
        os.makedirs(kavi_dir, exist_ok=True)
        if not os.path.isfile(kavi_config):
            os.popen(f'cp config.json {kavi_config}')
    except Exception as e:
        print("failed to create config-dir and/or config-file")
        sys.exist(0)
    finally:
        with open(kavi_config, "r") as fobj:
            config = json.load(fobj)


def download_and_get_model(repo_id="TheBloke/Mistral-7B-v0.1-GGUF", filename="*Q4_K_S.gguf"):
    """
    Download model from huggingface and then return model obj
    """
    return Llama.from_pretrained(
        repo_id=repo_id,
        filename=filename,
        verbose=True
    )


def get_model(model_path:str) -> Llama:
    """
    Load model from local filesystem and then return model obj
    """
    return Llama(
        model_path=model_path,
        n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
        n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
        n_gpu_layers=35, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
        verbose=False)


def prompt_model(llm: Llama, prompt: str, model_name="phi3") -> Dict:
    """
    run prompt query on model and return result
    """
    global prompt_template

    if prompt_template is None:
        prompt_template = config[model_name]["prompt_config"]["prompt"]
        # delete prompt text key from dict
        del config[model_name]["prompt_config"]["prompt"]
    # substitute prompt text inside propmt template string
    prompt_str:str = prompt_template.format(prompt)
    # pass prompt_string & entire prompt_config to model
    return llm(prompt_str, **config[model_name]["prompt_config"])


def doit(prompt_text):
    model_name= config["default_model"]
    model_path = config[model_name]["model_local_path"]
    llm = get_model(model_path)
    resp = prompt_model(llm=llm, prompt=prompt_text, model_name=model_name)
    return resp["choices"][0]["text"]    


def main():
    check_config_dir()
    demo = gr.Interface(fn=doit, inputs="textbox", outputs="textbox")
    demo.launch()


if __name__ == "__main__":
    main()