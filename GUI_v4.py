from tkinter import Tk, Text, Scrollbar, Frame, RIGHT, Y, LEFT, BOTH, Button, END, Toplevel, Label
from tkinter.ttk import Progressbar
import re
import keyword
import time

def run_custom_code_from_text(code_lines, output_callback, tac_callback):
    lines = [line.strip() for line in code_lines if line.strip()]
    if not lines or not lines[0].startswith("India"):
        output_callback("Code must start with 'India'")
        return

    context = {}
    temp_counter = 1
    n = len(lines)
    i = 1

    def new_temp():
        nonlocal temp_counter
        temp = f"t{temp_counter}"
        temp_counter += 1
        return temp

    def evaluate_condition(condition):
        try:
            return eval(condition, {}, context)
        except Exception as e:
            output_callback(f"[Condition Error] {condition} -> {e}")
            return False

    def handle_say(line):
        match = re.match(r'say\s+"(.*)"', line)
        if match:
            msg = match.group(1)
            output_callback(msg)
            tac_callback(f'{new_temp()} = "{msg}"')
        else:
            expr = line[4:].strip()
            try:
                val = eval(expr, {}, context)
                output_callback(str(val))
                tac_callback(f'{new_temp()} = {expr}')
            except Exception as e:
                output_callback(f"[say Error] {expr} -> {e}")

    def handle_block(start_index):
        block = []
        while start_index < n and lines[start_index] != "}":
            block.append(lines[start_index])
            start_index += 1
        return block, start_index + 1

    while i < n:
        line = lines[i]

        if line.startswith("-->"):
            i += 1
            continue

        if '=' in line and not line.startswith(("when", "otherwise", "repeat")):
            try:
                exec(line, {}, context)
                tac_callback(line)
            except Exception as e:
                output_callback(f"[Assignment Error] {line} -> {e}")
            i += 1

        elif line.startswith("say"):
            handle_say(line)
            i += 1

        elif line.startswith("when"):
            executed = False
            while i < n:
                line = lines[i]
                if line.startswith("when") or line.startswith("otherwise when"):
                    condition = line.split("when", 1)[1].strip().rstrip('{').strip()
                    tac_callback(f"if {condition} goto L{i}")
                    if evaluate_condition(condition) and not executed:
                        block, i = handle_block(i + 1)
                        tac_callback(f"L{i}:")
                        for stmt in block:
                            tac_callback(stmt)
                            if stmt.startswith("say"):
                                handle_say(stmt)
                            else:
                                try:
                                    exec(stmt, {}, context)
                                except:
                                    pass
                        executed = True
                    else:
                        _, i = handle_block(i + 1)
                elif line.startswith("otherwise"):
                    if not executed:
                        block, i = handle_block(i + 1)
                        tac_callback(f"L{i}:")
                        for stmt in block:
                            tac_callback(stmt)
                            if stmt.startswith("say"):
                                handle_say(stmt)
                            else:
                                try:
                                    exec(stmt, {}, context)
                                except:
                                    pass
                    else:
                        _, i = handle_block(i + 1)
                    break
                else:
                    break

        elif line.startswith("repeat"):
            match = re.match(r"repeat\s*\((\d+)\)\s*{", line)
            if match:
                times = int(match.group(1))
                block, i = handle_block(i + 1)
                tac_callback(f"# repeat {times} times")
                for _ in range(times):
                    for stmt in block:
                        tac_callback(stmt)
                        if stmt.startswith("say"):
                            handle_say(stmt)
                        else:
                            try:
                                exec(stmt, {}, context)
                            except:
                                pass
            else:
                output_callback("Syntax error in repeat")
                i += 1
        else:
            i += 1

win = Tk()
win.title('Custom Compiler')
win.geometry("600x500")

frame = Frame(win)
frame.pack(pady=10)

t1 = Text(frame, height=20, width=60)
t1.pack(side=LEFT, fill=BOTH)

scroll = Scrollbar(frame, command=t1.yview)
scroll.pack(side=RIGHT, fill=Y)

t1.config(yscrollcommand=scroll.set)

# Progress bar
pbar = Progressbar(win, orient='horizontal', length=300, mode='determinate')
pbar.pack(pady=10)

progress_label = Label(win, text="Progress: 0%")
progress_label.pack()


def on_run():
    code = t1.get("1.0", END).splitlines()

    def update_progress_bar():
        for i in range(101):
            pbar['value'] = i
            progress_label.config(text=f"Progress: {i}%")
            win.update_idletasks()
            time.sleep(0.01)

        show_output_windows()

    def show_output_windows():
        output_win = Toplevel(win)
        output_win.title("Output")
        output_box = Text(output_win, height=20, width=60)
        output_box.pack(padx=10, pady=10)

        tac_win = Toplevel(win)
        tac_win.title("Three Address Code")
        tac_box = Text(tac_win, height=20, width=60)
        tac_box.pack(padx=10, pady=10)

        tac_lines = []

        def output_callback(msg):
            output_box.insert(END, msg + '\n')
            output_box.see(END)

        def tac_callback(line):
            tac_lines.append(line)

        run_custom_code_from_text(code, output_callback, tac_callback)
        tac_box.insert(END, '\n'.join(tac_lines))
        tac_box.see(END)

    update_progress_bar()


btn = Button(win, text='Run Code', command=on_run)
btn.pack(pady=10)

win.mainloop()
