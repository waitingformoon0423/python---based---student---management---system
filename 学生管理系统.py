# 导入tkinter库，用于创建图形用户界面
import tkinter as tk
# 从tkinter库中导入messagebox模块，用于显示消息框
from tkinter import messagebox
# 从tkinter库中导入ttk模块，用于创建更现代化的小部件
from tkinter import ttk
# 从tkinter库中导入simpledialog模块，用于创建简单的对话框
from tkinter import simpledialog
# 导入sqlite3库，用于操作SQLite数据库
import sqlite3
# 导入os库，用于操作系统相关的功能
import os 
# 导入matplotlib.pyplot库，用于绘制图表
import matplotlib.pyplot as plt

from tkinter import scrolledtext
# 设置matplotlib的字体为中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 导入re库，用于正则表达式操作
import re
# 导入csv库，用于读写CSV文件
import csv
# 实现帮助文档


# 全局变量root，用于存储主窗口对象
root = None
# 全局变量tree，用于存储树状视图对象
tree = None
# 全局变量id_entry，用于存储学号输入框对象
id_entry = None
# 全局变量name_entry，用于存储姓名输入框对象
name_entry = None
# 全局变量age_entry，用于存储年龄输入框对象
age_entry = None
# 全局变量gender_entry，用于存储性别输入框对象
gender_entry = None
# 全局变量class_entry，用于存储班级输入框对象
class_entry = None
# 全局变量major_entry，用于存储专业输入框对象
major_entry = None
# 全局变量name，用于存储当前年级名称（此处赋值为None，后续会被更新）
name= None


"""
@author: BobZhu with MarsCode/Doubao api/DeepSeek
@date: 2024-12-17
@description: 学生管理系统
"""
def initial_student(grade):
    """连接数据库并初始化,并将学生信息插入到数据库中"""
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 执行SQL查询，统计students表中的记录数量
        cursor.execute('''
        SELECT COUNT(*) FROM students
        ''')
        # 获取查询结果的第一行第一列的值，即记录数量
        count = cursor.fetchone()[0]
        # 关闭数据库连接
        conn.close()

        # 如果记录数量大于0，说明学生信息已经初始化过了
        if count > 0:
            # 显示提示信息，告知用户学生信息已经初始化
            messagebox.showinfo("提示", "学生信息已经初始化,您可以点击更新树状视图查看。")
            # 返回空列表，表示初始化操作已完成
            return

        # 如果记录数量为0，说明学生信息尚未初始化，重新连接到数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建游标对象
        cursor = conn.cursor()
        # 执行SQL插入语句，向students表中插入四条学生记录
        cursor.execute('''
        INSERT INTO students (id, name, age, gender, class, major)
        VALUES ('ABC001', '张三', 18, '男', '一班', '计算机科学与技术'),
               ('ABC002', '李四', 19, '女', '二班', '软件工程'),
               ('ABC003', '王五', 20, '男', '三班', '计算机科学与技术'),
               ('ABC004', '赵六', 18, '女', '一班', '软件工程')
        ''')
        # 提交事务，将插入操作保存到数据库
        conn.commit()
        # 关闭数据库连接
        conn.close()
        # 显示提示信息，告知用户学生信息已初始化，并提示更新树状图
        messagebox.showinfo("提示", "已对学生信息进行初始化,请更新树状图")
    except sqlite3.Error as e:
        # 如果发生数据库错误，显示错误信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    except Exception as e:
        # 如果发生其他错误，显示错误信息
        messagebox.showinfo("提示", f"其他错误: {e}")
    # 返回空列表，表示初始化操作已完成
    return []




def show_students(grade): 
    """
    显示指定年级的学生信息到树状视图中。

    参数:
    grade (str): 学生所在的年级。

    返回:
    list: 包含所有学生信息的列表。
    """
    # 清空树状视图中的所有节点
    tree.delete(*tree.get_children()) 
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 执行SQL查询，获取所有学生的信息
        cursor.execute('''
        SELECT * FROM students
        ''')
        # 获取查询结果，返回一个包含所有学生信息的列表
        students = cursor.fetchall()
        # 关闭数据库连接
        conn.close()
        # 遍历学生信息列表，将每个学生的信息插入到树状视图中
        for student in students:
            tree.insert("", tk.END, values=(student[0], student[1], student[2], student[3], student[4], student[5]))
        # 显示提示信息，告知用户树状图已更新
        messagebox.showinfo("提示", "树状图已更新")
    except Exception as e:
        # 如果发生错误，显示错误信息，并提示用户打开帮助文档检查错误原因
        messagebox.showinfo("提示", f"发生错误：{e},请打开帮助文档检查错误原因")
    # 返回包含所有学生信息的列表
    return students

