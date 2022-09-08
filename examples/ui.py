from panik_core import *


game = Game()
event = Events()
window = Window("Panik - Core", 1920, 1080, r"assets\panik\logolowres.png")
window.setResizable()
keys = Keys()
ui = UI()
mouse = Mouse()

# ---------------- Assets ---------------- #
text = UIText('H, G, J, K, N, M', ui, 50, 50, 500, 300)
button = UIButton("Test", ui, 50, 400)
entry = UITextEntry("yoyo", ui, 175, 400)
dropdown = UIDropDownMenu(["1", "2"], "1", ui, 50, 500)
cred = UICredEntry("yoyo", ui, 175, 500)
slider = UIHorizontalSlider(ui, 175, 550, 200, 25, 0, (-100, 100))
label = UILabel("Single selection list --------- Multiple selection list", ui, 50, 575, 460)
list = UISelectionList(["background", "player"], ui, 50, 650)
check = UICheckList(["background", "player"], ui, 300, 650)
confdialog = UIConfirmationDialog("Confirm", "are you sure?", ui, 400, 375, priority=False)

def main():
    run = 1

    while run:
        dt = window.tick(30)

        events = event.get()
        for thing in events:
            if thing.type == event.QUIT:
                run = 0
            elif thing.type == event.KEY_PRESSED:
                if thing.key == keys.kH:
                    entry.hide()
                if thing.key == keys.kG:
                    entry.show()
                if thing.key == keys.kJ:
                    entry.disable()
                if thing.key == keys.kK:
                    entry.enable()
                if thing.key == keys.kN:
                    print(list.selection)
                if thing.key == keys.kM:
                    print(check.selection)
            if thing.type == event.BUTTON_CLICKED:
                if thing.ui_element == button.button:
                    print("Pressed")
            elif thing.type == event.TEXT_BOX_LINK_CLICKED:
                print(thing.link_target)
            elif thing.type == event.TEXT_ENTRY_FINISHED:
                if thing.ui_element == entry.textentry:
                    print(thing.text)
            elif thing.type == event.DROP_DOWN_MENU_CHANGED:
                if thing.ui_element == dropdown.dropdownmenu:
                    print(thing.text)
            elif thing.type == event.HORIZONTAL_SLIDER_MOVED:
                if thing.ui_element == slider.slider:
                    print(thing.value)
            elif thing.type == event.SELECTION_LIST_NEW_SELECTION:
                if thing.ui_element == list.selectionlist:
                    print("clicked", thing.text)
            elif thing.type == event.SELECTION_LIST_REMOVE_SELECTION:
                if thing.ui_element == list.selectionlist:
                    print("removed", thing.text)
            elif thing.type == event.SELECTION_LIST_DOUBLE_SELECT:
                if thing.ui_element == list.selectionlist:
                    print("double clicked", thing.text)
            elif thing.type == event.SELECTION_LIST_NEW_SELECTION:
                if thing.ui_element == list.selectionlist:
                    print("clicked", thing.text)
            elif thing.type == event.SELECTION_LIST_REMOVE_SELECTION:
                if thing.ui_element == list.selectionlist:
                    print("removed", thing.text)
            elif thing.type == event.DIALOG_CONFIRMED:
                if thing.ui_element == confdialog.confirmdialog:
                    print("Confirmed")
            ui.process_events(thing)

        window.blit([])
        window.update(ui, [entry, cred])

main()