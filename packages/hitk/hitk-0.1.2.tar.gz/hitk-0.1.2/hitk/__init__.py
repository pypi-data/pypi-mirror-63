# coding: utf-8
"""
こちらのパッケージには Tkinter を補間する有用な機能が定義されています。
"""

import ctypes, functools, logging, os, re, sys, threading, weakref, zipfile
import concurrent.futures
from datetime import datetime as _dt
from time import time as now
from logging import DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL
from traceback import format_exc

if sys.version_info < (3, 0):
  import Tkinter as tk, ttk
  from Queue import Queue, Empty
  import tkMessageBox as messagebox, tkSimpleDialog as simpledialog, \
      tkFileDialog as filedialog, tkFont as tkfont, Tkdnd as tkdnd
  import tkColorChooser as colorchooser

  from Tkinter import TclError, TOP, BOTTOM, LEFT, RIGHT, BOTH, \
    INSERT, END, SEL, SEL_FIRST, SEL_LAST, NORMAL, DISABLED, \
    Menu, Listbox, Text, Canvas, PhotoImage, PanedWindow, \
    StringVar, IntVar, DoubleVar, BooleanVar, Pack, Grid, Place
  from ScrolledText import ScrolledText
  tk.ScrolledText = ScrolledText

  from ttk import Label, Button, Entry, Checkbutton, Radiobutton, \
    Scrollbar, Notebook, Combobox, Frame, OptionMenu, LabelFrame, Treeview, \
    Progressbar, Panedwindow, Menubutton

  def _ucs(tt): return tt.decode('utf-8')

  try: import Tix as tix
  except: tix = None
  
else:
  import tkinter as tk
  from tkinter import ttk
  from queue import Queue, Empty
  from tkinter import messagebox, simpledialog, filedialog, \
    font as tkfont, dnd as tkdnd, colorchooser

  from tkinter import TclError, TOP, BOTTOM, LEFT, RIGHT, BOTH, \
    INSERT, END, SEL, SEL_FIRST, SEL_LAST, NORMAL, ACTIVE, DISABLED, \
    Menu, Listbox, Text, Canvas, PhotoImage, PanedWindow, \
    StringVar, IntVar, DoubleVar, BooleanVar, Pack, Grid, Place

  from tkinter.scrolledtext import ScrolledText
  tk.ScrolledText = ScrolledText
  
  from tkinter.ttk import Label, Button, Entry, Checkbutton, Radiobutton, \
    Scrollbar, Notebook, Combobox, OptionMenu, Frame, LabelFrame, Treeview, \
    Progressbar, Panedwindow, Menubutton

  def _ucs(tt): return tt
  unicode = str

  try: from tkinter import tix
  except: tix = None

ui = __import__(__name__)

platform = sys.platform

log = logging.getLogger(__name__)

from hitk.common import trace, trace_text, INIPreference
import hitk.cli

def _return_self(func):
  "カスケード呼び出しができるように自身を返すメソッドにするデコレータ"
  @functools.wraps(func)
  def wrap(self, *args, **kwargs):
    func(self, *args, **kwargs)
    return self
  return wrap

tk.Pack.pack = _return_self(tk.Pack.pack)
tk.Pack.pack_configure = _return_self(tk.Pack.pack_configure)
tk.Grid.grid = _return_self(tk.Grid.grid)
tk.Grid.grid_configure = _return_self(tk.Grid.grid_configure)
tk.Place.place = _return_self(tk.Place.place)
tk.Place.place_configure = _return_self(tk.Place.place_configure)

Combobox.set = _return_self(Combobox.set)


def _bind_darwin(func1):
  @functools.wraps(func1)
  def wrap(self, sequence=None, func=None, add=None):
    if sequence:
      if platform == 'darwin': sequence = sequence.replace('<Control-','<Command-')
      sequence = sequence.replace(r'<\Control-','<Control-')
    return func1(self, sequence=sequence, func=func, add=add)
  return wrap

def _bind_class_darwin(func1):
  @functools.wraps(func1)
  def wrap(self, className, sequence=None, func=None, add=None):
    if sequence:
      if platform == 'darwin': sequence = sequence.replace('<Control-','<Command-')
      sequence = sequence.replace(r'<\Control-','<Control-')
    return func1(self, className, sequence=sequence, func=func, add=add)
  return wrap

def _unbind_darwin(func1):
  @functools.wraps(func1)
  def wrap(self, sequence, funcid=None):
    if sequence:
      if platform == 'darwin': sequence = sequence.replace('<Control-','<Command-')
      sequence = sequence.replace(r'<\Control-','<Control-')
    return func1(self, sequence, funcid=funcid)
  return wrap

def _unbind_class_darwin(func1):
  @functools.wraps(func1)
  def wrap(self, className, sequence):
    if sequence:
      if platform == 'darwin': sequence = sequence.replace('<Control-','<Command-')
      sequence = sequence.replace(r'<\Control-','<Control-')
    return func1(self, clsasName, sequence)
  return wrap

def _return_text_darwin(func):
  @functools.wraps(func)
  def wrap(self, *args, **kw):
    res = func(self, *args, **kw)
    return res.replace('\r','\n') if type(res) in (str, unicode) else res
  return wrap

if platform == 'darwin':
  tk.Misc.selection_get = _return_text_darwin(tk.Misc.selection_get)
  tk.Misc.clipboard_get = _return_text_darwin(tk.Misc.clipboard_get)

tk.Misc.bind = _bind_darwin(tk.Misc.bind)
tk.Misc.bind_class = _bind_class_darwin(tk.Misc.bind_class)
tk.Misc.unbind = _unbind_darwin(tk.Misc.unbind)
tk.Misc.unbind_class = _unbind_class_darwin(tk.Misc.unbind_class)


def parse_geometry(geometry):
  m = re.match("(\d+)x(\d+)[+]?([-+]\d+)[+]?([-+]\d+)", geometry)
  if not m: raise ValueError("failed to parse geometry string")
  return map(int, m.groups())


class Timer():
  ''' タイマー制御インタフェース'''
  def start(self):
    pass
  def stop(self):
    pass
  def restart(self):
    pass


class AppContext():
  ''' アプリケーションが利用する共通機能を提供するインスタンス '''
  def show_info(self, msg, title=None):
    '情報メッセージをポップアップダイアログで出現させる'
    pass

  def show_error(self, msg, title=None):
    'エラーメッセージをポップアップダイアログで出現させる'
    pass

  def show_warnig(self, prompt, title='warning', **options):
    '警告メッセージをポップアップダイアログで出現させる'
    pass
  
  def input_text(msg, title=None):
    '１行テキスト入力を促すダイアログを出現させる'
    pass

  def ask_ok_cancel(self, prompt, title='ask', **options):
    pass

  def ask_yes_no(self, prompt, title='ask', **options):
    pass

  def ask_retry_cacnel(self, prompt, title='retry', **options):
    pass

  def ask_abort_retry_ignore(self, prompt, title='retry', **options):
    pass

  def ask_open_file(self, multiple=False, **options):
    pass

  def ask_save_file(self, **options):
    pass

  def ask_folder(self, **options):
    pass
  
  def execute(cmd, *closure, **kwargs):
    '別スレッドで処理を行う'
    pass

  def invoke_lator(cmd, *closure):
    'GUIスレッドで処理を行う'
    pass

  def invoke_and_wait(cmd, *closure):
    'GUIスレッドで処理を行い、その完了を待つ'
    pass

  def log(self, msg, *args, **kwargs):
    'アプリケーションログを出力する'
    pass

  def find_dialog(self, name, AppClass, master=None, *opts, **kwd):
    'ユーザ定義ダイアログを入手する'
    pass

  def update_title(self, app, msg=None):
    'タイトルバーを更新する'
    pass

  def bind_proc(self, cmd, proc=None):
    'イベント・バインド向けの手続きを入手する'
    pass

  def menu_proc(self, cmd, proc=None):
    'メニュー・バインド向けの手続きを入手する'
    pass

  def find_menu(self, name, entries=(), master=None, proc=None, font=None):
    'tk.Menuを定義の基づいて作成して入手する'
    pass

  def bind(self, sequence=None, func=None, add=None):
    '親コンテナにイベント手続きを割り当てる'
    pass

  def unbind(self, sequence, funcid=None):
    '親コンテナに登録しているイベント手続きを解除する'
    pass

  def timer(self, cmd, delay=None, proc=None, interval=None, repeat=False):
    'タイマーを作成する'
    return Timer()

  def close(self):
    'アプリを閉じる'
    pass

  def hide(self):
    'ウィンドウを隠す'
    pass
  
  def show(self):
    'ウィンドウを表示する'
    pass

  def dispose(self):
    'アプリと関連づくTkリソースを破棄する'
    pass

  def find_status_bar(self, base=None):
    pass

  
def show_error(prompt, title='error', **options):
  """ エラーダイアログ表示 
表示内容はクリップボードに設定される
"""
  if isinstance(prompt, Exception):
    prompt, title = trace_text(prompt)
  root.clipboard_clear()
  root.clipboard_append(prompt)
  messagebox.showerror(title, prompt, **options)


