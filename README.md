# 化学动力学模拟器

基于显式欧拉法的化学反应浓度-时间模拟工具，支持非基元反应、物质别名和交互式可视化。

## 📦 安装

### 1. 克隆项目

```bash
  git clone <你的仓库地址>
  cd kinetics-simulation
```

### 2. 安装依赖

确保已安装 Python，如没有python，请这样做：

#### macOS 系统

##### 通过官网安装

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载适用于 macOS 的最新 Python 安装包（.pkg 文件），大于3.8的版本即可
3. 双击下载的 .pkg 文件，按照安装向导完成安装
4. 打开"终端"（Terminal），验证安装：

   ```bash
   python3 --version
   pip3 --version
   ```

##### 使用 Homebrew 安装

1. 打开"终端"（Terminal）应用

2. 安装Homebrew

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. 按照终端提示完成安装（可能需要输入密码）
4. 如果终端提示需要将 Homebrew 添加到 PATH，请按照提示执行相应命令

5. 安装 Python：

   ```bash
   brew install python
   ```

6. 验证安装：

   ```bash
   python3 --version
   pip3 --version
   ```

#### Windows 系统

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新的 Python 安装包（.exe 文件），大于3.8的版本即可
3. 运行安装程序，**务必勾选** "Add Python to PATH"
4. 点击 "Install Now" 完成安装
5. 打开"命令提示符"（cmd）或 PowerShell，验证安装：

   ```bash
   python --version
   pip --version
   ```

> **提示**：pip 会随 Python 一起自动安装

## 🚀 快速开始

### 1. 准备控制文件

编辑 `control.yaml`：

```yaml
species:
  - [A, 1.0] # [名称, 初始浓度]
  - [B, 0.5, cat] # [名称, 初始浓度, 别名]

reactions:
  - ["A + B -- C", 1.0, 0.1] # [方程式, kf, kb]

dt: 0.01
steps: 5000
output: result # csv文件名
title: "反应动力学" # 可选，窗口标题
```

具体规则在`control.yaml`中有详细说明，也可参考tests中的案例的写法

### 2. 运行模拟

打开终端或命令提示符，依次运行：

```bash
# 安装依赖
pip install -r requirements.txt

# 使用安装的命令
pip install -e .    # 开发模式安装一次后可使用下列命令

# 运行模拟（读取 control.yaml 或指定配置文件）
kns my_config.yaml

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
├── control.yaml           # 控制文件模板
├── pyproject.toml         # 项目配置与依赖
├── requirements.txt       # Python 依赖列表
├── README.md              # 项目文档
├── LICENSE                # 开源协议
├── src/
│   └── kns/               # 核心模块包
│       ├── __init__.py
│       ├── simulation.py  # 主入口：I/O、参数处理
│       ├── parser.py      # 反应式解析器
│       ├── kinetics.py    # 速率计算与欧拉积分
│       └── io_plot.py     # 交互式绘图
├── tests/                 # 测试用例
│   ├── alias_order.yaml
│   ├── duplicate_order.yaml
│   ├── duplicate_substrate.yaml
│   ├── negative_rate.yaml
│   └── zero_initial.yaml
├── dat/                   # CSV 输出目录（.
├── pic/                   # PNG 输出目录（.

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

反应式中可用 `H+` 代替 `H_plus`。

## 🧪 测试

运行边界测试（使用终端、命令提示符等 CLI）：

```bash
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
