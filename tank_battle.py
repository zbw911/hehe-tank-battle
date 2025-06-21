import pygame
import sys
import random
import math
import os
import traceback
from pygame.locals import *
from assets.sound_manager import SoundManager

# 调试模式
DEBUG_MODE = True

def debug_print(message):
    """打印调试信息"""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

# 初始化pygame
debug_print("正在初始化pygame...")
try:
    pygame.init()
    debug_print(f"Pygame初始化完成: {pygame.get_init()}")
    debug_print(f"Pygame版本: {pygame.version.ver}")
    debug_print(f"SDL版本: {'.'.join(map(str, pygame.version.SDL))}")
    
    # 检查已初始化的模块
    initialized_modules = []
    # pygame.get_init()返回的是一个布尔值，不能使用_asdict()
    # 获取已初始化的模块信息
    debug_print("检查已初始化的模块...")
    if pygame.display.get_init():
        initialized_modules.append("display")
    if pygame.font.get_init():
        initialized_modules.append("font")
    if pygame.mixer.get_init():
        initialized_modules.append("mixer")
    if pygame.joystick.get_init():
        initialized_modules.append("joystick")
    debug_print(f"已初始化的模块: {', '.join(initialized_modules)}")
except Exception as e:
    print(f"pygame初始化失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('坦克大战')
clock = pygame.time.Clock()

# 加载图像函数
def load_image(name, scale=1):
    try:
        debug_print(f"正在加载图像: {name}")
        if not os.path.exists(name):
            print(f"错误: 图像文件不存在: {name}")
            debug_print(f"检查当前工作目录: {os.getcwd()}")
            debug_print(f"检查文件是否存在: {os.path.exists(name)}")
            debug_print(f"检查父目录是否存在: {os.path.exists(os.path.dirname(name))}")
            raise FileNotFoundError(f"图像文件不存在: {name}")
            
        debug_print(f"文件存在，尝试加载: {name}")
        image = pygame.image.load(name).convert_alpha()
        size = image.get_size()
        size = (int(size[0] * scale), int(size[1] * scale))
        debug_print(f"图像加载成功: {name}, 原始尺寸: {image.get_size()}, 缩放尺寸: {size}")
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"无法加载图像: {name}")
        print(f"错误详情: {e}")
        debug_print(f"Pygame错误详情: {e}")
        # 创建一个默认的表面作为替代
        surface = pygame.Surface((30, 30))
        surface.fill((255, 0, 255))  # 使用洋红色表示缺失的纹理
        debug_print("返回洋红色默认表面")
        return surface
    except Exception as e:
        print(f"加载图像时发生未知错误: {name}")
        print(f"错误类型: {type(e).__name__}, 错误详情: {e}")
        debug_print(f"错误详情: {e}")
        traceback.print_exc()
        # 创建一个默认的表面作为替代
        surface = pygame.Surface((30, 30))
        surface.fill((255, 0, 0))  # 使用红色表示错误
        debug_print("返回红色默认表面")
        return surface

# 资源路径
def get_asset_path(filename):
    try:
        debug_print(f"获取资源路径: {filename}")
        # 获取当前脚本的绝对路径
        current_script_path = os.path.abspath(__file__)
        debug_print(f"当前脚本路径: {current_script_path}")
        
        # 获取脚本所在目录
        script_dir = os.path.dirname(current_script_path)
        debug_print(f"脚本所在目录: {script_dir}")
        
        # 检查资源目录是否存在
        assets_dir = os.path.join(script_dir, 'assets')
        debug_print(f"资源目录路径: {assets_dir}")
        
        if not os.path.exists(assets_dir):
            print(f"资源目录不存在: {assets_dir}")
            debug_print(f"尝试创建资源目录: {assets_dir}")
            os.makedirs(assets_dir, exist_ok=True)
            debug_print(f"已创建资源目录: {assets_dir}")
        else:
            debug_print(f"资源目录已存在: {assets_dir}")
            # 列出资源目录中的文件
            files = os.listdir(assets_dir)
            debug_print(f"资源目录中的文件: {files}")
        
        # 构建资源文件的完整路径
        asset_path = os.path.join(assets_dir, filename)
        debug_print(f"完整资源路径: {asset_path}")
        
        # 检查资源文件是否存在
        if not os.path.exists(asset_path):
            print(f"警告: 资源文件不存在: {asset_path}")
            debug_print(f"检查当前工作目录: {os.getcwd()}")
            # 尝试在当前工作目录查找
            alt_path = os.path.join(os.getcwd(), 'assets', filename)
            debug_print(f"尝试替代路径: {alt_path}")
            if os.path.exists(alt_path):
                debug_print(f"在替代路径找到文件: {alt_path}")
                return alt_path
        else:
            debug_print(f"资源文件存在: {asset_path}")
        
        return asset_path
    except Exception as e:
        print(f"获取资源路径时出错: {e}")
        # 返回原始路径，让后续代码处理文件不存在的情况
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename)

