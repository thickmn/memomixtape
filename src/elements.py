from nicegui.elements.spinner import SpinnerTypes
from nicegui.tailwind_types.height import Height  
from nicegui.tailwind_types.width import Width  
from nicegui import ui


class Spinner(ui.spinner):
    def __init__(
        self,
        type: SpinnerTypes | None = "bars",
        *,
        size: str = "lg",
        color: str | None = "primary",
        thickness: float = 5,
        master: ui.spinner | None = None,
    ) -> None:
        super().__init__(type, size=size, color=color, thickness=thickness)
        self.visible = False
        if master is not None:
            self.bind_visibility_from(master, "visible")


class Body(ui.column):
    def __init__(self, height: Height = "[480px]", width: Width = "[240px]") -> None:
        super().__init__()
        self.tailwind.align_items("center").justify_content("between")
        self.tailwind.height(height).width(width)


class Column(ui.column):
    def __init__(self) -> None:
        super().__init__()
        self.tailwind.width("full").align_items("center")


class Row(ui.row):
    def __init__(self) -> None:
        super().__init__()
        self.tailwind.width("full").align_items("center").justify_content("center")