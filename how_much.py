# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pygame
import sys
import tkinter.messagebox as msg  # 메세지 팝업 라이브러리 소환
import datetime

# 개발자: 김예진
# 개발일: 2023-01-17~
# 프로그램 목적: 달러, 엔화, 위안, 유로의 환율을 알아보는 프로그램을 만든다

def crow(): #크롤링을 하는 함수
    global usa,jp,ch,eu,time,bank,gold_dom,gold_nat,oil
    # URL
    url_d = urlopen(
        "https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_USDKRW")  # 미국 달러 환율, 네이버증권
    url_y = urlopen(
        "https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW")  # 일본 환율, 네이버증권
    url_ch = urlopen(
        "https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_CNYKRW")  # 중국 환율, 네이버증권
    url_e = urlopen(
        "https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_EURKRW")  # 중국 환율, 네이버증권
    url_time = urlopen("https://finance.naver.com/marketindex/")  # 고시 시간

    url_gold = urlopen("https://finance.naver.com/marketindex/goldDetail.naver")  # 국내 금값 시세
    url_gold2 = urlopen("https://finance.naver.com/marketindex/worldGoldDetail.naver?marketindexCd=CMDT_GC&fdtc=2")  # 국내 금값 시세
    url_oil = urlopen(
        "https://finance.naver.com/marketindex/oilDetail.naver?marketindexCd=OIL_GSL")  # 휘발유 시세

    # SOUP
    soup_d = BeautifulSoup(url_d, "html.parser")
    soup_y = BeautifulSoup(url_y, "html.parser")
    soup_ch = BeautifulSoup(url_ch, "html.parser")
    soup_e = BeautifulSoup(url_e, "html.parser")
    soup_time = BeautifulSoup(url_time, "html.parser")
    soup_gold = BeautifulSoup(url_gold, "html.parser")
    soup_gold2 = BeautifulSoup(url_gold2, "html.parser")
    soup_oil = BeautifulSoup(url_oil, "html.parser")

    # KRW_VALUE
    value_d = soup_d.find("p", "no_today")  # p값 no_today 클래스에 오늘의 환율이 있음.
    value_y = soup_y.find("p", "no_today")  # p값 no_today 클래스에 오늘의 환율이 있음.
    value_ch = soup_ch.find("p", "no_today")  # p값 no_today 클래스에 오늘의 환율이 있음.
    value_e = soup_e.find("p", "no_today")  # p값 no_today 클래스에 오늘의 환율이 있음.
    value_time = soup_time.find("span", "date")
    value_bank = soup_e.find("span", "standard")
    value_gold = soup_gold.find("p", "no_today")
    value_gold2 = soup_gold2.find("p", "no_today")
    value_oil = soup_oil.find("p", "no_today")

    # STRIP
    dollar = value_d.text.strip()
    enwha = value_y.text.strip()
    yuan = value_ch.text.strip()
    euro = value_e.text.strip()
    tm = value_time.text.strip()
    bk = value_bank.text.strip()
    gd = value_gold.text.strip()
    gd2 = value_gold2.text.strip()
    oils = value_oil.text.strip()

    # VALUE_INDEX
    usa = float(dollar[0:8].replace(',', ''))
    jp = float(enwha[0:8].replace(',', ''))
    ch = float(yuan[0:8].replace(',', ''))
    eu = float(euro[0:8].replace(',', ''))
    gold_dom = str(gd[0:8].replace(',', ''))
    gold_nat = str(gd2[0:8].replace(',', ''))
    oil = str(oils[0:8].replace(',', '')) + " 원(W)"
    time = str(tm)
    bank = str(bk) + " 고시 기준"
crow()

# 전역변수부
monitor_size = (500,800) #창크기
start_x = 0
start_y = 0
final_x = 500
final_y = 800
main = 1 #메인메뉴의 값
menu = 2 #2번 메뉴의 값

#color
background_color = (47, 47, 48)
white = (70, 70, 74)
gray = (62, 62, 64)
orange = (112, 92, 76)
font_color = (205,205,205)
font_color1 = (255,255,255)
blue = (79, 161, 255)
black = (20, 20, 20)
white_color = (250,250,250)

#init
pygame.init()

#image
arrow1 = pygame.image.load("img/key1.png")
arrow2 = pygame.image.load("img/key2.png")
korea_flag = pygame.image.load("img/korea.png")
usa_flag = pygame.image.load("img/usa.png")
japan_flag = pygame.image.load("img/japan.png")
china_flag = pygame.image.load("img/china.png")
europ_flag = pygame.image.load("img/europ.png")
loading = pygame.image.load("img/re.png")

#Font
app_font = pygame.font.Font("font/pl.otf", 15)
app_font1 = pygame.font.Font("font/pr.otf", 20)
app_font3 = pygame.font.Font("font/pr.otf", 12)
app_font4 = pygame.font.Font("font/pm.otf", 20)

def content_write_gold(screen, value):
    sur = app_font.render("국내 금값(1g) | "+value+" 원(W)", True, font_color1)
    screen.blit(sur, [20,70])  #폰트 띄우기

def content_write_gold2(screen, value):
    sur = app_font.render("국제 금값(1toz) | "+value+" 달러($)", True, font_color1)
    screen.blit(sur, [20,140])  #폰트 띄우기

def content_write_oil(screen, value):
    sur = app_font.render("휘발유(리터) | "+value, True, font_color1)
    screen.blit(sur, [20,210])  #폰트 띄우기