# 坦克基类
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, tank_image, bullet_image, missile_image):
        super().__init__()
        self.image = tank_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 0  # 0: 上, 1: 右, 2: 下, 3: 左
        self.bullet_image = bullet_image
        self.missile_image = missile_image
        self.health = 100
        self.armor = 30  # 装甲值，影响弹开几率
        self.original_image = self.image
        
        # 射击冷却时间
        self.bullet_cooldown = 300  # 毫秒
        self.missile_cooldown = 1000  # 毫秒
        self.last_shot = 0
        self.last_missile = 0
        self.cooldown = 0
        self.missile_cooldown = 0
        self.original_image = self.image
    
    def update(self):
        # 冷却时间更新已经不需要了，因为我们使用了基于时间戳的冷却系统
        pass
    
    def move(self, dx, dy):
        # 计算新位置
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        # 边界检查
        if 0 <= new_x <= SCREEN_WIDTH - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = new_y
    
    def rotate(self, direction):
        self.direction = direction
        angle = -90 * direction  # 转换方向为角度
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def shoot_bullet(self):
        # 检查冷却时间
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < self.bullet_cooldown:
            return None
        
        self.last_shot = current_time
        
        # 根据坦克方向确定子弹的初始位置和速度
        bullet_speed = 10
        bullet_x, bullet_y = self.rect.center
        
        # 根据坦克方向调整子弹的初始位置，使其从炮口发射
        if self.direction == 0:  # 上
            bullet_y -= self.rect.height // 2
            bullet_dx, bullet_dy = 0, -bullet_speed
        elif self.direction == 1:  # 右
            bullet_x += self.rect.width // 2
            bullet_dx, bullet_dy = bullet_speed, 0
        elif self.direction == 2:  # 下
            bullet_y += self.rect.height // 2
            bullet_dx, bullet_dy = 0, bullet_speed
        elif self.direction == 3:  # 左
            bullet_x -= self.rect.width // 2
            bullet_dx, bullet_dy = -bullet_speed, 0
        
        # 创建子弹对象
        bullet = Bullet(bullet_x, bullet_y, bullet_dx, bullet_dy, self.direction, self)
        return bullet
    
    def shoot_missile(self):
        # 检查冷却时间
        current_time = pygame.time.get_ticks()
        if current_time - self.last_missile < self.missile_cooldown:
            return None
        
        self.last_missile = current_time
        
        # 根据坦克方向确定导弹的初始位置和速度
        missile_speed = 7
        missile_x, missile_y = self.rect.center
        
        # 根据坦克方向调整导弹的初始位置，使其从炮口发射
        if self.direction == 0:  # 上
            missile_y -= self.rect.height // 2
            missile_dx, missile_dy = 0, -missile_speed
        elif self.direction == 1:  # 右
            missile_x += self.rect.width // 2
            missile_dx, missile_dy = missile_speed, 0
        elif self.direction == 2:  # 下
            missile_y += self.rect.height // 2
            missile_dx, missile_dy = 0, missile_speed
        elif self.direction == 3:  # 左
            missile_x -= self.rect.width // 2
            missile_dx, missile_dy = -missile_speed, 0
        
        # 创建导弹对象
        missile = Missile(missile_x, missile_y, missile_dx, missile_dy, self.direction, self)
        return missile
    
    def take_damage(self, damage, is_missile):
        # 如果是普通炮弹，有几率弹开
        if not is_missile:
            deflect_chance = self.armor / 100  # 装甲值决定弹开几率
            if random.random() < deflect_chance:
                return "deflected"  # 炮弹被弹开
        
        # 受到伤害
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return "destroyed"
        return "hit"