def show_warnig(prompt, title='warning', **options):
  """ 警告ダイアログ表示
表示内容はクリップボードに設定される
 """
  root.clipboard_clear()
  root.clipboard_append(prompt)
  messagebox.showwarning(title, prompt, **options)


def show_info(prompt, title='info', **options):
  """ 情報ダイアログ表示
表示内容はクリップボードに設定される
 """
  root.clipboard_clear()
  root.clipboard_append(prompt)
  messagebox.showinfo(title, prompt, **options)


def ask_ok_cancel(prompt, title='ask', **options):
  """ [OK] [Cancel]　ボタン付の質問ダイアログ表示 """
  return messagebox.askokcancel(title, prompt, **options)


def ask_yes_no(prompt, title='ask', **options):
  """ [Yes] [No]　ボタン付の質問ダイアログ表示 """
  return messagebox.askyesno(title, prompt, **options)


def ask_retry_cacnel(prompt, title='retry?', **options):
  """ [Retry] [Cancel]　ボタン付の警告ダイアログ表示 """
  return messagebox.askretrycancel(title, prompt, **options)


def ask_abort_retry_ignore(prompt, title='retry?', **options):
  """ [Abort] [Retry] [Ignore]　ボタン付の警告ダイアログ表示 """
  options['type'] = messagebox.ABORTRETRYIGNORE
  options['icon'] = messagebox.WARNING
  return messagebox.askquestion(title, prompt, **options)


def ask_color(color=None, **options):
  """ 色選択ダイアログ表示 """
  return colorchooser.askcolor(color, **options)


def input_text(prompt, title='input', **options):
  """ テキスト入力のダイアログ表示 """
  return simpledialog.askstring(title, prompt, **options)

  
def ask_open_file(multiple=False, **options):
  """ ローカル・ファイルを選択させる
    optionsで指定できるパラメータ
  
    defaultextension - 補足サフィックス
    parent - 親ウィンドウ
    title - ダイアログの見出し
    initialdir - 初期ディレクトリ
    mustexist - 存在するディレクトリを選択させる場合はtrue
    filetypes: sequence of (label, pattern) tuples.
  """
  if platform == 'darwin': options.pop('filetypes', None)
  # macOSではファイルタイプの指定ができない（固まる）
  if multiple: return filedialog.askopenfilenames(**options)
  initialdir = options.pop('initialdir', '')
  if initialdir: options['initialdir'] = initialdir
  return filedialog.askopenfilename(**options)
  

def ask_save_file(**options):
  """ 保存用にローカル・ファイルを選択させる
    optionsで指定できるパラメータ
  
    defaultextension - 補足サフィックス
    parent - 親ウィンドウ
    title - ダイアログの見出し
    initialdir - 初期ディレクトリ
    initialfile - 初期選択ファイル
    mustexist - 存在するディレクトリを選択させる場合はtrue
    filetypes: sequence of (label, pattern) tuples.
"""
  if platform == 'darwin': options.pop('filetypes', None)
  # macOSではファイルタイプの指定ができない（固まる）
  initialdir = options.pop('initialdir', '')
  if initialdir: options['initialdir'] = initialdir
  return filedialog.asksaveasfilename(**options)


fonts = weakref.WeakValueDictionary()


def find_font(name):
  """
tkが認識する形式のフォント名を渡して、tkfontオブジェクトを入手する。
あるいは、family-size-weight-slant の形で指定するフォントをロードする。
過去にロードしていれば、同じインスタンスを返す
"""
  if name in fonts:
    font = fonts[name]
    if font: return font
  try:
    font = tkfont.nametofont(name)
    if verbose: trace('name of font', font, type(font), name)
    return font
  except TclError:
    enc = sys.getfilesystemencoding()
    fa = name.split('-')
    # trace(name, fa)
    while len(fa) < 4: fa.append('')
    (family, size, w, s) = fa

    if sys.version_info < (3, 0):
      try:
        if type(family) == unicode: family = family.encode(enc)
        if type(name) == unicode: name = name.encode(enc)
      except:
        pass

  weight = 'bold' if w == 'b' or w == 'bold' else 'normal'
  slant = 'italic' if s == 'i' or w == 'italic' else 'roman'
  if not size: size = 9
  font = tkfont.Font(name=name, family=family, size=size, weight=weight, slant=slant)
  if verbose: trace('tkfont', font, type(font))
  _save_font(font)
  return font


def _save_font(font):
  fn = font.name
  if type(fn) == str:
    try:
      enc = sys.getfilesystemencoding()
      if pyver == 2: fn = unicode(fn, enc)
    except NameError:
      pass

  if fn in fonts: return
  fonts[fn] = font


def find_bold_font(font):
  """指定するフォントのボールドフォントを入手する"""
  fa = font.actual()
  if fa['weight'] == 'bold': return font
  family = fa['family']
  size = int(fa.get('size', 10))
  weight = 'b'
  slant = 'i' if fa['slant'] == 'italic' else 'r'
  return find_font('%s-%d-%s-%s' % (family, abs(size), weight, slant))


class _MenuItem:
  """ メニューの表示項目名と手続きを保持"""

  def __init__(self, name, proc, *var):
    self.name = name
    self.proc = proc
    self.set_status = None
    if len(var) > 0: self.var = var[0]

  def __repr__(self):
    return "%s('%s')" % (self.proc.__name__, self.name)

  def doit(self):
    """メニュー選択で呼ばれる"""
    try:
      self.proc(self.name)
    except TclError as e:
      if self.set_status: self.set_status(str(e))

    except Exception as e:
      if self.set_status: self.set_status(str(e))
      show_error(e)

  def changeit(self):
    """ チェックアイテムやラジオボタンから呼ばれる"""
    self.proc(self.name, self.var.get())

  def change_notify(self, event):
    """ チェックアイテムやラジオボタンから呼ばれる"""
    try:
      self.proc(self.name, event, self.var.get())
      
    except TclError as e:
      if self.set_status: self.set_status(str(e))

    except Exception as e:
      if self.set_status: self.set_status(str(e))
      show_error(e)

  def notify(self, event):
    """イベント連携で呼ばれる"""
    try:
      return self.proc(self.name, event)
    except TclError as e:
      if self.set_status: self.set_status(str(e))

    except Exception as e:
      if self.set_status: self.set_status(str(e))
      show_error(e)


_var_master = None

class StringRef(object):
  "宣言的に利用できる tk.StringVar"

  VariableClass = tk.StringVar
  
  def __init__(self):
    self._vars = weakref.WeakKeyDictionary()

  def ref(self, instance):
    wdic = self._vars
    var = wdic.get(instance, None)
    if not var: wdic[instance] = var = self.VariableClass(master=_var_master)
    return var

  def __get__(self, instance, owner):
    if instance is None: return self
    return self.ref(instance).get()

  def __set__(self, instance, value):
    self.ref(instance).set(value)
    
  def __del__(self, instance): del self._vars[instance]


class IntRef(StringRef):
  VariableClass = tk.IntVar

class BooleanRef(StringRef):
  VariableClass = tk.BooleanVar

class DoubleRef(StringRef):
  VariableClass = tk.DoubleVar

  
# 別スレッドからGUI処理を受け取る間隔(ms)
_polling_interval = 300

_polling_timer = None

# ステータスバー表示メッセージ消去のDelay
_status_interval = 5000

# スレッドプールの最大平行処理数
_max_workers = int(os.environ.get('MAX_WORKERS','40'))

# スレッドプール
_executor = None

# 非同期処理をGUIスレッドに引き渡すためのキュー
_app_queue = Queue()


def _polling_queues():
  #非同期にGUI処理を行うための仕掛け
  global _polling_timer

  # キューから処理対象の手続きを取り出して、Tkが暇なときに動作するキューに詰め込み直す
  while True:
    #trace("_polling_queues ..", file=sys.stderr)
    try:
      task = _app_queue.get(block=False)
    except Empty:
      break
    else:
      root.after_idle(task)
      if verbose: trace('#idel task', task)
      
  _polling_timer = root.after(_polling_interval, _polling_queues)


