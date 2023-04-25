from dataclasses import dataclass

@dataclass
class Training:
    name:str = None
    room:str = None

@dataclass
class Formation:
    nom:str = None
    salle:str = None