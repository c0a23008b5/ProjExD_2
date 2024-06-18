import os
import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def reverse(kk_img: pg.Rect) -> dict:
    """
    引数：こうかとんの写真
    戻り値：辞書
    """
    return {
    (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),  # 左
    (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 左斜め上
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),  # 左斜め下
    (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0),   # 上
    (+5, 0): pg.transform.rotozoom(kk_img, 180, 1.0),  # 右
    (+5, -5): pg.transform.rotozoom(kk_img, -135, 1.0),  # 右斜め上
    (+5, +5): pg.transform.rotozoom(kk_img, 180, 1.0),  # 右斜め下
    (0, +5): pg.transform.rotozoom(kk_img, 90, 1.0),  # 下
    }

def check_wh(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんrctまたは爆弾rct
    戻り値:真理値タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    kk_images = reverse(kk_img)
    
    bb_img = pg.Surface((20, 20))  # 空のサーフェイスを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        
        kk_rct.move_ip(sum_mv)
        if check_wh(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        if sum_mv == [0, 0]:  # 何もキーが押されていない時
            screen.blit(kk_img, kk_rct)
        else:  # キーが押されている時の方向転換
            kk_img = kk_images[tuple(sum_mv)]  # reverse関数の辞書にアクセス
            screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_wh(bb_rct)
        if not yoko:  # 横方向の反転
            vx *= -1
        if not tate:  # 縦方向の反転
            vy *= -1        

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
