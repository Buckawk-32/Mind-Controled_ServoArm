import threading
import time

import blessed


class UI:
    def __init__(self, term: blessed.Terminal):
        self.term = term

        self.UIThread : threading.Thread
        self.isUIRunning = False

        self.TOP_TEXT = self.term.height - (self.term.height - 1) 
        self.CENTER_TEXT = self.term.height // 2
        self.BOTTOM_TEXT = self.term.height - 1

        # [0] how far right / [1] how far down 
        self.PANE_MARGINS = [self.term.width - (self.term.width - 20), self.term.height - 10, self.term.width - 30]

        self.CLIENT_INFO_TEXT_LOCATION = [1, 1]
        self.INPUT_TEXT_LOCATION = [1, self.PANE_MARGINS[1] + 1]
        self.OUTPUT_MESSAGE_LOCATION = [self.PANE_MARGINS[0] + 2, 1]
        self.DEV_CONSOLE_LOCATION = [self.PANE_MARGINS[2] + 2, 1]
        self.QUIT_TEXT_LOCATION = [self.term.width // 2, self.term.height // 2]

        self.CLIENT_NAME : str
        self.CLIENT_ID : int


        self.startThread()
        
    def __del__(self):
        if not self.isUIRunning:
            self.stop()

    def echo(self, s):
        print(s, end="", flush=True) 
        
    def setupUI(self):
        print(self.term.home + self.term.clear)
        print(self.term.set_window_title("TCP Client UI")) 


    def publishInputMessage(self, s: str):
        with self.term.location(self.OUTPUT_MESSAGE_LOCATION[0], self.OUTPUT_MESSAGE_LOCATION[1]):
            self.echo(f"{self.CLIENT_NAME}: " + self.term.green(s))
            
        self.OUTPUT_MESSAGE_LOCATION[1] += 1

    


    def startThread(self):
        self.setupUI()

        self.UIThread = threading.Thread(self.updateLoop())
        self.UIThread.start()
        self.isUIRunning = True

    def updateLoop(self):
        with self.term.fullscreen(), self.term.cbreak():
            self.writeToDevConsole("Starting Client TUI...")
            self.drawMargins()
            self.writeClientInfo()
            self.inputLoop()


    def drawMargins(self):
        #  INFO: Draws Borders
        for y in range(1, self.PANE_MARGINS[1]):
            with self.term.location(self.PANE_MARGINS[0], y):
                self.echo("|")

        for x in range(1, self.term.width):
            with self.term.location(x, self.PANE_MARGINS[1]):
                self.echo("-")

        for y in range(1, self.PANE_MARGINS[1]):
            with self.term.location(self.PANE_MARGINS[2], y):
                self.echo("|")
            
        self.writeToDevConsole("Drawn Margins...")


        #  INFO: Marks Text Locations
        with self.term.location(self.CLIENT_INFO_TEXT_LOCATION[0], self.CLIENT_INFO_TEXT_LOCATION[1]):
            self.echo("x")

        with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
            self.echo("x")
                
        with self.term.location(self.OUTPUT_MESSAGE_LOCATION[0], self.OUTPUT_MESSAGE_LOCATION[1]):
            self.echo("x")

        with self.term.location(self.DEV_CONSOLE_LOCATION[0], self.DEV_CONSOLE_LOCATION[1]):
            self.echo("x")

        self.writeToDevConsole("Marked Text Locations...")

    def drawQuitScreen(self):
        print(self.term.home + self.term.clear)

        print(self.term.move_y(self.CENTER_TEXT - 1) + self.term.center("TCP APPLICATION QUIT."))  # ty: ignore[invalid-argument-type]
        print(self.term.move_y(self.CENTER_TEXT) + self.term.center("PRESS ANY KEY TO LEAVE."))  # ty: ignore[invalid-argument-type]

        self.term.inkey()


    def inputLoop(self):
        while True:
            with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
                self.echo(" > ")
                msg = self.handleStrInput()
                if msg == "quit":
                    self.writeToDevConsole("Quitting Application...")
                    time.sleep(0.5)
                    self.drawQuitScreen()
                    break
                self.publishInputMessage(msg)

            with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
                self.echo(self.term.move_x(0) + self.term.clear_eol)  # ty: ignore[invalid-argument-type]
                


    def writeClientInfo(self):
        with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
            self.echo("Client Name? > ")
            name = self.handleStrInput()

            with self.term.location(self.CLIENT_INFO_TEXT_LOCATION[0], self.CLIENT_INFO_TEXT_LOCATION[1]):
                self.echo("Name: " + name)
            
            self.CLIENT_INFO_TEXT_LOCATION[1] += 1
            self.CLIENT_NAME = str(name)


        with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
            self.echo(self.term.move_x(0) + self.term.clear_eol)  # ty: ignore[invalid-argument-type]


        with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
            self.echo("Client ID? > ")
            id = self.handleIntInput()        

            with self.term.location(self.CLIENT_INFO_TEXT_LOCATION[0], self.CLIENT_INFO_TEXT_LOCATION[1]):
                self.echo("ID: " + id)

            self.CLIENT_INFO_TEXT_LOCATION[1] =+ 1
            self.CLIENT_ID = int(id)

        with self.term.location(self.INPUT_TEXT_LOCATION[0], self.INPUT_TEXT_LOCATION[1]):
            self.echo(self.term.move_x(0) + self.term.clear_eol)  # ty: ignore[invalid-argument-type]

        self.writeToDevConsole("Written Client Info...")


        
    def handleStrInput(self):
        text = ""
        while True:
            keyInput = self.term.inkey()
            if keyInput.is_sequence:
                if keyInput.name == "KEY_ENTER":
                    break
                elif keyInput.name == "KEY_ESCAPE":
                    text = ""
                    break
                elif keyInput.name == "KEY_BACKSPACE" or keyInput.name == "KEY_DELETE":  # noqa: SIM102
                    if len(text) > 0:
                        text = text[:-1]
                        self.echo("\b \b")

            elif keyInput.lower() == "q":
                return "quit"

            else:
                text += keyInput
                self.echo(keyInput)

        return text

    def handleIntInput(self):
        keyInput = ""
        num = ""
        while keyInput.lower() != "q":
            keyInput = self.term.inkey()
            if keyInput.is_sequence:
                if keyInput.name == "KEY_ENTER":
                    break
                elif keyInput.name == "KEY_ESCAPE":
                    num = ""
                    break
                elif keyInput.name == "KEY_BACKSPACE" or keyInput.name == "KEY_DELETE":  # noqa: SIM102
                    if len(num) > 0:
                        num = num[:-1]
                        self.echo("\b \b")

            else:
                num = keyInput
                self.echo(keyInput)

        return num


    def writeToDevConsole(self, s):
        with self.term.location(self.DEV_CONSOLE_LOCATION[0], self.DEV_CONSOLE_LOCATION[1]):
            self.echo(s)

        self.DEV_CONSOLE_LOCATION[1] += 1


    def stop(self):
        print(self.term.home + self.term.clear)
        
        if self.isUIRunning:
            self.UIThread.join()
            self.isUIRunning = False




if __name__ == "__main__":
    term = blessed.Terminal()
    ui = UI(term) 
