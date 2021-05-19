import random
import time
from functools import reduce
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from tkinter.ttk import Combobox

list_symbol = ['+', '-', '*', '/']
list_equation = []  # 以字符串形式存储单个算式
list_formula = []  # 存储所有算式（不包括结果）
list_answer = []  # 存储对应结果
root = Tk()
tree = ttk.Treeview(root, show='headings')
num = 0
difficulty = 0  # 算式难度系数

show_answer = 1  # 是否在生成算式时显示答案 1 显示 2 不显示


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


def Show_answers():
    global show_answer
    if show_answer != 1:
        show_answer = 1
        delButton(tree)
        get_tree(num)


def Hide_answers():
    global show_answer
    if show_answer == 1:
        show_answer = 2
        delButton(tree)
        get_tree(num)


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
                list_equation.append(get_num())
            else:
                list_equation.append(list_symbol[get_sign()])
        formula = reduce(lambda x, y: str(x) + str(y), list_equation)  # 合并成一个字符串
        answer = eval(formula)
        if answer % 1 == 0 and 0 <= answer <= 300 * difficulty - 200:  # 结果大小小于难度系数*300-200
            i += 1
            list_formula.append(formula)
            list_answer.append(answer)
        list_equation.clear()


def store_data():
    for i in range(num):
        with open("result.txt", "a") as f:
            f.write(list_formula[i] + '=' + str(list_answer[i]) + "\n")
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
            tree.insert('', i, values=(i + 1, list_formula[i], list_answer[i]))
        else:
            tree.insert('', i, values=(i + 1, list_formula[i], "**"))

    tree.place(x=0, y=0, width=450, height=350)
    scroll = Scrollbar()
    scroll.place(x=450, y=0, width=20, height=350)
    scroll.config(command=tree.yview)


def create_top():
    def get_formula_data():
        global difficulty, num, show_answer
        allow_submission = 1
        list_formula.clear()
        list_answer.clear()
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
            showinfo(title="通知", message="难度未进行选择")
            allow_submission = 0

        if b1.get() == '' or int(b1.get()) <= 0:
            showinfo(title="通知", message="输入数量不符合规范")
            allow_submission = 0
        if allow_submission == 1:  # 输入数据符合规范才会提交
            num = int(b1.get())
            show_answer = v.get()
            get_formula(num)
            get_tree(num)
            win1.destroy()

    v = IntVar()
    win1 = Toplevel(root)  # 生成子界面进行插入
    center_window(320, 120, win1)
    Label(win1, text="请选择难度:").grid(row=0, column=0, columnspan=1, sticky=W)
    Label(win1, text="请选择输入题目数量:").grid(row=1, column=0, columnspan=1, sticky=W)
    Label(win1, text="是否显示答案:").grid(row=2, column=0, columnspan=1, sticky=W)
    b1 = StringVar()
    Entry(win1, textvariable=b1).grid(row=1, column=1, columnspan=2)
    number = StringVar()
    numberChosen = Combobox(win1, width=12, textvariable=number)
    numberChosen['values'] = ('简单', '适中', '较难', '困难')
    numberChosen.grid(row=0, column=1, columnspan=1)
    show = ["是", "否"]
    Radiobutton(win1, variable=v, text=show[0], value=1).grid(row=2, column=1, columnspan=1)
    Radiobutton(win1, variable=v, text=show[1], value=2).grid(row=2, column=2, columnspan=1)

    # 要实现单选互斥的效果，
    # variable选项共享一个整型变量，
    # value需要设置不同的值

    Button(win1, text="取消", width=10, command=win1.destroy) \
        .grid(row=3, column=2, sticky=E, padx=10, pady=5)
    Button(win1, text="确定", width=10, command=get_formula_data) \
        .grid(row=3, column=0)
    win1.resizable(0, 0)
    win1.mainloop()


def test():
    def submit():
        pass
    if len(list_answer) == 0:
        showinfo(title="通知", message="无算式生成")
    else:
        v = IntVar()
        win2 = Toplevel(root)
        time_start = time.time()
        Label(win2, text=time_start).grid(row=0, column=0, columnspan=1, sticky=W)
        time_end = time.time()
        print('time cost', time_end - time_start, 's')
        Button(root, text="提交", width=10, command=submit).gird(row=1, column=1)
        Button(root, text="退出", width=10, command=quit_root).gird(row=1, column=0)


        center_window(420, 320, win2)
        win2.mainloop()


def get_interface():
    root.title('四则运算')
    center_window(600, 350, root)
    root.resizable(0, 0)
    Button(root, text="新建", width=10, command=create_top).place(x=500, y=10)
    Button(root, text="保存", width=10, command=store_data).place(x=500, y=160)
    Button(root, text="显示答案", width=10, command=Show_answers).place(x=500, y=60)
    Button(root, text="隐藏答案", width=10, command=Hide_answers).place(x=500, y=110)
    Button(root, text="测试", width=10, command=test).place(x=500, y=210)
    Button(root, text="退出", width=10, command=quit_root).place(x=500, y=300)
    mainloop()


def main():
    get_interface()


if __name__ == '__main__':
    main()
