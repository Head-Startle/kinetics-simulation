# 化学动力学模拟器

基于显式欧拉法的化学反应浓度-时间模拟工具，支持非基元反应、物质别名和交互式可视化。

## ✨ 功能特性

- **灵活的反应定义**：支持基元和非基元反应，可独立指定反应级数
- **物质别名**：无 26 字母限制，支持自定义物质名称和可选别名
- **数值积分**：显式欧拉法求解常微分方程组
- **交互式绘图**：
  - 滑块浏览任意时刻浓度
  - 播放/倒放动画
  - 保存 PNG 到指定目录
- **模块化设计**：代码分离为解析器、积分器、绘图模块

## 📦 安装

### 1. 克隆项目

```bash
git clone <你的仓库地址>
cd kinetics-simulation
```

### 2. 安装依赖

确保已安装 Python 3.8+，然后运行：

```bash
pip install -r requirements.txt
```

## 🚀 快速开始

### 1. 准备控制文件

编辑 `control.yaml`：

```yaml
species:
  - [A, 1.0] # [名称, 初始浓度]
  - [B, 0.5, cat] # [名称, 初始浓度, 别名]

reactions:
  - ["A + B -- C", 1.0, 0.1] # [方程式, kf, kb]
  - ["A + B(2) -- C", 0.5, 0.0] # 非基元：B的级数为2

dt: 0.01
steps: 5000
output: result # 自动补全 .csv
title: "反应动力学" # 可选，窗口标题
```

### 2. 运行模拟

> 注意：本项目已移除作为模块导入的入口（不再支持 `python -m kns`）。请使用安装后的命令行工具 `kns` 来运行模拟或绘图。

```bash
# 使用安装的命令（推荐）
pip install -e .    # 开发模式安装一次后可使用下列命令

# 运行模拟（读取 control.yaml 或指定配置文件）
kns
kns my_config.yaml

# 仅绘制已有 CSV 数据
kns --plot dat/result.csv
```

### 3. 查看结果

- CSV 数据：`dat/result.csv`
- 交互窗口：拖动滑块查看浓度变化，点击工具栏保存按钮存图到 `pic/`

## 📂 项目结构

```
simulation/
├── simulation.py      # 主入口：I/O、参数处理
├── parser.py          # 反应式解析器
├── kinetics.py        # 速率计算与欧拉积分
├── io_plot.py         # 交互式绘图
├── control.yaml       # 控制文件模板
├── tests/             # 边界测试用例
│   ├── alias_order.yaml
│   ├── duplicate_order.yaml
│   └── zero_initial.yaml
├── dat/               # CSV 输出目录（.gitignore）
└── pic/               # PNG 输出目录（.gitignore）
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
  - { name: "H_plus", initial: 0.0, alias: "H+" }
```

反应式中可用 `H+` 代替 `H_plus`。

## 🧪 测试

运行边界测试（使用 CLI）：

```bash
kns tests/alias_order.yaml
kns tests/duplicate_order.yaml
kns tests/zero_initial.yaml
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

### 扩展建议

- 替换积分器：在 `kinetics.py` 中换用 RK4 或 scipy.odeint
- 添加约束：在积分循环中加入守恒律或边界条件检查
- 并行计算：用 `multiprocessing` 并行运行多组参数

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
