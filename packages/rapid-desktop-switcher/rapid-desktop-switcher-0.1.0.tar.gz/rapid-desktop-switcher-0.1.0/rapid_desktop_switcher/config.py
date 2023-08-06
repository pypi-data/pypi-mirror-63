import configLoader as cl

DEFAULT_CONFIG = {
    'pressFirstAvail': [
        'escape'
    ],
    'pressFirstFriendly': [
        'Esc'
    ],
    'pressFirstDefault': -1,

    'desktopSwitchCommands': [
        ['winleft', 'F1'],
        ['winleft', 'F2'],
        ['winleft', 'F3'],
        ['winleft', 'F4'],
        ['winleft', 'F5'],
        ['winleft', 'F6'],
        ['winleft', 'F7'],
        ['winleft', 'F8'],
        ['winleft', 'F9'],
        ['winleft', 'F10'],
        ['winleft', 'F11'],
        ['winleft', 'F12']
    ],
    'desktopNamesFriendly': [
        'Desktop 1',
        'Desktop 2',
        'Desktop 3',
        'Desktop 4',
        'Desktop 5',
        'Desktop 6',
        'Desktop 7',
        'Desktop 8',
        'Desktop 9',
        'Desktop 10',
        'Desktop 11',
        'Desktop 12'
    ],
    'desktopDefault': 1,

    'triggerKeysAvail': [
        'Control_L',
        'Control_R',
        'Alt_L',
        'Alt_R',
        'Super_L',
        'Super_R',
        'Shift_R'
    ],
    'triggerKeysFriendly': [
        'Left Ctrl',
        'Right Ctrl',
        'Left Alt',
        'Right Alt',
        'Left Super',
        'Right Super',
        'Right Shift'
    ],
    'triggerKeyDefault': 6
}
fullConfig = cl.loadConfig('.rapidswitcher', DEFAULT_CONFIG)

# Validate the configuration
if not (
    # Validate keys to press first
    len(fullConfig['pressFirstAvail']) == len(fullConfig['pressFirstFriendly']) and
    fullConfig['pressFirstDefault'] >= -1 and
    fullConfig['pressFirstDefault'] < len(fullConfig['pressFirstAvail']) and
    # Validate desktops to switch to
    len(fullConfig['desktopSwitchCommands']) == len(fullConfig['desktopNamesFriendly']) and
    fullConfig['desktopDefault'] >= 1 and
    fullConfig['desktopDefault'] <= len(fullConfig['desktopSwitchCommands']) and
    # Validate trigger keys
    len(fullConfig['triggerKeysAvail']) == len(fullConfig['triggerKeysFriendly']) and
    fullConfig['triggerKeyDefault'] >= 0 and
    fullConfig['triggerKeyDefault'] < len(fullConfig['desktopSwitchCommands'])
):
    print('Invalid configuration')
    fullConfig = DEFAULT_CONFIG
# Set the options
toPressFirst = fullConfig['pressFirstDefault']
desktopToUse = fullConfig['desktopDefault']
triggerKey = fullConfig['triggerKeyDefault']
