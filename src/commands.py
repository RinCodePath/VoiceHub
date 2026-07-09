"""Unified command definitions with multi-language support."""

from src.config import CONFIG
from src.strings import get_string

# Single source of truth for all commands with localization keys
COMMANDS = {
    'browser': {
        'action': 'browser',
        'message_key': 'cmd_browser_message',
        'trigger_keys': ['cmd_browser_triggers'],
    },
    'editor': {
        'action': 'editor',
        'message_key': 'cmd_editor_message',
        'trigger_keys': ['cmd_editor_triggers'],
    },
    'game': {
        'action': 'game',
        'message_key': 'cmd_game_message',
        'trigger_keys': ['cmd_game_triggers'],
    },
    'help': {
        'action': 'help',
        'message_key': 'cmd_help_message',
        'trigger_keys': ['cmd_help_triggers'],
    },
    'change_lang': {
        'action': 'change_lang',
        'message_key': 'cmd_lang_message',
        'trigger_keys': ['cmd_lang_triggers'],
    },
    'shutdown': {
        'action': 'shutdown',
        'message_key': 'cmd_shutdown_message',
        'trigger_keys': ['cmd_shutdown_triggers'],
    }
}


def get_command_triggers(cmd_id):
    """Get all trigger phrases for a command in current language."""
    if cmd_id not in COMMANDS:
        return []
    
    trigger_keys = COMMANDS[cmd_id].get('trigger_keys', [])
    triggers = []
    for key in trigger_keys:
        trigger_phrases = get_string(key, [])
        if isinstance(trigger_phrases, list):
            triggers.extend(trigger_phrases)
    return triggers


def get_command_message(cmd_id):
    """Get command message in current language."""
    if cmd_id not in COMMANDS:
        return None
    message_key = COMMANDS[cmd_id].get('message_key')
    return get_string(message_key, '') if message_key else None


def find_command(text):
    """Find matching command from user input text.
    
    Args:
        text: User input text (voice recognized)
    
    Returns:
        dict: Command data if found, None otherwise
    """
    text = text.lower().strip()
    
    for cmd_id, cmd_data in COMMANDS.items():
        triggers = get_command_triggers(cmd_id)
        for trigger in triggers:
            if trigger.lower() in text:
                return {
                    'id': cmd_id,
                    'action': cmd_data['action'],
                    'message': get_command_message(cmd_id),
                    'triggers': triggers
                }
    return None


def get_all_commands_display():
    """Get all commands with their triggers for help display.
    
    Returns:
        dict: Command ID -> {action, message, triggers}
    """
    result = {}
    for cmd_id, cmd_data in COMMANDS.items():
        result[cmd_id] = {
            'action': cmd_data['action'],
            'message': get_command_message(cmd_id),
            'triggers': get_command_triggers(cmd_id)
        }
    return result
