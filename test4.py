# coding: cp936
import _thread
import threading
import win32gui
import win32con
import time
import wx
import wx.grid


# ���½ǵ���
class TestTaskbarIcon:
    def __init__(self):
        # ע��һ��������
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def showMsg(self, title, msg):
        # ԭ����ʹ��Shell_NotifyIconA���������װ���Shell_NotifyIcon����
        # �ݳ��ǲ���win32gui structure, ��ϡ���Ϳ�������.
        # ����Ա�ԭ����.
        nid = (self.hwnd,  # ���
               0,  # ����ͼ��ID
               win32gui.NIF_INFO,  # ��ʶ
               0,  # �ص���ϢID
               0,  # ����ͼ����
               "TestMessage",  # ͼ���ַ���
               msg,  # ������ʾ�ַ���
               0,  # ��ʾ����ʾʱ��
               title,  # ��ʾ����
               win32gui.NIIF_INFO  # ��ʾ�õ���ͼ��
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


class TestTable(wx.grid.PyGridTableBase):  # ���������


    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = {(1, 1): "Here",
            (2, 2): "is",
            (3, 3): "some",
            (4, 4): "data",
            }
        self.odd = wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)) #436 / 565
        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("sea green")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))


    # these five are the required methods
    def GetNumberRows(self):
        return 5


    def GetNumberCols(self):
        return 4


    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None


    def GetValue(self, row, col):  # Ϊ�����ṩ����
        value = self.data.get((row, col))
        if value is not None:
            return value
        else:
            return ' '

    def SetValue(self, row, col, value):  # ����ֵ
        self.data[(row, col)] = value


    # the table can also provide the attribute for each cell
    def GetAttr(self, row, col, kind):
         attr = [self.even, self.odd][row % 2]
         attr.IncRef()
         return attr


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Grid Table",
        size = (640, 480)) #437 / 565
        grid = wx.grid.Grid(self)
        table = TestTable()
        grid.SetTable(table, True)
#app = wx.PySimpleApp()
#frame = TestFrame()
#frame.Show()
#app.MainLoop()


from tkinter import *
from time import time, localtime, strftime


class ToolTip(Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """

    def __init__(self, wdgt, msg=None, msgFunc=None, delay=1, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        self.parent = self.wdgt.master  # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)  # Initalise the Toplevel
        self.withdraw()  # Hide initially
        self.overrideredirect(True)  # The ToolTip Toplevel should have no frame or title bar

        self.msgVar = StringVar()  # The msgVar will contain the text displayed by the ToolTip
        if msg == None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                aspect=1000).grid()  # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind('<Enter>', self.spawn,
                       '+')  # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)  # The after function takes a time argument in miliseconds

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.

        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False:  # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (
        event.x_root + 10, event.y_root + 10))  # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set(
                self.msgFunc())  # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget

        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


def xrange2d(n, m):
    """
    Returns a generator of values in a 2d range

    Arguments:
      n: The number of rows in the 2d range
      m: The number of columns in the 2d range
    Returns:
      A generator of values in a 2d range
    """
    return ((i, j) for i in xrange(n) for j in xrange(m))


def range2d(n, m):
    """
    Returns a list of values in a 2d range

    Arguments:
      n: The number of rows in the 2d range
      m: The number of columns in the 2d range
    Returns:
      A list of values in a 2d range
    """
    return [(i, j) for i in range(n) for j in range(m)]


def print_time():
    """
    Prints the current time in the following format:
    HH:MM:SS.00
    """
    t = time()
    timeString = 'time='
    timeString += strftime('%H:%M:', localtime(t))
    timeString += '%.2f' % (t % 60,)
    return timeString


def main():
    root = Tk()
    btnList = []
    for (i, j) in range2d(6, 4):
        text = 'delay=%i\n' % i
        delay = i
        if j >= 2:
            follow = True
            text += '+follow\n'
        else:
            follow = False
            text += '-follow\n'
        if j % 2 == 0:
            msg = None
            msgFunc = print_time
            text += 'Message Function'
        else:
            msg = 'Button at %s' % str((i, j))
            msgFunc = None
            text += 'Static Message'
        btnList.append(Button(root, text=text))
        ToolTip(btnList[-1], msg=msg, msgFunc=msgFunc, follow=follow, delay=delay)
        btnList[-1].grid(row=i, column=j, sticky=N + S + E + W)
    root.mainloop()


if __name__ == '__main__':
    main()

#if __name__ == '__main__':
# t = TestTaskbarIcon()
# t.showMsg("�����µ��ļ������¼�鿴", "Mr a2man!")
# t.showMsg("�����µ��ļ������¼�鿴222", "Mr a2man!2222")
# time.sleep(5)
# win32gui.DestroyWindow(t.hwnd)
# t.OnDestroy(t.hwnd,None,None,None)
