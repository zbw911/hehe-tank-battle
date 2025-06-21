import pygame
import os

class SoundManager:
    def __init__(self):
        # 初始化pygame混音器
        pygame.mixer.init()
        
        # 音效字典
        self.sounds = {}
        
        # 加载音效
        self.load_sounds()
    
    def get_asset_path(self, filename):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', filename)
    
    def load_sounds(self):
        # 这里我们没有实际的音效文件，所以创建一些简单的音效
        # 在实际项目中，你可以替换为真实的音效文件
        self.create_simple_sounds()
    
    def create_simple_sounds(self):
        # 创建简单的音效
        # 射击音效 - 短促的噪音
        self.create_shoot_sound()
        
        # 爆炸音效 - 较长的噪音
        self.create_explosion_sound()
        
        # 坦克移动音效 - 循环的低频噪音
        self.create_tank_move_sound()
        
        # 导弹发射音效 - 更强的射击音效
        self.create_missile_sound()
        
        # 弹开音效 - 金属碰撞声
        self.create_deflect_sound()
    
    def create_shoot_sound(self):
        # 创建射击音效
        sound = pygame.mixer.Sound(self.generate_shoot_sound())
        sound.set_volume(0.3)
        self.sounds['shoot'] = sound
    
    def create_explosion_sound(self):
        # 创建爆炸音效
        sound = pygame.mixer.Sound(self.generate_explosion_sound())
        sound.set_volume(0.5)
        self.sounds['explosion'] = sound
    
    def create_tank_move_sound(self):
        # 创建坦克移动音效
        sound = pygame.mixer.Sound(self.generate_tank_move_sound())
        sound.set_volume(0.2)
        self.sounds['tank_move'] = sound
    
    def create_missile_sound(self):
        # 创建导弹发射音效
        sound = pygame.mixer.Sound(self.generate_missile_sound())
        sound.set_volume(0.4)
        self.sounds['missile'] = sound
    
    def create_deflect_sound(self):
        # 创建弹开音效
        sound = pygame.mixer.Sound(self.generate_deflect_sound())
        sound.set_volume(0.3)
        self.sounds['deflect'] = sound
    
    def generate_shoot_sound(self):
        # 生成射击音效的字节数据
        # 这是一个简单的白噪声
        import array
        import math
        import random
        
        sample_rate = 22050
        duration = 0.2  # 秒
        n_samples = int(round(duration * sample_rate))
        
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            buf[i] = int(random.randint(-10000, 10000) * math.exp(-i / (sample_rate * 0.1)))
        
        return pygame.mixer.Sound(buffer=buf)
    
    def generate_explosion_sound(self):
        # 生成爆炸音效的字节数据
        import array
        import math
        import random
        
        sample_rate = 22050
        duration = 0.5  # 秒
        n_samples = int(round(duration * sample_rate))
        
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            buf[i] = int(random.randint(-20000, 20000) * math.exp(-i / (sample_rate * 0.2)))
        
        return pygame.mixer.Sound(buffer=buf)
    
    def generate_tank_move_sound(self):
        # 生成坦克移动音效的字节数据
        import array
        import math
        import random
        
        sample_rate = 22050
        duration = 1.0  # 秒
        n_samples = int(round(duration * sample_rate))
        
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            # 低频噪音
            buf[i] = int(random.randint(-5000, 5000) * (0.5 + 0.5 * math.sin(2 * math.pi * i / sample_rate * 10)))
        
        return pygame.mixer.Sound(buffer=buf)
    
    def generate_missile_sound(self):
        # 生成导弹发射音效的字节数据
        import array
        import math
        import random
        
        sample_rate = 22050
        duration = 0.3  # 秒
        n_samples = int(round(duration * sample_rate))
        
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            # 更强的噪音，带有下降的音调
            freq = 200 - 150 * (i / n_samples)
            buf[i] = int(random.randint(-15000, 15000) * math.exp(-i / (sample_rate * 0.15)) * 
                       (0.5 + 0.5 * math.sin(2 * math.pi * i / sample_rate * freq)))
        
        return pygame.mixer.Sound(buffer=buf)
    
    def generate_deflect_sound(self):
        # 生成弹开音效的字节数据
        import array
        import math
        import random
        
        sample_rate = 22050
        duration = 0.15  # 秒
        n_samples = int(round(duration * sample_rate))
        
        buf = array.array('h', [0] * n_samples)
        for i in range(n_samples):
            # 金属碰撞声
            freq = 800 + 400 * math.sin(i / n_samples * math.pi)
            buf[i] = int(10000 * math.sin(2 * math.pi * i / sample_rate * freq) * 
                       math.exp(-i / (sample_rate * 0.05)))
        
        return pygame.mixer.Sound(buffer=buf)
    
    def play_sound(self, sound_name):
        # 播放指定的音效
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def stop_sound(self, sound_name):
        # 停止指定的音效
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()