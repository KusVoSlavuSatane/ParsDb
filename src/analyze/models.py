from pydantic import RootModel


class Analyze(RootModel[dict[str, dict[str, dict[str, str]]]]):
    """Модель для данных вида {"2024Q1": {"stringi": {"hi": "значение"}}}."""

    root: dict[str, dict[str, dict[str, str]]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def items(self):
        return self.root.items()
