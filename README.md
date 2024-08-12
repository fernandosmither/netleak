![NetLeak](https://github.com/user-attachments/assets/c5b3e5fc-9380-4218-809b-ab28cbba79ec)
<p align="center">
    <em>NetLeak: Breaking E2EE Metadata Privacy via Network attacks</em>
</p>

---

**Paper**: <a href="" target="_blank">In progress...</a>

**Source Code**: <a href="https://github.com/fernandosmither/netleak" target="_blank">[https://github.com/fastapi/fastapi](https://github.com/fernandosmither/netleak)</a>

---

This project empirically demonstrates how resistant is Metadata Privacy of E2EE systems.

To accomplish this, we use a simple simulation using the `Python bindings` [signal-protocol](https://pypi.org/project/signal-protocol/) for the `Rust` implementation of the [Signal Protocol](https://signal.org/docs/) and aim to uncover who is talking to whom, after a series of messages are exchanged.

## Motivation

The motivation for this project is to understand how resistant are E2EE systems to Metadata Privacy. We usually assume that network adversaries break Metadata Privacy, but we want to empirically measure how critical these attacks actually.


## Setup

1. Install Python 3.9. You can use [pyenv](https://github.com/pyenv/pyenv) to manage Python versions.

2. Install poetry

```bash
# To install poetry, it's recommended to use pipx. If you don't have pipx, install it first with
sudo apt install pipx

# Install Poetry
pipx install poetry
```

3. Install dependencies

```bash
poetry install
```

4. Run the simulation

```bash
poetry run python main.py
```
