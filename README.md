# 坦克大战游戏

这是一个基于Pygame的坦克大战游戏，玩家可以控制一辆坦克与机器人坦克进行对战。

# 仅用于测试，依然有大量的Bug 比如子弹方向


----

## 游戏特点

- 玩家与机器人对战
- 支持发射普通炮弹和威力更大的导弹
- 坦克装甲系统，有几率弹开敌方炮弹
- 简单的爆炸效果和游戏状态显示
- 障碍物系统和碰撞检测
- 音效系统（射击、爆炸、移动等）

## 操作方法

- **W, A, S, D** - 控制坦克上、左、下、右移动
- **空格键** - 发射普通炮弹
- **M键** - 发射导弹（冷却时间较长）
- **R键** - 游戏结束后重新开始
- **ESC键** - 退出游戏

## 游戏规则

- 玩家坦克（绿色）初始生命值为100
- 机器人坦克（红色）初始生命值为100
- 普通炮弹造成10点伤害，但可能被装甲弹开
- 导弹造成30点伤害，无视装甲防御
- 坦克装甲值决定了弹开普通炮弹的几率
- 当任一方生命值降至0或以下时，游戏结束

## 运行要求

- Python 3.x
- Pygame库

## 安装依赖

### 方法1：使用pip安装
```
pip install pygame
```

### 方法2：使用国内镜像源安装
如果遇到网络问题，可以尝试使用国内镜像源：
```
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方法3：使用conda安装
如果你使用Anaconda或Miniconda：
```
conda install pygame
```

### 方法4：手动下载安装
1. 访问 https://www.pygame.org/download.shtml
2. 下载适合你系统的pygame安装包
3. 手动安装下载的包

## 运行游戏

### 使用启动器（推荐）
```
python main.py
```
启动器将自动启动游戏，并在pygame库未安装时提供安装指导。

### 直接运行游戏
```
python tank_battle.py
```

## 项目结构

```
game/
├── assets/                # 游戏资源文件夹
│   ├── background.svg     # 游戏背景
│   ├── bullet.svg         # 炮弹图像
│   ├── explosion.svg      # 爆炸效果
│   ├── missile.svg        # 导弹图像
│   ├── player_tank.svg    # 玩家坦克
│   ├── robot_tank.svg     # 机器人坦克
│   └── sound_manager.py   # 音效管理器
├── config.py              # 游戏配置文件
├── main.py                # 游戏启动器
├── tank_battle.py         # 主游戏文件
├── README.md              # 游戏说明文档
└── requirements.txt       # 依赖列表
```

## 常见问题解决

### 无法安装pygame
- 确保你的Python版本与pygame兼容
- 尝试更新pip: `pip install --upgrade pip`
- 尝试使用上述的其他安装方法

### 游戏运行时出现错误
- 确保所有资源文件都在正确的位置
- 检查Python版本是否为3.x
- 确保pygame已正确安装

祝您游戏愉快！