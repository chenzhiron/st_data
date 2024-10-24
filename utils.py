from datetime import datetime

def formatDate(date_str):
  try:
    # 格式化字符串，插入空格
    formatted_date_str = date_str[:10] + " " + date_str[10:]
    # 解析为 datetime 对象
    date_time_obj = datetime.strptime(formatted_date_str, "%Y/%m/%d %H:%M:%S")
    # 将 datetime 对象转换为时间戳
    timestamp = date_time_obj.timestamp()
    return timestamp
  except:
    return None

