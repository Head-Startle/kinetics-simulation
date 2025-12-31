# 命令行工具基本教程

- 工作目录就是属于命令行工具的“文件资源管理器/访达”界面，一个“办公室”。
- 当你想要告诉命令行工具打开/修改/读取一个文件时，我们需要告诉它这个文件的**所在地**和**名字**。所在地可以使用“相对路径”和“绝对路径”两种方法填写。前者就是从当前目录出发，一级一级深入到需要指定的文件；后者就是从电脑磁盘的最底层出发，一般需要从C或D或E盘开始一路指定。在到达目标文件的路径后，附上文件名，就可以给命令行工具传输文件了。
- 那么，工作目录，即这个“办公室”如何切换呢？**使用cd命令！**，cd意为“change directory”
- 通常情况下，打开命令提示符/PowerShell，光标前会有一串字符（一般是`C:\Users\yourname>`），这个就是工作目录。在显示屏上，我们已经习惯了看到目录下有哪些文件和子目录，但命令行工具不会，想要看到工作目录里有些什么，需要敲一行命令：
- 对于powershell：

  ```powershell
  # 当前目录，显示隐藏和系统项（等同于bash/zsh的 ls -la）
  Get-ChildItem -Force

  # 递归列出所有文件和文件夹，也就是深入到文件夹最底层
  Get-ChildItem -Recurse -Force

  # 仅列出文件（不含目录）
  Get-ChildItem -File

  # 以表格形式显示详细信息
  Get-ChildItem | Format-Table -AutoSize
  ```

- 对于macOS终端里运行的bash/zsh：

  ```bash
  # 当前目录，长列表并显示隐藏文件
  ls -la

  # 递归列出所有文件和目录
  ls -R

  # 仅列出文件（不含目录）
  ls -p | grep -v '/'

  # 长列表并以可读大小显示
  ls -lh
  ```

- 于是，我们就可以知道工作目录的结构与内容了。如果现在有一个子目录，比如叫 mydir，要切换到它可以这样做（注意可能的混淆点：Windows 路径分隔符与驱动器切换、~ 表示用户主目录、.. 表示父目录、cd - 返回上一个目录）。

- 在 macOS / Linux（bash/zsh）：

  ```bash
  # 进入子目录
  cd mydir
  # 或者
  cd ./mydir # 一个点表示当前所处的目录
  
  # 回到上级目录，连续两个点就表示上一级目录
  cd ..
  
  # 回到上上级目录就是：
  cd ../../
  
  # 绝对路径写法，用`/`开头
  cd /Users/yourname/路径/to/mydir
  
  # 进入主目录
  cd ~
  
  # 切回上一次目录
  cd -
  ```

- 在 Windows CMD：

  ```cmd
  # 进入子目录
  cd mydir
  
  # 回到上级目录
  cd ..
  
  # 切换到指定盘符的路径（若要同时切换盘符，使用 /d）
  cd /d D:\path\to\mydir
  
  # 查看当前目录
  cd
  ```

- 在 PowerShell（与 bash 类似）：

  ```powershell
  # 进入子目录
  cd mydir
  # 或
  Set-Location mydir
  
  # 查看当前位置
  Get-Location
  ```

- 额外提示：
  - 路径中有空格时用引号：cd "my folder"
  - 用 pwd（或 Get-Location 或 cd 无参数）确认当前目录
