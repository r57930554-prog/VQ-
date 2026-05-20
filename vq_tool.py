import cv2
import numpy as np
from pynput import mouse, keyboard
import threading
import time
from enum import Enum

# ==================== الإعدادات ====================

# المفاتيح
VALID_KEYS = [
    "As1", "Gf2", "Doushhsjuuhrhuh3", "Ihsjsjsj4", "Hfufifudu5",
    "Hdhehdudu6", "Hdhdhdhdh7", "Gfhdhdhdh8", "Hrhdhdhdb9", "Hsusjsiugfrbd10",
    "Ughhdhudhehh11", "Brhdhdhchdhh12", "Bfhfhfhdhxhxh13", "Bfhfhfhdhhdh14",
    "Hfhdhdhdhskai15", "Shshdhdhdhdhdhk16", "Jdjdhdydvegdvrhdy17",
    "Hthdbdcrxecrheu18", "Jdjdyfyevecdvehddyh19", "Hdhdhdhdhdbdv20"
]

# الألوان (BGR)
COLOR_GREEN = (0, 255, 0)  # 00ff00
COLOR_LIGHT_BLUE = (255, 200, 0)  # أزرق فاتح
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# نطاق اللون الأخضر (HSV)
LOWER_GREEN = np.array([40, 40, 40])
UPPER_GREEN = np.array([80, 255, 255])

class TargetType(Enum):
    HEAD = 1
    CHEST = 2
    RANDOM = 3

