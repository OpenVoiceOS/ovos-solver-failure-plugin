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




def test_lines_reads_the_locale_file_itself():
    """`_lines` is what the reply is drawn from, and no test called it.

    The tests above go through `continue_chat`, which picks one line at
    random, so they can only assert membership. This calls the method that
    does the reading, against an independent parse of the same file.
    """
    assert FailureChatEngine._lines("en-US") == _lines("en-US")


@pytest.mark.parametrize("lang", [None, "xx-XX"])
def test_lines_falls_back_to_404(lang):
    """No language, and a language nothing ships, both reach the default."""
    assert FailureChatEngine._lines(lang) == ["404"]


def test_lines_skips_comments_and_blank_lines(tmp_path, monkeypatch):
    """The comprehension this covers drops `#` lines and whitespace-only
    ones. No shipped locale file has either, so the case needs a file of its
    own rather than a locale that happens to be written that way today.
    """
    lang_dir = tmp_path / "en-US"
    lang_dir.mkdir()
    (lang_dir / "no_brain.dialog").write_text(
        "# a comment\nfirst line\n\n   \nsecond line\n#another\n")
    monkeypatch.setattr(pkg, "find_lang_dir", lambda base, lang: str(lang_dir))
    assert FailureChatEngine._lines("en-US") == ["first line", "second line"]
