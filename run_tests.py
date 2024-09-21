from tests import *
import sys, colorama

colorama.just_fix_windows_console()
colorama.init(autoreset=True)

for module in list(sys.modules):
    if module.startswith('tests'):
        if module == 'tests':
            continue
        print(colorama.Fore.CYAN + 'test \'' + module + '\': ', end = '')
        sys.modules[module].test()
        print(colorama.Fore.GREEN + 'ok')