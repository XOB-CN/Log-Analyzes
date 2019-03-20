# -*- coding:utf-8 -*-

class Template_Report(object):
    """Report输出模板"""

    @staticmethod
    def html_template(title, content):
        """str.format()的转义字符是两个大括号：{{}}"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                h2{{font-weight:bold; text-align:center;}}
                h3{{font-size:18px; font-weight:bold;}}
                .title{{color:blue;}}
                .log-line{{font-size:12px;}}
                .keyword{{font-size:12px; color:red;}}
                .detail{{font-size:12px;}}
            </style>
        </head>
        <body>
        {content}
        </body>
        </html>"""
        return html_content.format(title=title, content=content)

    @staticmethod
    def html_h(content, number, html_class='noting'):
        """html 的 h 标签"""
        return "<h"+str(number) +' class='+ html_class + ">" + content + "</h"+str(number)+">" + "\n"

    @staticmethod
    def html_div(content, html_class):
        """html 的 div 标签"""
        return "<div class=" + html_class + ">"+ content +"</div>" + "\n"

    @staticmethod
    def html_font(content, color='red'):
        """html 的 font 标签"""
        return '<font color="{color}">{content}</font>'.format(content=content, color=color)