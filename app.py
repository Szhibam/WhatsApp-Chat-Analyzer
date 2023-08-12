import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image



st.markdown("<h1 style='color: green; font-weight: bold; font-family: Arial;'>Whats App Chat Analysis</h1>", unsafe_allow_html=True)
#image = Image.open('tp_wap_logo.jpeg')
#image = image.convert("RGBA")
#st.image(image)
st.sidebar.title("Whats'app Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")   #i added th "sidebar" part after "st." and before ."file"
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)


    #now to diplay the data frame
    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis of", user_list)

    if st.sidebar.button("Show Analysis"):
    #     new_df = helper.df_for_user(selected_user, df)
    #     st.dataframe(new_df)



        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.markdown('<h1 style="color: gold; ">Group Stats</h1>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<h2 style="color: lightgrey; font-size: medium;">Total Messages</h2>', unsafe_allow_html=True)
            st.title(num_messages)
        with col2:
            #st.header("Total Words")
            st.markdown('<h2 style="color: lightgrey; font-size: medium;">Total Words</h2>',
                        unsafe_allow_html=True)
            st.title(words)
        with col3:
            #st.header("Total Media Shared")
            st.markdown('<h2 style="color: lightgrey; font-size: medium;">Total Media Shared</h2>', unsafe_allow_html=True)
            st.title(num_media_messages)
        with col4:
            #st.header("Total Links Shared")
            st.markdown('<h2 style="color: lightgrey; font-size: medium;">Total Links Shared</h2>',
                        unsafe_allow_html=True)
            st.title(num_links)



        col1, col2 = st.columns(2)

        #timeline
        with col1:
            #st.title("Monthly Timeline Analysis")
            st.markdown('<h1 style="color: cyan; font-size: larger;">Monthly Timeline Analysis</h1>', unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.set_facecolor('black')
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical', color='white')
            plt.yticks(rotation='horizontal', color='white')
            ax.xaxis.set_tick_params(color='white')
            ax.yaxis.set_tick_params(color='white')
            ax.yaxis.get_label().set_color('white')  # Set the color of the y-axis label to white
            fig.patch.set_facecolor('black')
            ax.spines['left'].set_color('white')
            # Set the color of the x-axis spine to white
            ax.spines['bottom'].set_color('white')

            # Adjust figure margins to remove any whitespace
            plt.subplots_adjust(left=0.08, bottom=0.15, right=0.97, top=0.93)
            st.pyplot(fig)



        # DAILY TIMELINE
        with col2:
            #st.title("Daily Timeline")
            st.markdown('<h1 style="color: cyan;font-size: larger; ">Daily Timeline</h1>', unsafe_allow_html=True)

            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize = (16, 17))
            ax.set_facecolor('black')
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='mediumpurple')
            plt.xticks(rotation='vertical', color='white')
            plt.yticks(rotation='horizontal', color='white')
            ax.xaxis.set_tick_params(color='white')
            ax.yaxis.set_tick_params(color='white')
            ax.yaxis.get_label().set_color('white')  # Set the color of the y-axis label to white
            fig.patch.set_facecolor('black')
            ax.spines['left'].set_color('white')
            # Set the color of the x-axis spine to white
            ax.spines['bottom'].set_color('white')

            # Adjust figure margins to remove any whitespace
            plt.subplots_adjust(left=0.08, bottom=0.15, right=0.97, top=0.93)
            st.pyplot(fig)

        #activity map
        #st.title('Activity Map')
        st.markdown('<h1 style="color: cyan;font-size: larger; ">Activity Map</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            #most busy day
            st.markdown('<h1 style="color: lightgrey;font-size: medium; ">Most Busy Day</h1>',
                        unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()

            #copy paste
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
            ax.bar(busy_day.index, busy_day.values, color='cornflowerblue')
            plt.xticks(rotation='vertical', color='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.tick_params(colors='white')
            st.pyplot(fig, clear_figure=True)
        with col2:
            #most Busy month
            st.markdown('<h1 style="color: lightgrey;font-size: medium; ">Most Busy Month</h1>',unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='mediumspringgreen')
            #changing the plot CSS
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
            plt.xticks(rotation='vertical', color='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['top'].set_color('white')
            plt.gca().spines['right'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.tick_params(colors='white')
            st.pyplot(fig)

        # ACTIVITY HEAT MAP
        st.markdown('<h1 style="color: lightgrey;font-size: medium;">Weakly Activity Map</h1>',
                    unsafe_allow_html=True)
        user_heatmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the size here (width, height)

        ax = sns.heatmap(user_heatmap)

        # Copy paste

        st.pyplot(fig)



        # finding the busiest user in the group(group level)
        if selected_user == "Overall":
            #st.title("Most Busy Users")
            st.markdown('<h1 style="color: cyan;font-size: larger; ">Most Busy Users</h1>', unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                fig.patch.set_facecolor('black')
                ax.set_facecolor('black')
                ax.bar(x.index, x.values, color='orchid')
                plt.xticks(rotation='vertical', color = 'white')
                plt.gca().spines['bottom'].set_color('white')
                plt.gca().spines['top'].set_color('white')
                plt.gca().spines['right'].set_color('white')
                plt.gca().spines['left'].set_color('white')
                plt.tick_params(colors='gold')
                st.pyplot(fig)
            with col2:
                #st.title("Busiest User")
                st.markdown('<h1 style="color: lightgrey;font-size: medium; ">Contribution Percentage</h1>',
                            unsafe_allow_html=True)
                st.dataframe(new_df)



        #wordcloud
        df_wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')
        ax.imshow(df_wc)
        #st.title("word Cloud")
        st.markdown('<h1 style="color: lightgrey;font-size: medium; ">Word Cloud</h1>',
                unsafe_allow_html=True)
        st.pyplot(fig)



        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1], color = 'aquamarine')
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        plt.xticks(rotation='vertical', color='white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['top'].set_color('white')
        plt.gca().spines['right'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        plt.tick_params(colors='white')

        #st.title("Most Common Words")
        st.markdown('<h1 style="color: cyan;font-size: larger; ">Most Common Wrords</h1>',
                unsafe_allow_html=True)

        st.pyplot(fig)




        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        #st.title("Emoji Analysis")
        st.markdown('<h1 style="color: lightgrey;font-size: medium; ">Emoji Analysis</h1>',
                unsafe_allow_html=True)


        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)



        

















