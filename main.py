#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os

def check_pygame():
    """检查pygame是否已安装"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame():
    """尝试安装pygame库"""
    print("\n正在尝试安装pygame库...")
    try:
        # 尝试不使用SSL验证安装
        print("尝试安装方式1...")
        os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--trusted-host", "pypi.org", 
             "--trusted-host", "files.pythonhosted.org", "--trusted-host", "pypi.tuna.tsinghua.edu.cn", 
             "pygame"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("pygame安装成功！")
            return True
        else:
            print("安装方式1失败，尝试安装方式2...")
            # 尝试使用国内镜像源
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--trusted-host", "pypi.tuna.tsinghua.edu.cn", 
                 "pygame", "-i", "http://pypi.tuna.tsinghua.edu.cn/simple"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("pygame安装成功！")
                return True
            else:
                print("自动安装失败。")
                return False
    except Exception as e:
        print(f"安装过程中出现错误：{e}")
        return False

def show_detailed_installation_guide():
    """显示详细的pygame安装指南"""
    print("\n===== Pygame详细安装指南 =====")
    print("\n方法1: 使用pip安装（命令行）")
    print("打开命令提示符(cmd)或PowerShell，运行:")
    print("python -m pip install --upgrade pip")
    print("python -m pip install pygame")
    
    print("\n方法2: 使用国内镜像源（推荐，网络更稳定）")
    print("python -m pip install pygame -i http://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn")
    
    print("\n方法3: 离线安装")
    print("1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame")
    print("2. 下载适合您Python版本的.whl文件")
    print("   例如: pygame-2.1.2-cp38-cp38-win_amd64.whl (Python 3.8, 64位)")
    print("3. 打开命令提示符，切换到下载目录")
    print("4. 运行: python -m pip install 文件名.whl")
    
    print("\n方法4: 使用conda安装（如果您使用Anaconda）")
    print("conda install -c conda-forge pygame")
    
    print("\n故障排除:")
    print("- 如果安装过程中出现SSL错误，请尝试方法2或方法3")
    print("- 确保您的Python版本与pygame兼容（推荐Python 3.6-3.9）")
    print("- 如果您使用的是虚拟环境，请确保在正确的环境中安装")
    print("\n安装完成后，请重新运行此程序。")

def download_pygame_whl():
    """下载适合当前Python版本的pygame whl文件"""
    import platform
    import urllib.request
    import os
    
    # 获取Python版本信息
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    is_64bit = platform.architecture()[0] == '64bit'
    arch = "win_amd64" if is_64bit else "win32"
    
    # 构建可能的文件名
    # 注意：这里使用的URL和文件名可能需要根据实际情况调整
    base_url = "https://download.lfd.uci.edu/pythonlibs/archived/"
    possible_versions = ["2.1.2", "2.0.1", "1.9.6"]
    
    print("\n正在尝试下载适合您系统的pygame安装包...")
    print(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}, 系统架构: {'64位' if is_64bit else '32位'}")
    
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # 尝试不同版本
    for version in possible_versions:
        filename = f"pygame-{version}-cp{py_version}-cp{py_version}{'' if int(py_version) >= 38 else 'm'}-{arch}.whl"
        url = base_url + filename
        target_path = os.path.join(download_dir, filename)
        
        try:
            print(f"尝试下载: {filename}")
            urllib.request.urlretrieve(url, target_path)
            print(f"\n下载成功! 文件保存在: {target_path}")
            
            # 尝试安装下载的whl文件
            print("\n正在安装下载的pygame包...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", target_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("pygame安装成功！")
                return True
            else:
                print(f"安装失败，错误信息: {result.stderr}")
                print(f"您可以手动安装下载的文件: python -m pip install {target_path}")
                return False
                
        except Exception as e:
            print(f"下载或安装失败: {e}")
    
    print("\n无法自动下载适合您系统的pygame安装包。")
    print("请访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame 手动下载。")
    return False

def main():
    print("欢迎来到坦克大战游戏！")
    print("正在启动Pygame图形版本...")
    
    # 检查pygame是否已安装
    if not check_pygame():
        print("错误：无法启动游戏。未检测到pygame库。")
        
        # 显示选项菜单
        print("\n请选择操作:")
        print("1. 尝试自动安装pygame (在线安装)")
        print("2. 尝试下载并安装pygame (离线安装包)")
        print("3. 查看详细安装指南")
        print("4. 退出")
        
        choice = input("请输入选项(1-4): ").strip()
        
        if choice == '1':
            if install_pygame():
                print("\n正在重新启动游戏...")
                try:
                    import tank_battle
                    return
                except ImportError as e:
                    print(f"导入游戏模块失败：{e}")
            else:
                print("\n自动安装失败，请尝试其他安装方式:")
                show_detailed_installation_guide()
        
        elif choice == '2':
            if download_pygame_whl():
                print("\n正在重新启动游戏...")
                try:
                    import tank_battle
                    return
                except ImportError as e:
                    print(f"导入游戏模块失败：{e}")
            else:
                print("\n请参考详细安装指南尝试其他方法:")
                show_detailed_installation_guide()
        
        elif choice == '3':
            show_detailed_installation_guide()
        
        else:
            print("退出程序。安装pygame后再次运行以启动游戏。")
    else:
        try:
            print("\n游戏启动中，请稍候...")
            # 导入并运行游戏
            import tank_battle
            # 调用游戏主函数
            tank_battle.main()
            # 如果游戏正常退出，显示提示
            print("\n游戏已结束。感谢您的游玩！")
            input("按Enter键退出...")
        except ImportError as e:
            print(f"\n导入游戏模块失败：{e}")
            print("\n请检查游戏文件是否完整，或者重新安装pygame库。")
            # 在错误情况下也等待用户确认
            input("\n按Enter键退出...")
        except FileNotFoundError as e:
            print(f"\n游戏资源文件缺失：{e}")
            print("\n请确保游戏资源文件（如图像、音效等）存在且路径正确。")
            input("\n按Enter键退出...")
        except Exception as e:
            print(f"\n游戏启动失败，错误类型：{type(e).__name__}")
            print(f"错误详情：{e}")
            print("\n请检查游戏文件是否完整，或者重新安装pygame库。")
            # 在错误情况下也等待用户确认
            input("\n按Enter键退出...")

if __name__ == "__main__":
    main()