class _Toplevel(tk.Toplevel):
  """ トップレベルウィンドウの件数を数えて、なくなったら終了させる"""
  def __init__(self, master=None, *args, **kargs):
    if not master: master = _find_root(os.environ.get("SCREEN", None))
    tk.Toplevel.__init__(self, master, *args, **kargs)
    self.is_dialog = isinstance(master, _Toplevel)
    self.__inc()
    self.focused_widget = self

  def __inc(self):
    if self.is_dialog: return
    global _frame_count, root
    _frame_count += 1
    try:
      root.winfo_id()
    except TclError as e:
      if verbose: trace('TRACE: %s (%s)' % (e, e.__class__.__name__), file=sys.err)
      # root が利用できなくなっているようだから置き換える
      root = self._root()
      root.update()
      root.withdraw()

  def exit(self):
    root.quit()
    if verbose: trace('TRACE: root quit.', file=sys.stderr)

  def __dec(self):
    if self.is_dialog: return
    global _frame_count
    _frame_count -= 1
    if _frame_count <= 0: self.exit()

  def destroy(self):
    """widgetを破棄する"""
    try:
      if hasattr(self.cc, 'polling_timer'):
        root.after_cancel(self.cc.polling_timer)
      self.cc._release()
    except:
      pass
    self.hide()
    tk.Misc.destroy(self)

  def hide(self):
    """表示を隠す"""
    # http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/
    self.update()
    self.withdraw()
    self.__dec()

  def show(self):
    """表示する"""
    self.update()
    self.deiconify()
    self.__inc()
    
  def dispose(self):
    self.destroy()
  
  def wakeup(self):
    try:
      if self.wm_state() == 'iconic':
        self.wm_withdraw()
        self.wm_deiconify()
      self.tkraise()
      self.focused_widget.focus_set()
    except TclError:
      # This can happen when the window menu was torn off.
      # Simply ignore it.
      pass

  def _set_transient(self, master, relx=0.5, rely=0.3):
    if not master: return
    widget = self
    widget.withdraw()  # Remain invisible while we figure out the geometry
    widget.transient(master)
    widget.update_idletasks()  # Actualize geometry information
    if master.winfo_ismapped():
      m_width = master.winfo_width()
      m_height = master.winfo_height()
      m_x = master.winfo_rootx()
      m_y = master.winfo_rooty()
    else:
      m_width = master.winfo_screenwidth()
      m_height = master.winfo_screenheight()
      m_x = m_y = 0
    w_width = widget.winfo_reqwidth()
    w_height = widget.winfo_reqheight()
    x = m_x + (m_width - w_width) * relx
    y = m_y + (m_height - w_height) * rely
    if x + w_width > master.winfo_screenwidth():
      x = master.winfo_screenwidth() - w_width
        # elif x < 0:
        #    x = 0
    if y + w_height > master.winfo_screenheight():
      y = master.winfo_screenheight() - w_height
    elif y < 0:
      y = 0
    widget.geometry('+%d+%d' % (x, y))
    widget.deiconify()  # Become visible at the desired location


class _AsyncTask:
  """非同期呼び出しをサポートするためのクラス
    別スレッドに呼び出しパラメータを引き渡すのと、
そのスレッドで生じた例外をキャッチしてエラー情報をGUIスレッドに渡す
"""
    
  def __init__(self, cmd, proc, closure, kwds):
    self.cmd = cmd
    self.proc = proc
    self.closure = closure
    self.kwds = kwds
    self.flag = False
    self.error = None
    self.msg = None

  def call(self):
    # このメソッドはGUIとは別のスレッドで動作する
    try:
      if verbose: trace('#task call', self.cmd, self.proc, self.closure, self.kwds, file=sys.stderr)
      rc = self.proc(self.cmd, *self.closure, **self.kwds)
      self.flag = True
      return rc
    except Exception as e:
      # show_error(msg)　# そのまま表示しようとすると固まった
      msg, title = trace_text(e)
      trace(msg, self.proc, file=sys.stderr)
      self.error = e
      self.msg = msg
      _app_queue.put(self.notify)
      return e
    
  def notify(self):
    """ EDTでダイアログを表示する"""
    show_error(self.msg, '%s - Internal Error' % self.error.__class__.__name__)


def application_name(app):
  """アプリケーション名の入手"""
  app_name = app.application_name if hasattr(app, "application_name") else \
    app.title if hasattr(app, "title") else None
  if not app_name: app_name = app.__class__.__name__
  trace(app_name)
  return app_name


def _entry_all_select(ev):
  ent = ev.widget
  ent.select_range(0, END)
  ent.icursor(END)
  return 'break'

def _text_all_select(ev):
  buf = ev.widget
  buf.tag_remove(SEL, '1.0', END)
  buf.tag_add(SEL, '1.0', END)
  buf.mark_set(INSERT, '1.0')
  buf.see(INSERT)
  return 'break'


def _text_select_present(buf):
  """バッファの範囲指定がされているか判定する"""
  try:
    pf = buf.index(SEL_FIRST)
    pl = buf.index(SEL_LAST)
    return not pl == pf
  except tk.TclError:
    return False


tk.Text.select_present = _text_select_present


def _top_bind(top):
  top.bind_class('Entry', '<Control-a>', _entry_all_select)
  top.bind_class('TEntry', '<Control-a>', _entry_all_select)
  top.bind_class('TCombobox', '<Control-a>', _entry_all_select)
  top.bind_class('Text', '<Control-a>', _text_all_select)

  
class _TkTimer(Timer):
  '''コマンド付きのタイマー操作'''
  def __init__(self, cmd, delay=None, proc=None, interval=None, repeat=False):
    self.cmd = cmd
    self.interval = interval # sec
    self.proc = proc
    self.timer = None
    self.delay = delay # sec
    self.count = 0
    self.repeat = True if interval else repeat

  def _timeout(self):
    try:
      self.count += 1
      self.proc(self.cmd, self)
    finally:
      if self.repeat:
        last = self.last
        delay = self.interval -  (now() - last)
        while delay < 0: delay += self.interval
        self.timer = root.after(int(delay * 1000), self._timeout)
      
  def start(self):
    delay = self.interval if self.repeat else self.delay
    self.last = now()
    self.timer = root.after(int(delay * 1000), self._timeout)

  def stop(self):
    if not self.timer: return
    root.after_cancel(self.timer)
    self.timer = None

  def restart():
    self.stop()
    self.start()

    
