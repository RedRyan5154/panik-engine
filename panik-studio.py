import panik_core
import json
import sys
import os

Window = panik_core.Window(
    "Panik - Studio -- V0.0.0", 1080, 720, r"assets/logolowres.png"
)
Window.bg = (50, 50, 60)
Window.showfps = True

# ------ Vartiables ------ #
projects = {}
assets = []
elements = {}
gui_tab = 1
project_path = ""

# ------ UI ------ #
SUI = panik_core.UI()
SUI.set_size(1080, 720)
UI = panik_core.UI()

# ------ Start screen elements ------ #
panel = panik_core.UIPanel(SUI, 1080 / 2 - 350, 720 / 2 - 350, 700, 700)
# logopanel = panik_core.UIPanel(SUI, 1080 / 2 - 80, 720 / 2 - 405, 160, 160)
logo = panik_core.UIImage(
    r"assets/logo.png", SUI, 1080 / 2 - 50, 720 / 2 - 300, 100, 100
)

projects_container = panik_core.UIContainer(
    SUI, 1080 / 2 - 300, 720 / 2 - 100, 630, 400
)


class Project_Panel:
    def __init__(self, name, path, thmbnl, y):
        y += 10
        self.panel = panik_core.UIButton(
            "", SUI, 0, y, 600, 100, projects_container.element
        )
        self.panel.element.oid = "proj"
        self.panel.element.oname = [path, name]

        self.icon = panik_core.UIImage(
            thmbnl,
            SUI,
            5,
            5 + y,
            90,
            90,
            projects_container.element,
        )

        self.text = panik_core.UIText(
            f"""<font color=#ab72ed size=4.5><b>{name}</b></font>
<br><br><font size=2.5>{path}</font>
""",
            SUI,
            100,
            2.5 + y,
            497.5,
            95,
            projects_container.element,
        )


def refresh_projects():
    json_projects = open("recent.json", "r").read()
    try:
        json_projects = json.loads(json_projects)
        projects_container.element.set_scrollable_area_dimensions(
            (
                600,
                (len(json_projects["Projects"]) * 100)
                + (5 * (len(json_projects["Projects"]) + 1)),
            )
        )
        for idx, p in enumerate(json_projects["Projects"]):
            projects[p] = Project_Panel(
                p,
                json_projects["Projects"][p]["path"],
                json_projects["Projects"][p]["icon"],
                idx * 100,
            )
    except:
        pass


_import = panik_core.UIButton("Import", SUI, 530, 180, 100, 50, panel.element)
_import.element.oid = "imp"

new = panik_core.UIButton("New", SUI, 430, 180, 100, 50, panel.element)
new.element.oid = "new"

# ------ Buttons ------ #
_gui_tab_button_el = panik_core.UIButton("Elements", UI, 14, 14, 80, 40)
_gui_tab_button_ma = panik_core.UIButton("Map", UI, 94, 14, 80, 40)
_gui_tab_button_ph = panik_core.UIButton("Physics", UI, 174, 14, 80, 40)
# ------ Containers ------ #
# 1
_proppanel = panik_core.UIWindow("Properties", UI, 0, 0, resizable=True)
_proppanel.element.close_window_button.kill()
_proppanel.element.title_bar.set_dimensions((265, 30))
_elempanel = panik_core.UIWindow("Elements", UI, 0, 0, resizable=True)
_elempanel.element.close_window_button.kill()
_elempanel.element.title_bar.set_dimensions((265, 30))
_elempanellist = panik_core.UISelectionList(
    elements,
    None,
    UI,
    0,
    30,
    container=_elempanel.element,
)
_elempanellist_add = panik_core.UIButton("+", UI, 0, 2, 40, 30, _elempanel.element)
# 2
_tilepanel = panik_core.UIWindow("Tiles", UI, 0, 0, resizable=True)
_tilepanel.element.close_window_button.kill()
_tilepanel.element.title_bar.set_dimensions((265, 30))
_tilepanel.hide()
_mapsetpanel = panik_core.UIWindow("Settings", UI, 0, 0, resizable=True)
_mapsetpanel.element.close_window_button.kill()
_mapsetpanel.element.title_bar.set_dimensions((265, 30))
_mapsetpanel.hide()
# 3
_propppanel = panik_core.UIWindow("Physics Properties", UI, 0, 0, resizable=True)
_propppanel.element.close_window_button.kill()
_propppanel.element.title_bar.set_dimensions((265, 30))
_propppanel.hide()
# . . .
_viewport = panik_core.UIWindow("Viewport", UI, 0, 0, resizable=True)
_viewport.element.close_window_button.kill()
_viewport.element.title_bar.set_dimensions((600, 30))
_assets = panik_core.UIWindow("Assets", UI, 0, 0, resizable=True)
_assets.element.close_window_button.kill()
_assets.element.title_bar.set_dimensions((600, 30))
_codepanel = panik_core.UIWindow("Code", UI, 0, 0, resizable=True)
_codepanel.element.close_window_button.kill()
_codepanel.element.title_bar.set_dimensions((600, 30))

