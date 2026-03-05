import ast



source = ("foute syntax",
"""
correct = 0
fout === 1
""")          

try:
    ast.parse(source[1])
except SyntaxError as e1:
    print(str(e1))
    # print(e1, e1.msg, e1.lineno, e1.offset, e1.text)
    
    raise
