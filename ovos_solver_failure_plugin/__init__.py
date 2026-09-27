import random
from os.path import dirname, join, isfile
from typing import List, Optional

from ovos_plugin_manager.templates.agents import AgentMessage, ChatEngine, MessageRole
from ovos_spec_tools.resources import find_lang_dir


class FailureChatEngine(ChatEngine):
    """The last link of a persona chain: a canned line saying nothing answered.

    It never fails and never declines, so a persona that ends with it always
    speaks. The line comes from ``locale/<lang>/no_brain.dialog``, resolved
    with the OVOS-INTENT-2 language fallback, or ``404`` when no locale fits.
    """

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config or {})

    @staticmethod
    def _lines(lang: Optional[str]) -> List[str]:
        if lang:
            lang_dir = find_lang_dir(join(dirname(__file__), "locale"), lang)
            path = join(lang_dir, "no_brain.dialog") if lang_dir else ""
            if path and isfile(path):
                with open(path) as f:
                    lines = [l for l in f.read().split("\n") if l.strip() and not l.startswith("#")]
                if lines:
                    return lines
        return ["404"]

    def continue_chat(self, messages: List[AgentMessage],
                      session_id: str = "default",
                      lang: Optional[str] = None,
                      units: Optional[str] = None,
                      tools: Optional[list] = None) -> AgentMessage:
        return AgentMessage(role=MessageRole.ASSISTANT, content=random.choice(self._lines(lang)))