# 玩家坦克类
class PlayerTank(Tank):
    def __init__(self, x, y):
        # 加载坦克图像
        tank_image = load_image(get_asset_path('player_tank.svg'))
        bullet_image = load_image(get_asset_path('bullet.svg'))
        missile_image = load_image(get_asset_path('missile.svg'))
        
        super().__init__(x, y, 5, tank_image, bullet_image, missile_image)
        self.original_image = self.image
    
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        
        # 移动控制 - 先确定方向，只在方向改变时才旋转
        new_direction = None
        if keys[K_w]:
            new_direction = 0  # 上
        elif keys[K_d]:
            new_direction = 1  # 右
        elif keys[K_s]:
            new_direction = 2  # 下
        elif keys[K_a]:
            new_direction = 3  # 左
        
        # 只在方向改变时才旋转
        if new_direction is not None and new_direction != self.direction:
            self.rotate(new_direction)
        
        # 根据当前方向移动
        if self.direction == 0 and keys[K_w]:  # 上
            self.move(0, -self.speed)
        elif self.direction == 1 and keys[K_d]:  # 右
            self.move(self.speed, 0)
        elif self.direction == 2 and keys[K_s]:  # 下
            self.move(0, self.speed)
        elif self.direction == 3 and keys[K_a]:  # 左
            self.move(-self.speed, 0)
        
        # 添加射击控制
        if keys[K_SPACE]:
            bullet = self.shoot_bullet()
            if bullet:
                return bullet
        
        # 添加导弹控制
        if keys[K_m]:
            missile = self.shoot_missile()
            if missile:
                return missile
        
        return None

# 机器人坦克类
class RobotTank(Tank):
    def __init__(self, x, y):
        # 加载坦克图像
        tank_image = load_image(get_asset_path('robot_tank.svg'))
        bullet_image = load_image(get_asset_path('bullet.svg'))
        missile_image = load_image(get_asset_path('missile.svg'))
        
        super().__init__(x, y, 3, tank_image, bullet_image, missile_image)
        self.original_image = self.image
        self.move_timer = 0
        self.move_interval = 60  # 每隔一段时间改变移动方向
        self.target = None
    
    def update(self):
        super().update()
        
        # 定时改变移动方向
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            new_direction = random.randint(0, 3)
            if new_direction != self.direction:  # 只在方向改变时才旋转
                self.rotate(new_direction)
        
        # 根据当前方向移动
        if self.direction == 0:  # 上
            self.move(0, -self.speed)
        elif self.direction == 1:  # 右
            self.move(self.speed, 0)
        elif self.direction == 2:  # 下
            self.move(0, self.speed)
        elif self.direction == 3:  # 左
            self.move(-self.speed, 0)
    
    def ai_shoot(self, player):
        # 设置目标
        self.target = player
        
        # 计算与玩家的距离
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 根据距离和随机因素决定是否射击
        if distance < 300 and random.random() < 0.03:
            # 确定射击方向
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.rotate(1)  # 右
                else:
                    self.rotate(3)  # 左
            else:
                if dy > 0:
                    self.rotate(2)  # 下
                else:
                    self.rotate(0)  # 上
            
            # 随机决定使用炮弹还是导弹
            current_time = pygame.time.get_ticks()
            if random.random() < 0.2 and current_time - self.last_missile >= self.missile_cooldown:
                return self.shoot_missile()
            elif current_time - self.last_shot >= self.bullet_cooldown:
                return self.shoot_bullet()
        
        return None

# 子弹/导弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, direction, owner):
        super().__init__()
        self.image = owner.bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = dx
        self.dy = dy
        self.direction = direction
        self.owner = owner
        self.is_missile = False
        self.damage = 10
    
    def update(self):
        # 根据速度向量移动
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # 如果超出屏幕边界，则删除
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, direction, owner):
        super().__init__()
        self.image = owner.missile_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = dx
        self.dy = dy
        self.direction = direction
        self.owner = owner
        self.is_missile = True
        self.damage = 30
    
    def update(self):
        # 根据速度向量移动
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # 如果超出屏幕边界，则删除
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

# 爆炸效果类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, is_large=False):
        super().__init__()
        self.size = 50 if is_large else 30
        self.original_image = load_image(get_asset_path('explosion.svg'))
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.max_frame = 5
    
    def update(self):
        self.frame += 1
        if self.frame >= self.max_frame:
            self.kill()  # 确保从所有精灵组中移除
            return True  # 返回True表示已经完成爆炸动画
        else:
            # 爆炸动画效果
            size = int(self.size * (1 - self.frame / self.max_frame))
            self.image = pygame.transform.scale(self.original_image, (size, size))
            self.rect = self.image.get_rect(center=self.rect.center)
            return False  # 返回False表示爆炸动画还在进行中

