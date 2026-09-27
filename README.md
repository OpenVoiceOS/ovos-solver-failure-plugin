# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> ovos-solver-failure-plugin

A chat engine plugin for OpenVoiceOS personas that never answers the question. It always returns a canned line, so it works as the last link of a persona chain when every other handler declines. Registered as `ovos-solver-failure-plugin` in the `opm.agents.chat` entry-point group.

## Install

```bash
pip install ovos-solver-failure-plugin
```

## Usage

In a persona file, list it last:

```json
{"name": "OldSchoolBot", "solvers": ["ovos-solver-rivescript-plugin", "ovos-solver-failure-plugin"]}
```

Directly:

```python
from ovos_plugin_manager.templates.agents import AgentMessage, MessageRole
from ovos_solver_failure_plugin import FailureChatEngine

engine = FailureChatEngine()
reply = engine.continue_chat([AgentMessage(MessageRole.USER, "hello")], lang="en-US")
print(reply.content)
# 404 brain not found
```

The plugin ships lines for `en-US`, `da-DK`, `fr-FR`, and `sv-SE` in `locale/<lang>/no_brain.dialog`. The `lang` argument picks the closest shipped language (`en-us` and `en-GB` both resolve to `en-US`). If no shipped language is close enough, the reply is `404`.

## Related projects

- [OpenVoiceOS/ovos-persona](https://github.com/OpenVoiceOS/ovos-persona): chains handlers, including this one, to answer user queries.
- [OpenVoiceOS/ovos-solver-BM25-plugin](https://github.com/OpenVoiceOS/ovos-solver-BM25-plugin): a sibling question solver plugin.
- [OpenVoiceOS/ovos-ddg-solver-plugin](https://github.com/OpenVoiceOS/ovos-ddg-solver-plugin): a sibling question solver plugin backed by DuckDuckGo.

## License

MIT
