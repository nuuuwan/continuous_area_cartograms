from utils import Log as LogUtils, COLOR_FOREGROUND, Console



class Log(LogUtils):
    def debug_temp(self, *args):
        text = f'[{self.name}] ' + ' '.join([str(arg) for arg in args])
        print(Console.format(
            text,
            foreground=COLOR_FOREGROUND.LIGHT_GRAY,
        ), end='\r')