class _TkAppContext(AppContext):

  def execute(self, cmd, *closure, **kwargs):
    """タスクをスレッド・プール経由で動作させる """
    global _executor, _polling_timer
    if not _executor:
      _executor = concurrent.futures.ThreadPoolExecutor(max_workers=_max_workers, thread_name_prefix='tke')
    if not _polling_timer: _polling_timer = root.after(_polling_interval, _polling_queues)
    proc = kwargs.get('proc', self._apps[-1].execute_task)
    if verbose: trace('async proc', proc, _max_workers, '\n', _executor)
    task = _AsyncTask(cmd, proc, closure, kwargs)
    task.app = self
    res = _executor.submit(self._run_task, task)

  def _run_task(self, task):
    # 別スレッドで動作する
    if verbose: trace('async call', task)
    th = threading.currentThread()
    th.task = task
    return task.call()

  def invoke_lator(self, cmd, *closure, **kwds):
    """GUIの処理キューに処理を登録する"""
    th = threading.currentThread()
    task = _AsyncTask(cmd, th.task.proc, closure, kwds)
    task.app = self
    _app_queue.put(task.call)
    if verbose: trace('#invoke_lator', cmd, task.proc, closure, kwds)

  def invoke_and_wait(self, cmd, *closure, **kwds):
    """GUIに処理を依頼して完了するまで待つ"""
    th = threading.currentThread()
    th.task.flag = False
    task = _AsyncTask(cmd, th.task.proc, closure, kwds)
    task.app = self
    _app_queue.put(task.call)
    if verbose: trace('#invoke_and_wait', cmd, task.proc, closure, kwds)
    while not task.flag: sleep(0.2)

  def __init__(self):
    self._last_status = None
    self._blist = []
    self._bind_map = {}
    self.menu = {}  # メニュー・アイテム名でメニュー・アイテムが引ける
    self._menu_map = {}  # メニュー名でメニューインスタンスを引ける
    self._log_level = INFO
    self._dialogs = {} # 関連するダイアログのインスタンスを入手する
    self._notify_timer = None
    
  def log(self, msg, *args, **kwargs):
    """ログ出力のための簡易メソッド。
デフォルトはINFOレベル
"""
    level = kwargs.pop('level', self._log_level)
    trace(msg % args if '%' in msg else msg, file=sys.stderr)

  def ref(self, name, app=None):
    # アプリケーションに定義されている宣言式のVariable変数を入手する
    if not app: app = self._apps[-1]
    name = name.split('/')[0]
    refs = app.__class__.__dict__.get(name)
    return refs.ref(app) if refs else None

  def _configure_notify(self, ev):
    timer, top = self._notify_timer, self.top
    if timer: top.after_cancel(timer)
    self._notify_timer = top.after(500, lambda le=ev: self._configure_proc(le))

  def _configure_proc(self, ev):
    # 位置が変わったら呼び出される
    self._notify_timer = None
    top = self.top
    geom = top.geometry()
    w = top.winfo_width()
    h = top.winfo_height()
    x = top.winfo_x()
    y = top.winfo_y()
    rx = top.winfo_rootx()
    ry = top.winfo_rooty()

    if verbose:
      trace('geometry', geom)
      trace('wi', w, h, x, y, rx, ry)
    
  def _setup_widget(self, wi, level='', dump=False, app=None):
    # テーマや追加のメニュー等を作成する
    setup_theme(wi)

    if isinstance(wi, (Entry, tk.Entry, Combobox)):
      var = self.ref(wi._name, app)
      if var: wi['textvariable'] = var
      if verbose: trace('binding textvariable', wi._name, 'var', var, wi, var.get() if var else '')
      if hasattr(wi, 'label'): self.bind_focus(wi, wi.label)
        
    if isinstance(wi, (Entry, Combobox)):
      register_entry_popup(wi)
        
    elif isinstance(wi, (Button, tk.Button)):
      self.bind_focus(wi)

    elif isinstance(wi, (Checkbutton, tk.Checkbutton)):
      var = self.ref(wi._name, app)
      if var: wi['variable'] = var
      if verbose: trace('binding variable', wi._name, 'var', var, wi, var.get() if var else '')
      self.bind_focus(wi)

    elif isinstance(wi, (Radiobutton, tk.Radiobutton)):
      var = self.ref(wi._name, app)
      if var: wi['variable'] = var
      if verbose: trace('binding variable', wi._name, 'var', var, wi, var.get() if var else '')
      val = wi._name.split('/')
      if len(val) > 1: wi['value'] = val[1]
      self.bind_focus(wi)
        
    elif isinstance(wi, Text): register_text_popup(wi)
    elif isinstance(wi, Treeview): register_tree_bind(wi)
    elif isinstance(wi, (Label, tk.Label)):
      var = self.ref(wi._name, app)
      if var: wi['textvariable'] = var
      if hasattr(wi, 'label_for'):
        self.bind_focus(wi.label_for, wi)
        
    if dump: trace('%s' % level, wi.__class__.__name__)
    for w2 in wi.winfo_children():
      self._setup_widget(w2, level=level + ' ', dump=dump)

  def _create_app(self, app):
    global _var_master
    self._apps = [app]
    self.top = top = _var_master = _Toplevel()
    app.cc = self  # ここで共通機能を提供するインスタンスを差し込む
    fr = Frame(top, name='base').pack(side='top', fill=BOTH, expand=1)
    app.create_widgets(fr)
    self._setup_widget(fr, dump=os.environ.get('DUMP_WIDGET', ''))
    fr.focus_set()
    bar = app.create_menubar()
    if bar: top.configure(menu=bar) # メニューバーがあれば設定する
    self.update_title(app)
    _top_bind(top)
    self._notify = top.bind("<Configure>", self._configure_notify)
    return top

  def _create_dialog(self, AppClass, *opts, **kwd):
    """ダイアログとして利用するMuClientをインスタンス化する
    AppClass のインスタンスが返る
    """
    global _var_master
    master = kwd.pop('master', self.top)

    if opts or kwd:
      app = AppClass(*opts, **kwd)
    else:
      app = AppClass()

    cc = self.__class__()
    cc._apps = [app]
    cc.top = top = _var_master = _Toplevel(master)
    app.cc = cc
    fr = Frame(top).pack(side='top', fill=BOTH, expand=1)
    app.create_widgets(fr)
    cc._setup_widget(fr, dump=os.environ.get('DUMP_WIDGET', ''))
    cc.update_title(app)
    top.focus()
    top._set_transient(master)
    _top_bind(top)
    return app

  def find_dialog(self, name, AppClass, master=None, *opts, **kwd):
    """ダイアログとして利用するUIClientを入手する
        AppClass のインスタンスが返る
    """
    if not master: master = self.top
    dig = self._dialogs.get(name, None)
    if dig:
      if not isinstance(dig, AppClass):
        raise ValueError('dialog is not %s' % AppClass)
    else:
      self._dialogs[name] = dig = self._create_dialog(AppClass, master=master, *opts, **kwd)
      
    return dig
  
  def remove_client(self, app=None, in_destroy=False):
    """ 管理対象のクライアントを削除する"""
    if not app: app = self._apps[-1]
    if app in self._apps: self._apps.remove(app)
    try:
      app.release()
    except Exception as e:
      self.log('while release: %s (%s)', e, e.__class__.__name__, level=ERROR)

    #pm = self._post_windows.get(str(app), None)
    #if pm: unregister_windowlist_callback(pm)
    if not self._apps:
      if not in_destroy: self.top.destroy()
      return

    # 前のclientに戻す
    app = self._apps[-1]
    self.menu = app.menu
    self.top.configure(menu=app.menubar)
    self.update_title(app)

  def update_title(self, app, msg=None):
    app_name = application_name(app)
    if not msg: msg = app.get_title() if hasattr(app, "get_title") else app.title
    msg = "%s - %s" % (msg, app_name) if msg else app_name
    self.top.title(msg)
    
  def _release(self, in_destroy=True):
    """管理対象のクライアントのreleaseを呼び出す"""
    for app in reversed(self._apps):
      self.remove_client(app, in_destroy)

  def _perform(self, cmd, *args):
    """メニューで選択したら呼び出される手続き"""
    trace(cmd, args, file=sys.stderr)

  def _find_menu_item(self, cmd, proc):
    if not proc: proc = self._perform
    cmd_key = '%s.%s' % (cmd, proc.__name__)
    if cmd_key in self._bind_map: return self._bind_map[cmd_key]
    mi = _MenuItem(cmd, proc)
    if hasattr(self, 'status'): mi.set_status = self.set_status
    self._bind_map[cmd_key] = mi
    return mi

  def bind_proc(self, cmd, proc=None):
    """キー割り当てに利用する手続きを返す"""
    return self._find_menu_item(cmd, proc).notify

  def menu_proc(self, cmd, proc=None):
    """メニュー割り当てに利用する手続きを返す"""
    return self._find_menu_item(cmd, proc).doit

  def find_menu(self, name, entries=(), master=None, proc=None, font=None):
    """ メニュー定義テキストよりメニュー・インスタンスを作成する
    param: entries メニュー項目を定義した配列
    """
    if not proc: proc = self._perform
    if not master: master = self.top

    if verbose: trace(name, entries)
    for me in entries:
      en = me[0].split(';')[0]
      self._menu_map[en] = menu = self._create_menu(me, master, proc, font)

    if verbose: trace("menu keys", en, menu.keys())

    names = name.split(':')
    if len(names) == 1:
      menu = self._menu_map.get(name, None)
    else:
      # 複数のエントリをルックアップする（メニューバー用）
      menu = tk.Menu(master, tearoff=False)
      for mn in names:
        sub = self._menu_map.get(mn, None)
        if not sub: continue
        un, cap = item_caption(sub._ent.split(';')[1])
        menu.add_cascade(label=cap, under=un, menu=sub)
      
    return menu

  def _create_menu(self, entries, master=None, proc=None, font=None):
    """ メニュー定義テキストよりメニュー・インスタンスを作成する
param: entries メニュー項目を定義した配列
"""
    menu = tk.Menu(master, tearoff=False)
    rg = StringVar()
    menu._ent = ent = entries[0]
    if type(ent) in (str, unicode):
      cmd = ent.split(';')[0]
      if cmd:
        self.menu[cmd] = rg
        self.menu['%s.menu' % cmd] = menu
        # メニューが表示される前に呼び出されるフックを登録
        menu.config(postcommand=self.menu_proc('%s.post' % cmd, proc))

    for ent in entries[1:]:
      if type(ent) in (list, tuple):
        # 入れ子のメニューを構成
        sub = self._create_menu(ent, menu, proc, font)
        md = ent[0].split(';')
        while len(md) < 4: md.append('')
        un, cap = item_caption(md[1])
        menu.add_cascade(label=cap, under=un, menu=sub)
        continue

      id = ent.split(';')
      while len(id) < 4: id.append('')
      un, cap = item_caption(id[1])
      cmd, shortcut, icon_name = id[0], id[2], id[3]
      icon = find_image(icon_name)
      if platform == 'darwin': shortcut = shortcut.replace('ctrl-', 'Command-')
        
      if cap == '': cap = cmd
      mi = _MenuItem(cmd, proc)

      if cmd == '-' or not cmd:
        menu.add_separator()
        rg = StringVar()
        continue
      
      elif cmd[0] == '+':
        # チェック・メニュー項目
        cv = IntVar()
        mi = _MenuItem(cmd[1:], proc, cv)
        menu.add_checkbutton(label=cap, under=un, variable=cv,
                             command=mi.changeit, font=font, accelerator=shortcut)
        self.menu[cmd[1:]] = cv
        
      elif cmd[0] == '*':
        # 選択メニュー項目
        mi = _MenuItem(cmd[1:], proc, rg)
        menu.add_radiobutton(label=cap, under=un, variable=rg, value=mi.name,
                             command=mi.changeit, font=font, accelerator=shortcut)
        self.menu[cmd[1:]] = rg

      else:
        # 一般メニュー項目
        mi = _MenuItem(cmd, proc)
        try:
          menu.add_command(label=cap, under=un, command=mi.doit,
                           font=font, accelerator=shortcut, compound='left', image=icon)
        except TclError:
          menu.add_command(label=cap, under=un, command=mi.doit,
                           font=font, accelerator=shortcut)

      if shortcut:
        #アクセラレータ向けのテキストをバインド向けに調整
        bind_key = shortcut #.lower()
        for acl, sym in (
            ('ctrl-', 'Control-'),
            ('command-', 'Command-'),
            ('--','-minus'),
            ('-+', '-equal' if platform == 'darwin' else '-plus' ),
        ): bind_key = bind_key.replace(acl, sym)
        
        bind_seq = '<%s>' % bind_key

        if verbose: trace('accelerator', cmd, bind_seq )
        try:
          if cmd[0] in ('+','*'):
            self.bind(bind_seq, mi.change_notify)
          else:
            self.bind(bind_seq, mi.notify)
        except TclError as e:
          trace(cmd, bind_seq, e)
          
    return menu

  def bind_focus(self, ent, label=None):
    if not ent or platform == 'darwin': return
    
    if label:
      text = label.cget('text')
      pos = label.cget('underline')
    elif isinstance(ent, (Button, tk.Button)):
      text = ent.cget('text')
      pos = ent.cget('underline')
    else:
      return
    if pos < 0: return # 未設定
    
    keysym = text[pos].lower()
    if isinstance(ent, (Entry, Combobox, tk.Entry)):
      self.bind('<Alt-%s>' % keysym, lambda event, wi=ent: entry_focus(wi))
    elif isinstance(ent, (Button, tk.Button)):
      self.bind('<Alt-%s>' % keysym, lambda ev, wi=ent: wi.focus_set() or wi.invoke())

  def bind(self, sequence=None, func=None, add=None):
    funcid = self.top.bind(sequence, func, add)
    self._blist.append((sequence, func, add, funcid))
    return funcid
  
  def _rebind_all(self, last_bind_list):
    # 同じ内容を再バインドする
    blist = []
    top = self.top
    for sequence, func, add, _ in last_bind_list:
      funcid = top.bind(sequence, func, add)
      blist.append((sequence, func, add, funcid))
    self._blist = blist
 
  def _unbind_all(self):
    # 過去にバイドした内容を全部解放する
    top = self.top
    for sequence, func, add, funcid in self._blist:
      top.unbind(sequence, funcid)
   
  def unbind(self, sequence, funcid=None):
    self.top.unbind(sequence, funcid)

  def timer(self, cmd, delay=None, proc=None, interval=None, repeat=False):
    # タイマーの生成
    if not proc: proc = self._apps[-1].perform
    tt = _TkTimer(cmd, delay, proc, interval, repeat)
    return tt

  def close(self):
    self.remove_client()

  def hide(self): self.top.hide()
  def show(self): self.top.show()
    
  def dispose(self):
    while self._apps:
      self.remove_client()
      
  destroy = dispose

  def _update_status(self):
    """一定時間経過したらステータスを空にする"""
    self.status_timer = None
    self._status.set('')

  def _set_status(self, msg, *args):
    """ステータスバーに表示するテキストの設定"""
    tmsg = msg % args if '%' in msg else msg
    self._last_status = tmsg

    #self.log(msg, *args)
    if hasattr(self, '_status'):
      self._status.set(tmsg)
      if self.status_timer: root.after_cancel(self.status_timer)
      self.status_timer = root.after(_status_interval, self._update_status)

  def set_status(self, msg, *args):
    self._set_status(msg, *args)

  @property
  def status(self):
    return self._last_status

  @status.setter
  def status(self, msg):
    return self._set_status(msg)

  def find_status_bar(self, base=None):
    """ステータスバーを入手する。まだ作成されていなければ作成する """
    if not base: base = self.top
    if hasattr(base, 'status_bar'): return base.status_bar
    fr = Frame(base).pack(side=BOTTOM, fill='x')
    self._status = var = StringVar()
    self.status_timer = None
    ent = tk.Entry(fr, textvariable=var, takefocus=0, state='readonly', relief='flat')
    ent.pack(side=LEFT, fill=BOTH, expand=1)
    base.status_bar = fr
    return fr

  def set_clipboard_text(self, text):
    """ クリップボードにテキストを設定する"""
    root.clipboard_clear()
    root.clipboard_append(text)

  def show_error(self, prompt, title='error', **options):
    """ エラーダイアログ表示 """
    options['parent'] = self.top
    show_error(prompt, title, **options)

  def show_warnig(self, prompt, title='warning', **options):
    """ 警告ダイアログ表示 """
    options['parent'] = self.top
    show_warnig(prompt, title, **options)

  def show_info(self, prompt, title='info', **options):
    """ 情報ダイアログ表示 """
    options['parent'] = self.top
    show_info(prompt, title, **options)
    
  def ask_ok_cancel(self, prompt, title='ask', **options):
    """ [OK] [Cancel]　ボタン付の質問ダイアログ表示 """
    options['parent'] = self.top
    return ask_ok_cancel(prompt, title, **options)

  def ask_yes_no(self, prompt, title='ask', **options):
    """ [Yes] [No]　ボタン付の質問ダイアログ表示 """
    options['parent'] = self.top
    return ask_yes_no(prompt, title, **options)

  def ask_retry_cacnel(self, prompt, title='retry', **options):
    """ [Retry] [Cancel]　ボタン付の警告ダイアログ表示 """
    options['parent'] = self.top
    return ask_retry_cacnel(prompt, title, **options)

  def ask_abort_retry_ignore(self, prompt, title='retry', **options):
    options['parent'] = self.top
    return ask_abort_retry_ignore(prompt, title, **options)

  def ask_color(self, color=None, **options):
    """ 色選択ダイアログ表示 """
    options['parent'] = self.top
    return ask_color(color, **options)

  def input_text(self, prompt, title='input', **options):
    """ テキスト入力のダイアログ表示 """
    options['parent'] = self.top
    return input_text(prompt, title, **options)

  def ask_open_file(self, multiple=False, **options):
    """ ローカル・ファイルを選択させる
    optionsで指定できるパラメータ

    defaultextension - 補足サフィックス
    parent - 親ウィンドウ
    title - ダイアログの見出し
    initialdir - 初期ディレクトリ
    mustexist - 存在するディレクトリを選択させる場合はtrue
    filetypes: sequence of (label, pattern) tuples.
"""
    options['parent'] = self.top
    return ask_open_file(multiple=multiple, **options)

  def ask_save_file(self, **options):
    """ 保存用にローカル・ファイルを選択させる
    optionsで指定できるパラメータ

    defaultextension - 補足サフィックス
    parent - 親ウィンドウ
    title - ダイアログの見出し
    initialdir - 初期ディレクトリ
    initialfile - 初期選択ファイル
    mustexist - 存在するディレクトリを選択させる場合はtrue
    filetypes: sequence of (label, pattern) tuples.
"""
    options['parent'] = self.top
    return ask_save_file(**options)

  def ask_folder(self, **options):
    """ 保存用にローカル・ディレクトリを選択させる
TK8.3から利用できる
"""
    options['parent'] = self.top
    initialdir = options.pop('initialdir', '')
    if initialdir: options['initialdir'] = initialdir
    return filedialog.askdirectory(**options)


