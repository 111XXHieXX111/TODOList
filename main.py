from flet import *
import time, pickle, os

Todos = []
path = "TODOSaves.data"

def TODOCreate(text, tasklist:ListView, page:Page):
    def destroy(e):
        btn.disabled = True
        container.opacity = 0
        page.update()
        time.sleep(0.4)
        tasklist.controls.remove(container)
        global Todos
        if text in Todos:
            Todos.remove(text)
        page.update()
        save()

    def Hovered(e):
        e.control.scale = 1.07 if e.data == "true" else 1.0
        page.update()

    btn = ElevatedButton("Destroy", on_click=destroy, on_hover=Hovered, animate_scale=Animation(300, "easeInOut"))

    container = Container(
        Row([
            Text(text, expand=True, font_family="mono"),
            btn
        ], expand=True, alignment=alignment.center),
        width=210,
        height=50,
        border_radius=15,
        expand=True,
        padding=5,
        animate_opacity=Animation(300, "easeOut"),
        bgcolor=Colors.GREY_900
    )

    return container

def AddToTodos(obj, tasklist, page):
    global Todos
    if obj.strip() and obj not in Todos:
        Todos.append(obj)
        tasklist.controls.append(TODOCreate(obj, tasklist, page))
        page.update()

def save():
    with open(path, "wb") as f:
        pickle.dump(Todos, f)

def load(tasklist, page):
    global Todos
    if os.path.exists(path):
        with open(path, "rb") as f:
            Todos = pickle.load(f)
            for todo in Todos:
                tasklist.controls.append(TODOCreate(todo, tasklist, page))

def main(pg:Page):
    pg.title = "TODOList"
    pg.theme = Theme(font_family="mono")
    pg.fonts = {
        "Mono": "JetBrainsMono-Bold.ttf"
    }

    def add_task(e):
        AddToTodos(Name.value, tasklist, pg)
        Name.value = ""
        pg.update()
        save()

    tasklist = ListView(
        expand=True,
        spacing=10,
        padding=20,
        first_item_prototype=True
    )

    try:
        load(tasklist, pg)
    except Exception: pass

    Name = TextField(hint_text="Name", expand=True, border_radius=15, border_color=Colors.GREY_800, height=50)

    maincont = Container(
        Column([
            Row([
                Name,
                ElevatedButton("Create", width=210, height=50, color=Colors.WHITE, on_click=add_task)
            ]),
            tasklist
        ])
    )
    
    pg.add(ListView([maincont]))

if __name__ == "__main__":
    app(main)
