import random
from functools import reduce
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from tkinter.ttk import Combobox

list1 = ['+', '-', '*', '/']
list2 = []  # 以字符串形式存储单个算式
list3 = []  # 存储所有算式（不包括结果）
list4 = []  # 存储对应结果
root = Tk()
tree = ttk.Treeview(root, show='headings')
num = 0
difficulty = 0
show_answer = 1


def center_window(w, h, self):  # 使窗口出现在界面中央
    # 获取屏幕 宽、高
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    self.geometry('%dx%d+%d+%d' % (w, h, x, y))


def quit_root():
    if askyesno("提示", "确定要退出？") == 1:
        root.destroy()


def get_sign():
    return random.randint(0, 3)


def get_num():
    return random.randint(1, 100)


def delButton(self):
    x = self.get_children()
    for item in x:
        self.delete(item)


def get_formula(number):
    i = 0
    while i < number:
        symbol = random.randint(2, 5)
        for j in range(2 * symbol + 1):
            if j % 2 == 0:
                list2.append(get_num())
            else:
                list2.append(list1[get_sign()])
        formula = reduce(lambda x, y: str(x) + str(y), list2)
        answer = eval(formula)
        if answer % 1 == 0 and 0 <= answer <= 300 * difficulty - 200:
            i += 1
            list3.append(formula)
            list4.append(answer)
        list2.clear()


def store_data():
    for i in range(num):
        with open("result.txt", "a") as f:
            f.write(list3[i] + '=' + str(list4[i]) + "\n")
    showinfo(title="通知", message="存储成功!")


def get_tree(tree_number):
    tree["columns"] = ('num', 'formula', 'answer')

    tree.column('num', width=60, anchor='center')
    tree.column('formula', width=250, anchor='center')
    tree.column('answer', width=140, anchor='center')

    tree.heading('num', text='序号')
    tree.heading('formula', text='算式')
    tree.heading('answer', text='答案')
    for i in range(tree_number):
        if show_answer == 1:
            tree.insert('', i, values=(i + 1, list3[i], list4[i]))
        else:
            tree.insert('', i, values=(i + 1, list3[i], "**"))

    tree.place(x=0, y=0, width=450, height=350)
    scroll = Scrollbar()
    scroll.place(x=450, y=0, width=20, height=350)
    scroll.config(command=tree.yview)


def create_top():
    def get_formula_data():
        global difficulty, num, show_answer
        list3.clear()
        list4.clear()
        delButton(tree)
        if numberChosen.get() == '简单':
            difficulty = 1
        elif numberChosen.get() == '适中':
            difficulty = 2
        elif numberChosen.get() == '较难':
            difficulty = 3
        elif numberChosen.get() == '困难':
            difficulty = 4
        else:
            showinfo(title="通知", message="不能为空")
        show_answer = v.get()
        num = int(b1.get())
        get_formula(num)
        get_tree(num)
        win.destroy()

    v = IntVar()
    win = Toplevel(root)  # 生成子界面进行插入
    center_window(320, 120, win)
    Label(win, text="请选择难度:").grid(row=0, column=0, columnspan=1, sticky=W)
    Label(win, text="请选择输入题目数量:").grid(row=1, column=0, columnspan=1, sticky=W)
    Label(win, text="是否显示答案:").grid(row=2, column=0, columnspan=1, sticky=W)
    b1 = StringVar()
    Entry(win, textvariable=b1).grid(row=1, column=1, columnspan=2)
    number = StringVar()
    numberChosen = Combobox(win, width=12, textvariable=number)
    numberChosen['values'] = ('简单', '适中', '较难', '困难')
    numberChosen.grid(row=0, column=1, columnspan=1)
    show = ["是", "否"]
    r1 = Radiobutton(win, variable=v, text=show[0], value=1).grid(row=2, column=1, columnspan=1)
    r2 = Radiobutton(win, variable=v, text=show[1], value=2).grid(row=2, column=2, columnspan=1)

    # 要实现单选互斥的效果，
    # variable选项共享一个整型变量，
    # value需要设置不同的值

    Button(win, text="取消", width=10, command=win.destroy) \
        .grid(row=3, column=2, sticky=E, padx=10, pady=5)
    Button(win, text="确定", width=10, command=get_formula_data) \
        .grid(row=3, column=0)
    win.resizable(0, 0)
    win.mainloop()


def get_interface():
    root.title('四则运算')
    center_window(600, 350, root)
    root.resizable(0, 0)
    Button(root, text="新建", width=10, command=create_top).place(x=500, y=10)
    Button(root, text="保存", width=10, command=store_data).place(x=500, y=60)
    Button(root, text="退出", width=10, command=root.destroy).place(x=500, y=300)
    mainloop()


def main():
    get_interface()


if __name__ == '__main__':
    main()
