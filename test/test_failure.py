"""The failure plugin speaks the localized line for the language it is asked in."""
import os

import pytest

from ovos_plugin_manager.templates.agents import AgentMessage, ChatEngine, MessageRole

import ovos_solver_failure_plugin as pkg
from ovos_solver_failure_plugin import FailureChatEngine

LOCALE = os.path.join(os.path.dirname(pkg.__file__), "locale")


def _lines(lang_dir):
    with open(os.path.join(LOCALE, lang_dir, "no_brain.dialog")) as f:
        return [l for l in f.read().split("\n") if l.strip() and not l.startswith("#")]


def _ask(engine, lang):
    return engine.continue_chat([AgentMessage(MessageRole.USER, "anything")], lang=lang)


def test_is_a_chat_engine():
    assert isinstance(FailureChatEngine(), ChatEngine)


@pytest.mark.parametrize("lang,lang_dir", [("en-US", "en-US"), ("en-us", "en-US"), ("da-DK", "da-DK"), ("en-GB", "en-US")])
def test_answers_a_line_from_the_locale_file(lang, lang_dir):
    reply = _ask(FailureChatEngine(), lang)
    assert reply.role == MessageRole.ASSISTANT
    assert reply.content in _lines(lang_dir), (lang, reply.content)


def test_unknown_language_answers_404():
    assert _ask(FailureChatEngine(), "xx-XX").content == "404"


def test_every_shipped_locale_has_lines():
    dirs = sorted(d for d in os.listdir(LOCALE) if os.path.isdir(os.path.join(LOCALE, d)))
    assert dirs == ["da-DK", "en-US", "fr-FR", "sv-SE"]
    for d in dirs:
        assert _lines(d), d
