import webbrowser

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[1]
    return f'<a target="_blank" href="www.google.com">google here</a>'

# link is the column with hyperlinks
df['link'] = df['link'].apply(make_clickable)
df = df.to_html(escape=False)
st.write(df, unsafe_allow_html=True)
