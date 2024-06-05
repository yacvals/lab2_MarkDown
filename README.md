# Markdown_Subset_Viewer

## Опис
Цей застосунок є консольним парсером Markdown, який перетворює обмежену підмножину розмітки Markdown у HTML.

## Інструкція зі зборки та запуску
1. Клонувати репозиторій:
   git clone [https://github.com/yacvals/Markdown_Subset_Viewer)
2. Запустити застосунок: 
   `python app.py /path/to/markdown/file [--out /path/to/output.html]`
### Використання
Для виведення результату в стандартний вивід:
`python app.py /path/to/markdown/file`
Для виведення результату у файл:
`python app.py /path/to/markdown/file --out output.html`

### Приклад використання:
```
Життєвий принцип канібала-романтика? ```Шлях до серця лежить через шлунок```
Як в китаї називають сина Петра? **петроСЯН**
`Стара студентська традиція:` щороку ми з друзями ходимо на сесію. Ну і паримося там ...
```
На виході отримуємо:
```
<p>
Життєвий принцип канібала-романтика? <tt></tt><tt>Шлях до серця лежить через шлунок</tt><tt></tt>
Як в китаї називають сина Петра? <b>петроСЯН</b>
<tt>Стара студентська традиція:</tt> щороку ми з друзями ходимо на сесію. Ну і паримося там ...
</p>
```
[Revert commit](https://github.com/yacvals/Markdown_Subset_Viewer/commit/9c1deb34367cb402dc4107b28d0cef141d6bd084)
[Test Failed](https://github.com/yacvals/lab2_MarkDown/actions/runs/9389574319)