class UIClient(object):
  'GUIアプリケーションのユーザコードで実装するメソッドの定義'

  def create_widgets(self, base):
    '''このタイミングでユーザコードはGUIを組み立てる
  baseにはGUIパーツを組み立てる場所が渡されてくる。（通常はフレーム）'''
    pass

  def create_menubar(self):
    '''アプリケーションが固有メニューを提供する場合、このタイミングで作成する'''
    pass

  def execute_task(self, cmd, *closure, **option):
    '''別スレッドで動作する処理'''
    trace('execute', cmd, closure)

  title = '' # このプロパティからタイトルを入手する
  
  cc = AppContext() # このプロパティに共通機能を提供するインスタンスを差し込む

  def release(self):
    pass

  
class AppException(Exception):
  """アプリケーション例外のベースクラス """
  pass


class App(UIClient):
  """GUIアプリケーションのユーザコードが継承するクラス"""

  @classmethod
  def run(Cls, args=(), *opts, **kwopts):
    top = Cls.start(*opts,**kwopts)
    if platform == 'darwin':
      # アプリケーション（自身）を手前に持ってくるためのAPI呼び出し
      try:
        from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
        app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
        app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
      except: pass
      
    top.after_idle(top.tkraise) # ウィンドウを手前にもってくる
    retry = 1
    while retry:
      try:
        root.mainloop() # イベントループに入る
        retry = 0
      except Exception as e:
        msg, title = trace_text(e)
        trace('Warn: ', title, ' in mainloop ', msg)

    if verbose: trace('done.')

  @classmethod
  def start(Cls, *args, **opts):
    app = Cls(*args,**opts)
    cc = _TkAppContext()
    top = cc._create_app(app)
    top.lift()
    top.after_idle(top.tkraise) # ウィンドウを手前にもってくる
    return top
              
  def bind_proc(self, cmd, proc=None):
    """ キー割り当てに利用する手続きを返す"""
    if not proc: proc = self.perform
    return self.cc.bind_proc(cmd, proc)

  def menu_proc(self, cmd, proc=None):
    """ メニュー割り当てに利用する手続きを返す"""
    if not proc: proc = self.perform
    return self.cc.menu_proc(cmd, proc)

  def find_menu(self, name, entries=(), master=None, proc=None, font=None):
    """メニュー定義テキストよりメニュー・インスタンスを作成する"""
    if not proc and hasattr(self, 'perform'): proc = self.perform
    if not entries and hasattr(self, 'menu_items'): entries = self.menu_items
    return self.cc.find_menu(name, entries, master, proc, font)

  def perform(self, cmd, *args):
    """メニューで選択したら呼び出される手続き"""
    trace(cmd, args, file=sys.stderr)
  
  def close(self):
    self.cc.close()

  def dispose(self):
    self.cc.dispose()

  def create_menubar(self):
    if hasattr(self, 'menu_bar'):
      return self.find_menu(self.menu_bar)

  def execute_task(self, cmd, *closure, **options):
    trace('execute', cmd, closure, options, file=sys.stderr)
    
