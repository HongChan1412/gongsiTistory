from tistory_post import tistoryPost
from gongsi_crawl import Gongsi
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time

last_gongsi = 0
id = "starha0128"    #티스토리 테스트
pw = "Qkrgkdyd1479@"
url = "starha0128"

def job(id, pw, url, term):
  last_gongsi = 0
  print("프로세스 시작")
  while True:
    try:
      print("공시 크롤링 시작")
      gongsi = Gongsi().get_gongsi(last_gongsi)
      if gongsi:
        print("공시 크롤링 완료")
        if len(gongsi['var_list']) == 0:
          print("더이상 공시가 없음")
          break
        print("티스토리 포스팅 시작")
        if tistoryPost(id, pw, url).do_post(gongsi):
          last_gongsi += gongsi['last_gongsi']
          print("티스토리 포스팅 성공")
          time.sleep(60 * int(term))
        else:
          print("티스토리 포스팅 실패")
      else:
        print("공시 크롤링 실패")
    except KeyboardInterrupt:
        break
    except Exception as e:
      print(e) 
  print("프로세스 종료")
    
def main():
  try:
    print("""
  ___              _  _     _____  _               _        
  |_  |            (_)| |   /  ___|| |             | |       
    | | _   _  ___  _ | | __\ `--. | |_  _   _   __| | _   _ 
    | || | | |/ __|| || |/ / `--. \| __|| | | | / _` || | | |
/\__/ /| |_| |\__ \| ||   < /\__/ /| |_ | |_| || (_| || |_| |
\____/  \__,_||___/|_||_|\_\\____/  \__| \__,_| \__,_| \__, |
                                                        __/ |
                                                      |___/       
""")
    sched = BackgroundScheduler(timezone='Asia/Seoul')
    sched.start()
    input_time = input("시각을 입력해주세요 ex) 09:00 : ")
    input_term = input("포스팅 간격(분)을 입력해주세요 ex) 240 : ")
    input_id = input("티스토리 ID를 입력해주세요 : ")
    input_pw = input("티스토리 PW를 입력해주세요 : ")
    input_url = input("티스토리 URL을 입력해주세요 : ")  
    input_hour = input_time.split(":")[0]
    input_minute = input_time.split(":")[1]
    input_id = "moneymachine.vip@gmail.com"    
    input_pw = "money1366"
    input_url = "stockstudy-gongsi"
    try:
      sched.add_job(job, 'cron', hour=input_hour, minute=input_minute, id="gongsiPost", args = [input_id, input_pw, input_url, input_term],misfire_grace_time=600)
    except:
      try:
        print("기존 Job 제거 후 새로 추가")
        sched.remove_all_jobs()
        sched.add_job(job, 'interval', hours=1, id="gongsiPost")
      except JobLookupError as e:
        print("Scheduler 오류 발생", e)
        return
    while True:
      try:
        print("Running main process............","| [time] ", str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)+":"+str(time.localtime().tm_sec))
        time.sleep(600)  
      except KeyboardInterrupt:
        import sys
        print("Ctrl + C 중지, Job 제거 후 프로그램 종료")
        sched.remove_all_jobs()
        sys.exit()
  except KeyboardInterrupt:
    print("Ctrl + C 중지")
    
if __name__ == "__main__":
  main()