def update_tree(tree, grade):
    """
    更新树状视图中的学生信息。

    参数:
    tree (ttk.Treeview): 树状视图对象。
    grade (str): 学生所在的年级。
    """
    # 清空树状视图中的所有节点
    tree.delete(*tree.get_children())
    # 调用show_students函数，重新加载并显示学生信息
    show_students(grade)

def select_student(tree):
    """
    显示选中学生的详细信息。

    参数:
    tree (ttk.Treeview): 树状视图对象。
    """
    # 获取当前选中的树状视图节点
    selected_item = tree.selection()
    # 如果有节点被选中
    if selected_item:
        # 获取选中节点的值（即学生信息）
        item_values = tree.item(selected_item, "values")
        # 显示选中学生的详细信息
        messagebox.showinfo("选择的学生", f"学号: {item_values[0]}\n姓名: {item_values[1]}\n年龄: {item_values[2]}\n性别: {item_values[3]}\n班级: {item_values[4]}\n专业: {item_values[5]}")
    else:
        # 如果没有节点被选中，显示提示信息，要求用户选择一个学生
        messagebox.showinfo("提示", "请选择一个学生")

def update_student(tree):
    """
    更新选中学生的信息。

    参数:
    tree (ttk.Treeview): 树状视图对象。
    """
    # 获取当前选中的树状视图节点
    selected_item = tree.selection()
    # 如果有节点被选中
    if selected_item:
        # 获取选中节点的值（即学生信息）
        item_values = tree.item(selected_item, "values")

        # 将树状视图中的值填充到输入框中
        id_entry.delete(0, tk.END)
        id_entry.insert(0, item_values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, item_values[1])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, item_values[2])
        gender_entry.delete(0, tk.END)
        gender_entry.insert(0, item_values[3])
        class_entry.delete(0, tk.END)
        class_entry.insert(0, item_values[4])
        major_entry.delete(0, tk.END)
        major_entry.insert(0, item_values[5])
    else:
        # 如果没有节点被选中，显示提示信息，要求用户选择一个学生
        messagebox.showinfo("提示", "请选择一个学生")