# ------ Dynamicly position elements ------ #
def position(element, sx, sy, px, py):
    element.element.set_dimensions((sx, sy))
    element.element.set_position((px, py))


def doPositioning():
    global viewport_manager
    sx, sy = Window.winsize
    UI.set_size(sx, sy)
    if gui_tab == 1:
        _tilepanel.hide()
        _mapsetpanel.hide()
        _propppanel.hide()
        _proppanel.show()
        _elempanel.show()
        position(_proppanel, min(max(sx / 6.5, 295), 330), sy / 2 - 50, 0, 0 + 40)
        position(_elempanel, min(max(sx / 6.5, 295), 330), sy / 2, 0, sy - sy / 2)
        _elempanellist.element.set_dimensions(
            (min(max(sx / 6.5, 295), 330) - 32, (sy / 2 - 59) - 30)
        )
    elif gui_tab == 2:
        _proppanel.hide()
        _elempanel.hide()
        _propppanel.hide()
        _tilepanel.show()
        _mapsetpanel.show()
        position(_tilepanel, min(max(sx / 6.5, 295), 330), sy / 2 - 50, 0, 0 + 40)
        position(_mapsetpanel, min(max(sx / 6.5, 295), 330), sy / 2, 0, sy - sy / 2)
    elif gui_tab == 3:
        _propppanel.show()
        _proppanel.hide()
        _elempanel.show()
        _tilepanel.hide()
        _mapsetpanel.hide()
        position(_propppanel, min(max(sx / 6.5, 295), 330), sy / 2 - 50, 0, 0 + 40)
        position(_elempanel, min(max(sx / 6.5, 295), 330), sy / 2, 0, sy - sy / 2)
        _elempanellist.element.set_dimensions(
            (min(max(sx / 6.5, 295), 330) - 32, (sy / 2 - 59) - 30)
        )
    position(
        _viewport,
        sx - min(max(sx / 6.5, 295), 330) - sx / 3.5,
        sy / 10 * 7.5,
        min(max(sx / 6.5, 295), 330),
        0,
    )
    position(
        _assets,
        sx - min(max(sx / 6.5, 295), 330) - sx / 3.5,
        sy / 10 * 2.5,
        min(max(sx / 6.5, 295), 330),
        _viewport.element.rect.h,
    )
    position(_codepanel, sx / 3.5, sy, sx - sx / 3.5, 0)

    # bg.x, bg.y = sx / 2, sy / 2


aspect_ratio = panik_core.Rect("Aspect Ratio", 0, 0, 100, 100, (0, 0, 0), 4)
aspect_ratio.showcolision = True
label = panik_core.Text("Aspect Ratio", "16:9")


def doViewPort():
    prev_pos = _viewport.element.rect
    viewport_manager.width = _viewport.element.rect.w - 50
    viewport_manager.height = _viewport.element.rect.h - 70
    viewport_manager.x = _viewport.element.rect.x + _viewport.element.rect.w / 2
    viewport_manager.y = _viewport.element.rect.y + 13 + _viewport.element.rect.h / 2
    viewport_manager.updateSize()

    vpx, vpy = viewport_manager.width, viewport_manager.height
    width = vpx - 150

    _aspect = 9 / 16

    aspect_ratio.w = width
    aspect_ratio.h = _aspect * width

    aspect_ratio.x, aspect_ratio.y = (
        viewport_manager.width / 2,
        viewport_manager.height / 2,
    )
    # print(vpx, vpy)

    viewport_manager.blit([aspect_ratio, label])
    viewport_manager.update()


