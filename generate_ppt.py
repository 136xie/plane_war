import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. 初始化 PPT 并设置 16:9 比例
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 定义科技风配色
COLOR_BG = RGBColor(10, 10, 35)       # 深邃太空蓝
COLOR_TEXT_MAIN = RGBColor(255, 255, 255) # 纯白
COLOR_TEXT_MUTED = RGBColor(180, 180, 200) # 灰蓝
COLOR_ACCENT = RGBColor(0, 255, 255)   # 极光青（高亮色）
COLOR_BORDER = RGBColor(40, 40, 100)   # 边界线

# 辅助函数：应用深色背景
def apply_dark_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

# 辅助函数：创建统一标题
def add_slide_header(slide, title_text):
    apply_dark_background(slide)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = "Microsoft YaHei"
    p.font.color.rgb = COLOR_ACCENT

# ==================== SLIDE 1: 封面页 ====================
slide_layout = prs.slide_layouts[6] # 空白布局
slide1 = prs.slides.add_slide(slide_layout)
apply_dark_background(slide1)

# 添加装饰性左侧青色线条
left_line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.0), Inches(0.1), Inches(3.5))
left_line.fill.solid()
left_line.fill.fore_color.rgb = COLOR_ACCENT
left_line.line.color.rgb = COLOR_ACCENT

# 添加主标题框
title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
tf = title_box.text_frame
tf.word_wrap = True

p_main = tf.paragraphs[0]
p_main.text = "基于 C 语言与底层 Win32 API 的\n2D 矢量空战游戏设计与实现"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.name = "Microsoft YaHei"
p_main.font.color.rgb = COLOR_TEXT_MAIN
p_main.space_after = Pt(20)

p_sub = tf.add_paragraph()
p_sub.text = "—— 探索轻量化渲染、非阻塞交互与静态内存优化的实时游戏开发"
p_sub.font.size = Pt(18)
p_sub.font.name = "Microsoft YaHei"
p_sub.font.color.rgb = COLOR_TEXT_MUTED
p_sub.space_after = Pt(40)

p_info = tf.add_paragraph()
p_info.text = "汇报人：你的名字   |   专业：计算机科学与技术   |   指导老师：老师名字"
p_info.font.size = Pt(14)
p_info.font.name = "Microsoft YaHei"
p_info.font.color.rgb = COLOR_ACCENT

# ==================== SLIDE 2: 选题背景 ====================
slide2 = prs.slides.add_slide(slide_layout)
add_slide_header(slide2, "选题背景与立意")

# 左侧栏 (现状与瓶颈)
left_box = slide2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "常规教学实践的局限"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

points = [
    "大多数 C 语言实践局限于学生管理系统等静态控制台程序",
    "学生对高频实时系统（Real-time System）缺乏底层逻辑认知",
    "对硬件中断、异步事件检测及内存碎片控制缺乏演练环境"
]
for pt in points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)

# 右侧栏 (突破口与立意)
right_box = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "本项目的研究立意"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

r_points = [
    "完全摆脱商用重型引擎，用纯 C99 标准进行底层游戏开发",
    "直接与 Win32 硬件层进行非阻塞式高频异步数据交互",
    "构建微秒级的轻量级渲染与快速内存复用机制",
    "将离散数学、动力学公式与底层内存管理进行工程融合"
]
for pt in r_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 3: 技术栈选型 ====================
slide3 = prs.slides.add_slide(slide_layout)
add_slide_header(slide3, "技术栈与开发环境选型")

# 左侧：技术栈堆栈图
tech_box = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_tech = tech_box.text_frame
tf_tech.word_wrap = True
p = tf_tech.paragraphs[0]
p.text = "三层架构技术选型"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

stack = [
    "图形层 (EasyX Library)：轻量级窗口管理，免去复杂的 DX/GL 样板代码，专注于矢量渲染核心算法。",
    "系统层 (Win32 API)：通过 <windows.h> 直接截获硬件中断状态，实现微秒级高频异步输入检测。",
    "语言层 (Standard C99)：显式内存控制、指针操纵，最大化 CPU 运算能效，不依赖运行时垃圾回收机制。"
]
for item in stack:
    p_item = tf_tech.add_paragraph()
    p_item.text = "• " + item
    p_item.font.size = Pt(14)
    p_item.font.color.rgb = COLOR_TEXT_MUTED
    p_item.space_after = Pt(12)

