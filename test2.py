# coding:utf-8

import wx


def openfile(event):  # 定义打开文件事件

    path = path_text.GetValue()

    with open(path, "r", encoding="utf-8") as f:  # encoding参数是为了在打开文件时将编码转为utf8

        content_text.SetValue(f.read())


app = wx.App()

frame = wx.Frame(None, title="Gui Test Editor", pos=(1000, 200), size=(500, 400))

panel = wx.Panel(frame)

path_text = wx.TextCtrl(panel)

open_button = wx.Button(panel, label="打开")

open_button.Bind(wx.EVT_BUTTON, openfile)  # 绑定打开文件事件到open_button按钮上

save_button = wx.Button(panel, label="保存")

content_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

#  wx.TE_MULTILINE可以实现以滚动条方式多行显示文本,若不加此功能文本文档显示为一行


box = wx.BoxSizer()  # 不带参数表示默认实例化一个水平尺寸器

box.Add(path_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

# proportion：相对比例

# flag：填充的样式和方向,wx.EXPAND为完整填充，wx.ALL为填充的方向

# border：边框

box.Add(open_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

box.Add(save_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

v_box = wx.BoxSizer(wx.VERTICAL)  # wx.VERTICAL参数表示实例化一个垂直尺寸器

v_box.Add(box, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

v_box.Add(content_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

panel.SetSizer(v_box)  # 设置主尺寸器

frame.Show()

app.MainLoop()

#app = wx.App()
#app = wx.PySimpleApp()

class GridData(wx.grid.PyGridTableBase):
    _cols = "a b c".split()
    _data = [
        "1 2 3".split(),
        "4 5 6".split(),
        "7 8 9".split()
    ]
    _highlighted = set()

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)


class Test(wx.Frame):
    def __init__(self):
        #wx.Frame.__init__(self, None)
        self.Fram();
        self.data = GridData()
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(self.data)

        btn = wx.Button(self, label="set a2 to x")
        btn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.grid, 1, wx.EXPAND)
        self.Sizer.Add(btn, 0, wx.EXPAND)

    def OnTest(self, event):
        self.data.set_value(1, 0, "x")

# app.TopWindow = Test()
# app.TopWindow.Show()
# app.MainLoop()
#if __name__ == '__main__':
#    show2()