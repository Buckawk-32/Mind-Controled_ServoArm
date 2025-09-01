import keyboard

def test(callback):
    print(callback.name)

keyboard.hook(test)
keyboard.wait()