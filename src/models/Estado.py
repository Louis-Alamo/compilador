class Estado:
    def __init__(self, s: str, i: int,r: str, a: list[str], b: list[str], a_copy: list[int],  alternativas: list[int] = None) -> None:
        self.r = r
        self.s = s
        self.i = i
        self.a = a[:]
        self.a_copy = a_copy[:]
        self.b = b[:]
        self.alternativas = alternativas[:] if alternativas else []

    def __str__(self) -> str:
        RESET = "\033[0m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        MAGENTA = "\033[35m"

        return (f"R: {RED}{self.r}{RESET}\t"
                f"S: {GREEN}{self.s}{RESET}\t"
                f"I: {YELLOW}{self.i}{RESET}\t"
                f"A_copy: {CYAN}{self.a_copy}{RESET}\t"
                f"A: {CYAN}{self.a}{RESET}\t"
                f"B: {MAGENTA}{self.b}{RESET}")
