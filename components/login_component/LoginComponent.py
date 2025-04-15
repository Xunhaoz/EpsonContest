import os
from urllib.parse import urlencode

import gradio as gr


class LoginComponent:
    js = """
    <script>
        function checkUserCookie() {
            const cookies = document.cookie.split(';');
    
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.indexOf('access_token=') === 0) {
                    window.location.href = '/';
                    return true;
                }
            }
            return false;
        }
    
        function refreshCookiesAndCheck() {
            fetch(window.location.href, {
                method: 'GET',
                credentials: 'same-origin',
                cache: 'no-store'
            })
            .then(response => {
                if (!checkUserCookie()) {
                    setTimeout(refreshCookiesAndCheck, 5000);
                }
            })
            .catch(error => {
                console.error('刷新 cookie 時發生錯誤:', error);
                setTimeout(refreshCookiesAndCheck, 5000);
            });
        }
    
        document.addEventListener('DOMContentLoaded', function() {
            if (!checkUserCookie()) {
                refreshCookiesAndCheck();
            }
        });
    
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            if (!checkUserCookie()) {
                refreshCookiesAndCheck();
            }
        }
    </script>
    """

    def __init__(self, client_id: str = None, redirect_uri: str = None, scope: str = None, auth_url: str = None):
        auth_params = {
            "response_type": 'code',
            "client_id": client_id or os.getenv('CLIENT_ID'),
            "redirect_uri": redirect_uri or os.getenv('REDIRECT_URI'),
            "scope": scope or os.getenv('SCOPE')
        }

        link = f"{auth_url or os.getenv('AUTH_URL')}?{urlencode(auth_params)}"

        with gr.Blocks(fill_height=True, head=self.js) as self.login_page:
            gr.Image(
                "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                show_label=False, height='50vh', show_download_button=False, show_fullscreen_button=False, container=False)
            gr.Button("Epson Connect 登入", link=link)

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.login_page, path=url)
