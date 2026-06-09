import pygame
import random

pygame.init()

screen = pygame.display.set_mode((500, 650))
pygame.display.set_caption("Match Game")

white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (100, 100, 255)
yellow = (255, 255, 200)

items = ["togi", "norigae", "binyeo", "jangdo", "chojong"]
pics = {}

for name in items:
    try:
        img = pygame.image.load(name + ".jpg")
        pics[name] = pygame.transform.scale(img, (64, 64))
    except:
        pics[name] = None

# 初始化6*6棋盘
board = []
for i in range(6):
    row = []
    for j in range(6):
        row.append(random.choice(items))
    board.append(row)

score = 0
steps = 20
selected_row = -1
selected_col = -1
game_over = False
show_congrats = False
show_intro = False
font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 45)

def draw_board():
    for i in range(6):
        for j in range(6):
            x = j * 70 + 40
            y = i * 70 + 100
            pygame.draw.rect(screen, white, (x, y, 60, 60))
            pygame.draw.rect(screen, black, (x, y, 60, 60), 2)
            
            item = board[i][j]
            if item is not None and pics[item] is not None:
                screen.blit(pics[item], (x - 2, y - 2))
            
            if selected_row == i and selected_col == j:
                pygame.draw.rect(screen, green, (x, y, 60, 60), 4)

def find_match():
    match_list = []
    # 横向查找三连
    for i in range(6):
        for j in range(4):
            if board[i][j] == board[i][j+1] == board[i][j+2]:
                match_list.append((i, j))
                match_list.append((i, j+1))
                match_list.append((i, j+2))
    # 纵向查找三连
    for i in range(4):
        for j in range(6):
            if board[i][j] == board[i+1][j] == board[i+2][j]:
                match_list.append((i, j))
                match_list.append((i+1, j))
                match_list.append((i+2, j))
    # 基础去重
    new_list = []
    for pos in match_list:
        if pos not in new_list:
            new_list.append(pos)
    return new_list

def remove_match(match_list):
    for i, j in match_list:
        board[i][j] = None

# 修复下落逻辑，彻底解决空白格子
def drop_down():
    for j in range(6):
        temp = []
        # 收集当前列有效元素
        for i in range(6):
            if board[i][j] is not None:
                temp.append(board[i][j])
        # 整列清空
        for i in range(6):
            board[i][j] = None
        # 从底部向上填充原有图案
        idx = 5
        while temp:
            board[idx][j] = temp.pop()
            idx -= 1
        # 空位补充新图案
        for i in range(6):
            if board[i][j] is None:
                board[i][j] = random.choice(items)

def clear_matches():
    while True:
        m = find_match()
        if len(m) == 0:
            break
        remove_match(m)
        drop_down()

def draw_congrats_popup():
    s = pygame.Surface((500, 650))
    s.set_alpha(180)
    s.fill(black)
    screen.blit(s, (0, 0))
    
    popup_x = 100
    popup_y = 220
    popup_w = 300
    popup_h = 150
    pygame.draw.rect(screen, white, (popup_x, popup_y, popup_w, popup_h))
    pygame.draw.rect(screen, blue, (popup_x, popup_y, popup_w, popup_h), 3)
    
    text1 = big_font.render("Congratulations!", True, blue)
    text1_x = popup_x + (popup_w - text1.get_width()) // 2
    screen.blit(text1, (text1_x, popup_y + 30))
    
    text2 = font.render("You cleared the game!", True, black)
    text2_x = popup_x + (popup_w - text2.get_width()) // 2
    screen.blit(text2, (text2_x, popup_y + 80))
    
    btn_w = 100
    btn_h = 35
    btn_x = popup_x + (popup_w - btn_w) // 2
    btn_y = popup_y + popup_h - 55
    pygame.draw.rect(screen, green, (btn_x, btn_y, btn_w, btn_h))
    pygame.draw.rect(screen, black, (btn_x, btn_y, btn_w, btn_h), 2)
    
    btn_text = font.render("Continue", True, black)
    btn_text_x = btn_x + (btn_w - btn_text.get_width()) // 2
    btn_text_y = btn_y + (btn_h - btn_text.get_height()) // 2
    screen.blit(btn_text, (btn_text_x, btn_text_y))
    
    return pygame.Rect(btn_x, btn_y, btn_w, btn_h)