_frame_count = 0

verbose = int(os.environ.get('VERBOSE', '0'))

root = None
style = None

def _find_root(*args,**opts):
  """アプリケーション全体制御用のウィジェットの作成
  パッケージを取り込んだだけでルートを作成しないように調整している
  """
  global root, style
  try:
    if root: return root
    root = tix.Tk(*args,**opts) if tix else tk.Tk(*args,**opts)
    root.state('withdrawn')  # 普段から表示しない

  except TclError as e:
    if verbose:
      sys.stderr.write('WARN: while Tk initialize: %s\n%s\n%s\nroot:%s\n' % (
        e, format_exc(), '\n'.join(sys.path), root))
    else:
      sys.stderr.write('WARN: while Tk initialize: %s\n' % e)

  style = ttk.Style(root)


def setup_theme(wi):
  """"ttkのスタイルを適用する"""
  if platform == 'darwin':
    # https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm
    # https://github.com/nomad-software/tcltk/blob/master/dist/library/ttk/aquaTheme.tcl
    if isinstance(wi, (Text, Listbox, Canvas)):
      wi.configure(highlightbackground='systemBevelInactiveDark',
#      wi.configure(highlightbackground='red',
                   borderwidth='1',
                    highlightcolor='systemHighlight')
  return wi


if platform == 'darwin':
  _mc = re.compile(r'[(][&](\w+)[)]')

  def item_caption(item):
    """
    メニュー・アイテムに含まれる& の位置と、それを除いたテキストを返す
    macOSでは ニモニックは除外する
    """
    item = _ucs(item)
    p = item.find('&')
    if p < 0:
      return -1, item
    elif p == 0:
      return -1, item[1:]

    if _mc.search(item): return -1, _mc.sub('', item)
    return -1, item.replace('&', '')

else:
  def item_caption(item):
    """メニュー・アイテムに含まれる& の位置と、それを除いたテキストを返す"""
    item = _ucs(item)
    p = item.find('&')
    if p < 0:
      return -1, item
    elif p == 0:
      return 0, item[1:]

    return p, item[0:p] + item[p + 1:]

  

def entry_focus(ent):
  """Entryにフォーカスを当てる"""
  ent.focus_set()
  ent.select_range(0, END)
  ent.icursor(END)
  return ent


class _EntryPopup():
  """Entry に簡易ポップアップメニューを付与する"""

  def __init__(self, ent=None):
    self.buf = ent
    menu = tk.Menu(ent if ent else root, tearoff=0)
    self.menu = menu
    for me, proc in (
        ('cut;切り取り(&T)', self.cut),
        ('copy;コピー(&C)', self.copy),
        ('paste;貼り付け(&P)', self.paste),
        ('select_all;全て選択(&A)', self.select_all),
    ):
      cmd, item = me.split(';')
      # あとで言語によってitemを切り替える処理を入れる
      
      un, cap = item_caption(item)
      menu.add_command(label=cap, underline=un, command=proc)
      menu.config(postcommand=self._post)

  def _post(self):
    # 切り取りとコピーのstatの調整
    stat = tk.ACTIVE if self.buf.select_present() else tk.DISABLED
    menu = self.menu
    menu.entryconfigure(0, state=stat)
    menu.entryconfigure(1, state=stat)

  def _bind(self, ent):
    menu = self.menu

    def popup(event):
      self.buf = event.widget
      menu.tk_popup(event.x_root, event.y_root)
      return 'break'

    def popup_app(event):
      self.buf = event.widget
      menu.tk_popup(event.widget.winfo_rootx(), event.widget.winfo_rooty())
      return 'break'

    ent.bind('<Control-Button-1>', popup)
    ent.bind('<Button-%d>' % (2 if sys.platform == 'darwin' else 3,), popup)
    ent.bind('<Shift-F10>', popup_app)
    try:
      ent.bind('<App>', popup_app)
    except:
      pass  # for cygwin/X
    try:
      ent.bind('<Menu>', popup_app)
    except:
      pass
    ent.shortcut = None
    
  def cut(self):
    buf = self.buf
    if not buf.select_present(): return
    pf = buf.index(SEL_FIRST)
    pe = buf.index(SEL_LAST)
    text = buf.get()[pf:pe]
    buf.delete(SEL_FIRST, SEL_LAST)
    buf.clipboard_clear()
    buf.clipboard_append(text)

  def copy(self):
    buf = self.buf
    if not buf.select_present(): return
    pf = buf.index(SEL_FIRST)
    pe = buf.index(SEL_LAST)
    text = buf.get()[pf:pe]
    buf.clipboard_clear()
    buf.clipboard_append(text)

  def paste(self):
    buf = self.buf
    if buf.select_present(): buf.delete(SEL_FIRST, SEL_LAST)
    try:
      text = buf.selection_get(selection='CLIPBOARD')
      buf.insert(INSERT, text)
    except tk.TclError:
      pass
    
  def select_all(self):
    buf = self.buf
    buf.select_range(0, END)
    buf.icursor(END)
    

def entry_store(ent, text, limit=30):
  """Comboboxに選択テキストを追加する"""
  if not text: return
  values = list(ent.cget('values'))
  if text in values: values.remove(text)
  values.insert(0, text)
  ent['values'] = values[:limit]
  return ent

ttk.Combobox.store = entry_store

def register_shortcut(target, shortcut):
  """ポップアップメニューを登録する"""
  if not shortcut: return

  def popup(event):
    shortcut.tk_popup(event.x_root, event.y_root)
    return 'break'

  def popup_app(event):
    shortcut.tk_popup(event.widget.winfo_rootx(), event.widget.winfo_rooty())
    return 'break'

  target.bind('<Control-Button-1>', popup)
  target.bind('<Button-%d>' % (2 if platform == 'darwin' else 3), popup)
  target.bind('<Shift-F10>', popup_app)
  try:
    target.bind('<App>', popup_app)
  except:
    pass  # for cygwin/X
  try:
    target.bind('<Menu>', popup_app)
  except:
    pass
  # if need_unpost: shortcut.bind('<FocusOut>', lambda ev, wi=shortcut: wi.unpost())
  target.shortcut = shortcut
  return target


_entry_popup = None


def register_entry_popup(ent):
  global _entry_popup
  if not _entry_popup: _entry_popup = _EntryPopup(ent)
  if not hasattr(ent, 'shortcut'): _entry_popup._bind(ent)
  return ent


class _TextPopup(_EntryPopup):
  """テキストウィジェットに簡易ポップアップメニューを付与する"""

  def cut(self):
    buf = self.buf
    if not _text_select_present(buf): return
    text = buf.get(SEL_FIRST, SEL_LAST)
    buf.delete(SEL_FIRST, SEL_LAST)
    buf.clipboard_clear()
    buf.clipboard_append(text)

  def copy(self):
    buf = self.buf
    if not _text_select_present(buf): return
    pf = buf.index(SEL_FIRST)
    pe = buf.index(SEL_LAST)
    text = buf.get(pf, pe)
    buf.clipboard_clear()
    buf.clipboard_append(text)
    
  def paste(self):
    buf = self.buf
    try:
      text = buf.selection_get(selection='CLIPBOARD')
      if _text_select_present(buf): buf.delete(SEL_FIRST, SEL_LAST)
      buf.insert(INSERT, text)
    except TclError:
      pass

  def select_all(self):
    buf = self.buf
    buf.tag_add(SEL, "1.0", END)
    buf.mark_set(INSERT, "1.0")
    buf.see(INSERT)

    
_text_popup = None


def register_text_popup(buf):
  global _text_popup
  if not _text_popup: _text_popup = _TextPopup(buf)
  if not hasattr(buf, 'shortcut'): _text_popup._bind(buf)
  return buf


try:
  if sys.version_info < (3, 0):
    from idlelib.ToolTip import ToolTip, ListboxToolTip

    def set_tool_tip(btn, text):
      """ツールチップを表示する"""
      if type(text) == list or type(text) == tuple:
        ListboxToolTip(btn, text)
      else:
        ToolTip(btn, text)
  else:
    from idlelib.tooltip import Hovertip

    def set_tool_tip(btn, text):
      """ツールチップを表示する"""
      Hovertip(btn, text)

except ImportError as e:
  sys.stderr.write("WARN: cannot use tooltip: %s\n" % e)

  def set_tool_tip(btn, text):
    pass

# 画像のキャッシュ用
images = {}

