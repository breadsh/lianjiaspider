
def analyzelianjiasecondhand(tree):
    elemenlst = tree.find_class('info-panel')
    rowlst = []
    for e in elemenlst:
        lst = []
        lst.append(';'.join(e.find_class('where')[0].text_content().strip().split()))
        lst.append(''.join(e.find_class('con')[0].text_content().strip().split()))
        subway = e.find_class('fang-subway-ex')
        if len(subway) == 0:
            lst.append('')
        else:
            lst.append(subway[0].text_content())
        taxfree = e.find_class('taxfree-ex')
        if len(taxfree) == 0:
            lst.append('')
        else:
            lst.append(taxfree[0].text_content())
        haskey = e.find_class('haskey-ex')
        if len(haskey) == 0:
            lst.append('')
        else:
            lst.append(haskey[0].text_content())
        rowlst.append(lst)
    return rowlst