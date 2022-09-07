import feedparser

class Gongsi():
  def __init__(self) -> None:
    pass
  
  def convert_time(self, text):
    day_week = {'Mon':'월','Tue':'화','Wed':'수','Thu':'목','Fri':'금','Sat':'토','Sun':'일'}.get(text[0])
    month = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}.get(text[2])
    # return f"{text[3]}년 {month}월 {text[1]}일 {day_week}요일 {text[4]}"
    return text[4][:5]
  
  def do_filter(self, text):
    filter_list = ["TIGER","KODEX","KINDEX","HANARO","ARIRANG","KBSTAR","KOSEF","SOL","TIMEFOLIO","WOORI","KTOP","FOCUS","레버리지","인덱스","코스닥","KOSDAQ","코스피","KOSPI","나스닥","NASDAQ","항셍","유로스탁스","S&P","CSI300","합성","ETN","ETF","ELW","스팩","SPAC","선물","롱","숏","파생"]
    for i in filter_list:
      if i in text:
        return False
    return True  

  
  def get_gongsi(self, last_gongsi):
    try:
      parse_rss = feedparser.parse("http://kind.krx.co.kr:80/disclosure/rsstodaydistribute.do?method=searchRssTodayDistribute&repIsuSrtCd=&mktTpCd=0&searchCorpName=&currentPageSize=1000")
      var_list = []
      link_list = []
      j = 0
      k = 0
      column_list = ["회사명","공시 바로가기","시간","분류"]
      for i in reversed(parse_rss['entries']):
        if j >= last_gongsi: 
          if not self.do_filter(i['title']):
            continue
          var_list.append([])
          link_list.append(i['link'])
          var_list[k].append(i['author'])
          var_list[k].append(i['title'][len(i['author'])+1:])
          var_list[k].append(self.convert_time(i['updated'].replace(',','').split(' ')))
          var_list[k].append(i['tags'][0]['term'])
          k+=1
        j+=1
      
      gongsi = {'column_list':column_list,'var_list':var_list,'link_list':link_list,'last_gongsi':len(parse_rss['entries'])}
      
      return gongsi
    except Exception as e:
      print(e)
      return False
