ChatGPT Plugin for Theorem Proving in Lean
==========================================

https://github.com/lean-dojo/LeanDojoChatGPT/assets/5431913/cfbb11e0-3e52-4174-a1b5-c855f79873dd

We use [LeanDojo](https://github.com/lean-dojo/LeanDojo) to build a [ChatGPT plugin](https://openai.com/blog/chatgpt-plugins), enabling ChatGPT to prove theorems by interacting with Lean. For details, please read Appendix E of our paper:

[LeanDojo: Theorem Proving with Retrieval-Augmented Language Models](https://leandojo.org/)      
Neural Information Processing Systems (NeurIPS), 2023  
[Kaiyu Yang](https://yangky11.github.io/), [Aidan Swope](https://aidanswope.com/about), [Alex Gu](https://minimario.github.io/), [Rahul Chalamala](https://rchalamala.github.io/),  
[Peiyang Song](https://peiyang-song.github.io/), [Shixing Yu](https://billysx.github.io/), [Saad Godil](https://www.linkedin.com/in/saad-godil-9728353/), [Ryan Prenger](https://www.linkedin.com/in/ryan-prenger-18797ba1/), [Anima Anandkumar](http://tensorlab.cms.caltech.edu/users/anima/)

[![GitHub license](https://img.shields.io/github/license/MineDojo/MineDojo)](https://github.com/MineDojo/MineDojo/blob/main/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**⚠️ This repo is outdated due to changes in OpenAI's APIs: https://github.com/lean-dojo/LeanDojoChatGPT/issues/5.**

## Requirements

* Run `pip install loguru quart quart_cors lean-dojo` to install Python dependencies.
* Currently, you need developer access to [ChatGPT plugins](https://openai.com/blog/chatgpt-plugins) in order to use this repo.


## Steps to Launch the Plugin

First, launch the backend server:
```bash
CONTAINER=docker python main.py --port 23456 --url https://github.com/yangky11/lean-example --commit 5a0360e49946815cb53132638ccdd46fb1859e2a
```

Then, go to https://chat.openai.com/?model=gpt-4-plugins. Click "Plugin store" -> "Develop your own plugin." Enter "localhost:23456" and click "Find manifest file." After the plugin is found, click "Install localhost plugin."

After the plugin is successfully installed, you can ask ChatGPT to prove theorems simply by telling it the name of the theorem and where it is defined. For example:
```
I want you to prove a theorem in Lean. The theorem's name is `hello_world`, and it is defined in the file `src/example.lean`. Please explain the theorem to me, lay out a high-level proof plan, and then try various tactics to prove the theorem.
```
It may take some time to initialize the proof search.



You can play with the prompt to control ChatGPT's behavior. For example, you can ask it to produce a high-level proof plan before trying any tactic. 


## Questions and Bugs

* For general questions and discussions, please use [GitHub Discussions](https://github.com/lean-dojo/LeanDojoChatGPT/discussions).  
* To report a potential bug, please open an issue. In the issue, please include your OS information, the version of LeanDojo, the exact steps to reproduce the error, a screenshot of ChatGPT (if applicable), and complete logs printed by the backend server in debug mode (setting the environment variable `VERBOSE` to 1). The more details you provide, the better we will be able to help you. 


## Citation

```bibtex
@inproceedings{yang2023leandojo,
  title={{LeanDojo}: Theorem Proving with Retrieval-Augmented Language Models},
  author={Yang, Kaiyu and Swope, Aidan and Gu, Alex and Chalamala, Rahul and Song, Peiyang and Yu, Shixing and Godil, Saad and Prenger, Ryan and Anandkumar, Anima},
  booktitle={Neural Information Processing Systems (NeurIPS)},
  year={2023}
}
```
