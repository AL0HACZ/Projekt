import webview

def main():
    window = webview.create_window(
        title='Autopedia',
        url='http://127.0.0.1:5000/',
        width=1024,
        height=768,
        resizable=True
    )

    webview.start(user_agent='Autopedia App')

if __name__ == '__main__':
    main()