# 右侧：开发环境列表
env_box = slide3.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_env = env_box.text_frame
tf_env.word_wrap = True
p_env = tf_env.paragraphs[0]
p_env.text = "工程开发环境配置"
p_env.font.size = Pt(20)
p_env.font.bold = True
p_env.font.color.rgb = COLOR_ACCENT
p_env.space_after = Pt(14)

envs = [
    "编译器：Microsoft Visual C++ (MSVC) / GCC",
    "IDE 环境：Visual Studio 2022 / VS Code",
    "调试工具：Windows Debugger / 显式内存泄漏检测工具",
    "版本控制：Git 协作与本地分支演进管理"
]
for env in envs:
    p_env_item = tf_env.add_paragraph()
    p_env_item.text = "• " + env
    p_env_item.font.size = Pt(14)
    p_env_item.font.color.rgb = COLOR_TEXT_MUTED
    p_env_item.space_after = Pt(12)


# ==================== SLIDE 4: 系统设计与有限状态机 ====================
slide4 = prs.slides.add_slide(slide_layout)
add_slide_header(slide4, "系统整体设计与有限状态机 (FSM)")

left_box = slide4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "游戏有限状态机 (FSM)"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

fsm_points = [
    "STATE_MENU (菜单态)：绘制粒子星空背景，渲染文字呼吸闪烁动画，阻塞等待 SPACE 键触发初始化。",
    "STATE_PLAYING (游戏态)：执行主物理逻辑更新、多重碰撞检测循环、图层堆叠绘制渲染。",
    "STATE_GAMEOVER (结算态)：停止物理更新，维持背景星空渲染，监听键盘复位 (R) 或退出 (ESC)。"
]
for pt in fsm_points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)

right_box = slide4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "帧率锁定与控制流"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

ctrl_points = [
    "使用 Sleep(16) 将游戏主循环约束在 16ms 周期内（约 60 帧/秒）。",
    "物理运动按帧计步：飞机坐标位移速度完全与硬件刷新率（屏幕扫描）保持一致，带来平滑视觉体验。",
    "将数据控制（FSM）与渲染完全解耦，每个状态分支只调用当前状态所需的渲染函数。"
]
for pt in ctrl_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)


# ==================== SLIDE 5: 静态对象池设计 ====================
slide5 = prs.slides.add_slide(slide_layout)
add_slide_header(slide5, "数据结构设计与“静态对象池”内存管理")

left_box = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "数据结构设计 (C 语言 Struct)"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

struct_points = [
    "Player：玩家位置 (x,y)、尺寸 (w,h)、命数、无敌与开火冷却计时器。",
    "Bullet & Enemy：子弹与敌机的活动标记 active、血量、类型等属性。",
    "Particle：爆炸粒子运动向量 (vx,vy)、当前寿命、最大寿命、活动状态。",
    "所有结构体紧凑布局，最大化提升 CPU 缓存命中率。"
]
for pt in struct_points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)

right_box = slide5.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "静态对象池机制 (Object Pool)"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

pool_points = [
    "避开动态内存管理：频繁调用 malloc/free 会产生严重的内存碎片，系统开销极大并会导致频繁卡顿。",
    "预先分配：全局静态数组初始化 g_bullets[100] 与 g_enemies[50]。",
    "安全回收：通过 getFreeBullet() 检索空闲 active 标记并激活，超出边界或击中时一键回收状态。",
    "时间复杂度：实现 O(1) 的超高速无延迟内存复用，保证游戏流畅，杜绝任何内存泄露漏洞。"
]
for pt in pool_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 6: 难点一：非阻塞异步输入 ====================
slide6 = prs.slides.add_slide(slide_layout)
add_slide_header(slide6, "开发难点解析一：非阻塞异步按键处理")

left_box = slide6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "技术挑战与瓶颈"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

