class Config:
    """
    Holds configuration options.
    """

    def __init__(self) -> None:
        self.allow_plugins = True
        self.serviceable = False
        self.non_serviceable = False
        self.critSysTerm = False
        self.hidden = False
        self.hex = False
        self.rev = False
        self.severities = []
        self.only = False
