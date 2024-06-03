from dataclasses import dataclass


@dataclass
class Sound:
    """
    Класс, содержащий  информацию об песне
    """
    name: str
    url: str