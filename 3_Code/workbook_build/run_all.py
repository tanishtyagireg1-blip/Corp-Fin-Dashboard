import sys
for f in ('build1','build2','build3','build4','build5','build5b','build6','build7'): exec(open(f'/home/claude/wai/{f}.py').read())
wb.save('/home/claude/wai/Titan_WAI_Analysis.xlsx')
print('saved')
