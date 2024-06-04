import sys
import re


def parse_markdown(md_text):
    html_output = []
    paragraphs = md_text.split('\n\n')

    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'_(.*?)_')
    monospaced_pattern = re.compile(r'`(.*?)`')
    preformatted_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    for paragraph in paragraphs:
        if preformatted_pattern.match(paragraph):
            preformatted_text = preformatted_pattern.findall(paragraph)[0]
            html_output.append(f'<pre>{preformatted_text}</pre>')
        else:
            paragraph = bold_pattern.sub(r'<b>\1</b>', paragraph)
            paragraph = italic_pattern.sub(r'<i>\1</i>', paragraph)
            paragraph = monospaced_pattern.sub(r'<tt>\1</tt>', paragraph)
            html_output.append(f'<p>{paragraph}</p>')

    return '\n'.join(html_output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py /path/to/markdown [--out /path/to/output.html]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) == 4 and sys.argv[2] == '--out':
        output_file = sys.argv[3]

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            md_text = file.read()

        html_output = parse_markdown(md_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(html_output)
        else:
            print(html_output)
    except Exception as e:
        print(f"Error: invalid markdown {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()