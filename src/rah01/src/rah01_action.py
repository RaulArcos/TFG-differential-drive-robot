from pid_controller import PIDController

class RAH01Action:
    def __init__(self) -> None:
        self._pid_angular = PIDController(0.3, 0.000001, 0.0)
        self._pid_linear = PIDController(0.6, 0.000002, 0.0)

    