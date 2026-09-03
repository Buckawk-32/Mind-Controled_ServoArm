import threading

import blessed


class UI:
    def __init__(self, term: blessed.Terminal):
        self.term = term

        self.UIThread : threading.Thread
        self.isUIRunning = False

        self.TOP_TEXT = self.term.height - (self.term.height - 1) 
        self.CENTER_TEXT = self.term.height // 2
        self.BOTTOM_TEXT = self.term.height - 1

        self.startThread()
        
    def __del__(self):
        if not self.isUIRunning:
            self.stop()

        
    def setupUI(self):
        print(self.term.home + self.term.clear)
        print(self.term.set_window_title("TCP Client UI")) 


    def sendInputMessage(self):
    


    def startThread(self):
        self.setupUI()

        self.UIThread = threading.Thread(self.inputLoop())
        self.UIThread.start()
        self.isUIRunning = True

    def inputLoop(self):
        print(f"Term height: {self.term.height}")
        print(f"Term Width: {self.term.width}")

        with self.term.fullscreen(), self.term.cbreak():
            print(self.term.move_y(self.TOP_TEXT) + self.term.center("Test Top"))
            print(self.term.move_y(self.CENTER_TEXT) + self.term.center("Test Center"))
            print(self.term.move_y(self.BOTTOM_TEXT) + self.term.center("Test Bottom"))
            self.term.inkey()


    def stop(self):
        print("Killing UI Thread...")
        self.UIThread.join()




if __name__ == "__main__":
    term = blessed.Terminal()
    print("Starting Terminal Application...")
    ui = UI(term) 

