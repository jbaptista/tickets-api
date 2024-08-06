from typing import Any, Type, TypeVar

from fastapi import Depends, FastAPI, Request


def register_state(app: FastAPI, state: Any):
    if not getattr(app.state, "class_registry", None):
        app.state.class_registry = {state.__class__: state}
    else:
        app.state.class_registry[state.__class__] = state


T = TypeVar("T")


def load_state(state_type: Type[T]) -> T:
    def state_loader(request: Request) -> T:
        return request.app.state.class_registry[state_type]

    return Depends(state_loader)
