def main():
    import config
    import pyautogui as auto
    import os
    import time
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QCheckBox
    try:
        from pyxhook import pyxhook as ph
    except:
        from pyhook import pyhook as ph

    # Set up GUI
    class UI_MESSAGES:
        windowTitle = 'Rapid virtual desktop switcher'
        pressFirstLabel = 'Press this key first: '
        desktopSelectLabel = 'Switch to this desktop: '
        triggerKeyLabel = 'Activate when this key is pressed: '

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle(UI_MESSAGES.windowTitle)
    mainLayout = QVBoxLayout()

    # Area to select key to press first
    pressFirstLayout = QHBoxLayout()

    # Checkbox for if the user even wants to press a key first
    pressFirstCheck = QCheckBox()
    pressFirstCheck.setChecked(config.toPressFirst != -1)
    pressFirstLayout.addWidget(pressFirstCheck)

    # The label
    pressFirstLabel = QLabel(UI_MESSAGES.pressFirstLabel)
    pressFirstLayout.addWidget(pressFirstLabel)

    # The list of available keys to press first
    pressFirstChoices = QComboBox()
    for item in config.fullConfig['pressFirstFriendly']:
        pressFirstChoices.addItem(item)
    pressFirstChoices.setCurrentIndex(
        config.toPressFirst if config.toPressFirst >= 0 else 0)
    pressFirstLayout.addWidget(pressFirstChoices)

    # Add the layout as a nested layout within the main layout
    mainLayout.addLayout(pressFirstLayout)

    # Selector for which desktop to use
    desktopSelectorLayout = QHBoxLayout()
    desktopSelectorLayout.addWidget(QLabel(UI_MESSAGES.desktopSelectLabel))
    desktopChoices = QComboBox()
    for item in config.fullConfig['desktopNamesFriendly']:
        desktopChoices.addItem(item)
    desktopChoices.setCurrentIndex(config.desktopToUse - 1)
    desktopSelectorLayout.addWidget(desktopChoices)
    mainLayout.addLayout(desktopSelectorLayout)

    # Trigger key selector
    triggerKeyLayout = QHBoxLayout()
    triggerKeyLayout.addWidget(QLabel(UI_MESSAGES.triggerKeyLabel))
    triggerKeyChoices = QComboBox()
    for item in config.fullConfig['triggerKeysFriendly']:
        triggerKeyChoices.addItem(item)
    triggerKeyChoices.setCurrentIndex(config.triggerKey)
    triggerKeyLayout.addWidget(triggerKeyChoices)
    mainLayout.addLayout(triggerKeyLayout)

    window.setLayout(mainLayout)
    window.show()

    def switchDesktop(desktop):
        if pressFirstCheck.isChecked():
            auto.press(config.fullConfig['pressFirstAvail']
                       [pressFirstChoices.currentIndex()])
        auto.hotkey(*config.fullConfig['desktopSwitchCommands'][desktop])

    def handleKbd(event):
        if event.Key == config.fullConfig['triggerKeysAvail'][triggerKeyChoices.currentIndex()]:
            time.sleep(0.5)
            switchDesktop(desktopChoices.currentIndex())

    hm = ph.HookManager()
    hm.KeyDown = handleKbd
    hm.HookKeyboard()
    hm.start()

    app.exec_()  # Start running the GUI
    hm.cancel()  # When the GUI exits, stop the keyboard listener


main()
