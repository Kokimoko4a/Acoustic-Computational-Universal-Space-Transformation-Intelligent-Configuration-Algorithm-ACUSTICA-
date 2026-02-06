import pyvista as pv
import numpy as np

def generate_detailed_sax_hall():
    plotter = pv.Plotter(title="ACUSTICA - Pro Saxophone Studio")
    plotter.set_background("#121212") # Тъмно сив модерен фон

    # 1. ОСНОВНА КОНСТРУКЦИЯ (Шестоъгълник)
    # По-висока резолюция за по-гладки ръбове
    hall_base = pv.Cylinder(radius=12, height=0.2, center=(0, 0, 0), resolution=6, direction=(0, 0, 1))
    plotter.add_mesh(hall_base, color="#333333", label="Floor")

    # 2. АКУСТИЧНИ СТЕНИ С ПРОМЕНЛИВА ГЕОМЕТРИЯ
    for i in range(6):
        angle = i * (np.pi / 3)
        x = 11.5 * np.cos(angle)
        y = 11.5 * np.sin(angle)
        
        # Основна стена
        wall = pv.Cube(center=(x, y, 4), x_length=0.4, y_length=11, z_length=8)
        # Завъртаме стената, за да следва шестоъгълника
        wall.rotate_z(np.degrees(angle) + 90, inplace=True)
        plotter.add_mesh(wall, color="#5D4037", opacity=0.9)

        # ДОБАВЯНЕ НА ДЕТАЙЛИ: Вертикални дифузори (Diffusers)
        # Тези "ребра" по стените разбиват звуковите вълни
        for j in range(-4, 5):
            offset = j * 1.2
            # Изчисляваме позицията на всяко ребро върху стената
            dx = x + (offset * -np.sin(angle))
            dy = y + (offset * np.cos(angle))
            
            diffuser = pv.Box(bounds=[dx-0.1, dx+0.1, dy-0.1, dy+0.1, 0, 8])
            diffuser.rotate_z(np.degrees(angle), inplace=True)
            # Различна височина за по-добра дифузия (алгоритмичен дизайн)
            scale_z = 0.5 + np.random.rand() * 0.5
            diffuser.scale([1, 1, scale_z], inplace=True)
            
            plotter.add_mesh(diffuser, color="#D2B48C")

    # 3. АКУСТИЧЕН ТАВАН (Тип "Cloud")
    # Наклонен таван, за да няма успоредност с пода
    ceiling = pv.Cylinder(radius=11, height=0.3, center=(0, 0, 8.5), resolution=6, direction=(0, 0, 1))
    ceiling.rotate_x(5, inplace=True) # 5 градуса наклон за акустика
    plotter.add_mesh(ceiling, color="#8B4513", opacity=0.7)

    # 4. ЦЕНТРАЛНА СЦЕНА И СТОЙКА ЗА САКСОФОН
    stage = pv.Cylinder(radius=3, height=0.4, center=(0, 0, 0.2), resolution=50)
    plotter.add_mesh(stage, color="darkred")
    
    # Визуализация на източника на звук (Саксофонист)
    mic_stand = pv.Cylinder(radius=0.1, height=2, center=(0, 0, 1.2))
    plotter.add_mesh(mic_stand, color="silver")

    print("Детайлният модел на ACUSTICA е готов!")
    plotter.add_text("Advanced Saxophone Diffusion Hall", position="upper_left", font_size=10)
    
    # Добавяме легенда или координати за ориентиране
    plotter.add_axes()
    plotter.show()

if __name__ == "__main__":
    generate_detailed_sax_hall()