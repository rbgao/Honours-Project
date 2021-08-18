def section_remover(p):
    try:
        del p['Text']['Members Present']
    except: 
        pass
    try:
        del p['Text']['Members present']
    except: 
        pass
    try:
        del p['Text']['Others Present']
    except: 
        pass
    try:
        del p['Text']['Others present']
    except: 
        pass
    try:
        del p['Text']['Members Participating']
    except: 
        pass
    try:
        del p['Text']['Members participating']
    except: 
        pass
    try:
        del p['Text']['Others Participating']
    except: 
        pass
    try:
        del p['Text']['Others participating']
    except: 
        pass
    try:
        del p['Text']['The decision']
    except: 
        pass
    try:
        del p['Text']['The Decision']
    except: 
        pass
    try:
        del p['Text']['Present']
    except: 
        pass
    try:
        del p['Text']['Minutes']
    except: 
        pass
    try:
        del p['Text']['Board Member']
    except: 
        pass
    try:
        del p['Text']['Board Members']
    except: 
        pass
    try:
        del p['Text']['Governor - Final Meeting'] ## Maybe not? 
    except: 
        pass