def main():
    global gui_tab, viewport_manager
    run = 1
    srun = 1
    wincount = 0
    brcount = 0
    elements = []
    ren_text_2d = """<p>2D rendering using PyGame</p>
<br><p>Has post procesing and hardware acceleration and UI</p>
<br><p>Optimal for: 2D projects</p>"""
    ren_text_3d = """<p>3D rendering with OpenGL and PyGame window</p>
<br><p>Has shaders, post-procesing and hardware acceleration</p><p>3D rendering with shaders, lighting and colision</p>
<br><p>Optimal for: For complex 2D or 3D projects</p><p>(Still under Development!)</p>"""
    refresh_projects()
    while srun:
        Window.tick(30)
        events = panik_core.Events.get()

        for event in events:
            if event.type == panik_core.QUIT:
                srun = 0
                run = 0
                sys.exit()
            if event.type == panik_core.BUTTON_DOUBLE_CLICKED:
                if hasattr(event.ui_element, "oid"):
                    if event.ui_element.oid == "proj":
                        project_path = event.ui_element.oname[0]
                        project_name = event.ui_element.oname[1]
                        tmp_json = open("recent.json", "r").read()
                        tmp_json = json.loads(tmp_json)
                        proj = {
                            project_name: {
                                "path": project_path,
                                "icon": r"/home/red/Desktop/games/assets/logo.png",
                            }
                        }
                        tmp_json["Projects"].pop(project_name)
                        tmp_json["Projects"] = {**proj, **tmp_json["Projects"]}
                        with open("recent.json", "w") as f:
                            json.dump(tmp_json, f)
                        srun = 0
            if event.type == panik_core.BUTTON_CLICKED:
                if hasattr(event.ui_element, "oid"):
                    if event.ui_element.oid == "bro" and brcount < 1:
                        fb = panik_core.UIFileDialog(
                            "Choose project path",
                            "",
                            SUI,
                            1080 / 2 - 300,
                            720 / 2 - 200,
                            600,
                            400,
                            False,
                            True,
                        )
                        brcount += 1
            if event.type == panik_core.BUTTON_CLICKED:
                if hasattr(event.ui_element, "oid"):
                    if event.ui_element.oid == "sub":
                        try:
                            project_path = path_input.element.get_text()
                            project_name = name_input.element.get_text()
                            default_logo = open(
                                r"/home/red/Desktop/games/assets/logo.png",
                                "rb",
                            ).read()
                            os.mkdir(project_path + "/" + project_name)
                            open(
                                project_path + "/" + project_name + "/icon.png", "wb"
                            ).write(default_logo)
                            tmp_json = open("recent.json", "r").read()
                            tmp_json = json.loads(tmp_json)
                            proj = {
                                project_name: {
                                    "path": project_path,
                                    "icon": r"/home/red/Desktop/games/assets/logo.png",
                                }
                            }
                            tmp_json["Projects"] = {**proj, **tmp_json["Projects"]}
                            with open("recent.json", "w") as f:
                                json.dump(tmp_json, f)
                            srun = 0
                        except:
                            window_new.close()
                            noti = panik_core.UIConfirmationDialog(
                                "Error",
                                "This projects already exists",
                                SUI,
                                1080 / 2 - 130,
                                720 / 2 - 125,
                            )
                            noti.element.cancel_button.kill()
            if event.type == panik_core.BUTTON_CLICKED:
                if hasattr(event.ui_element, "oid"):
                    if event.ui_element.oid == "new" and wincount < 1:
                        wincount += 1
                        window_new = panik_core.UIWindow(
                            "New Project",
                            SUI,
                            1080 / 2 - 400,
                            720 / 2 - 350,
                            800,
                            700,
                        )
                        name_label = panik_core.UILabel(
                            "Project name:               ",
                            SUI,
                            5,
                            30,
                            300,
                            50,
                            window_new.element,
                        )
                        name_input = panik_core.UITextEntry(
                            "My-Game", SUI, 300, 30, 300, 50, window_new.element
                        )
                        name_input.element.set_forbidden_characters(
                            [" ", "/", "<", ">", ":", '"', "\\", "|", "?", "*"]
                        )
                        path_label = panik_core.UILabel(
                            "Project path:               ",
                            SUI,
                            5,
                            130,
                            300,
                            50,
                            window_new.element,
                        )
                        path_input = panik_core.UITextEntry(
                            "", SUI, 300, 130, 300, 50, window_new.element
                        )
                        path_button = panik_core.UIButton(
                            "Browse", SUI, 620, 130, 75, 50, window_new.element
                        )
                        path_button.element.oid = "bro"
                        submit = panik_core.UIButton(
                            "Create", SUI, 650, 550, 75, 50, window_new.element
                        )
                        submit.element.oid = "sub"
                        submit.disable()
                        renderer = panik_core.UISelectionList(
                            ["2D (PyGame)", "3D (OpenGL)"],
                            "2D (PyGame)",
                            SUI,
                            40,
                            230,
                            200,
                            86,
                            window_new.element,
                        )
                        renderer_text = panik_core.UIText(
                            ren_text_2d, SUI, 250, 230, 450, 250, window_new.element
                        )
                        elements.append(name_input)
                        elements.append(path_input)
            if event.type == panik_core.WINDOW_CLOSED:
                if event.ui_element == window_new.element:
                    try:
                        fb.element.kill()
                    except:
                        pass
                    wincount += -1
                else:
                    brcount += -1
            if event.type == panik_core.PATH_SELECTED:
                path_input.element.set_text(event.text)
            try:
                if (
                    name_input.element.get_text() != ""
                    and path_input.element.get_text() != ""
                    and renderer.selection == "2D (PyGame)"
                ):
                    submit.enable()
                else:
                    submit.disable()
            except:
                pass
            if event.type == panik_core.SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == renderer.element:
                    if event.text == "2D (PyGame)":
                        renderer_text.element.set_text(ren_text_2d)
                    elif event.text == "3D (OpenGL)":
                        renderer_text.element.set_text(ren_text_3d)
            SUI.process_events(event)

        Window.update(SUI, ui=elements)

    # set dynamic element positioning
    Window.setTitle(f"Panik - Studio -- ({project_name})")
    Window.setResizable()
    full = False

    viewport_manager = panik_core.Subwindow(1080 / 2, 720 / 2, 100, 100)
    viewport_manager.bg = (255, 255, 255)

    doPositioning()

    while run:
        Window.tick(100)

        events = panik_core.Events.get()

        for event in events:
            if event.type == panik_core.QUIT:
                run = 0
            if event.type == panik_core.KEY_PRESSED:
                if event.key == panik_core.kQ:
                    run = 0
                elif event.key == panik_core.kK:
                    Window.devmode = not Window.devmode
            if event.type == panik_core.SCREENRESIZE:
                doPositioning()
            if event.type == panik_core.BUTTON_CLICKED:
                if event.ui_element == _elempanellist_add.element:
                    print("done")
                    wincount += 1
                    window_new = panik_core.UIWindow(
                        "New Project",
                        UI,
                        1080 / 2 - 400,
                        720 / 2 - 350,
                        800,
                        700,
                    )
                    name_label = panik_core.UILabel(
                        "Project name:               ",
                        UI,
                        5,
                        30,
                        300,
                        50,
                        window_new.element,
                    )
                    name_input = panik_core.UITextEntry(
                        "My-Game", UI, 300, 30, 300, 50, window_new.element
                    )
                    name_input.element.set_forbidden_characters(
                        [" ", "/", "<", ">", ":", '"', "\\", "|", "?", "*"]
                    )
                    path_label = panik_core.UILabel(
                        "Project path:               ",
                        UI,
                        5,
                        130,
                        300,
                        50,
                        window_new.element,
                    )
                    path_input = panik_core.UITextEntry(
                        "", UI, 300, 130, 300, 50, window_new.element
                    )
                    path_button = panik_core.UIButton(
                        "Browse", UI, 620, 130, 75, 50, window_new.element
                    )
                    path_button.element.oid = "bro"
                    submit = panik_core.UIButton(
                        "Create", UI, 650, 550, 75, 50, window_new.element
                    )
                    submit.element.oid = "sub"
                    submit.disable()
                    renderer = panik_core.UISelectionList(
                        ["2D (PyGame)", "3D (OpenGL)"],
                        "2D (PyGame)",
                        UI,
                        40,
                        230,
                        200,
                        86,
                        window_new.element,
                    )
                    renderer_text = panik_core.UIText(
                        ren_text_2d, UI, 250, 230, 450, 250, window_new.element
                    )
                    elements.append(name_input)
                    elements.append(path_input)
            if event.type == panik_core.BUTTON_CLICKED:
                if event.ui_element == _gui_tab_button_el.element:
                    _viewport.element.set_display_title("Elements")
                    gui_tab = 1
                    doPositioning()
                elif event.ui_element == _gui_tab_button_ma.element:
                    _viewport.element.set_display_title("Map")
                    gui_tab = 2
                    doPositioning()
                elif event.ui_element == _gui_tab_button_ph.element:
                    _viewport.element.set_display_title("Physics")
                    gui_tab = 3
                    doPositioning()
            UI.process_events(event)

        # viewport

        doViewPort()

        Window.blit([])
        _viewport.element.drawable_shape.base_surface.blit(viewport_manager.WIN, (0, 0))
        Window.update(UI)


if __name__ == "__main__":
    main()
