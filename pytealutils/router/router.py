from pyteal import (
    Bytes,
    CompileOptions,
    Cond,
    Expr,
    Mode,
    OnComplete,
    Return,
    TealType,
    Txn,
    compileTeal,
)


class ApplicationRouter:
    def __init__(self, default: Expr):
        self.handlers = []

        self.oc_handlers = {
            "delete": [OnComplete.DeleteApplication, default],
            "update": [OnComplete.UpdateApplication, default],
            "closeout": [OnComplete.CloseOut, default],
            "optin": [OnComplete.OptIn, default],
        }

    def on_delete(self, handler: Expr):
        self.oc_handlers["delete"][1] = handler

    def on_update(self, handler: Expr):
        self.oc_handlers["update"][1] = handler

    def on_closeout(self, handler: Expr):
        self.oc_handlers["closeout"][1] = handler

    def on_optin(self, handler: Expr):
        self.oc_handlers["optin"][1] = handler

    def handle(self, name: str, handler: Expr):
        self.handlers.append(
            [Txn.application_args[0] == Bytes(name), Return(handler())]
        )

    def __teal__(self, options: "CompileOptions"):
        return Cond(
            *[
                [Txn.on_completion() == handler[0], handler[1]]
                for _, handler in self.oc_handlers.items()
            ],
            *self.handlers,
        ).__teal__(options)

    def type_of(self):
        return TealType.uint64

    def has_return(self):
        return True

    def compile(self, **kwargs):
        return compileTeal(self, mode=Mode.Application, version=6, **kwargs)
