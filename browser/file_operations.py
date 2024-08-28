from PyQt5.QtWidgets import QFileDialog

def open_file(self):
    filename, _ = QFileDialog.getOpenFileName(
        self,
        'Open file',
        '',
        'Hypertext Markup Language (*.htm *.html);;'
        'All files (*.*)',
    )

    if filename:
        with open(filename, 'r') as file:
            html = file.read()

        self.tabs.currentWidget().setHtml(html)
        self.urlbar.setText(filename)

def save_file(self):
    filename, _ = QFileDialog.getSaveFileName(
        self,
        'Save Page As',
        '',
        'Hypertext Markup Language (*.htm *html);;'
        'All files (*.*)',
    )

    if filename:
        def writer(html):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html)

        self.tabs.currentWidget().page().toHtml(writer)