def find_image(image_name):
  """パスを探索して画像を読み込む"""
  if not image_name: return None
  image_name = image_name.strip()
  if not image_name: return None
  
  if image_name in images: return images[image_name]
  img = None
  try:
    # trace("findImage",zipboot, file=syserr)
    fpath = []
    fpath.extend(sys.path)
    fpath.append(os.getcwd())
    
    for pt in fpath:
      #trace(pt, "..", file=sys.stderr)
      if not os.path.exists(pt): continue
      if zipfile.is_zipfile(pt):
        try:
          with zipfile.ZipFile(image_name) as zf:
            img = tk.PhotoImage(data=zf.read(image_name))
            # trace("read from %s in %s" % (imageName, pt))
            break
        except:
          continue

      fn = os.path.join(pt, image_name)
      if os.path.exists(fn):
        img = tk.PhotoImage(file=fn)
        break

      fn = fn.replace('/', '\\')
      #trace(fn, "..", file=sys.stderr)
      if os.path.exists(fn):
        img = tk.PhotoImage(file=fn)
        break
        
    if img: images[image_name] = img

  except Exception as e:
    trace(e)
  return img


def scrolled_widget(master=None, Klass=Text,  **options):
  '''スクロールバー付きのWidgetを作成する'''
  
  fr = Frame(master)
  fr.pack(side='top', fill='both', expand=1)
  sbar = Scrollbar(fr)

  if type(Klass) == Text:
    options['width'] = options.pop('width', 40)
    options['height'] = options.pop('height', 10)
    options['undo'] = options.pop('undo', 1)
    options['maxundo'] = options.pop('maxundo', 10000)

  buf = Klass(fr, **options)
  sbar.config(command=buf.yview)
  sbar.pack(side='right', fill='y')

  buf.config(yscrollcommand=sbar.set)
  buf.pack(side='left', fill='both', expand=1)
  buf.frame = fr
  buf.sbar = sbar
  
  return buf


def __node_up(ev):
  """ツリーの選択ノードを上方向に広げる"""
  tree = ev.widget
  iid = tree.focus()
  sel = tree.selection()
  if sel and len(sel) > 1 and sel[-1] == iid and ev.state & 1:
    tree.selection('remove', (iid,))
  ny = tree.bbox(iid)[1]
  niid = tree.identify_row(ny)
  if niid:
    if ev.state & 1: tree.selection('add', (niid,))
    tree.focus(niid)
    tree.see(niid)
  return 'break'


def __node_down(ev):
  """ツリーの選択ノードを下方向に広げる"""
  tree = ev.widget
  iid = tree.focus()
  sel = tree.selection()
  if sel and len(sel) > 1 and sel[0] == iid and ev.state & 1:
    tree.selection('remove', (iid,))
  bbox = tree.bbox(iid)
  ny = bbox[1] + bbox[3] + 1
  niid = tree.identify_row(ny)
  if niid:
    if ev.state & 1: tree.selection('add', (niid,))
    tree.focus(niid)
    tree.see(niid)
  return 'break'


def __node_toggle_select(ev):
  """ツリーの選択ノードを反転する"""
  tree = ev.widget
  iid = tree.focus()
  if iid: tree.selection('toggle', (iid,))
  return 'break'


def __node_key_action(ev):
  keysym = ev.keysym
  tree = ev.widget

  if 'Home' == keysym:
    items = tree.get_children()
    if items:
      tree.selection_set('')
      iid = items[0]
      tree.focus(iid)
      tree.see(iid)
      if ev.state & 4 == 4: tree.selection_set(iid)

  elif 'End' == keysym:
    items = tree.get_children()
    if items:
      iid = items[-1]
      tree.focus(iid)
      tree.see(iid)
      if ev.state & 4 == 4: tree.selection_set(iid)

  elif 'Next' == keysym:
    h = tree.winfo_height()
    iid = tree.identify_row(h)
    if not iid: return
    tree.focus(iid)
    if ev.state & 4 == 0: tree.selection_set(iid)

  elif 'Prior' == keysym:
    h = tree.winfo_height()
    iid = tree.identify_row(0)
    if not iid: iid = tree.get_children()[0]
    tree.focus(iid)
    if ev.state & 4 == 0: tree.selection_set(iid)

    
def __reset_key_string(tbl):
  tbl.key_timer = None
  tbl.key_string = ''
  #trace('reset tree key')

def __find_item(prefix, tbl):
  #trace('find', prefix)
  iid = tbl.focus()
  iid = tbl.next(iid)
  while iid:
    text = tbl.item(iid, 'text')
    if text.startswith(prefix): return iid
    iid = tbl.next(iid)


def __any_key_press(ev):
  """キーがタイプされたときに呼び出される"""
  tbl = ev.widget
  if tbl.key_timer: tbl.after_cancel(tbl.key_timer)
  tbl.key_timer = tbl.after(800, lambda wi=tbl: __reset_key_string(wi))
  ks = tbl.key_string + ev.char
  if not ks: return
  # trace('string: ', ks)
  tbl.key_string = ks
  iid = __find_item(ks, tbl)
  if iid:
    tbl.focus(iid)
    tbl.see(iid)
    tbl.selection_set(iid) # 移動する


def register_tree_bind(tree):
  # ツリー操作のためのキー・バインド

  if hasattr(tree, 'skip_bind'): return tree

  if 'tree' in map(str, tree.cget('show')):
    tree.key_timer = None
    tree.key_string = ''
    for bk, proc in (
        ('<\Control-Up>', __node_up),
        ('<\Control-Down>', __node_down),
        ('<Shift-Up>', __node_up),
        ('<Shift-Down>', __node_down),
        ('<space>', __node_toggle_select),
        ('<\Control-Home>', __node_key_action),
        ('<\Control-End>', __node_key_action),
        ('<Next>', __node_key_action),
        ('<Prior>', __node_key_action),
    ): tree.bind(bk, proc)

    if not hasattr(tree, 'cell'):
      tree.bind('<KeyPress>', __any_key_press, '+')

  return tree



def _isnumeric(s):
  """test if a string is numeric"""
  for c in s:
    if c in '0123456789-.':
      numeric = True
    else:
      return False
  return numeric


def _change_numeric(data):
  """if the data to be sorted is numeric change to float"""
  # change child to a float
  return [(float(cd), iid) if cd else ('', iid) for cd, iid in data]


def sorter(tbl, tcol, col, descending=0, change_float=0):
  """sort tree contents when a column header is clicked on"""
  # grab values to sort
  if col == '#0':
    data = [(tbl.item(iid, 'text'), iid) for iid in tbl.get_children('')]
  else:
    data = [(tbl.set(iid, col), iid) for iid in tbl.get_children('')]

  if log: log.debug('sort %s,%s,%s,%s', tcol, col, descending, change_float)
  # trace(data )
  # if the data to be sorted is numeric change to float
  if change_float: data = _change_numeric(data)
  # now sort the data in place
  data.sort(reverse=descending)
  for pos, item in enumerate(data): tbl.move(item[1], '', pos)
  # switch the heading so that it will sort in the opposite direction
  tbl.heading(tcol, command=lambda tcol=tcol, col=col: sorter(tbl, tcol, col, int(not descending), change_float))



def _cell_info(ev, tbl):
  item = tbl.identify('item', ev.x, ev.y)
  column = tbl.identify('column', ev.x, ev.y)
  return item, column


cell_debug = int(os.environ.get('CELL_DEBUG', '0'))

