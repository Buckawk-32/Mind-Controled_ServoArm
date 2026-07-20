from enum import Enum
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input

CLIENT_ID : int
CLIENT_NAME : str



class ClientHomeScreen(Screen):
    TITLE = "Home Screen"
    SUB_TITLE = "Identification"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(type="integer", placeholder="Please Type Client ID > ")
        yield Input(type="text", placeholder="Please Type Client Name > ")
        yield Footer()

    def handle_submit(self, event: Input.Submitted) -> None:
        





class ClientUIManager(App):
    SCREENS = {"homeScreen" : lambda: ClientHomeScreen(), }


    def on_mount(self) -> None:
        self.push_screen(ClientHomeScreen())
    

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to Client Chatbot!")
        yield Footer()




    






if __name__ == "__main__":





