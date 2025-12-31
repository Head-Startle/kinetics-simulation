# 化学动力学模拟器

基于显式欧拉法的化学反应浓度-时间模拟工具，支持非基元反应、物质别名和交互式可视化。

## 📦 安装

### 1. 克隆项目

开发者通常会使用git工具克隆项目，它能够实现代码在本地与远程之间的同步，记录代码的更改历史，以便于项目发布与更新，这里不详细介绍。

最简单的办法是直接下载zip压缩包，然后在本地解压，解压位置任选。

然后打开电脑上的**命令行工具**（如Windows操作系统的命令提示符/PowerShell，macOS的终端），切换工作目录到该文件夹。

更多关于命令行工具的基础操作（什么是工作目录、如何切换、常用查看/列出命令等）已整理到独立文档：[CLI-instruction.md](CLI-instruction.md)。请移步查看该文件以获取完整教程。

### 2. 安装python

确保已安装 Python，如没有python，请这样做：

#### macOS 系统

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载适用于 macOS 的最新 Python 安装包（.pkg 文件）
3. 双击下载的 .pkg 文件，按照安装向导完成安装
4. 打开"终端"（Terminal），验证安装：

   ```bash
   python3 --version
   ```

#### Windows 系统

**最简单的方案**：打开PowerShell，直接输入：

```powershell
python
```

在win10/11版本中，电脑已经预置了一个python占位符。运行后，电脑会跳转至Microsoft Store，在那里安装即可。

然后验证安装：

```powershell
python --version
```

或者走官网途径：

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新的 Python 安装管理器(.msix文件)
3. 打开运行，跳出提示，全选y（yes）即可
4. 打开"命令提示符"（cmd）或 PowerShell，验证安装：

   ```powershell
   python --version
   ```

   应跳出安装的版本号。如报错，请至电脑的设置-环境变量-用户变量-Path里,把刚安装的python.exe的路径移到最前面，该路径可直接在开始菜单栏查找python应用程序，获取其路径得到。

## 🚀 快速开始-前提：已安装好python

### 1. 准备控制文件

编辑 `control.yaml`，推荐用vsCode，但直接用记事本/文本编辑编辑也可：

```yaml
species:
  - [A, 1.0] # [名称, 初始浓度]
  - [B, 0.5, alias] # [名称, 初始浓度, 别名]

reactions:
  - ["A + B -- C", 1.0, 0.1] # [方程式, kf, kb]

dt: 0.01
steps: 5000
output: result # csv文件名
title: "反应动力学" # 可选，窗口标题
```

具体规则在`control-example.yaml`中有详细说明，也可参考tests中的案例的写法

### 2. 运行模拟

打开终端或命令提示符，切换到项目根目录，依次运行：

```bash
# 安装项目及其依赖
python3 -m pip install -e .
# 若报错，使用：
python -m pip install -e .

# 运行模拟（读取 control.yaml 或指定配置文件）
kns my_config.yaml
# kns 之后指定控制文件。处在项目根目录时，直接输入文件名可找到目标文件；不处在项目根目录，或需要外部文件夹的控制文件，请指定完整路径

# 仅绘制已有 CSV 数据
kns --plot dat/result.csv
# --plot 之后指定用来绘图的csv文件。处在项目根目录时，./dat/result/csv可找到目标文件；不处在项目根目录，或需要外部文件夹的csv文件，请指定完整路径
```

### 3. 查看结果

- CSV 数据：`dat/result.csv`
- 交互窗口：拖动滑块查看浓度变化，点击工具栏保存按钮存图到 `pic/`

## 📂 项目结构

```
kinetics-simulation/
├── control.yaml # 控制文件模板（示例配置）
├── pyproject.toml # 项目配置与依赖（可用于安装）
├── README.md # 项目文档
├── LICENSE # MIT 许可证
├── src/
│ └── kns/ # 核心包
│ ├── **init**.py # python包标识
│ ├── simulation.py # 主入口：参数处理、YAML 读取、CSV 写入、运行模拟
│ ├── parser.py # 反应式解析器
│ ├── kinetics.py # 速率计算与显式欧拉积分
│ └── io_plot.py # 交互绘图与图片保存
├── tests/ # 测试用例
│ ├── alias_order.yaml
│ ├── duplicate_order.yaml
│ ├── duplicate_substrate.yaml
│ ├── negative_rate.yaml
│ └── zero_initial.yaml
├── dat/ # CSV 输出目录（运行后生成）
└── pic/ # PNG 输出目录（运行时保存绘图）

```

## 🔬 语法说明

### 反应式语法

- **基元反应**（质量作用定律）：
  ```yaml
  "2A + B -- 3C" # 速率 = k[A]²[B]
  ```
- **非基元反应**（自定义级数）：
  ```yaml
  "A + B(2) -- C" # B的级数=2，速率 = k[A][B]²，但物质变化量按系数1计算
  ```
- **可逆反应**：
  ```yaml
  ["A -- B", 1.0, 0.5] # kf=1.0, kb=0.5
  ```

### 物质别名

```yaml
species:
  - ["H2O", 1.0, "water"]
```

反应式中`H2O`和`water`可任意使用

## 🧪 测试

运行测试（使用终端、命令提示符等 CLI）：

```bash
kns control- example.yaml
kns tests/catalyst.yaml
kns tests/duplicate_substrate.yaml
kns tests/negative_rate.yaml
kns tests/zero_initial.yaml
kns order_conflict.yaml
```

## 📊 输出

### CSV 格式

```
time,A,B,C
0,1,0.5,0
0.01,0.99,0.495,0.005
...
```

### 交互窗口功能

- **滑块**：查看任意时刻浓度
- **Play/Reverse**：自动播放/倒放
- **工具栏保存**：保存当前帧为 PNG（默认 `pic/`）

## 🛠️ 开发

### 模块职责

- `parser.py`：解析反应式字符串，支持化学计量数和反应级数
- `kinetics.py`：速率计算（`rate_from_side`）与显式欧拉积分（`simulate`）
- `io_plot.py`：matplotlib 交互绘图，预创建 artists 避免卡顿
- `simulation.py`：主入口，负责 YAML 读取、CSV 写入、目录管理

## 📝 注意事项

- **数值稳定性**：显式欧拉法对刚性问题可能不稳定，建议 dt < 0.01
- **性能**：步数 > 10000 时可能较慢，考虑降采样或换用编译型积分器
- **0^0 处理**：速率计算中 0^0 被视为 1

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

如有问题或建议，请通过 GitHub Issues 联系。