def save_changes(tree, selected_item):
    """
    保存修改后的学生信息到树状视图和数据库中。

    参数:
    tree (ttk.Treeview): 树状视图对象。
    selected_item (str): 选中的树状视图节点的ID。
    """
    # 获取输入框中的新值
    new_values = [
        id_entry.get(),
        name_entry.get(),
        age_entry.get(),
        gender_entry.get(),
        class_entry.get(),
        major_entry.get()
    ]
    # 检查学号格式是否正确
    if not re.match(r'^[A-Za-z0-9]{6}$', new_values[0]):
        messagebox.showinfo("提示", "学号格式不正确，请重新输入")
        return

    # 更新树状视图中的学生信息
    tree.item(selected_item, values=new_values)

    # 更新数据库中的学生信息
    grade = root.title().split("学生管理系统")[0]
    conn = sqlite3.connect(get_db_path(grade))
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students
        SET name = ?, age = ?, gender = ?, class = ?, major = ?
        WHERE id = ?
    ''', (new_values[1], new_values[2], new_values[3], new_values[4], new_values[5], new_values[0]))
    conn.commit()
    conn.close()
    messagebox.showinfo("提示", "学生信息已更新")



def delete_student(tree):
    """
    删除选中的学生信息。

    参数:
    tree (ttk.Treeview): 树状视图对象。
    """
    # 获取当前选中的树状视图节点
    selected_item = tree.selection()
    # 如果有节点被选中
    if selected_item:
        # 显示确认删除对话框
        confirmation = messagebox.askyesno("确认删除", "确定要删除选中的学生吗？")
        # 如果用户确认删除
        if confirmation:
            # 获取选中节点的值（即学生信息）
            item_values = tree.item(selected_item, "values")
            # 从树状视图中删除选中的节点
            tree.delete(selected_item)

            # 从数据库中删除学生信息
            grade = root.title().split("学生管理系统")[0]
            conn = sqlite3.connect(get_db_path(grade))
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (item_values[0],))
            conn.commit()
            conn.close()
    else:
        # 如果没有节点被选中，显示提示信息，要求用户选择一个学生
        messagebox.showinfo("提示", "请选择一个学生")

def add_student(grade):
    """
    添加学生信息到数据库中。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    # 获取用户输入的学号
    id_value = id_entry.get()
    # 获取用户输入的姓名
    name_value = name_entry.get()
    # 获取用户输入的年龄
    age_value = age_entry.get()
    # 获取用户输入的性别
    gender_value = gender_entry.get()
    # 获取用户输入的班级
    class_value = class_entry.get()
    # 获取用户输入的专业
    major_value = major_entry.get()

    # 使用正则表达式检查学号格式是否正确
    if not re.match(r'^[A-Za-z0-9]{6}$', id_value):
        messagebox.showinfo("提示", "学号格式不正确，请重新输入")
        return

    # 检查姓名是否为空
    if not name_value:
        messagebox.showinfo("提示", "姓名不能为空，请重新输入")
        return

    try:
        # 将年龄转换为整数
        age = int(age_value)
    except ValueError:
        messagebox.showinfo("提示", "年龄必须为数字，请重新输入")
        return

    try:
        # 连接到数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象
        cursor = conn.cursor()
        # 执行SQL插入语句
        cursor.execute('''
            INSERT INTO students (id, name, age, gender, class, major)
            VALUES (?,?,?,?,?,?)
        ''', (id_value, name_value, age, gender_value, class_value, major_value))
        # 提交事务
        conn.commit()
        # 关闭数据库连接
        conn.close()
        # 显示学生信息
        show_students(grade)
    except sqlite3.Error as e:
        messagebox.showinfo("提示", f"数据库错误: {e}")
    except Exception as e:
        messagebox.showinfo("提示", f"其他错误: {e}")


def search_students(criteria, value, grade):
    """
    根据指定的条件和值搜索学生信息，并更新树状视图。

    参数:
    criteria (str): 搜索条件，例如 "id", "name", "age" 等。
    value (str): 搜索的值。
    grade (str): 学生所在的年级。

    返回:
    None
    """
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象
        cursor = conn.cursor()
        # 执行SQL查询语句，根据条件和值搜索学生信息
        cursor.execute(f'''
            SELECT * FROM students WHERE {criteria} = ?
        ''', (value,))
        # 获取查询结果
        students = cursor.fetchall()
        # 关闭数据库连接
        conn.close()
        # 清空树状视图中的所有项目
        tree.delete(*tree.get_children())
        # 将查询结果插入到树状视图中
        for student in students:
            tree.insert("", 0, values=(student[0], student[1], student[2], student[3], student[4], student[5]))
        # 显示提示信息，告知用户树状图已更新
        messagebox.showinfo("提示", "树状图已更新") 
    except sqlite3.Error as e:
        # 如果发生SQLite数据库错误，显示错误信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    except Exception as e:
        # 如果发生其他类型的错误，显示错误信息
        messagebox.showinfo("提示", f"其他错误: {e}")

def export_to_csv(grade):
    """
    将指定年级的学生信息从数据库导出为CSV文件。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 从数据库中查询所有学生信息
        cursor.execute("SELECT * FROM students")
        # 获取查询结果
        students = cursor.fetchall()
        # 关闭数据库连接
        conn.close()

        # 打开一个CSV文件，准备写入数据
        with open(f"{grade}_students.csv", "w", newline="", encoding="utf-8") as csvfile:
            # 创建一个CSV写入器对象
            writer = csv.writer(csvfile)
            # 写入CSV文件的表头
            writer.writerow(["学号", "姓名", "年龄", "性别", "班级", "专业"])
            # 写入所有学生信息
            writer.writerows(students)

        # 显示成功导出的提示信息
        messagebox.showinfo("提示", "数据已成功导出为CSV文件")
    # 如果发生SQLite数据库错误
    except sqlite3.Error as e:
        # 显示数据库错误提示信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    # 如果发生其他类型的错误
    except Exception as e:
        # 显示其他错误提示信息
        messagebox.showinfo("提示", f"其他错误: {e}")


def show_students(grade):
    """
    从数据库中获取指定年级的所有学生信息，并将这些信息显示在树状视图中。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    # 清空树状视图中的所有数据
    tree.delete(*tree.get_children()) 

    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 从数据库中查询所有学生信息
        cursor.execute('''
        SELECT * FROM students
        ''')
        # 获取查询结果
        students = cursor.fetchall()
        # 关闭数据库连接
        conn.close()

        # 遍历查询结果，将每个学生的信息插入到树状视图中
        for student in students:
            tree.insert("",tk.END,values=(student[0],student[1],student[2],student[3],student[4],student[5]))
        # 显示成功更新树状视图的提示信息
        messagebox.showinfo("提示", "树状图已更新")
    # 如果发生任何异常
    except Exception as e:
        # 显示错误提示信息
        messagebox.showinfo("提示", f"发生错误：{e},请打开帮助文档检查错误原因")


def show_age_distribution(grade):
    """
    从数据库中获取指定年级的学生年龄分布，并显示为柱状图。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 从数据库中查询学生年龄分布
        cursor.execute("SELECT age, COUNT(*) FROM students GROUP BY age")
        # 获取查询结果
        age_distribution = cursor.fetchall()
        # 关闭数据库连接
        conn.close()

        # 提取年龄和对应的学生数量
        ages = [row[0] for row in age_distribution]
        counts = [row[1] for row in age_distribution]

        # 使用matplotlib绘制柱状图
        plt.bar(ages, counts)
        # 设置x轴标签
        plt.xlabel("年龄")
        # 设置y轴标签
        plt.ylabel("学生数量")
        # 设置图表标题
        plt.title(f"{grade} 学生年龄分布")
        # 显示图表
        plt.show()
    # 如果发生SQLite数据库错误
    except sqlite3.Error as e:
        # 显示数据库错误提示信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    # 如果发生其他类型的错误
    except Exception as e:
        # 显示其他错误提示信息
        messagebox.showinfo("提示", f"其他错误: {e}")



def show_gender_ratio(grade):
    """
    从数据库中获取指定年级的学生性别比例，并显示为饼图。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    try:
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 从数据库中查询学生性别比例
        cursor.execute("SELECT gender, COUNT(*) FROM students GROUP BY gender")
        # 获取查询结果
        gender_ratio = cursor.fetchall()
        # 关闭数据库连接
        conn.close()

        # 提取性别和对应的学生数量
        genders = [row[0] for row in gender_ratio]
        counts = [row[1] for row in gender_ratio]

        # 使用matplotlib绘制饼图
        plt.pie(counts, labels=genders, autopct='%1.1f%%')
        # 设置图表标题
        plt.title(f"{grade}学生性别分布")
        # 显示图表
        plt.show()
    # 如果发生SQLite数据库错误
    except sqlite3.Error as e:
        # 显示数据库错误提示信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    # 如果发生其他类型的错误
    except Exception as e:
        # 显示其他错误提示信息
        messagebox.showinfo("提示", f"其他错误: {e}")

def clear_students(grade):
    """
    清空指定年级的学生信息。

    参数:
    grade (str): 学生所在的年级。

    返回:
    None
    """
    try:
        # 清空树状视图中的所有数据
        tree.delete(*tree.get_children())
        # 连接到指定年级的数据库
        conn = sqlite3.connect(get_db_path(grade))
        # 创建一个游标对象，用于执行SQL语句
        cursor = conn.cursor()
        # 从数据库中删除所有学生信息
        cursor.execute("DELETE FROM students")
        # 提交事务
        conn.commit()
        # 关闭数据库连接
        conn.close()
        # 再次清空树状视图中的所有数据，确保界面与数据库同步
        tree.delete(*tree.get_children())
        # 显示成功清空学生信息的提示信息
        messagebox.showinfo("提示", "学生信息已清空")
    # 如果发生SQLite数据库错误
    except sqlite3.Error as e:
        # 显示数据库错误提示信息
        messagebox.showinfo("提示", f"数据库错误: {e}")
    # 如果发生其他类型的错误
    except Exception as e:
        # 显示其他错误提示信息
        messagebox.showinfo("提示", f"其他错误: {e}")

def create_menu_bar(root, grade):
    """
    创建菜单栏，并添加菜单项和对应的命令。

    参数:
    root (tk.Tk): 主窗口对象。
    grade (str): 学生所在的年级。

    返回:
    None
    """
    # 创建一个菜单栏对象
    menu_bar = tk.Menu(root)
    # 将菜单栏配置到主窗口
    root.config(menu=menu_bar)
    # 创建一个“文件”菜单
    file_menu = tk.Menu(menu_bar, tearoff=0)
    # 将“文件”菜单添加到菜单栏
    menu_bar.add_cascade(label="文件", menu=file_menu)
    # 在“文件”菜单中添加“初始化学生信息”菜单项，点击时调用initial_student函数
    file_menu.add_command(label="初始化学生信息", command=lambda: initial_student(grade))
    # 在“文件”菜单中添加“查看所有学生信息”菜单项，点击时调用show_students函数
    file_menu.add_command(label="查看所有学生信息", command=lambda: show_students(grade))
    # 在“文件”菜单中添加“添加学生信息”菜单项，点击时调用add_student函数
    file_menu.add_command(label="添加学生信息", command=lambda: add_student(grade))
    # 在“文件”菜单中添加“清空学生信息”菜单项，点击时调用clear_students函数
    file_menu.add_command(label="清空学生信息", command=lambda: clear_students(grade))
    # 在“文件”菜单中添加“更新树状图”菜单项，点击时调用update_tree函数
    file_menu.add_command(label="更新树状图", command=lambda: update_tree(tree,grade))
    # 在“文件”菜单中添加“导出为CSV”菜单项，点击时调用export_to_csv函数
    file_menu.add_command(label="导出为CSV", command=lambda: export_to_csv(grade))
    # 在“文件”菜单中添加分隔线
    file_menu.add_separator()
    # 在“文件”菜单中添加“退出”菜单项，点击时退出程序
    file_menu.add_command(label="退出", command=root.quit)
    # 创建一个“扩展”菜单
    expand_menu = tk.Menu(menu_bar, tearoff=0)
    # 将“扩展”菜单添加到菜单栏
    menu_bar.add_cascade(label="扩展", menu=expand_menu)
    # 在“扩展”菜单中添加“图表展示年龄分布”菜单项，点击时调用show_age_distribution函数
    expand_menu.add_command(label="图表展示年龄分布", command=lambda: show_age_distribution(grade))
    # 在“扩展”菜单中添加“图表展示性别比例”菜单项，点击时调用show_gender_ratio函数
    expand_menu.add_command(label="图表展示性别比例", command=lambda: show_gender_ratio(grade))
    # 创建一个“帮助”菜单
    help_menu = tk.Menu(menu_bar, tearoff=0)
    # 将“帮助”菜单添加到菜单栏
    menu_bar.add_cascade(label="帮助", menu=help_menu)
    # 在“帮助”菜单中添加“关于”菜单项，点击时调用show_about函数
    help_menu.add_command(label="关于", command=lambda: show_about())
    help_menu.add_command(label="帮助文档", command=lambda: show_help())

def show_about():
    """
    显示关于信息的对话框。

    """
    # 显示一个包含关于信息的消息框
    messagebox.showinfo("关于", "241217 written by BobZhu \nThanks for your use")

def show_help():
    """
    显示帮助文档的窗口，包含详细的使用说明。
    """
    # 创建一个新的顶级窗口
    help_window = tk.Toplevel()
    help_window.title("帮助文档")
    help_window.geometry("800x600")

    # 创建滚动文本框
    text_area = scrolledtext.ScrolledText(
        help_window,
        wrap=tk.WORD,
        width=100,
        height=30,
        font=("Arial", 10)
    )
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 帮助文档内容
    help_content = """
    学生管理系统帮助文档

    一、基本操作
    1. 初始化学生信息：
       - 功能：在数据库中生成示例学生数据（张三、李四等）。
       - 操作：点击【文件】→【初始化学生信息】。
       - 注意：仅当数据库为空时生效，重复初始化会提示已存在数据。

    2. 添加学生：
       - 填写所有字段后点击【添加】按钮。
       - 学号格式：6位字符（字母/数字组合），例如：ABC123。
       - 年龄必须为数字。

    3. 修改学生信息：
       - 步骤：
         1. 在表格中选中学生。
         2. 修改对应字段。
         3. 点击【保存】。
       - 注意：学号不可修改。

    4. 删除学生：
       - 选中学生后点击【删除】，需二次确认。

    二、数据管理
    1. 搜索功能：
       - 支持按学号/姓名搜索：
         1. 在左侧下拉框选择条件(id/name)。
         2. 输入关键字后点击【搜索】。
       - 清空搜索框并搜索可显示全部数据。

    2. 数据导出：
       - 点击【文件】→【导出为CSV】。
       - 文件保存在程序同级目录,命名格式:年级_students.csv。

    3. 清空数据：
       - 点击【文件】→【清空学生信息】将删除所有数据。

    三、图表功能
    1. 年龄分布图：
       - 点击【扩展】→【图表展示年龄分布】显示柱状图。

    2. 性别比例图：
       - 点击【扩展】→【图表展示性别比例】显示饼图。

    四、常见问题
    1. 学号格式错误：
       - 必须为6位字符（如CS001），前三位建议代表专业。

    2. 年龄输入非数字：
       - 系统会提示“年龄必须为数字”。

    3. 数据不显示：
       - 确保已点击【更新树状图】或执行过搜索/初始化操作。

    技术支持：BobZhu@mars.com | 版本：v2.1 (2024-12-17)
    """

    # 插入帮助内容并禁用编辑
    text_area.insert(tk.INSERT, help_content)
    text_area.configure(state='disabled')  # 设置为只读模式

    # 添加关闭按钮
    close_button = ttk.Button(
        help_window,
        text="关闭",
        command=help_window.destroy
    )
    close_button.pack(pady=10)

def create_input_frame(main_frame, grade):
    """
    创建并返回一个用于输入学生信息的框架。

    参数:
    main_frame (tk.Frame): 主窗口的框架。
    grade (str): 学生所在的年级。

    返回:
    tk.Frame: 创建的输入框架。
    """
    # 使用 global 关键字声明这些变量为全局变量，以便在函数外部访问它们
    global id_entry, name_entry, age_entry, gender_entry, class_entry, major_entry

    # 创建一个新的框架，用于放置输入部件
    input_frame = tk.Frame(main_frame)
    # 使用 pack 布局管理器将输入框架放置在主框架的左侧，并填充和扩展以适应窗口大小
    input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建一个下拉列表框，用于选择搜索条件（学号或姓名）
    combo_box = ttk.Combobox(input_frame, values=["id", "name"])
    # 使用 grid 布局管理器将下拉列表框放置在输入框架的第一行第一列，并设置内边距
    combo_box.grid(row=0, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入搜索关键字
    search_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第一行第二列，并设置内边距
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # 创建一个按钮，用于触发搜索功能，点击时调用 search_students 函数，并传递下拉列表框的值和输入框的值作为参数
    search_button = ttk.Button(input_frame, text="搜索", command=lambda: search_students(combo_box.get(), search_entry.get(), grade))
    # 使用 grid 布局管理器将按钮放置在输入框架的第二行第一列，并设置内边距
    search_button.grid(row=1, column=0, padx=5, pady=5)

    # 创建一个标签，用于显示学号的输入提示信息
    id_label = tk.Label(input_frame, text="学号(6位,前三位为专业代码，后三位为数字)")
    # 使用 grid 布局管理器将标签放置在输入框架的第三行第一列，并设置内边距
    id_label.grid(row=2, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入学号
    id_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第三行第二列，并设置内边距
    id_entry.grid(row=2, column=1, padx=5, pady=5)

    # 创建一个标签，用于显示姓名的输入提示信息
    name_label = tk.Label(input_frame, text="姓名")
    # 使用 grid 布局管理器将标签放置在输入框架的第四行第一列，并设置内边距
    name_label.grid(row=3, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入姓名
    name_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第四行第二列，并设置内边距
    name_entry.grid(row=3, column=1, padx=5, pady=5)

    # 创建一个标签，用于显示年龄的输入提示信息
    age_label = tk.Label(input_frame, text="年龄")
    # 使用 grid 布局管理器将标签放置在输入框架的第五行第一列，并设置内边距
    age_label.grid(row=4, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入年龄
    age_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第五行第二列，并设置内边距
    age_entry.grid(row=4, column=1, padx=5, pady=5)

    # 创建一个标签，用于显示性别的输入提示信息
    gender_label = tk.Label(input_frame, text="性别")
    # 使用 grid 布局管理器将标签放置在输入框架的第六行第一列，并设置内边距
    gender_label.grid(row=5, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入性别
    gender_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第六行第二列，并设置内边距
    gender_entry.grid(row=5, column=1, padx=5, pady=5)

    # 创建一个标签，用于显示班级的输入提示信息
    class_label = tk.Label(input_frame, text="班级")
    # 使用 grid 布局管理器将标签放置在输入框架的第七行第一列，并设置内边距
    class_label.grid(row=6, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入班级
    class_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第七行第二列，并设置内边距
    class_entry.grid(row=6, column=1, padx=5, pady=5)

    # 创建一个标签，用于显示专业的输入提示信息
    major_label = tk.Label(input_frame, text="专业")
    # 使用 grid 布局管理器将标签放置在输入框架的第八行第一列，并设置内边距
    major_label.grid(row=7, column=0, padx=5, pady=5)

    # 创建一个输入框，用于输入专业
    major_entry = ttk.Entry(input_frame)
    # 使用 grid 布局管理器将输入框放置在输入框架的第八行第二列，并设置内边距
    major_entry.grid(row=7, column=1, padx=5, pady=5)

    # 返回创建的输入框架
    return input_frame


def create_button_frame(input_frame, grade):
    """
    创建一个包含按钮的框架，用于执行学生管理系统中的添加、删除、更新和保存操作。

    参数:
    input_frame (tk.Frame): 父框架，按钮框架将放置在其中。
    grade (str): 学生所在的年级。

    返回:
    tk.Frame: 创建的按钮框架。
    """
    # 创建一个新的框架，用于放置按钮
    button_frame = tk.Frame(input_frame)
    # 使用 grid 布局管理器将按钮框架放置在父框架中
    button_frame.grid(row=8, column=0, columnspan=2, sticky=tk.EW)  # 使用 grid 布局

    # 创建“添加”按钮，点击时调用 add_student 函数
    add_button = ttk.Button(button_frame, text="添加", command=lambda: add_student(grade))
    # 使用 grid 布局管理器将“添加”按钮放置在按钮框架中
    add_button.grid(row=0, column=0, padx=5, pady=5)

    # 创建“删除”按钮，点击时调用 delete_student 函数
    delete_button = ttk.Button(button_frame, text="删除", command=lambda: delete_student(tree))
    # 使用 grid 布局管理器将“删除”按钮放置在按钮框架中
    delete_button.grid(row=0, column=1, padx=5, pady=5)

    # 创建“修改”按钮，点击时调用 update_student 函数
    update_button = ttk.Button(button_frame, text="修改", command=lambda: update_student(tree))
    # 使用 grid 布局管理器将“修改”按钮放置在按钮框架中
    update_button.grid(row=0, column=2, padx=5, pady=5)

    # 创建“保存”按钮，点击时调用 save_changes 函数
    confirm_button = ttk.Button(button_frame, text="保存", command=lambda: save_changes(tree, tree.selection()))
    # 使用 grid 布局管理器将“保存”按钮放置在按钮框架中
    confirm_button.grid(row=0, column=3, padx=5, pady=5)

    # 返回创建的按钮框架
    return button_frame


def create_display_frame(main_frame):
    """
    创建并返回一个用于显示学生信息的框架。

    参数:
    main_frame (tk.Frame): 主窗口的框架。

    返回:
    tk.Frame: 创建的显示框架。
    """
    # 创建一个新的框架，用于显示学生信息
    display_frame = tk.Frame(main_frame)
    # 将新创建的框架放置在主框架的右侧，并填充整个可用空间
    display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    # 返回创建的显示框架
    return display_frame

# 自定义函数:树状图函数部分
def create_tree_view(root):
    """
    创建一个用于显示学生信息的树状视图。

    参数:
    root (tk.Tk or tk.Frame): 树状视图的父容器。

    返回:
    ttk.Treeview: 创建的树状视图对象。
    """
    # 创建一个新的树状视图对象
    tree = ttk.Treeview(root)
    # 创建一个样式对象，用于配置树状视图的外观
    style = ttk.Style()
    # 设置树状视图的字体为Arial，大小为12
    style.configure("Treeview", font=("Arial", 12))
    # 设置树状视图只显示列标题，不显示第一列的图标
    tree["show"] = "headings"  

    # 定义树状视图的列，包括学号、姓名、年龄、性别、班级和专业
    tree["columns"] = ("id", "name", "age", "gender", "class", "major")

    # 设置每列的宽度和对齐方式
    tree.column("id", width=50, anchor=tk.CENTER)
    tree.column("name", width=100, anchor=tk.CENTER)
    tree.column("age", width=50, anchor=tk.CENTER)
    tree.column("gender", width=50, anchor=tk.CENTER)
    tree.column("class", width=100, anchor=tk.CENTER)
    tree.column("major", width=100, anchor=tk.CENTER)

    # 设置每列的标题文本
    tree.heading("id", text="学号")
    tree.heading("name", text="姓名")
    tree.heading("age", text="年龄")
    tree.heading("gender", text="性别")
    tree.heading("class", text="班级")
    tree.heading("major", text="专业")
    # 将树状视图放置在父容器中，并填充整个可用空间
    tree.pack(fill=tk.BOTH, expand=True)
    # 绑定鼠标左键点击事件，当点击树状视图时，调用select_student函数
    tree.bind("<Button-1>", lambda event: select_student(tree))

    # 返回创建的树状视图对象
    return tree
def get_db_path(grade):
    """
    根据年级生成数据库文件路径。

    参数:
    grade (str): 学生所在的年级。

    返回:
    str: 数据库文件的路径。
    """
    # 使用格式化字符串生成数据库文件路径，文件名格式为"{grade}.db"
    return f"{grade}.db"


def check_db_exists(grade):
    """
    检查指定年级的数据库是否存在，如果不存在则创建数据库并初始化表。

    参数:
    grade (str): 学生所在的年级。
    """
    # 获取指定年级的数据库文件路径
    db_path = get_db_path(grade)
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        # 如果数据库文件不存在，则创建数据库并初始化表
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT,
                name TEXT ,
                age INTEGER,
                gender TEXT,
                class TEXT,
                major TEXT
            )
        ''')
        conn.commit()
        conn.close()



