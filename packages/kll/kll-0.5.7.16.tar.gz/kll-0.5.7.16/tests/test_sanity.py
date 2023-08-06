'''
sanity test
Runs basic options to make sure Python can initialize and arguments can be used
'''

### Imports ###

from tests.klltest import kll_run



### Tests ###

def test_version():
    '''
    Calls --version argument
    '''
    args = ['--version']
    ret = kll_run(args)
    assert ret == 0

def test_help():
    '''
    Calls --help argument
    '''
    args = ['--help']
    ret = kll_run(args)
    assert ret == 0

def test_path():
    '''
    Calls --path argument
    '''
    args = ['--path']
    ret = kll_run(args)
    assert ret == 0

def test_layout_cache_path():
    '''
    Calls --layout-cache-path argument
    '''
    args = ['--layout-cache-path']
    ret = kll_run(args)
    assert ret == 0

def test_layout_cache_refresh():
    '''
    Calls --layout-cache-refresh argument
    '''
    args = ['--layout-cache-refresh']
    ret = kll_run(args)
    assert ret == 0

