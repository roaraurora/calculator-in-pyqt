# -*- coding: utf-8 -*-
# @File  : PY9_PyQt5.py
# @Author: deeeeeeeee
# @Date  : 2018/6/17
"""Simple PY9_PyQt5
    support_order defines all order supported
    UI based on PyQt5
    Implement algorithms by Python builtin-function eval()
"""
import sys
import re
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QLineEdit)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    """A subclass of QWidget, that appear as one single window,
        consist of a QGridLayout object which filled by a ReadOnly QLineEdit and a bunch of QPushButton
    """
    support_order = {'(': '(', ')': ')', '÷': '/', '×': '*', 'x2': '**2', 'x3': '**3', 'xy': '**', '%': '%'}

    def __init__(self):
        super().__init__()
        self.history = ''
        # self.result = ''
        self.initUI()

    def initUI(self):
        """main UI implement"""
        grid = QGridLayout()
        self.setLayout(grid)
        self.lcd = QLineEdit()
        self.lcd.setAlignment(Qt.AlignRight)
        self.lcd.setMaxLength(28)
        self.lcd.setText('0')
        self.lcd.setReadOnly(True)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.lcd, 0, 0, 1, 10)

        names = ['(', ')', 'mc', 'm+', 'm-', 'mr', 'AC', '+/-', '%', '÷',
                 '2nd', 'x2', 'x3', 'xy', 'ex', '10x', '7', '8', '9', '×',
                 '1/x', '2√x', '3√x', 'y√x', 'ln', 'log10', '4', '5', '6', '-',
                 'x!', 'sin', 'cos', 'tan', 'e', 'EE', '1', '2', '3', '+',
                 'Rad', 'sinh', 'cosh', 'tanh', 'pi', 'Rand', '0', '', '.', '=']
        positions = [(i, j) for i in range(1, 6) for j in range(10)]

        for position, name in zip(positions, names):
            if name == '0':
                position = (5, 6, 1, 2)
            if name == '':
                continue
            name = ' ' * ((5 - len(name)) - int((5 - len(name)) / 2)) + name + ' ' * int((5 - len(name)) / 2)

            if position[1] == 9:
                button = BasicMathButton(name)
            elif position[1] in range(6, 9) and position[0] in range(2, 6):
                button = NumberButton(name)
            else:
                button = QPushButton(name)
            button.clicked.connect(self.calc)
            grid.addWidget(button, *position)
        self.move(600, 400)
        self.setWindowTitle('Calculator V1.0')
        self.setWindowOpacity(0.9)
        self.show()

    def calc(self):
        """main calculate implement"""
        button_value = str.strip(self.sender().text(), ' ')
        order = Calculator.support_order.get(button_value) or button_value
        print("order => {}".format(order))
        if isinstance(self.sender(), (NumberButton, BasicMathButton)) or button_value in Calculator.support_order.keys():
            try:
                if order == '=':
                    self.history = str(eval(Calculator.pre_handle(self.history)))
                    float(self.history)  # this could cause ValueError
                else:
                    temp_history = self.history + order
                    if not Calculator.is_valid_expr(temp_history):
                        print("@Unknown Error:  history => {}".format(temp_history))
                        return
                    self.history = temp_history
            except Exception as e:
                print("invalid input @calc:{} \nReason: {}".format(self.history, e))
                self.history = ''
        if order == 'AC':
            self.history = ''
        self.lcd.setText(self.history or '0')
        return

    @staticmethod
    def is_valid_expr(expression):
        """check if expression is valid"""
        try:
            if expression[-1] in ['+', '-', '*', '/', '.', '(', '0', '%']:
                expression = expression + '1'
            expression = Calculator.pre_handle(expression)
            eval(expression)
        except Exception as e:
            print("invalid input @valid:{} \n Reason: {}".format(expression, e))
            return False
        return True

    @staticmethod
    def pre_handle(expression):
        """pre processing expression"""
        split_by_bck = expression.split(')', -1)
        if len(split_by_bck) > 1:
            for i in range(len(split_by_bck)):
                if sum([split_by_bck[j].count('(') for j in range(0, i + 1)]) < i:
                    raise SyntaxError
        match_list = re.findall(r'[+\-*/(]0([\d]+)', expression)
        for march in match_list:
            expression = expression.replace('0' + march, march)
        return expression + ')' * (expression.count('(') - expression.count(')'))


class BasicMathButton(QPushButton):
    """this button appear in light color"""
    def __init__(self, name):
        super().__init__(name)


class NumberButton(QPushButton):
    """this button appear in orange and located in right"""
    def __init__(self, name):
        super().__init__(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    qss_file = open('PY9_PyQt5.qss').read()
    calculator.setStyleSheet(qss_file)
    sys.exit(app.exec_())
