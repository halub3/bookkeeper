"""
Описан класс, представляющий бюджет за период, декомпозированный на категории
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Расходная операция.
    period - период (дни)
    category - id категории расходов
    amount - сумма
    pk - id записи в базе данных
    """
    period: int
    category: int
    amount: int
    pk: int = 0