input_challenges = [
    "C 语言自带的输入函数（如 scanf、getch）属于阻塞式，会导致主线程静止等待，无法用于实时游戏。",
    "不支持多键无冲突并按，玩家无法在斜向飞行的同时进行高频射击。",
    "键盘重复延迟会导致连续输入出现卡顿感。"
]
for pt in input_challenges:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)

right_box = slide6.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "非阻塞掩码按键宏解决方案"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

input_solutions = [
    "核心代码：#define KEY_DOWN(vk) ((GetAsyncKeyState(vk) & 0x8000) ? 1 : 0)",
    "硬件级直接查询：通过 Win32 API 异步侦察硬件按键物理电平，毫秒级反馈且绝不卡死进程。",
    "掩码位运算：使用 0x8000 (二进制 1000 0000 0000 0000) 与系统返回值进行 AND 运算，精准提取最高位状态。",
    "多键并行：各判定独立执行，玩家能完美多键无冲突并按，实现丝滑的斜方向移动。"
]
for pt in input_solutions:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 7: 难点二：双缓冲 ====================
slide7 = prs.slides.add_slide(slide_layout)
add_slide_header(slide7, "开发难点解析二：高频消隐与双缓冲渲染")

left_box = slide7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "技术挑战与闪烁成因"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

render_challenges = [
    "实时游戏每秒重绘 60 次，直接在屏幕物理画布上频繁“擦除并画画”，会导致显示器捕捉到未画完的“半成品”。",
    "同屏处理数百个几何矢量体时，高频硬件刷新会造成强烈的、刺眼的屏幕闪烁。",
    "图形层级重叠错误，导致飞机、子弹互相覆盖异常。"
]
for pt in render_challenges:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)

right_box = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "双缓冲与图层渲染控制"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

render_solutions = [
    "使用 BeginBatchDraw() 锁定物理前台，将所有几何绘制指令拦截在隐藏的后台内存画布中。",
    "待整帧（背景星空、子弹、粒子、飞机、UI）拼接堆叠完毕后，调用 FlushBatchDraw() 一瞬间复制到屏幕。",
    "图层渲染顺序控制：背景 -> 道具/子弹 -> 敌机 -> 粒子 -> 玩家机体 -> 顶层 UI。保证无任何视觉遮挡 Bug。"
]
for pt in render_solutions:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 8: 算法亮点 ====================
slide8 = prs.slides.add_slide(slide_layout)
add_slide_header(slide8, "算法亮点：AABB 碰撞检测与动力学拟真")

left_box = slide8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "AABB 碰撞算法与边界检测"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

aabb_points = [
    "中心与对称性建模：将游戏实体抽象为 Axis-Aligned Bounding Box (AABB) 轴对齐包围盒模型。",
    "边界极限计算：依据中心 (x,y) 和 (w,h) 推导 Left/Right/Top/Bottom 四向边界。",
    "碰撞检测核心公式：(l1 < r2 && r1 > l2 && t1 < b2 && b1 > t2)。",
    "极佳的运算效率：在大循环（子弹 100 x 敌人 50）中，耗时近乎为零，对物理帧率无任何负面抖动。"
]
for pt in aabb_points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)

right_box = slide8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "物理动力学与渐变数值拟真"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

physics_points = [
    "正弦漂移：大飞机横向叠加 sinf(frameCount * 0.05f) * 1.5f 位移，模拟空气阻力下的平滑摆动。",
    "重力加速度拟真：碎片爆发后垂直速度高频加算 vy += 0.15f，呈现流畅的拟真抛物线下坠轨迹。",
    "粒子寿命光衰退计算：依据 ratio = life/maxLife 比例，动态插值计算 RGB 颜色通道（黄->橙->深红）及半径大小。"
]
for pt in physics_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 9: 游戏业务流与机制 ====================
slide9 = prs.slides.add_slide(slide_layout)
add_slide_header(slide9, "系统业务流设计与游戏渐进式机制")

left_box = slide9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "高内聚的系统业务流"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

