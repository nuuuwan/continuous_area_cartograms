from utils import Log as LogUtils, COLOR_FOREGROUND, COLOR_BACKGROUND, COLOR_FORMAT, Console



class Log(LogUtils):
    def debug_temp(self, *args):
        text = f'[{self.name}] ' + ' '.join([str(arg) for arg in args])
        print(Console.format(
            text,
            foreground=COLOR_FOREGROUND.LIGHT_GRAY,
            background=COLOR_BACKGROUND.BLACK,
            format=COLOR_FORMAT.FAINT,
        ), end='\r')