class VQWeaponTester:
    def __init__(self):
        self.authenticated = False
        self.current_key = ""
        self.running = False
        self.auto_fire_enabled = False
        self.drag_force = 0.5  # قوة السحب من 0 إلى 1
        self.target_type = TargetType.RANDOM
        self.camera = None
        self.mouse_controller = mouse.Controller()
        self.listener = None
        self.screen_width = 1920
        self.screen_height = 1080
        
    def login(self):
        """شاشة تسجيل الدخول"""
        print("=" * 50)
        print("🔐 VQ - نظام اختبار الأسلحة")
        print("=" * 50)
        print("أدخل مفتاح الدخول:")
        key = input("> ").strip()
        
        if key in VALID_KEYS:
            self.authenticated = True
            self.current_key = key
            print(f"✅ تم التحقق بنجاح! مرحباً بك 💙")
            return True
        else:
            print("❌ مفتاح خاطئ!")
            return False
    
    def on_mouse_click(self, x, y, button, pressed):
        """معالج نقرات الماوس"""
        if pressed:
            if button == mouse.Button.left:
                # كليك يسار = Auto Fire
                self.auto_fire_enabled = True
                self.fire()
            elif button == mouse.Button.right:
                # كليك يمين = تعديل الإيم (للإشارة)
                pass
    
    def on_keyboard_press(self, key):
        """معالج لوحة المفاتيح"""
        try:
            if key == keyboard.Key.esc:
                self.running = False
        except AttributeError:
            pass
    
    def detect_green_circle(self, frame):
        """كشف الدائرة الخضراء"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        
        # تجميع المناطق الخضراء
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        circles = []
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:  # حد أدنى للحجم
                circles.append((int(x), int(y), int(radius)))
        
        return circles
    
    def get_target_position(self, circle_x, circle_y, circle_radius):
        """حساب موقع الهدف حسب النوع"""
        if self.target_type == TargetType.HEAD:
            # الرأس في أعلى الدائرة
            target_y = circle_y - circle_radius // 2
            target_x = circle_x
        elif self.target_type == TargetType.CHEST:
            # الصدر في منتصف الدائرة
            target_x = circle_x
            target_y = circle_y
        else:  # RANDOM
            # اختيار عشوائي
            choice = np.random.randint(0, 2)
            if choice == 0:
                target_y = circle_y - circle_radius // 2
            else:
                target_y = circle_y
            target_x = circle_x
        
        return int(target_x), int(target_y)
    
    def aim_at_target(self, target_x, target_y):
        """توجيه الإيم نحو الهدف"""
        current_x, current_y = self.mouse_controller.position
        
        # حساب الفرق
        diff_x = target_x - current_x
        diff_y = target_y - current_y
        
        # تطبيق قوة السحب
        move_x = int(diff_x * self.drag_force)
        move_y = int(diff_y * self.drag_force)
        
        # تحريك الماوس
        new_x = current_x + move_x
        new_y = current_y + move_y
        
        self.mouse_controller.position = (new_x, new_y)
    
    def fire(self):
        """إطلاق النار"""
        print("💥 إطلاق!")
    
    def update_drag_force(self, increment):
        """تحديث قوة السحب"""
        self.drag_force = max(0.1, min(1.0, self.drag_force + increment))
        print(f"⚙️ قوة السحب: {self.drag_force:.2f}")
    
    def change_target_type(self):
        """تبديل نوع الهدف"""
        if self.target_type == TargetType.HEAD:
            self.target_type = TargetType.CHEST
            print("🎯 الهدف: الصدر")
        elif self.target_type == TargetType.CHEST:
            self.target_type = TargetType.RANDOM
            print("🎲 الهدف: عشوائي")
        else:
            self.target_type = TargetType.HEAD
            print("🎯 الهدف: الرأس")
    
    def main_loop(self):
        """الحلقة الرئيسية"""
        self.camera = cv2.VideoCapture(0)
        self.running = True
        
        # إعداد مستمع الماوس
        mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        mouse_listener.start()
        
        # إعداد مستمع لوحة المفاتيح
        keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_press)
        keyboard_listener.start()
        
        print("\n" + "=" * 50)
        print("🎮 البرنامج قيد التشغيل!")
        print("=" * 50)
        print("🖱️  كليك يسار: Auto Fire")
        print("📊 حرف U/D: تعديل قوة السحب")
        print("🔄 حرف T: تبديل نوع الهدف")
        print("🛑 ESC: إيقاف")
        print("=" * 50 + "\n")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                # الحصول على حجم الإطار
                height, width = frame.shape[:2]
                self.screen_width = width
                self.screen_height = height
                
                # كشف الدوائر الخضراء
                circles = self.detect_green_circle(frame)
                
                # معالجة كل دائرة خضراء
                for circle_x, circle_y, circle_radius in circles:
                    # رسم الدائرة
                    cv2.circle(frame, (circle_x, circle_y), circle_radius, COLOR_LIGHT_BLUE, 2)
                    
                    # حساب موقع الهدف
                    target_x, target_y = self.get_target_position(circle_x, circle_y, circle_radius)
                    
                    # رسم الهدف
                    cv2.circle(frame, (target_x, target_y), 5, COLOR_GREEN, -1)
                    
                    # توجيه الإيم إذا كان Auto Fire مفعلاً
                    if self.auto_fire_enabled:
                        self.aim_at_target(target_x, target_y)
                
                # عرض معلومات على الشاشة
                info_text = f"Drag Force: {self.drag_force:.2f} | Target: {self.target_type.name}"
                cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_LIGHT_BLUE, 2)
                
                # عرض FPS
                frame_count += 1
                elapsed = time.time() - start_time
                if elapsed > 1:
                    fps = frame_count / elapsed
                    cv2.putText(frame, f"FPS: {fps:.0f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_LIGHT_BLUE, 2)
                    frame_count = 0
                    start_time = time.time()
                
                # عرض الإطار
                cv2.imshow('VQ - Weapon Testing Tool', frame)
                
                # معالجة المفاتيح
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q أو ESC
                    self.running = False
                elif key == ord('u'):  # زيادة قوة السحب
                    self.update_drag_force(0.1)
                elif key == ord('d'):  # تقليل قوة السحب
                    self.update_drag_force(-0.1)
                elif key == ord('t'):  # تبديل نوع الهدف
                    self.change_target_type()
        
        except KeyboardInterrupt:
            print("\n⛔ تم الإيقاف بواسطة المستخدم")
        
        finally:
            self.running = False
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            mouse_listener.stop()
            keyboard_listener.stop()
            print("\n✅ تم إغلاق البرنامج بنجاح")

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    tester = VQWeaponTester()
    
    # محاولة تسجيل الدخول
    attempts = 0
    while attempts < 3 and not tester.authenticated:
        if not tester.login():
            attempts += 1
            if attempts < 3:
                print(f"محاولات متبقية: {3 - attempts}\n")
    
    if tester.authenticated:
        # تشغيل البرنامج الرئيسي
        tester.main_loop()
    else:
        print("❌ فشل التحقق - تم إغلاق البرنامج")