# ERATranslateHelper
一个用于翻译ERA游戏的翻译工具

Version: Python 3.7.2

Depandencies: tkinter, configparser, js2py


功能：

1、对选择的ERB文件进行处理，提取所有PRINT和DATAFORM行（以下简称行）。

2、通过百度web翻译接口，对选定行进行翻译。

3、格式自动替换，会自动将百分号（如%CALLNAME%）、三项表达式（\@ A? B#C\@）进行替换，避免格式错误。

4、保存翻译好的行，并替换到源文件中，同时保留并注释原文字。

5、支持对所有行进行自动翻译。

6、对选定文件夹内的所有文件转码（从SHIFT-JIS到UTF-8 with BOM）

(2019.4.29)

7、增加了查找、替换翻译内容的功能。

(2019.5.3)

8、增加了关闭时保存确认。

TODO：
1、词典