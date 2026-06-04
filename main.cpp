#define NOMINMAX
#include <graphics.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <tchar.h>

#define WINDOW_WIDTH  720
#define WINDOW_HEIGHT 960
#define MAX_BULLETS   100
#define MAX_ENEMIES   50
#define MAX_PARTICLES 200
#define MAX_STARS     80
#define PLAYER_SPEED  6
#define BULLET_SPEED  10
#define SHOOT_CD      8
#define INVINCIBLE    90
#define MAX_LIVES     3

#define ENEMY_SMALL  0
#define ENEMY_MEDIUM 1
#define ENEMY_BIG    2

#define STATE_MENU     0
#define STATE_PLAYING  1
#define STATE_GAMEOVER 2

#define KEY_DOWN(vk) ((GetAsyncKeyState(vk) & 0x8000) ? 1 : 0)

/* ===== structs ===== */
typedef struct { float x,y; int w,h; int lives; int invTimer; int shootTimer; } Player;
typedef struct { float x,y; int w,h; int active; } Bullet;
typedef struct { float x,y; int w,h; int speed; int hp; int type; int active; } Enemy;
typedef struct { float x,y; float vx,vy; int life,maxLife; int active; } Particle;
typedef struct { float x,y; int speed,bright; } Star;

/* ===== globals ===== */
Player   g_player;
Bullet   g_bullets[MAX_BULLETS];
Enemy    g_enemies[MAX_ENEMIES];
Particle g_particles[MAX_PARTICLES];
Star     g_stars[MAX_STARS];
int g_score, g_highScore, g_state, g_enemySpawnTimer, g_enemySpawnRate, g_frameCount;

/* ===== helpers ===== */
static int imin(int a,int b){return a<b?a:b;}
static int imax(int a,int b){return a>b?a:b;}

void initStars(){
    for(int i=0;i<MAX_STARS;i++){
        g_stars[i].x=(float)(rand()%WINDOW_WIDTH);
        g_stars[i].y=(float)(rand()%WINDOW_HEIGHT);
        g_stars[i].speed=rand()%3+1;
        g_stars[i].bright=rand()%156+100;
    }
}

void initGame(){
    g_player.x=WINDOW_WIDTH/2.0f; g_player.y=WINDOW_HEIGHT-120.0f;
    g_player.w=50; g_player.h=60; g_player.lives=MAX_LIVES;
    g_player.invTimer=60; g_player.shootTimer=0;
    for(int i=0;i<MAX_BULLETS;i++)   g_bullets[i].active=0;
    for(int i=0;i<MAX_ENEMIES;i++)   g_enemies[i].active=0;
    for(int i=0;i<MAX_PARTICLES;i++) g_particles[i].active=0;
    g_score=0; g_enemySpawnTimer=0; g_enemySpawnRate=45; g_frameCount=0;
    initStars();
}

/* ===== object pool ===== */
Bullet* getFreeBullet(){
    for(int i=0;i<MAX_BULLETS;i++) if(!g_bullets[i].active)return &g_bullets[i];
    return NULL;
}
Enemy* getFreeEnemy(){
    for(int i=0;i<MAX_ENEMIES;i++) if(!g_enemies[i].active)return &g_enemies[i];
    return NULL;
}
Particle* getFreeParticle(){
    for(int i=0;i<MAX_PARTICLES;i++) if(!g_particles[i].active)return &g_particles[i];
    return NULL;
}

/* ===== spawn ===== */
void spawnBullet(){
    Bullet*b=getFreeBullet(); if(!b)return;
    b->x=g_player.x; b->y=g_player.y-g_player.h/2; b->w=6; b->h=14; b->active=1;
}
void spawnEnemy(){
    Enemy*e=getFreeEnemy(); if(!e)return;
    int r=rand()%100;
    if(r<70){ e->type=ENEMY_SMALL; e->w=30;e->h=30; e->speed=rand()%3+3; e->hp=1; }
    else if(r<90){ e->type=ENEMY_MEDIUM; e->w=40;e->h=40; e->speed=rand()%2+2; e->hp=2; }
    else{ e->type=ENEMY_BIG; e->w=55;e->h=55; e->speed=1; e->hp=4; }
    e->x=(float)(rand()%(WINDOW_WIDTH-e->w)+e->w/2);
    e->y=(float)(-e->h); e->active=1;
}
void spawnExplosion(float x,float y,int count){
    for(int i=0;i<count;i++){
        Particle*p=getFreeParticle(); if(!p)break;
        p->x=x; p->y=y;
        float angle=(float)(rand()%360)*3.14159f/180.0f;
        float speed=(float)(rand()%5)+2.0f;
        p->vx=cosf(angle)*speed; p->vy=sinf(angle)*speed;
        p->maxLife=rand()%20+15; p->life=p->maxLife; p->active=1;
    }
}

/* ===== update ===== */
void updatePlayer(){
    if(KEY_DOWN('A')||KEY_DOWN(VK_LEFT))  g_player.x-=PLAYER_SPEED;
    if(KEY_DOWN('D')||KEY_DOWN(VK_RIGHT)) g_player.x+=PLAYER_SPEED;
    if(KEY_DOWN('W')||KEY_DOWN(VK_UP))    g_player.y-=PLAYER_SPEED;
    if(KEY_DOWN('S')||KEY_DOWN(VK_DOWN))  g_player.y+=PLAYER_SPEED;
    g_player.x=(float)imax(g_player.w/2,imin(WINDOW_WIDTH-g_player.w/2,(int)g_player.x));
    g_player.y=(float)imax(g_player.h/2,imin(WINDOW_HEIGHT-g_player.h/2,(int)g_player.y));
    if(g_player.shootTimer>0)g_player.shootTimer--;
    if(KEY_DOWN(VK_SPACE)&&g_player.shootTimer<=0){
        float sx=g_player.x;
        g_player.x=sx-10;spawnBullet();
        g_player.x=sx+10;spawnBullet();
        g_player.x=sx; g_player.shootTimer=SHOOT_CD;
    }
    if(g_player.invTimer>0)g_player.invTimer--;
}

void updateBullets(){
    for(int i=0;i<MAX_BULLETS;i++){
        if(!g_bullets[i].active)continue;
        g_bullets[i].y-=BULLET_SPEED;
        if(g_bullets[i].y<-20)g_bullets[i].active=0;
    }
}

void updateEnemies(){
    for(int i=0;i<MAX_ENEMIES;i++){
        if(!g_enemies[i].active)continue;
        g_enemies[i].y+=(float)g_enemies[i].speed;
        if(g_enemies[i].y>WINDOW_HEIGHT+60)g_enemies[i].active=0;
        if(g_enemies[i].type==ENEMY_BIG)
            g_enemies[i].x+=sinf((float)g_frameCount*0.05f+(float)i)*1.5f;
    }
    g_enemySpawnTimer++;
    if(g_enemySpawnTimer>=g_enemySpawnRate){
        g_enemySpawnTimer=0; spawnEnemy();
        g_enemySpawnRate=imax(15,45-g_score/500);
    }
}

void updateParticles(){
    for(int i=0;i<MAX_PARTICLES;i++){
        if(!g_particles[i].active)continue;
        g_particles[i].x+=g_particles[i].vx;
        g_particles[i].y+=g_particles[i].vy;
        g_particles[i].vy+=0.15f;
        g_particles[i].life--;
        if(g_particles[i].life<=0)g_particles[i].active=0;
    }
}

void updateStars(){
    for(int i=0;i<MAX_STARS;i++){
        g_stars[i].y+=(float)g_stars[i].speed;
        if(g_stars[i].y>WINDOW_HEIGHT){ g_stars[i].y=0; g_stars[i].x=(float)(rand()%WINDOW_WIDTH); }
    }
}

/* ===== collision ===== */
int checkCollision(float x1,float y1,int w1,int h1, float x2,float y2,int w2,int h2){
    float l1=x1-w1/2.0f,r1=x1+w1/2.0f,t1=y1-h1/2.0f,b1=y1+h1/2.0f;
    float l2=x2-w2/2.0f,r2=x2+w2/2.0f,t2=y2-h2/2.0f,b2=y2+h2/2.0f;
    return (l1<r2 && r1>l2 && t1<b2 && b1>t2);
}

void checkBulletEnemyCollisions(){
    for(int i=0;i<MAX_BULLETS;i++){
        if(!g_bullets[i].active)continue;
        for(int j=0;j<MAX_ENEMIES;j++){
            if(!g_enemies[j].active)continue;
            if(checkCollision(g_bullets[i].x,g_bullets[i].y,g_bullets[i].w,g_bullets[i].h,
                              g_enemies[j].x,g_enemies[j].y,g_enemies[j].w,g_enemies[j].h)){
                g_bullets[i].active=0; g_enemies[j].hp--;
                spawnExplosion(g_bullets[i].x,g_bullets[i].y,3);
                if(g_enemies[j].hp<=0){
                    int cnt=(g_enemies[j].type==ENEMY_BIG)?40:(g_enemies[j].type==ENEMY_MEDIUM)?20:10;
                    spawnExplosion(g_enemies[j].x,g_enemies[j].y,cnt);
                    switch(g_enemies[j].type){
                    case ENEMY_SMALL:g_score+=10;break;
                    case ENEMY_MEDIUM:g_score+=20;break;
                    case ENEMY_BIG:g_score+=50;break;
                    }
                    g_enemies[j].active=0;
                }
                break;
            }
        }
    }
}

void checkPlayerEnemyCollisions(){
    if(g_player.invTimer>0)return;
    for(int i=0;i<MAX_ENEMIES;i++){
        if(!g_enemies[i].active)continue;
        if(checkCollision(g_player.x,g_player.y,g_player.w,g_player.h,
                          g_enemies[i].x,g_enemies[i].y,g_enemies[i].w,g_enemies[i].h)){
            spawnExplosion(g_enemies[i].x,g_enemies[i].y,25);
            g_enemies[i].active=0;
            spawnExplosion(g_player.x,g_player.y,15);
            g_player.lives--; g_player.invTimer=INVINCIBLE;
            if(g_player.lives<=0){
                spawnExplosion(g_player.x,g_player.y,60);
                if(g_score>g_highScore)g_highScore=g_score;
                g_state=STATE_GAMEOVER;
            }
            break;
        }
    }
}

/* ===== render ===== */
void drawBackground(){
    setbkcolor(RGB(5,5,30)); cleardevice();
    for(int i=0;i<MAX_STARS;i++){
        int b=g_stars[i].bright;
        if(g_stars[i].speed==1)b/=3; else if(g_stars[i].speed==2)b=b*2/3;
        setfillcolor(RGB(b,b,b));
        int r=(g_stars[i].speed==3)?2:1;
        solidcircle((int)g_stars[i].x,(int)g_stars[i].y,r);
    }
}

void drawPlayer(){
    if(g_player.invTimer>0 && (g_frameCount/6)%2==0)return;
    int x=(int)g_player.x, y=(int)g_player.y;

    setfillcolor(RGB(30,144,255)); setlinecolor(RGB(100,180,255));
    solidellipse(x-12,y-25,x+12,y+20);

    setfillcolor(RGB(0,255,255)); setlinecolor(RGB(100,255,255));
    solidellipse(x-5,y-10,x+5,y+5);

    {
        POINT p[3]={{x-12,y+5},{x-30,y+15},{x-12,y-5}};
        setfillcolor(RGB(70,130,220)); setlinecolor(RGB(120,160,240));
        solidpolygon(p,3);
    }
    {
        POINT p[3]={{x+12,y+5},{x+30,y+15},{x+12,y-5}};
        solidpolygon(p,3);
    }
    {
        POINT p[3]={{x-8,y+20},{x+8,y+20},{x,y+35}};
        setfillcolor(RGB(50,100,200));
        solidpolygon(p,3);
    }

    int fl=8+(g_frameCount%10)*2;
    setfillcolor(RGB(255,200,50)); setlinecolor(RGB(255,150,0));
    {
        POINT p[3]={{x-6,y+25},{x+6,y+25},{x,y+25+fl}};
        solidpolygon(p,3);
    }
}

void drawEnemySingle(Enemy*e){
    int x=(int)e->x, y=(int)e->y;
    switch(e->type){
    case ENEMY_SMALL:
        setfillcolor(RGB(220,50,50)); setlinecolor(RGB(255,100,100));
        {
            POINT p[3]={{x,y+15},{x-15,y-15},{x+15,y-15}};
            solidpolygon(p,3);
        }
        break;
    case ENEMY_MEDIUM:
        setfillcolor(RGB(240,140,30)); setlinecolor(RGB(255,180,60));
        {
            POINT p[4]={{x-20,y-15},{x+20,y-15},{x+5,y+20},{x-5,y+20}};
            solidpolygon(p,4);
        }
        if(e->hp==2){ setfillcolor(RGB(255,100,100)); solidcircle(x,y+5,4); }
        break;
    case ENEMY_BIG:
        setfillcolor(RGB(160,50,200)); setlinecolor(RGB(200,100,240));
        {
            POINT p[5]={{x,y-27},{x+27,y+10},{x+10,y+27},{x-10,y+27},{x-27,y+10}};
            solidpolygon(p,5);
        }
        setfillcolor(RGB(255,255,100));
        for(int i=0;i<e->hp;i++)solidcircle(x-8+i*6,y-10,2);
        break;
    }
}

void drawEnemies(){
    for(int i=0;i<MAX_ENEMIES;i++) if(g_enemies[i].active)drawEnemySingle(&g_enemies[i]);
}

void drawBullets(){
    for(int i=0;i<MAX_BULLETS;i++){
        if(!g_bullets[i].active)continue;
        int bx=(int)g_bullets[i].x, by=(int)g_bullets[i].y;
        setfillcolor(RGB(100,100,0)); solidellipse(bx-6,by-8,bx+6,by+8);
        setfillcolor(RGB(255,255,50)); solidellipse(bx-3,by-5,bx+3,by+5);
        setfillcolor(RGB(255,255,255)); solidcircle(bx,by-2,1);
    }
}

void drawParticles(){
    for(int i=0;i<MAX_PARTICLES;i++){
        if(!g_particles[i].active)continue;
        float ratio=(float)g_particles[i].life/g_particles[i].maxLife;
        int r,g,b;
        if(ratio>0.6f){r=255;g=(int)(255*(ratio-0.4f)/0.6f);b=0;}
        else if(ratio>0.3f){r=255;g=(int)(150*ratio/0.6f);b=0;}
        else{r=(int)(255*ratio/0.3f);g=0;b=0;}
        int size=(int)(3.0f*ratio)+1;
        setfillcolor(RGB(r,g,b));
        solidcircle((int)g_particles[i].x,(int)g_particles[i].y,size);
    }
}

void drawUI(){
    setfillcolor(RGB(0,0,0)); setlinecolor(RGB(50,50,50));
    solidrectangle(0,0,WINDOW_WIDTH,40);
    settextstyle(24,0,_T("Consolas")); setbkmode(TRANSPARENT);
    TCHAR t[64];

    settextcolor(RGB(255,255,200));
    _stprintf_s(t,_T("Score: %d"),g_score); outtextxy(20,6,t);

    _stprintf_s(t,_T("Best: %d"),g_highScore); outtextxy(240,6,t);

    settextcolor(RGB(255,80,80));
    _stprintf_s(t,_T("HP x %d"),g_player.lives); outtextxy(500,6,t);

    if(g_player.invTimer>0){ settextcolor(RGB(100,200,255)); outtextxy(620,6,_T("INV")); }
    setlinecolor(RGB(40,40,100)); line(0,42,WINDOW_WIDTH,42);
}

void drawMenu(){
    drawBackground();
    setbkmode(TRANSPARENT);
    settextstyle(56,0,_T("Consolas")); settextcolor(RGB(50,200,255));
    outtextxy(140,220,_T("PLANE WAR"));
    settextstyle(24,0,_T("Consolas")); settextcolor(RGB(180,180,200));
    outtextxy(160,320,_T("C Programming - EasyX"));
    settextstyle(22,0,_T("Consolas")); settextcolor(RGB(150,200,150));
    outtextxy(200,430,_T("WASD / Arrow   Move"));
    outtextxy(200,470,_T("SPACE          Shoot"));
    outtextxy(200,510,_T("Q              Back to Menu"));
    outtextxy(200,550,_T("ESC            Quit"));
    if((g_frameCount/30)%2==0){
        settextstyle(28,0,_T("Consolas")); settextcolor(RGB(255,255,100));
        outtextxy(170,620,_T("Press SPACE to Start"));
    }
    updateStars();
    FlushBatchDraw();
}

void drawGameOver(){
    drawBackground();
    setbkmode(TRANSPARENT);
    settextstyle(48,0,_T("Consolas")); settextcolor(RGB(255,100,100));
    outtextxy(180,260,_T("GAME OVER"));
    settextstyle(30,0,_T("Consolas")); settextcolor(RGB(255,255,150));
    TCHAR t[64];
    _stprintf_s(t,_T("Score: %d"),g_score); outtextxy(220,370,t);
    _stprintf_s(t,_T("Best: %d"),g_highScore); outtextxy(220,410,t);
    if((g_frameCount/30)%2==0){
        settextstyle(24,0,_T("Consolas")); settextcolor(RGB(255,255,100));
        outtextxy(160,530,_T("R=Restart  ESC=Quit"));
    }
    updateStars();
    FlushBatchDraw();
}

/* ===== main loop ===== */
void updateGame(){
    updatePlayer(); updateBullets(); updateEnemies();
    checkBulletEnemyCollisions(); checkPlayerEnemyCollisions();
    updateParticles(); updateStars();
}

void render(){
    drawBackground(); drawBullets(); drawEnemies();
    drawParticles(); drawPlayer(); drawUI(); FlushBatchDraw();
}

int main(){
    initgraph(WINDOW_WIDTH,WINDOW_HEIGHT);
    BeginBatchDraw();
    srand((unsigned)time(NULL));
    initGame(); g_highScore=0; g_state=STATE_MENU; g_frameCount=0;

    while(1){
        g_frameCount++;
        switch(g_state){
        case STATE_MENU:
            drawMenu();
            if(KEY_DOWN(VK_SPACE)){ initGame(); g_state=STATE_PLAYING; }
            if(KEY_DOWN(VK_ESCAPE)) goto exitGame;
            break;
        case STATE_PLAYING:
            updateGame(); render();
            if(KEY_DOWN('Q')){ g_state=STATE_MENU; }
            if(KEY_DOWN(VK_ESCAPE)) goto exitGame;
            break;
        case STATE_GAMEOVER:
            drawGameOver();
            if(KEY_DOWN('R')){ initGame(); g_state=STATE_PLAYING; }
            if(KEY_DOWN(VK_ESCAPE)) goto exitGame;
            updateStars(); updateParticles();
            break;
        }
        Sleep(16);
    }
exitGame:
    EndBatchDraw(); closegraph(); return 0;
}