# 游戏状态显示
class StatusDisplay:
    def __init__(self):
        try:
            # 尝试加载支持中文的字体
            font_path = None
            # 尝试常见的中文字体
            possible_fonts = [
                'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
                'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
                'C:\\Windows\\Fonts\\msyh.ttc',    # 微软雅黑
                'C:\\Windows\\Fonts\\simkai.ttf',  # 楷体
            ]
            
            for font in possible_fonts:
                if os.path.exists(font):
                    font_path = font
                    debug_print(f"找到中文字体: {font}")
                    break
            
            if font_path:
                self.font = pygame.font.Font(font_path, 36)
                debug_print("成功加载中文字体")
            else:
                # 如果找不到中文字体，使用默认字体
                debug_print("未找到中文字体，使用默认字体")
                self.font = pygame.font.Font(None, 36)
        except Exception as e:
            debug_print(f"加载字体时出错: {e}")
            # 出错时使用默认字体
            self.font = pygame.font.Font(None, 36)
    
    def show_health(self, surface, player, robot):
        # 显示玩家生命值
        player_health_text = self.font.render(f"玩家生命: {player.health}", True, GREEN)
        surface.blit(player_health_text, (10, 10))
        
        # 显示机器人生命值
        robot_health_text = self.font.render(f"机器人生命: {robot.health}", True, RED)
        surface.blit(robot_health_text, (SCREEN_WIDTH - 200, 10))
    
    def show_message(self, surface, message, color=WHITE):
        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(text, text_rect)

