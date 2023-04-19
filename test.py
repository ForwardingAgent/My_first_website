
# T = input()
# R = input()
# s = T + R
# if s == 'ножницыбумага' or 'каменьножницы' or 'бумагакамень':
#     print('Тимур')
# elif R == T:
#     print('ничья')
# else:
#     print('Руслан')


class Video:
    def __init__(self):
        pass

    def create(self, name):  # для задания имени name текущего видео (метод сохраняет имя name в локальном атрибуте name объекта класса Video);
        self.name = name

    def play(self):  # для воспроизведения видео (метод выводит на экран строку "воспроизведение видео <name>").
        return print('воспроизведение видео', self.name)


class YouTube:
    videos = []  # для хранения добавленных объектов класса Video (изначально список пуст).

    def __init__(self):
        pass

    @classmethod
    def add_video(cls, video):  # для добавления нового видео (метод помещает объект video класса Video в список);
        cls.videos.append(video)
        print(cls.videos)

    @classmethod
    def play(cls, video_indx):  # для проигрывания видео из списка по указанному индексу (индексация с нуля) (здесь cls - ссылка на класс YouTube). И список (тоже внутри класса YouTube):
        # Video.play(cls.videos[video_indx])  моё, вызываю def play из Video передавая параметр, а в Video нет play с параметром
        cls.videos[video_indx].play()

v1, v2 = Video(), Video()
v1.create('Python')
v2.create('Python ООП')
YouTube.add_video(v1)
YouTube.add_video(v2)
YouTube.play(0)
YouTube.play(1)

