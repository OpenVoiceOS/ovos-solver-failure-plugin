import random
from os.path import dirname
from os.path import isfile


from ovos_plugin_manager.templates.solvers import QuestionSolver


class FailureSolver(QuestionSolver):
    enable_tx = False
    priority = 9999

    def __init__(self, config=None):
        config = config or {}
        super().__init__(config)

    # officially exported Solver methods
    def get_spoken_answer(self, query, context=None):
        context = context or {}
        lang = context.get("lang") or "en-us"
        lines = ["404"]  # all langs
        path = f"{dirname(__file__)}/locale/{lang}/no_brain.dialog"
        if isfile(path):
            with open(path) as f:
                lines = [l for l in f.read().split("\n")
                         if l.strip() and not l.startswith("#")]
        return random.choice(lines)


if __name__ == "__main__":
    bot = FailureSolver()
    print(bot.get_spoken_answer("hello!"))
    print(bot.spoken_answer("Olá", {"lang": "pt-pt"}))
