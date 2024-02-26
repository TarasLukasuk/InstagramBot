from ui import InstagramBotGUI
import tkinter as tk


def main():
    root = tk.Tk()
    root.iconbitmap('create_an_icon_that_shows_sending_messages_to_Instagram_S1278494694_St25_G7.5.ico')
    gui = InstagramBotGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