flow_points = [
    "输入捕获 -> 玩家数据更新 -> 子弹运动物理更新 -> 敌机运动与自动生成 -> 多重交叉碰撞检测 -> 粒子状态更新 -> 全画面批量重绘。",
    "主循环每帧（16ms）无卡顿地完整清洗上述数据队列，各模块通过函数指针级高内聚组织。"
]
for pt in flow_points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)

right_box = slide9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "渐进式难度与防御保障机制"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

mech_points = [
    "自适应动态出怪率：g_enemySpawnRate = imax(15, 45 - g_score/500)。随着分数升高，出怪频率呈指数提升，难度渐进式增加。",
    "无敌防护盾（invTimer）：刚出生或撞击后赋予 90 帧无敌时间（此时飞机交替闪烁表示），极大优化了连续受击的游戏体验。"
]
for pt in mech_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(12)


# ==================== SLIDE 10: 总结与展望 ====================
slide10 = prs.slides.add_slide(slide_layout)
add_slide_header(slide10, "系统设计总结与未来优化展望")

left_box = slide10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf_l = left_box.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "工程实践与设计总结"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT_MAIN
p.space_after = Pt(14)

summary_points = [
    "成功使用纯 C 语言与系统级 Win32 API 搭建出一个非阻塞的高帧率 2D 实时图形交互系统。",
    "在零图片依赖、常驻几百个活动粒子的极限混战情况下，CPU 占用率牢牢控制在 1% 以下，编译后程序大小仅数百 KB。",
    "系统深刻锻炼了对结构体指针、静态对象池复用、非阻塞输入检测、二进制位运算、经典图形学及双缓冲流水线的实战能力。"
]
for pt in summary_points:
    p_pt = tf_l.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)

right_box = slide10.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
tf_r = right_box.text_frame
tf_r.word_wrap = True
p_r = tf_r.paragraphs[0]
p_r.text = "未来优化方向展望"
p_r.font.size = Pt(20)
p_r.font.bold = True
p_r.font.color.rgb = COLOR_ACCENT
p_r.space_after = Pt(14)

future_points = [
    "引入高精度 Delta Time（时间物理步长分离）：彻底让逻辑物理位移与刷新率帧率解耦，完美自适应当前主流的 144Hz 甚至更高刷新率电竞显示器。",
    "音效管理（Windows MCI）：使用系统级 mciSendString 多线程加载外部音效，丰富游戏的视听表现。",
    "行为树 AI：为后期 Boss 战引入更高级的行为决策树 AI 模型，设计复杂的子弹躲避及编队运动策略。"
]
for pt in future_points:
    p_pt = tf_r.add_paragraph()
    p_pt.text = "• " + pt
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = COLOR_TEXT_MUTED
    p_pt.space_after = Pt(10)


# ==================== SLIDE 11: 感谢页 ====================
slide11 = prs.slides.add_slide(slide_layout)
apply_dark_background(slide11)

# 添加装饰性左侧青色线条
left_line = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.2), Inches(0.1), Inches(3.0))
left_line.fill.solid()
left_line.fill.fore_color.rgb = COLOR_ACCENT
left_line.line.color.rgb = COLOR_ACCENT

title_box = slide11.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11.0), Inches(4.0))
tf = title_box.text_frame
tf.word_wrap = True

p_main = tf.paragraphs[0]
p_main.text = "感谢各位老师的聆听！"
p_main.font.size = Pt(44)
p_main.font.bold = True
p_main.font.name = "Microsoft YaHei"
p_main.font.color.rgb = COLOR_TEXT_MAIN
p_main.space_after = Pt(20)

p_sub = tf.add_paragraph()
p_sub.text = "恳请各位评委老师批评指正"
p_sub.font.size = Pt(22)
p_sub.font.name = "Microsoft YaHei"
p_sub.font.color.rgb = COLOR_TEXT_MUTED
p_sub.space_after = Pt(40)

p_info = tf.add_paragraph()
p_info.text = "THE END. WELCOME TO Q&A"
p_info.font.size = Pt(16)
p_info.font.bold = True
p_info.font.name = "Consolas"
p_info.font.color.rgb = COLOR_ACCENT

# 保存文件
prs.save("defense_presentation.pptx")
print("PowerPoint file generated successfully as 'defense_presentation.pptx'!")
