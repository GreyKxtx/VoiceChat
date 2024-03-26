import pyaudio


def open_input_stream(FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=44100, CHUNK=1024):
    """
    Создает и открывает поток для записи аудиоданных.

    :param FORMAT: Формат аудиоданных (например, pyaudio.paInt16)
    :param CHANNELS: Количество аудиоканалов (1 для моно, 2 для стерео и т. д.)
    :param RATE: Частота дискретизации в Гц
    :param CHUNK: Размер фрагмента аудиоданных для чтения
    :return: Объект PyAudio stream для записи аудиоданных
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return stream

def open_output_stream(FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=44100):
    """
    Создает и открывает поток для воспроизведения аудиоданных.

    :param FORMAT: Формат аудиоданных (например, pyaudio.paInt16)
    :param CHANNELS: Количество аудиоканалов (1 для моно, 2 для стерео и т. д.)
    :param RATE: Частота дискретизации в Гц
    :return: Объект PyAudio stream для воспроизведения аудиоданных
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    return stream
