import tkinter
import threading

import openai

import Main


def test01():
    for i in range(60):
        messagesText.insert(tkinter.END, "TEST"+'\n', "USER")


def chat_to_ai():
    submitButton.config(state=tkinter.DISABLED)
    ans = "API调用失败"
    ipt = inputEntry.get()
    inputEntry.delete(0, tkinter.END)
    #UserMessagesLabel = tkinter.Label(cv, text="User:" + ipt, background="#87CEFA")
    #UserMessagesLabel.pack(anchor="nw")
    messagesText.config(state=tkinter.NORMAL)
    messagesText.insert(tkinter.END, "USER:" + ipt + '\n', "USER")
    messagesText.config(state=tkinter.DISABLED)
    flag = True
    cnt=0
    while flag:
        cnt += 1
        if cnt >= 100:
            submitButton.config(state=tkinter.NORMAL)
            return
        flag = False
        try:
            ans = Main.chat(ipt)
            #AIMessageLabel = tkinter.Label(cv, text="AI:" + ans, background="#E1FFFF")
            #AIMessageLabel.pack(anchor="nw")
            messagesText.config(state=tkinter.NORMAL)
            messagesText.insert(tkinter.END, "AI:" + ans + '\n', "AI")
            messagesText.config(state=tkinter.DISABLED)
        except openai.RateLimitError:
            flag = True
    submitButton.config(state=tkinter.NORMAL)


def start_thread():
    listenMessage = threading.Thread(target=chat_to_ai)
    listenMessage.start()


if __name__ == '__main__':
    root = tkinter.Tk()


    root.title("化学海龟汤")
    root.geometry("800x600")
    root["background"] = "#F0F8FF"
    #root.attributes('-topmost', True)


    messagesFrame = tkinter.Frame(root)

    #cv = tkinter.Canvas(root, width=300, height=100, scrollregion=(0, 0, 100, 300))
    messagesText = tkinter.Text(
        messagesFrame,
        width=300,
        height=100,
        padx=20,
        pady=20,
        wrap="char",
        state=tkinter.DISABLED,
    )

    #cvScrollbar = tkinter.Scrollbar(cv, orient="vertical", command=cv.yview)
    messagesScrollbar = tkinter.Scrollbar(messagesText, orient="vertical", command=messagesText.yview)
    #cv.configure(yscrollcommand=cvScrollbar.set)
    messagesText.configure(yscrollcommand=messagesScrollbar.set)

    messagesText.tag_configure("USER", foreground="blue")
    messagesText.tag_configure("AI", foreground="green")

    inputFrame = tkinter.Frame(root, background="#F0F8FF")

    inputEntry = tkinter.Entry(inputFrame, width=100)

    submitButton = tkinter.Button(inputFrame, text='发送', command=start_thread)


    messagesFrame.pack(side="top", fill="both", expand=True)

    #cv.pack(side="top", fill="both", expand=True)
    messagesText.pack(side="top", fill="both", expand=True)

    #cvScrollbar.pack(side='right', fill="y")
    messagesScrollbar.pack(side="right")

    inputEntry.pack(side="bottom")

    submitButton.pack(side="right")

    inputFrame.pack(side="bottom")

    #test01()

    apiFrame = tkinter.Frame(root)
    apiFrame.pack(anchor="se")

    apiKeyFrame = tkinter.Frame(apiFrame)
    apiKeyFrame.pack(side="top")
    apiKeyLabel = tkinter.Label(apiKeyFrame, text="自定义api key（留空为默认）:")
    apiKeyLabel.pack(side="left")
    apiKeyEntry = tkinter.Entry(apiKeyFrame, show="*")
    apiKeyEntry.pack(side="left")

    baseUrlFrame = tkinter.Frame(apiFrame)
    baseUrlFrame.pack(side="top")
    baseUrlLabel = tkinter.Label(baseUrlFrame, text="自定义base url（留空为默认）:")
    baseUrlLabel.pack(side="left")
    baseUrlEntry = tkinter.Entry(baseUrlFrame, show="*")
    baseUrlEntry.pack(side="left")

    aiModelNameFrame = tkinter.Frame(apiFrame)
    aiModelNameFrame.pack(side="top")
    aiModelNameLabel = tkinter.Label(aiModelNameFrame, text="自定义model name（留空为默认）:")
    aiModelNameLabel.pack(side="left")
    aiModelNameEntry = tkinter.Entry(aiModelNameFrame)
    aiModelNameEntry.pack(side="left")
    apiButton = tkinter.Button(apiFrame, text="提交")
    apiButton.pack(side="left", expand=True)

    root.mainloop()