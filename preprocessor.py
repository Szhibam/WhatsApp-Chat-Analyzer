import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{1,2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'date': dates, 'user_messages': messages})
    # converting date type
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\d\w\W]+?):\s',
                         message)  ##In the provided code snippet, the first bracket in the regex pattern '([\w\W]+):\s' is used to create a capturing group in the regular expression.

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    # here if i write month_name() after dt it will give me the names instead
    df['day'] = df['date'].dt.day
    #to extract the name of the day we write
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    #heat map
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period



    return df