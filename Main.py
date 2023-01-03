from Interface import Interface
    
if(__name__=='__main__'):
    resolutions = {0: '32x32', 1: '64x64', 2: '128x128'}
    types = ['nature_block', 'block']
    ui = Interface(resolutions, types)
    ui.start()
    