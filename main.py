"""ChatGPT plugin for ChatGPT to interact with Lean through LeanDojo.
"""
import json
import argparse
import quart
import quart_cors
from quart import request
from loguru import logger

from lean_dojo import *

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")
repo = None
theorem = None
dojo = None
states = dict()


@app.post("/initialize_proof_search")
async def initialize_proof_search():
    data = await request.get_json(force=True)

    global theorem
    global dojo
    global states

    theorem = Theorem(repo, data["theorem_file_path"], data["theorem_name"])

    (dojo, s) = Dojo(theorem).__enter__()
    assert isinstance(s, TacticState)
    states[s.id] = s

    return quart.Response(
        response=json.dumps({"state_id": s.id, "state": s.pp}), status=200
    )


@app.post("/run_tactic")
async def run_tactic():
    data = await request.get_json(force=True)

    global states

    s = dojo.run_tac(states[data["state_id"]], data["tactic"])

    if isinstance(s, TacticState):
        res = {
            "state_id": s.id,
            "state": s.pp,
            "proof_finished": False,
        }
        states[s.id] = s
    elif isinstance(s, ProofGivenUp):
        res = {
            "error": "The proof is abandoned because of `sorry`.",
            "proof_finished": False,
        }
    elif type(s) in (TacticError, TimeoutError):
        res = {
            "error": s.error,
            "proof_finished": False,
        }
    else:
        assert isinstance(s, ProofFinished)
        res = {
            "proof_finished": True,
        }
    return quart.Response(response=json.dumps(str(res)), status=200)


@app.get("/logo.jpg")
async def plugin_logo():
    return await quart.send_file("images/logo.jpg", mimetype="image/jpg")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers["Host"]
    with open("manifest.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"http://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers["Host"]
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"http://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", type=str, default="https://github.com/yangky11/lean-example"
    )
    parser.add_argument(
        "--commit", type=str, default="5a0360e49946815cb53132638ccdd46fb1859e2a"
    )
    parser.add_argument("--port", type=int, default=23333)
    args = parser.parse_args()
    logger.info(args)

    global repo
    repo = LeanGitRepo(args.url, args.commit)
    assert is_available_in_cache(
        repo
    ), f"{repo} hasn't been traced yet. See https://leandojo.readthedocs.io/en/latest/getting-started.html."

    app.run(debug=True, host="localhost", port=args.port)


if __name__ == "__main__":
    main()