def draw_intro_popup():
    s = pygame.Surface((500, 650))
    s.set_alpha(180)
    s.fill(black)
    screen.blit(s, (0, 0))
    
    popup_w = 420
    popup_h = 460
    popup_x = (500 - popup_w) // 2
    popup_y = (650 - popup_h) // 2
    
    pygame.draw.rect(screen, yellow, (popup_x, popup_y, popup_w, popup_h))
    pygame.draw.rect(screen, blue, (popup_x, popup_y, popup_w, popup_h), 3)
    
    title = big_font.render("Haengso Museum Artifacts", True, blue)
    title_x = popup_x + (popup_w - title.get_width()) // 2
    screen.blit(title, (title_x, popup_y + 15))
    
    pygame.draw.line(screen, blue, (popup_x + 20, popup_y + 55), (popup_x + popup_w - 20, popup_y + 55), 2)
    
    texts = [
        "1. Pottery - Main archaeological artifact",
        "2. Norigae - Traditional ornament",
        "3. Binyeo - Korean hairpin",
        "4. Jangdo - Women's self-defense tool",
        "5. Chojong Bell - University symbol"
    ]
    
    y = popup_y + 85
    for t in texts:
        txt = font.render(t, True, black)
        txt_x = popup_x + (popup_w - txt.get_width()) // 2
        screen.blit(txt, (txt_x, y))
        y += 45
    
    btn_w = 80
    btn_h = 35
    btn_x = popup_x + (popup_w - btn_w) // 2
    btn_y = popup_y + popup_h - 55
    pygame.draw.rect(screen, green, (btn_x, btn_y, btn_w, btn_h))
    pygame.draw.rect(screen, black, (btn_x, btn_y, btn_w, btn_h), 2)
    
    btn_text = font.render("Close", True, black)
    btn_text_x = btn_x + (btn_w - btn_text.get_width()) // 2
    btn_text_y = btn_y + (btn_h - btn_text.get_height()) // 2
    screen.blit(btn_text, (btn_text_x, btn_text_y))
    
    return pygame.Rect(btn_x, btn_y, btn_w, btn_h)

clock = pygame.time.Clock()
running = True

# 开局自动清理初始自带的三连
clear_matches()

while running:
    screen.fill(gray)
    
    # 绘制分数、步数与棋盘
    score_text = font.render("Score: " + str(score), True, black)
    steps_text = font.render("Steps: " + str(steps), True, black)
    screen.blit(score_text, (20, 30))
    screen.blit(steps_text, (400, 30))
    draw_board()
    
    # 游戏结束提示
    if game_over and not show_congrats and not show_intro:
        if score >= 20:
            show_congrats = True
        else:
            msg = font.render("Game Over! Click to close", True, red)
            screen.blit(msg, (150, 300))
    
    # 绘制弹窗
    if show_congrats:
        btn_rect = draw_congrats_popup()
    if show_intro:
        close_rect = draw_intro_popup()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 分数不足，点击关闭窗口
        if game_over and score < 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
            continue
        
        # 通关弹窗按钮逻辑
        if show_congrats:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    show_congrats = False
                    show_intro = True
            continue
        
        # 介绍弹窗按钮逻辑
        if show_intro:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_rect.collidepoint(event.pos):
                    running = False
            continue
        
        # 鼠标点击选格子、交换
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            r = (y - 100) // 70
            c = (x - 40) // 70
            if 0 <= r < 6 and 0 <= c < 6:
                if selected_row == -1:
                    selected_row = r
                    selected_col = c
                else:
                    r1 = selected_row
                    c1 = selected_col
                    r2 = r
                    c2 = c
                    # 仅相邻格子可交换
                    if (abs(r1 - r2) + abs(c1 - c2)) == 1:
                        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                        m = find_match()
                        if len(m) > 0:
                            remove_match(m)
                            drop_down()
                            clear_matches()
                            score = score + 2
                        else:
                            # 无匹配，还原并扣除步数
                            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                            steps = steps - 1
                    # 取消选中状态
                    selected_row = -1
                    selected_col = -1
                    
                    # 分数达标，短暂延迟后结束游戏
                    if score >= 20 and not game_over:
                        pygame.display.flip()
                        pygame.time.wait(300)
                        game_over = True
                    # 步数用完，游戏结束
                    if steps <= 0:
                        game_over = True
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