def content_write_Title(screen):
    sur = app_font4.render("How Much:", True, black)
    screen.blit(sur, [15,15])  #폰트 띄우기
def content_write_Title2(screen):
    sur = app_font.render("오늘의 환율이 궁금하다면? (Beta)", True, black)
    screen.blit(sur, [121,20])  #폰트 띄우기

class Nation :
    #각 국가별 환율 값을 이용해 그래프를 그릴 때 쓸 클래스
    #nation기본값 0, 1-미국, 2-일본 3-중국, 4-유럽
    nation = 0
    value = 1000
    graph_y = 0
    graph_X = 0
    def draw_g(self,screen,nation,value): #객체이름.draw_g(monitor,1,dollar)하면 그래프 그려짐
        pygame.draw.rect(screen, white, [start_x-30, start_y + 100*nation + 300, value/1000*200+30, 30], border_radius=7)
        if nation == 1: txt = "미국 USD" ;  screen.blit(usa_flag, [start_x + value / 1000 * 200 -35, start_y + 100*nation + 300+5]) #각 나라별 번호일 때 국기와 글씨를 표시.
        elif nation ==2: txt = "일본 JPY";  screen.blit(japan_flag, [start_x + value / 1000 * 200 -35, start_y + 100*nation + 300+5])
        elif nation == 3:txt = "중국 CNY";  screen.blit(china_flag, [start_x + value / 1000 * 200 -35, start_y + 100*nation + 300+5])
        elif nation == 4: txt = "유럽 EUR";  screen.blit(europ_flag, [start_x + value / 1000 * 200 -35, start_y + 100*nation + 300+5])
        else : txt = "국가 화폐 1개 = ( )원"
        sur = app_font.render(txt, True, font_color)
        txt2 = str(value)
        sur1 = app_font1.render(txt2 + " 원", True, font_color1)
        screen.blit(sur, [start_x + value / 1000 * 200 + 12, start_y + 100*nation + 300+5]) #나라명
        if nation != 0:
            screen.blit(sur1, [start_x + value / 1000 * 200 + 82, start_y + 100 * nation + 300]) #환율값 표시


def quitgame():  # 종료의사를 묻는 메세지박스
    str = msg.askquestion("프로그램을 종료하시겠습니까?", "'예(Y)'를 눌러 프로그램을 종료합니다.")
    if str == 'yes':
        pygame.quit()
        sys.exit()
def quit_button():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitgame()
def no_content(screen):  # 준비중일때
    sur1 = app_font1.render("해당 기능은 준비중입니다.", True, font_color1)
    screen.blit(sur1, [150, 395])

#main
def main():
    state = main #기본 상태

    monitor = pygame.display.set_mode(monitor_size)
    pygame.display.set_caption("How Much: 오늘의 환율이 궁금하다면?")  # 윈도우 제목

    while True:

        monitor.fill(background_color)
        # func
        quit_button()
        now = datetime.datetime.now() #현재시간
        second = int(now.second)

        if state == main : #메인 메뉴일때
            for i in range(21): #그래프 긋기
                pygame.draw.line(monitor, gray, (start_x+i*20,start_y), (start_x+i*20,final_y), width=3)
                if i%5==0 and i != 0:
                    pygame.draw.line(monitor, orange, (start_x+i*20,start_y), (start_x+i*20,final_y), width=5)
            pygame.draw.rect(monitor, white, [start_x-30, start_y + 300, 200+30, 30], border_radius=7)
            #nation coin to won
            KOR = Nation()
            KOR.draw_g(monitor, 0, 1000)
            USA = Nation()
            USA.draw_g(monitor,1,usa)
            JP = Nation()
            JP.draw_g(monitor, 2, jp)
            CH = Nation()
            CH.draw_g(monitor, 3, ch)
            EU = Nation()
            EU.draw_g(monitor, 4, eu)
            monitor.blit(arrow2, [441, 250]) 
            #화살표를 모니터에 띠운다
            monitor.blit(app_font1.render(time, True, font_color1), [15, 760])
            monitor.blit(app_font1.render(bank, True, font_color1), [175, 760])
            # 환율 위의 기타 항목
            pygame.draw.rect(monitor, background_color, [start_x, start_y+55, final_x, 50])
            content_write_gold(monitor, gold_dom)
            pygame.draw.rect(monitor, background_color, [start_x, start_y + 125, final_x, 50])
            content_write_gold2(monitor, gold_nat)
            pygame.draw.rect(monitor, background_color, [start_x, start_y + 195, final_x, 50])
            content_write_oil(monitor, oil)
            pygame.draw.rect(monitor,white_color, [start_x, start_y, final_x, 55])
            content_write_Title(monitor) #제목 띄우기
            content_write_Title2(monitor)  # 제목 띄우기

            #누르면 넘어가게 만든다
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = menu

        if state == menu: #두번째 메뉴
            no_content(monitor) #아직 기능을 준비중인 페이지
            monitor.blit(arrow1, [-10, 250])
            # 누르면 넘어가게 만든다
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = main

        #print(now.second)
        if now.minute % 3 == 0 :
            if now.second <= 3 :
                monitor.blit(loading, [0, 0])
                monitor.blit(app_font1.render("새로고침 중...", True, blue), [380, 760])
                crow()  # 3분마다 새로고침함.
        pygame.display.update()
        pygame.time.Clock().tick(30)  # fps 30프레임

if __name__ == '__main__' : #메인 함수 실행
    main()