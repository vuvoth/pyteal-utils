from pyteal import Approve, Int, Reject, Subroutine, TealType

from .router import ApplicationRouter


def test_create():
    r = ApplicationRouter(Approve())

    r.on_delete(Reject())
    r.on_update(Reject())

    @Subroutine(TealType.uint64)
    def vote():
        return Int(1)

    r.handle("vote", vote)

    print(r.compile())
