from urlextract import URLExtract
from wordcloud import  WordCloud
import  pandas as pd
from collections import  Counter
import emoji

extract = URLExtract()

# creating a separate dataframe to display for spesific user
def df_for_user(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # removing "group_notifications" from words
    new_df = df[df['user'] != 'group_notification']
    # removing "<meadia omitted>\n" from word count
    new_df = new_df[new_df['message'] != '<Media omitted>\n']


    # fetch total number of messages
    num_messages = new_df.shape[0]

    # fetch total number of words
    words = []
    for message in new_df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetching the links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(
        columns = {'index' : 'name', 'user' : 'percent'})
    return x, df

def create_wordcloud(selected_user, df):

    # removing group notifications from dataframe
    df = df[df['user'] != 'group_notification']
    # removing "<meadia omitted>\n" from word count
    df = df[df['message'] != '<Media omitted>\n']

    # removing mentions from wordcloud
    df = df[~df['message'].str.contains('^@\\d{11}')]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)



    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500, min_font_size=10, background_color='green')
    # removing stop words
    df['message'] = df['message'].apply(remove_stop_words)

    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return  df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # to make sure the data frame doesnot contains any menstions e.g @8967096345
    df = df[~df['message'].str.contains('^@\\d{11}')]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        # converting everything in lower case
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return  most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.unicode_codes.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return  emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    # RESET INDEX CONVERTED IT INTO A DATA FRAME

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    return  df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    #forming the pivot table
    user_heatmap=df.pivot_table(index =  'day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap







