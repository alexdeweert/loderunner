import interfaces.ibasestate as ibasestate

class IdleState(ibasestate.IBaseState):
    def __init__(self, entity) -> None:
        super().__init__()
        self.entity = entity