def create_main_window(grade):
    """
    创建主窗口并设置布局。

    参数:
    grade (str): 学生所在的年级。
    """
    # 声明全局变量root，以便在函数内部修改全局变量的值
    global root
    # 创建主窗口对象
    root = tk.Tk()
    # 设置主窗口的标题，包含年级信息
    root.title(grade+"学生管理系统")
    # 设置主窗口的大小为1200x640像素
    root.geometry("1200x640")
    # 创建菜单栏
    create_menu_bar(root, grade)

    # 创建主框架，用于放置其他组件
    main_frame = tk.Frame(root)
    # 将主框架填充整个窗口，并允许其扩展
    main_frame.pack(fill=tk.BOTH, expand=True)
    # 用frame模块将窗口分为输入框、按钮、显示框
    input_frame = create_input_frame(main_frame,grade)
    button_frame =create_button_frame(input_frame,grade)
    display_frame = create_display_frame(main_frame)

    # 创建树状视图，用于显示学生信息
    global tree
    tree = create_tree_view(display_frame)
    # 将树状视图填充整个显示框架，并允许其扩展
    tree.pack(fill=tk.BOTH, expand=True)
    
    # 配置窗口的行和列，使其在窗口大小调整时自适应
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 运行窗口的主循环，使窗口保持显示状态
    root.mainloop()


if __name__ == "__main__":
    """
    程序的主入口点。

    此代码块在脚本直接运行时执行，而不是作为模块导入时执行。
    它会提示用户输入年级，然后检查该年级的数据库是否存在。
    如果存在，则创建主窗口并显示学生信息；
    如果不存在，则显示提示信息并退出程序。
    """
    # 使用 simpledialog 模块提示用户输入年级
    current_grade = simpledialog.askstring("选择年级", "请输入年级(例如:24级):")
    # 将用户输入的年级赋值给全局变量 name
    name = current_grade
    # 如果用户输入了年级
    if current_grade:
        # 检查该年级的数据库是否存在
        check_db_exists(current_grade)
        # 创建主窗口并显示学生信息
        create_main_window(current_grade)
    else:
        # 如果用户没有输入年级，显示提示信息并退出程序
        messagebox.showinfo("提示", "未选择年级，程序将退出。")
