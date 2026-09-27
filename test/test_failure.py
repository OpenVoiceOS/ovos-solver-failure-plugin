"""The failure plugin speaks the localized line for the language it is asked in."""
import os

import pytest

from ovos_plugin_manager.templates.agents import AgentMessage, ChatEngine, MessageRole

import ovos_solver_failure_plugin as pkg
from ovos_solver_failure_plugin import FailureChatEngine

LOCALE = os.path.join(os.path.dirname(pkg.__file__), "locale")


def _lines(lang_dir):
    with open(os.path.join(LOCALE, lang_dir, "no_brain.dialog")) as f:
        return [ln for ln in f.read().split("\n")
                if ln.strip() and not ln.startswith("#")]


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
    """Read the shipped directories rather than naming them.

    This asserted the listing equalled a four-locale literal, so adding a
    fifth (``kab``, which dev did) failed a test about line content. Which
    languages ship is not this test's property: a locale arrives by dropping
    a directory in, and a test that has to be edited for that is a tax on
    the next translation. What is worth holding is that whatever ships is
    usable.
    """
    dirs = sorted(d for d in os.listdir(LOCALE) if os.path.isdir(os.path.join(LOCALE, d)))
    assert dirs, f"no locale directories under {LOCALE}: the package data is missing"
    for d in dirs:
        path = os.path.join(LOCALE, d, "no_brain.dialog")
        assert os.path.isfile(path), f"{d} ships no no_brain.dialog"
        assert _lines(d), f"{d}/no_brain.dialog has no usable line"


