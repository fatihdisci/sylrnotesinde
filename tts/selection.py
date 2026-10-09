"""Resolve the active narrator without silently reinstalling discarded candidates."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def narrator_config():
    return json.loads((ROOT/'config/narrator.json').read_text())

def selected_models(model=None, all_models=False):
    models=json.loads((ROOT/'config/models.json').read_text())
    active=narrator_config()['activeModel']
    keys=list(models) if all_models or (model is None and active is None) else [model or active]
    return {key:models[key] for key in keys}

def add_selection_arguments(parser):
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--model',choices=list(selected_models(all_models=True)))
    group.add_argument('--all',action='store_true',help='Explicitly include all comparison candidates')
