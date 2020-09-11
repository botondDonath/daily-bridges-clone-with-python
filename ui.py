from view import Display


class UI:
    INDENT = "\t"
    GAME_TITLE = "DAILY BRIDGES"
    MAIN_MENU_OPTIONS = {"p": "Play", "q": "Quit"}
    INGAME_OPTIONS = {"c": "Cancel", "q": "Quit"}
    STEP_OPTIONS = {"c": "Connect", "d": "Disconnect", "u": "Undo",
                    "e": "Exit current game", "q": "Quit"}
    POS_PROMPT_TEMPLATE = "Position ([A-%c][1-%d]): "

    def new_game(self, display: Display):
        self.display = display
        last_letter = Display.ALPHABET[self.grid_size - 1]
        self.pos_prompt = UI.POS_PROMPT_TEMPLATE.format(last_letter, display.grid.size)

    def show(self, menu, show_grid=True, error=None):
        '''Clears screen,
        then prints game title,
        then shows grid int its current state if the 'show_grid' flag is set to true,
        then prints menu,
        then if there was an erroneous input, prints the error message.'''

        self.display.clear()
        self.out(self.game_title(), end="\n")
        if show_grid:
            self.display.show_grid()
        if isinstance(menu, dict):
            menu = self.menu(menu)
        self.out(menu, before="\n", end="\n")
        if error is not None:
            self.out(error, before="\n")

    def out(self, output, before="", end=""):
        print(before + output, end=end)

    def game_title(self):
        words = UI.GAME_TITLE.split(" ")
        return "  ".join(map(lambda w: " ".join(w.split("")), words))

    def menu(self, options: dict):
        return "\nOptions:\n" + "\n".join(
            f"{UI.INDENT}{letter}) {option}"
            for letter, option in options.items()
        )

    def get_input(self, prompt: str = None, converter=lambda x: x):
        inp = input(self.pos_prompt if prompt is None else prompt)
        return converter(inp)
