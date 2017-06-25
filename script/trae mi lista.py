from os import listdir, mkdir, rename
from os.path import isdir, join
from shutil import copyfile


def process_m3u(filename, fd):
    folder_name = filename[:-4]

    if not isdir(filename):
        try:
            mkdir(folder_name)
        except:
            echo("No he podido crear carpeta $carpeta :(")

    count = 0
    print("\tVeamos qué musiquilla tiene...\n")
    for line in fd.readlines():
        if line[0] == '/':
            count += 1
            try:
                line_parts = line.split('/')
                new_name = str(count) + ' - ' + line_parts[-1]
                copyfile(line, line(folder_name, new_name))
            except:
                print("\t\tERROR AL COPIAR {}\n".format(line))
                count -= 1
            else:
                print("\t\tcopiado {}\n".format(line))

    print("\n\tHe copiado {} canciones. Lo peto.\n\n".format(str(count)))


if __name__ == "__main__":

    try:
        files_in_pwd = listdir('.')
    except:
        exit("CALAMIDAD!! $!")

    for m3ufile in [file_ for file_ in files_in_pwd if file_.endswith('.m3u')]:
        print("He encontrado la lista {} !".format(m3ufile))
        with open(file_) as m3ufile:
            process_m3u(file_, m3ufile)

    print("ya está cosaaa! :)")
