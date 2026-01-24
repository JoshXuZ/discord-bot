from __future__ import annotations
from abc import ABC, abstractmethod
import re

class MetalPriceProvider(ABC):
    @abstractmethod
    def metal(self) -> str: ...

    @abstractmethod
    def calculate(self, html) -> float: ...

class PriceProvider(MetalPriceProvider):
    def __init__(self, metal):
        self._metal = metal.upper()

    def metal(self):
        return self._metal.lower()
    
    def calculate(self, html):
        block = re.search(r'<ul[^>]+id="hprice"[^>]*>(.*?)</ul>', html, re.S | re.I)
        if not block:
            raise ValueError("Could not find hprice block")

        hprice = block.group(1)

        li = re.search(rf'<li\b[^>]*>.*?BUY\s+{self._metal}.*?</li>', hprice, re.S | re.I)
        if not li:
            raise ValueError(f"Could not find BUY {self._metal} row")

        row = li.group(0)

        m = re.search(
            rf'href="[^"]*/store/{self.metal()}"[^>]*>\s*([\d,]+(?:\.\d+)?)\s*/oz',
            row,
            re.S | re.I
        )
        if not m:
            raise ValueError(f"Could not find price for {self._metal}")

        return float(m.group(1).replace(",", ""))