class _EditableCell():
  """編集可能なセルをテーブルに拡張する"""

  def __init__(self, tbl, **opts):
    self.table = tbl
    var = tk.StringVar()
    self._cell = cell = tk.Entry(tbl, textvariable=var, bd=1, )
    cell._var = var
    cell.timer = None
    cell.info = None
    cell._editinfo = None
    cell.keysym = None
    self._retry = 0
    cell.bind('<KeyPress>', self._key_press)
    cell.bind('<FocusIn>', self._cell_focus_in)
    cell.bind('<FocusOut>', self._cell_focus_out)
    register_entry_popup(cell)

    self.delay = opts.get('resize_delay', 300)

    for cond, proc in (
        ('<KeyPress>', self._key_press),
        ('<MouseWheel>', lambda ev, cell=cell: cell.place_forget()),
    ): tbl.bind(cond, proc, '+')

    for cond, proc in (
        ('<Button-1>', self._select),
        ('<Configure>', self._resize),
    ): tbl.bind(cond, proc)

  @property
  def font(self):
    fn = self._cell.cget('font')
    font = ui.find_font(fn)
    return font
    
  @font.setter
  def font(self, font):
    self._cell.config(font=font)

  def _select(self, ev):
    self._cell.info = info = _cell_info(ev, self.table)
    if not info[1] == '#0': self._cell_update(with_value=True)

  def _resize(self, ev):
    cell = self._cell
    tbl = self.table
    if cell_debug: trace('table resize', tbl.winfo_width(), 'x', tbl.winfo_height())
    # trace(ev.x, ev.y, ev.width, ev.height)
    if not cell.info: cell.place_forget(); return
    if cell.timer: cell.after_cancel(cell.timer)
    cell.timer = cell.after(self.delay, self._cell_update)

  def _cell_update(self, with_value=False):
    """選択されたセル位置を調整する"""
    cell = self._cell
    tbl = self.table
    #cell.place_forget()
    if not cell.info: cell.place_forget(); return
    item, column = cell.info[:2]

    tw, th, xv, yv = tbl.winfo_width(), tbl.winfo_height(), tbl.xview(), tbl.yview()
    if cell_debug: trace(tw, th, 'xview', xv, xv[0] * tw, xv[1] * tw, 'yview', yv, yv[0] * th, yv[1] * th)

    bbox1 = tbl.bbox(item)  # 行全体の位置
    if not bbox1:
      tbl.see(item)  # 見える位置に移動させる
      bbox1 = tbl.bbox(item)  # 行全体の位置

    if cell_debug: trace('table-box', bbox1, 'item', item, 'column', column, 'info', cell.info)
    bbox = tbl.bbox(item, column)
    if not bbox:
      if cell_debug: trace('no cell-box')
      return

    x, y, w, h = bbox
    if cell_debug: trace('cell-box', bbox, column)

    if x < 0:
      # 画面外にあるので、横スクロールさせる
      rw = bbox1[2] - bbox1[0]  # 全体の幅
      rx = 0 if column == '#1' else abs(bbox1[0] - bbox[0])  # 表示開始位置
      trace('left-scroll: rx', rx, 'rw', rw, 'post', float(rx) / rw)
      tbl.xview_moveto(float(rx) / rw)
      cell.after_idle(lambda wv=with_value: self._cell_update(wv))
      return
    
    if x > tw:
      # 画面外にあるので、横スクロールさせる
      rw = bbox1[2] - bbox1[0]  # 全体の幅
      rx = abs(bbox1[0] + bbox[0]) + bbox[2]  # 表示開始位置
      if cell_debug: trace('over: rx', rx, 'rw', rw, 'post', float(rx) / rw)
      tbl.xview_moveto(float(rx) / rw)
      cell.after_idle(lambda wv=with_value: self._cell_update(wv))
      return

    bd = 3 if sys.platform == 'darwin' else 1
    
    #cell.place_forget()
    cell.place(x=x - bd, y=y - bd, width=w + bd * 2, height=h + bd * 2)
    cell.update()
    if with_value and column != '#0':
      cell.after_idle(lambda iid=item, cid=column: cell._var.set(tbl.set(iid, cid)))

  def _cell_active(self):
    cell = self._cell
    keysym = cell.keysym
    cell.keysym = None
    if keysym:
      cell.after_idle(lambda wi=cell,sym=keysym: wi.event_generate('<KeyPress>', keysym=sym))
    else:
      cell.select_range(0, END)
    cell.icursor(END)
    cell.config(bg='gray')
    
  def _cell_focus_in(self, ev):
    cell = self._cell
    tbl = self.table
    if not cell.info: return
    cell._editinfo = cell.info
    cell.after_idle(self._cell_active)

  def _cell_focus_out(self, ev):
    cell = self._cell
    tbl = self.table
    cell.after_idle(lambda wi=cell: wi.config(bg='snow'))
    if not cell._editinfo: return
    item, column = cell._editinfo[:2]
    value = cell._var.get()
    tbl.set(item, column, value)

  def _key_press(self, ev):
    '''cellに割り当てるキー操作'''
    #if ev.state & 4 == 4: return
    cell = self._cell
    tbl = self.table
    ewi = ev.widget

    # ----------- 内部手続き定義　ここから

    def _get_cell_info(keysym=None, with_shift=False, with_ctrl=False, tab_action=True):
      """cell位置を入手する"""
      dc = ( )
      if keysym:
        dc = tbl.cget('displaycolumns')
        if dc[0] == '#all': dc = tbl.cget('columns')
        if cell_debug: trace('keysym:', keysym, 'tab:', tab_action, 'ctrl:', with_ctrl, 'shift:', with_shift)

      if cell.info:
        iid, column = cell.info
      else:
        iid = tbl.focus()
        column = '#1'
      
      def _cpos(cn):
        return int(cn[1:]) - 1 if cn.startswith('#') else dc.index(column)

      dflag = platform == 'darwin' and tab_action and with_ctrl
      
      if cell_debug: trace(iid, column)
      if ('Left' == keysym and tab_action and with_ctrl) or ('a' == keysym and dflag):
        iid = tbl.focus()
        column = '#1'
        
      elif ('Right' == keysym and tab_action and with_ctrl) or ('e' == keysym and dflag):
        iid = tbl.focus()
        column = '#%d' % len(dc)
        
      elif ('Right' == keysym and tab_action) or ('Tab' == keysym and not with_shift) or ('f' == keysym and dflag):
        pos = 1 + _cpos(column)
        if pos < len(dc): column = dc[pos]
        if not tab_action:
          tbl.after_idle(lambda wi=tbl, sym='F2': wi.event_generate('<KeyPress>', keysym=sym))

      elif ('Left' == keysym and tab_action) or ('Tab' == keysym and with_shift) or ('b' == keysym and dflag):
        pos = _cpos(column)
        if pos > 0: column = dc[pos - 1]
        if not tab_action:
          tbl.after_idle(lambda wi=tbl, sym='F2': wi.event_generate('<KeyPress>', keysym=sym))
            
      elif ('p' == keysym and dflag) or ('Return' == keysym and with_shift):
          tbl.after_idle(lambda wi=tbl, sym='Up': wi.event_generate('<KeyPress>', keysym=sym))
          
      elif ('n' == keysym and dflag) or ('Return' == keysym and not with_shift):
          tbl.after_idle(lambda wi=tbl, sym='Down': wi.event_generate('<KeyPress>', keysym=sym))
        
      elif 'Up' == keysym:
        iid = tbl.focus()
        iid = tbl.prev(iid)
        if not tab_action and iid:
          tbl.focus(iid)
          tbl.see(iid)
          tbl.focus_set()
          tbl.after_idle(lambda wi=tbl, sym='F2': wi.event_generate('<KeyPress>', keysym=sym))

      elif 'Down' == keysym:
        iid = tbl.focus()
        iid = tbl.next(iid)
        if not tab_action and iid:
          tbl.focus(iid)
          tbl.see(iid)
          tbl.focus_set()
          tbl.after_idle(lambda wi=tbl, sym='F2': wi.event_generate('<KeyPress>', keysym=sym))

      elif 'Next' == keysym:
        iid = tbl.focus()
      
      elif 'Prior' == keysym:
        iid = tbl.focus()
      
      elif 'Home' == keysym:
        iid = tbl.focus()
        if tab_action and (ev.state & 4 != 4): column = '#1'
      
      elif 'End' == keysym:
        iid = tbl.focus()
        if tab_action and (ev.state & 4 != 4): column = '#%d' % len(dc)
      
      elif 'Escape' == keysym:
        cell._editinfo = None
        tbl.focus_set()

      elif 'F2' == keysym and tab_action:
        cell.focus_set()
        try:
          fn = tbl.tag_configure('normal')['font']
          if type(fn) in (str, unicode, tuple):
            fn = ui.find_font(fn)
          cell.font = fn
        except: pass

      elif tab_action and not with_ctrl and keysym != '??':
        cell.keysym = keysym
        cell.focus_set()
        cell.update()

      return iid, column

    # ----------- 内部手続き定義　ここまで
    
    if cell_debug:
      trace('columns:', tbl.cget('columns'))
      trace('displaycolumns:', tbl.cget('displaycolumns'))
      trace('cell-key', ev.serial, ev.keysym, ev.widget)
    info = _get_cell_info(ev.keysym, (ev.state & 1) == 1, (ev.state & 4) == 4, ewi == tbl)
    if cell_debug: trace(info)
    cell.info = info
    if ewi == tbl or ev.keysym == 'Escape':
      self._cell_update(with_value=True)

  def _init_update(self):
    tbl = self.table
    tbl.focus_set()
    iid = tbl.focus()

    if not iid and self._retry < 3:
      tbl.after_idle(self, cell._init_update)
      self._retry += 1
      return

    column = '#1'
    self._cell.info =  iid, column
    tbl.after_idle(lambda wv=1: self._cell_update(wv))
    
def register_editable_cell(tbl):
  cell = _EditableCell(tbl)
  tbl.cell = cell
  tbl.after_idle(cell._init_update)
  return tbl


def strftime(pattern="%Y-%m%d-%H%M", unixtime=None):
    tt = _dt.fromtimestamp(unixtime) if unixtime else _dt.now()
    return tt.strftime(pattern)


try:
  if platform == 'win32':
    from .dnd01 import register_dnd_notify
    from .icon01 import get_icon
  else:
    from .dnd02 import register_dnd_notify
    from .icon02 import get_icon
    
except:
  def register_dnd_notify(win, dnd_notify):
    pass

  def get_icon(path, **opts):
    pass

  
if __name__ == '__main__':
    class EmptyApp(UIClient): pass
    class EmptyApp2(App): pass

    App.start(EmptyApp)
    EmptyApp2.run()

  
