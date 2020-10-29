import random, time, math
WIDTH = 480
HEIGHT = 680
backgrounds = []
backgrounds.append(Actor("map", topleft=(0, 0)))
backgrounds.append(Actor("map", bottomleft=(0, 0)))
hero = Actor("warplane_1", midbottom=(WIDTH // 2, HEIGHT - 50))
hero.speed = 5
hero.animcount = 0
hero.score = 0
hero.live = 5
hero.unattack = False
hero.ukcount = 0
gameover = False
hero.power = False
enemies = []
powers = []
bullets = []
tweens = ["linear", "accelerate", "decelerate","accel_decel", \
          "in_elastic", "out_elastic", "in_out_elastic", \
          "bounce_end", "bounce_start", "bounce_start_end"]

def spawn_enemy():
    origin_x = random.randint(50, WIDTH)
    target_x = random.randint(50, WIDTH)
    tn = random.choice(tweens)
    dn = random.randint(3, 6)
    enemy = Actor("enemy1", bottomright=(origin_x, 0))
    if random.randint(1, 100) < 20:
        enemy.image = "enemy2"
    enemies.append(enemy)
    animate(enemy, tween=tn, duration=dn, topright=(target_x, HEIGHT))



def update_enemy():
    global gameover
    for enemy in enemies:
        if enemy.top >= HEIGHT:
            enemies.remove(enemy)
            continue
        n = enemy.collidelist(bullets)
        if n != -1:
            enemies.remove(enemy)
            bullets.remove(bullets[n])
            sounds.shooted.play()
            hero.score += 200 if enemy.image == "enemy2" else 100

        elif enemy.colliderect(hero) and not hero.unattack:
            hero.live -= 1
            if hero.live > 0:
                hero.unattack = True
                hero.ukcount = 100
                enemies.remove(enemy)
                sounds.shooted.play()
            else:
                sounds.gameover.play()
                gameover = True
                music.stop()
                time.sleep(0.5)


def draw():
    if gameover:
        screen.blit("gameover", (0, 0))
        return
    for backimgae in backgrounds:
        backimgae.draw()
    for bullet in bullets:
        bullet.draw()
    for powerup in powers:
        powerup.draw()
    for enemy in enemies:
        enemy.draw()
    draw_hero()
    draw_hud()



def update_hero():
    move_hero()
    hero.animcount = (hero.animcount + 1) % 20
    if hero.animcount == 0:
        hero.image = "warplane_1"
    elif hero.animcount == 10:
        hero.image = "warplane_2"
    if hero.unattack:
        hero.ukcount -= 1
        if hero.ukcount <= 0:
            hero.unattack = False
            hero.ukcount = 100

def move_hero():
    if keyboard.right:
        hero.x += hero.speed
    elif keyboard.left:
        hero.x -= hero.speed
    if keyboard.down:
        hero.y += hero.speed
    elif keyboard.up:
        hero.y -= hero.speed
    if hero.left < 0:
        hero.left = 0
    elif hero.right > WIDTH:
        hero.right = WIDTH
    if hero.top < 0:
        hero.top = 0
    elif hero.bottom > HEIGHT:
        hero.bottom = HEIGHT
    if keyboard.space:
        clock.schedule_unique(shoot, 0.1)
def update_background():
    for backimage in backgrounds:
        backimage.y += 5
        if backimage.top > HEIGHT:
            backimage.bottom = 0


def update():
    if gameover:
        clock.unschedule(spawn_enemy)
        return
    update_background()
    update_hero()
    update_bullets()
    update_powerup()
    update_enemy()


def draw_hero():
    if hero.unattack:
        if hero.ukcount % 5 == 0:
            return
    hero.draw()

def shoot():
    sounds.bullet.play()
    bullets.append(Actor("bullet", midbottom=(hero.x, hero.top)))

    if hero.power:
        leftbullet = Actor("bullet", midbottom=(hero.x, hero.top))
        leftbullet.angle = 10
        bullets.append(leftbullet)
        rightbullet = Actor("bullet", midbottom=(hero.x, hero.top))
        rightbullet.angle = -10
        bullets.append(rightbullet)

def update_bullets():
    for bullet in bullets:
        theta = math.radians(bullet.angle + 90)
        bullet.x += 10 * math.cos(theta)
        bullet.y -= 10 * math.sin(theta)
        if bullet.bottom < 0:
            bullets.remove(bullet)

def update_powerup():
    for powerup in powers:
        powerup.y += 2
        if powerup.top > HEIGHT:
            powers.remove(powerup)
        elif powerup.colliderect(hero):
            powers.remove(powerup)
            hero.power = True
            clock.schedule(powerdown, 5.0)
    if random.randint(1, 1000) < 5:
            x = random.randint(50, WIDTH)
            powerup = Actor("powerup", bottomright=(x, 0))
            powers.append(powerup)


def powerdown():
    hero.power = False

def draw_hud():
    for i in range(hero.live):
        screen.blit("live", (i * 35, HEIGHT - 65))
    screen.draw.text(str(hero.score), topleft=(20, 20),
                     fontname="marker_felt", fontsize=25)

music.play("simplethunder")
clock.schedule_interval(spawn_enemy, 1.0)




