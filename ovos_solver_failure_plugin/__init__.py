import random
from os.path import dirname, isfile
from typing import Optional, List, Tuple

from ovos_plugin_manager.templates.agents import RetrievalEngine


class DefaultFailureMessage(RetrievalEngine):
    def __init__(self, config=None):
        config = config or {}
        super().__init__(config)

    def query(self, query: str, lang: Optional[str] = None, k: int = 3) -> List[Tuple[str, float]]:
        """
        Searches the knowledge base for relevant documents or data.

        Args:
            query: The search string.
            lang: BCP-47 language code.
            k: The maximum number of results to return.

        Returns:
            List of tuples (content, score) for the top k matches.
        """
        lines = ["404"]  # all langs
        if lang:
            path = f"{dirname(__file__)}/locale/{lang.lower()}/no_brain.dialog"
            if isfile(path):
                with open(path) as f:
                    lines = [l for l in f.read().split("\n")
                             if l.strip() and not l.startswith("#")]
        return [(random.choice(lines), 0.01)]


if __name__ == "__main__":
    bot = DefaultFailureMessage()
    print(bot.query("hello!", lang="en-US"))
    print(bot.query("Olá", lang="pt-pt"))