# 障碍物类
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((127, 140, 141))  # 灰色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 主游戏类
class Game:
    def __init__(self):
        try:
            debug_print("正在初始化游戏对象...")
            # 加载背景
            background_path = get_asset_path('background.svg')
            debug_print(f"加载背景图像: {background_path}")
            self.background = load_image(background_path)
            debug_print("背景加载完成")
            
            # 初始化音效管理器
            debug_print("初始化音效管理器...")
            self.sound_manager = SoundManager()
            debug_print("音效管理器初始化完成")
            
            # 创建精灵组
            debug_print("创建精灵组...")
            self.all_sprites = pygame.sprite.Group()
            self.obstacles = pygame.sprite.Group()
            self.player_bullets = pygame.sprite.Group()
            self.robot_bullets = pygame.sprite.Group()
            self.explosions = pygame.sprite.Group()
            debug_print("精灵组创建完成")
            
            # 创建障碍物
            debug_print("创建障碍物...")
            self.create_obstacles()
            debug_print("障碍物创建完成")
            
            # 创建坦克
            debug_print("创建玩家坦克...")
            self.player = PlayerTank(100, 300)
            debug_print("创建机器人坦克...")
            self.robot = RobotTank(600, 300)
            
            debug_print("将坦克添加到精灵组...")
            self.all_sprites.add(self.player)
            self.all_sprites.add(self.robot)
            
            debug_print("创建状态显示...")
            self.status_display = StatusDisplay()
            self.game_over = False
            self.winner = None
            
            # 坦克移动音效状态
            self.player_moving = False
            
            debug_print("游戏对象初始化完成")
        except Exception as e:
            print(f"游戏初始化失败: {type(e).__name__}: {e}")
            traceback.print_exc()
            raise
    
    def create_obstacles(self):
        # 从背景SVG中提取障碍物位置
        obstacles = [
            (200, 150, 50, 50),  # x, y, width, height
            (550, 400, 50, 50),
            (350, 250, 30, 100),
            (650, 150, 30, 100),
            (150, 450, 100, 30)
        ]
        
        for x, y, width, height in obstacles:
            obstacle = Obstacle(x, y, width, height)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                
                # 玩家射击
                if event.key == K_SPACE and not self.game_over:
                    bullet = self.player.shoot_bullet()
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.player_bullets.add(bullet)
                        self.sound_manager.play_sound('shoot')
                
                # 玩家发射导弹
                if event.key == K_m and not self.game_over:
                    missile = self.player.shoot_missile()
                    if missile:
                        self.all_sprites.add(missile)
                        self.player_bullets.add(missile)
                        self.sound_manager.play_sound('missile')
                
                # 重新开始游戏
                if event.key == K_r and self.game_over:
                    self.__init__()
        
        return True
    
    def run_logic(self):
        if not self.game_over:
            # 更新所有精灵前先获取玩家可能的射击
            player_projectile = self.player.update()
            if player_projectile:
                self.all_sprites.add(player_projectile)
                self.player_bullets.add(player_projectile)
                if player_projectile.is_missile:
                    self.sound_manager.play_sound('missile')
                else:
                    self.sound_manager.play_sound('shoot')
            
            # 更新除玩家外的所有精灵
            for sprite in self.all_sprites:
                if sprite != self.player:  # 跳过玩家，因为已经更新过了
                    sprite.update()
            
            # 更新爆炸效果
            explosions_to_remove = []
            for explosion in self.explosions:
                if explosion.update():  # 如果爆炸动画完成
                    explosions_to_remove.append(explosion)
            
            # 移除已完成的爆炸效果
            for explosion in explosions_to_remove:
                self.explosions.remove(explosion)
            
            # 检测玩家移动状态并播放音效
            keys = pygame.key.get_pressed()
            if keys[K_w] or keys[K_a] or keys[K_s] or keys[K_d]:
                if not self.player_moving:
                    self.sound_manager.play_sound('tank_move')
                    self.player_moving = True
            else:
                if self.player_moving:
                    self.sound_manager.stop_sound('tank_move')
                    self.player_moving = False
            
            # 检测坦克与障碍物碰撞
            # 玩家坦克
            tank_collisions = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if tank_collisions:
                # 简单的碰撞响应：将坦克推回
                if self.player.direction == 0:  # 上
                    self.player.rect.y += self.player.speed
                elif self.player.direction == 1:  # 右
                    self.player.rect.x -= self.player.speed
                elif self.player.direction == 2:  # 下
                    self.player.rect.y -= self.player.speed
                elif self.player.direction == 3:  # 左
                    self.player.rect.x += self.player.speed
            
            # 机器人坦克
            tank_collisions = pygame.sprite.spritecollide(self.robot, self.obstacles, False)
            if tank_collisions:
                # 简单的碰撞响应：将坦克推回并改变方向
                if self.robot.direction == 0:  # 上
                    self.robot.rect.y += self.robot.speed
                    self.robot.direction = 2
                    self.robot.rotate(self.robot.direction)
                elif self.robot.direction == 1:  # 右
                    self.robot.rect.x -= self.robot.speed
                    self.robot.direction = 3
                    self.robot.rotate(self.robot.direction)
                elif self.robot.direction == 2:  # 下
                    self.robot.rect.y -= self.robot.speed
                    self.robot.direction = 0
                    self.robot.rotate(self.robot.direction)
                elif self.robot.direction == 3:  # 左
                    self.robot.rect.x += self.robot.speed
                    self.robot.direction = 1
                    self.robot.rotate(self.robot.direction)
            
            # 机器人AI射击
            robot_bullet = self.robot.ai_shoot(self.player)
            if robot_bullet:
                self.all_sprites.add(robot_bullet)
                self.robot_bullets.add(robot_bullet)
                if robot_bullet.is_missile:
                    self.sound_manager.play_sound('missile')
                else:
                    self.sound_manager.play_sound('shoot')
            
            # 检测子弹与障碍物碰撞
            for bullet in self.player_bullets:
                if pygame.sprite.spritecollide(bullet, self.obstacles, False):
                    self.explosions.add(Explosion(bullet.rect.center))
                    self.sound_manager.play_sound('explosion')
                    bullet.kill()
            
            for bullet in self.robot_bullets:
                if pygame.sprite.spritecollide(bullet, self.obstacles, False):
                    self.explosions.add(Explosion(bullet.rect.center))
                    self.sound_manager.play_sound('explosion')
                    bullet.kill()
            
            # 检测玩家子弹与机器人碰撞
            hits = pygame.sprite.spritecollide(self.robot, self.player_bullets, True)
            for bullet in hits:
                result = self.robot.take_damage(bullet.damage, bullet.is_missile)
                
                if result == "deflected":
                    # 显示弹开效果
                    self.explosions.add(Explosion(bullet.rect.center))
                    self.sound_manager.play_sound('deflect')
                    self.sound_manager.play_sound('deflect')
                elif result == "hit":
                    # 显示命中效果
                    self.explosions.add(Explosion(bullet.rect.center))
                    self.sound_manager.play_sound('explosion')
                    self.sound_manager.play_sound('explosion')
                elif result == "destroyed":
                    # 显示坦克被摧毁效果
                    self.explosions.add(Explosion(self.robot.rect.center, True))
                    self.sound_manager.play_sound('explosion')
                    self.game_over = True
                    self.winner = "player"
            
            # 检测机器人子弹与玩家碰撞
            hits = pygame.sprite.spritecollide(self.player, self.robot_bullets, True)
            for bullet in hits:
                result = self.player.take_damage(bullet.damage, bullet.is_missile)
                
                if result == "deflected":
                    # 显示弹开效果
                    self.explosions.add(Explosion(bullet.rect.center))
                elif result == "hit":
                    # 显示命中效果
                    self.explosions.add(Explosion(bullet.rect.center))
                elif result == "destroyed":
                    # 显示坦克被摧毁效果
                    self.explosions.add(Explosion(self.player.rect.center, True))
                    self.sound_manager.play_sound('explosion')
                    self.game_over = True
                    self.winner = "robot"
    
    def display_frame(self):
        # 绘制背景
        screen.blit(self.background, (0, 0))
        
        # 绘制所有精灵
        self.all_sprites.draw(screen)
        self.explosions.draw(screen)
        
        # 显示状态
        if not self.game_over:
            self.status_display.show_health(screen, self.player, self.robot)
        else:
            if self.winner == "player":
                self.status_display.show_message(screen, "你赢了! 按R键重新开始", GREEN)
            else:
                self.status_display.show_message(screen, "你输了! 按R键重新开始", RED)
        
        # 更新屏幕
        pygame.display.flip()

