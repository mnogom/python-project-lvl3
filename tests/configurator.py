"""Configurator."""

from urllib.parse import urljoin


def get_contents():
    """Get html, css, img, js test content."""

    with open("tests/fixtures/demo_page/in/example.html", "r") as file:
        html_text = file.read()
    with open("tests/fixtures/demo_page/in/css/abs-styles.css", "rb") as file:
        css_content = file.read()
    with open("tests/fixtures/demo_page/in/img/rel-googlelogo.png", "rb") as file:
        img_content = file.read()
    with open("tests/fixtures/demo_page/in/js/rel-scripts.js", "rb") as file:
        js_content = file.read()

    return html_text, css_content, img_content, js_content


def setup_mock(mock_up, url: str, include_assets: bool):
    """Setup mock up for url.
    :param mock_up: mock object
    :param url: url
    :param include_assets: include demo assets
    """

    if include_assets:
        (html_text,
         css_content,
         img_content,
         js_content) = get_contents()

        mock_up.get(url, text=html_text)
        mock_up.get(urljoin(url, "css/abs-styles.css"), content=css_content)
        mock_up.get(urljoin(url, "img/rel-googlelogo.png"), content=img_content)
        mock_up.get(urljoin(url, "js/rel-scripts.js"), content=js_content)

    else:
        mock_up.get(url, text="empty")
