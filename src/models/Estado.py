class Estado:
    def __init__(self, s: str, i: int,r: str, a: list[str], b: list[str], alternativas: list[int] = None) -> None:
        self.r = r
        self.s = s
        self.i = i
        self.a = a[:]
        self.b = b[:]
        self.alternativas = alternativas[:] if alternativas else []

    def __str__(self) -> str:
        return f"R: {self.r}\tS: {self.s}\tI: {self.i}\tA: {self.a}\tB: {self.b}"