# 主函数
def main():
    debug_print("游戏主函数开始执行")
    try:
        debug_print("正在初始化游戏主循环...")
        game = Game()
        done = False
        
        debug_print("游戏开始运行主循环...")
        frame_count = 0
        start_time = pygame.time.get_ticks()
        min_run_time = 3000  # 至少运行3秒
        
        # 显示一个欢迎消息
        font = pygame.font.Font(None, 36)
        welcome_text = font.render("坦克大战游戏已启动! 按ESC键退出", True, WHITE)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(welcome_text, welcome_rect)
        pygame.display.flip()
        
        while not done:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            
            # 确保游戏至少运行一段时间
            if elapsed_time < min_run_time:
                debug_print(f"游戏运行中: {elapsed_time/1000:.1f}秒 / {min_run_time/1000}秒")
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
            
            # 只有在最小运行时间后才处理游戏逻辑
            if elapsed_time >= min_run_time:
                done = not game.process_events()
                game.run_logic()
                game.display_frame()
            else:
                # 在最小运行时间内，只显示欢迎消息
                screen.fill(BLACK)
                screen.blit(welcome_text, welcome_rect)
                # 显示倒计时
                countdown = font.render(f"游戏将在 {(min_run_time - elapsed_time) / 1000:.1f} 秒后开始...", True, WHITE)
                countdown_rect = countdown.get_rect(center=(SCREEN_WIDTH // 2, 100))
                screen.blit(countdown, countdown_rect)
                pygame.display.flip()
            
            clock.tick(FPS)
            frame_count += 1
            if frame_count % 100 == 0 and DEBUG_MODE:
                debug_print(f"游戏已运行 {frame_count} 帧")
        
        debug_print("游戏主循环正常结束")
    except Exception as e:
        print(f"游戏运行时发生错误: {type(e).__name__}: {e}")
        traceback.print_exc()
        # 在发生错误时显示错误信息并等待几秒钟
        try:
            debug_print("尝试显示错误信息...")
            font = pygame.font.Font(None, 36)
            error_text1 = font.render(f"错误: {type(e).__name__}", True, RED)
            error_text2 = font.render(f"{str(e)}", True, RED)
            error_text3 = font.render("按ESC键退出", True, WHITE)
            
            error_rect1 = error_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            error_rect2 = error_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            error_rect3 = error_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            
            screen.fill(BLACK)
            screen.blit(error_text1, error_rect1)
            screen.blit(error_text2, error_rect2)
            screen.blit(error_text3, error_rect3)
            pygame.display.flip()
            
            debug_print("错误信息已显示，等待用户按ESC键退出...")
            # 等待用户按ESC键退出
            waiting = True
            wait_time = 0
            while waiting and wait_time < 300:  # 最多等待10秒
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        waiting = False
                clock.tick(30)
                wait_time += 1
                if wait_time % 30 == 0:
                    debug_print(f"已等待 {wait_time//30} 秒...")
        except Exception as e2:
            print(f"显示错误信息时发生另一个错误: {e2}")
            traceback.print_exc()
    
    debug_print("正在退出游戏...")
    pygame.quit()
    debug_print("pygame已退出")
    sys.exit()

if __name__ == "__main__":
    main()